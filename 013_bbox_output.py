from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground
from utils.anchor_point import AnchorPoint
from utils.layers_fake import LayersFake

import torch

distance_colors = [
    PURE_RED,           # left
    PURE_GREEN,         # up
    PURE_BLUE,          # right
    PURE_YELLOW,        # down
]

def create_grid_cells(ref, n):
    # TODO, make rectangular ref work
    sq = Square(
        stroke_width=1,
        side_length=ref.width,
        grid_xstep=ref.width/n,
        grid_ystep=ref.width/n,
    )
    sq.move_to(ref)
    sq.grid_lines.set_stroke(width=1)
    return sq

def rect_from_point(point, left, up, right, down, **kwargs):
    x, y, z = point

    x_min = x - left
    x_max = x + right
    y_min = y - down
    y_max = y + up

    rect = Rectangle(
        width=x_max - x_min,
        height=y_max - y_min,
        stroke_width=1,
        stroke_opacity=0.3,
        **kwargs
    )

    rect.move_to([
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        z
    ])

    return rect

def create_anchor_points(ref, n, offsets):
    dx, dy = ref.width / n, ref.height / n
    aps = VGroup(*[
            AnchorPoint(
                ref.get_corner(UL)
                + DOWN * dx * (i + 0.5)
                + RIGHT * dy * (j + 0.5),   # position
                offsets[i*n+j],             # offset
            )
            for i in range(n)
            for j in range(n)
        ])
    return aps

def get_anchor_pos(ref, n, i, j):
    dx, dy = ref.width / n, ref.height / n
    pos = ref.get_corner(UL) + DOWN*dx*(i+0.5) + RIGHT*dy*(j+0.5)
    return pos

def yolo_box_to_rect(img, cx, cy, w, h, **kwargs):
    x = cx * img.width
    y = cy * img.height

    rect = Rectangle(
        width=w * img.width,
        height=h * img.height,
        stroke_color=PURE_YELLOW,
        stroke_width=2,
        **kwargs
    )

    rect.move_to(img.get_corner(UL) + RIGHT * x + DOWN * y)
    return rect

def point_in_rect(point, rect):
    x, y, _ = point

    return (
        rect.get_left()[0] <= x <= rect.get_right()[0]
        and rect.get_bottom()[1] <= y <= rect.get_top()[1]
    )

def load_tensors():
    # sequence of directions: left, up, right, down
    pre_box = torch.load('assets/tensors/_pre_box.pt', weights_only=True, map_location='cpu')  # 1, 64, 8400
    norm_box = torch.load('assets/tensors/_norm_box.pt', weights_only=True, map_location='cpu')  # 1, 64, 8400
    dist_box = torch.load('assets/tensors/_dist_box.pt', weights_only=True, map_location='cpu')  # 1, 4, 8400
    decoded_box = torch.load('assets/tensors/_decoded_box.pt', weights_only=True, map_location='cpu')  # 1, 4, 8400

    pre_cls = torch.load('assets/tensors/_pre_cls.pt', weights_only=True, map_location='cpu')  # 1, 3, 8400
    norm_cls = torch.load('assets/tensors/_norm_cls.pt', weights_only=True, map_location='cpu')  # 1, 3, 8400

    return pre_box, norm_box, dist_box, decoded_box, pre_cls, norm_cls

class MainScene(Scene):
    def construct(self) -> None:
        (
            background,
        ) = load_everything(S012_EVERYTHING)
        # FIXME, manually setup background shape
        background._w = 640
        background._h = 640

        pre_box, norm_box, dist_box, decoded_box, pre_cls, norm_cls = load_tensors()

        # ************************************************************
        self.next_section(
            'init, show background shape before output design',
            skip_animations=True,
        )
        # ************************************************************
        self.add(background)
        self.wait()
        self.play(background.show_passing_flash())
        self.wait()

        # ************************************************************
        self.next_section(
            'from grid cells to anchor points',
            skip_animations=True,
        )
        # ************************************************************
        # create grid cells
        grid = create_grid_cells(background.background, 20)
        self.play(Write(grid))
        self.wait()

        # create anchors points, based on tensor content
        offsets = dist_box[0, :, 8000:].transpose(0,1)      # (400,4)
        anchors = create_anchor_points(
            background,
            20,
            offsets,
        )
        self.play(Write(anchors, lag_ratio=0.02))
        self.wait()
        self.play(AnimationGroup(
            background.unwrite_shape_texts(),
            Unwrite(grid),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'anchor point capture thinking',
            skip_animations=True,
        )
        # ************************************************************
        dd = float(background.width) / 20       # TODO, make 20 variable

        self.play(AnimationGroup(
            *(anchor.to_rect(
                dd,
                stroke_width=1,
                stroke_opacity=0.3,
                stroke_color=WHITE,
            ) for anchor in anchors),
            lag_ratio=0.003,
        ))
        self.wait()
        self.play(AnimationGroup(
            *(anchor.to_dot() for anchor in anchors),
            lag_ratio=0.003,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'identify important anchor points ',
            skip_animations=True,
        )
        # ************************************************************
        # plot reference bboxes
        bboxes = VGroup(
            *(yolo_box_to_rect(background.background, cx, cy, w, h) for _,cx,cy,w,h in background.data),
        )
        self.play(Write(bboxes))
        self.wait()
        # stress those anchors inside rects
        inside_anchors = VGroup(
            *(dot for dot in anchors if any(point_in_rect(dot.dot.get_center(),rect) for rect in bboxes))
        )

        # identify those anchors inside reference bboxes
        self.play(AnimationGroup(
            dot.animate.set_color(RED) for dot in inside_anchors
        ))
        self.wait()

        # let inside anchors capture
        self.play(AnimationGroup(
            *(anchor.to_rect(
                dd,
                stroke_width=1,
                stroke_opacity=1.0,
                stroke_color=RED,
            ) for anchor in inside_anchors),
            lag_ratio=0.03,
        ))
        self.wait()

        # back to background + anchor points
        self.play(AnimationGroup(
            *(anchor.to_dot() for anchor in inside_anchors),
            lag_ratio=0.03,
        ))
        self.wait()
        self.play(AnimationGroup(
            *(anchor.animate.set_color(WHITE) for anchor in inside_anchors),
            Unwrite(bboxes),
        ))
        self.wait()

        # TODO: which target to capture? inside/inside-multiple/outside

        # ************************************************************
        self.next_section(
            'sample anchor, single dddd(640) representation',
            skip_animations=True,
        )
        # ************************************************************
        sample_index = 189
        sample_anchor = anchors[sample_index]    # FIXME, change this
        anchors.save_state()                    # for restore later
        anchors.generate_target()
        anchors.target.set_stroke(opacity=0.2)
        anchors.target[sample_index].set_stroke(opacity=1.0)

        # focus on sample anchor
        self.play(MoveToTarget(anchors))
        self.wait()

        # offset trackers
        o_trackers = [ValueTracker(v) for v in sample_anchor.offset]

        # manual create sample rect
        sample_center = sample_anchor.orig_center   # FIXME, orig_center exist only after calling to_rect
        from utils.anchor_point import rect_from_point
        sample_rect = always_redraw(
            lambda: rect_from_point(
                sample_center,
                (d*dd for d in [t.get_value() for t in o_trackers]),
                stroke_width=2,
                stroke_opacity=1.0,
                stroke_color=WHITE,
            )
        )
        self.play(ReplacementTransform(
            sample_anchor,
            sample_rect,
        ))
        self.wait()

        # manual create sample arrows
        sample_arrows = always_redraw(
            lambda: VGroup(
                Arrow(
                    start=sample_center,
                    end=(
                        sample_center[0]-o_trackers[0].get_value()*dd,
                        sample_center[1],
                        0,
                    ),
                    stroke_width=3,
                    tip_length=0.15,
                    buff=0.0,
                ),
                Arrow(
                    start=sample_center,
                    end=(
                        sample_center[0],
                        sample_center[1]+o_trackers[1].get_value()*dd,
                        0,
                    ),
                    stroke_width=3,
                    tip_length=0.15,
                    buff=0.0,
                ),
                Arrow(
                    start=sample_center,
                    end=(
                        sample_center[0]+o_trackers[2].get_value()*dd,
                        sample_center[1],
                        0,
                    ),
                    stroke_width=3,
                    tip_length=0.15,
                    buff=0.0,
                ),
                Arrow(
                    start=sample_center,
                    end=(
                        sample_center[0],
                        sample_center[1]-o_trackers[3].get_value()*dd,
                        0,
                    ),
                    stroke_width=3,
                    tip_length=0.15,
                    buff=0.0,
                ),
            )
        )
        # problem if write one by one
        self.play(Write(sample_arrows, lag_ratio=0.3))
        self.wait()

        # manual create sample direction texts
        sample_diss = always_redraw(
            lambda: VGroup(
                Integer(
                    o_trackers[0].get_value()*32,
                ).scale(0.4).next_to(
                    sample_arrows[0],
                    UP,
                    buff=0.05,
                ).set_z_index(4),
                Integer(
                    o_trackers[1].get_value() * 32,
                ).scale(0.4).next_to(
                    sample_arrows[1],
                    RIGHT,
                    buff=0.05,
                ).set_z_index(3),
                Integer(
                    o_trackers[2].get_value() * 32,
                ).scale(0.4).next_to(
                    sample_arrows[2],
                    DOWN,
                    buff=0.05,
                ).set_z_index(2),
                Integer(
                    o_trackers[3].get_value() * 32,
                ).scale(0.4).next_to(
                    sample_arrows[3],
                    LEFT,
                    buff=0.05,
                ).set_z_index(1),
            )
        )
        self.play(Write(sample_diss, lag_ratio=0.3))
        self.wait()

        # TODO, change offsets multiple times
        for _ in range(1):
            self.play(AnimationGroup(
                *(tracker.animate.set_value(np.random.uniform(2,8))
                  for tracker in o_trackers),
            ))
            self.wait(0.3)
        self.wait()

        # ************************************************************
        self.next_section(
            'with colored arrangement, single dddd(640) representation',
            skip_animations=True,
        )
        # ************************************************************
        # change color of each distance and arrow
        self.play(AnimationGroup(
            *(AnimationGroup(
                dis.animate.set_color(distance_colors[i]),
                sample_arrows[i].animate.set_color(distance_colors[i]).set_opacity(0.5),
            ) for i,dis in enumerate(sample_diss)),
            lag_ratio=0.3,
        ))
        self.wait()

        # arrange distance in IN order, most properties of distance kept here during animation
        _offset_scale = 0.15
        self.play(AnimationGroup(
            sample_diss[0].animate.move_to(sample_center+DL*_offset_scale*1.5).set_opacity(1.0).scale(2.0),
            sample_diss[1].animate.move_to(sample_center + DL * _offset_scale * 0.5).set_opacity(0.8).scale(1.8),
            sample_diss[2].animate.move_to(sample_center + DL * _offset_scale * -0.5).set_opacity(0.6).scale(1.6),
            sample_diss[3].animate.move_to(sample_center + DL * _offset_scale * -1.5).set_opacity(0.4).scale(1.4),
        ))
        self.wait()

        # reset updaters of sample_diss and sample_arrows
        sample_diss.clear_updaters()
        sample_diss[0].add_updater(
            lambda mob: mob.set_value(
                o_trackers[0].get_value() * 32,
            ),)
        sample_diss[1].add_updater(
            lambda mob: mob.set_value(
                o_trackers[1].get_value() * 32,
            ),)
        sample_diss[2].add_updater(
            lambda mob: mob.set_value(
                o_trackers[2].get_value() * 32,
            ),)
        sample_diss[3].add_updater(
            lambda mob: mob.set_value(
                o_trackers[3].get_value() * 32,
            ),)

        sample_arrows[0].add_updater(
            lambda mob: mob.put_start_and_end_on(
                start=sample_center,
                end=(
                    sample_center[0] - o_trackers[0].get_value() * dd,
                    sample_center[1],
                    0,
                ),
            )
        )
        sample_arrows[1].add_updater(
            lambda mob: mob.put_start_and_end_on(
                start=sample_center,
                end=(
                    sample_center[0],
                    sample_center[1] + o_trackers[1].get_value() * dd,
                    0,
                ),
            )
        )
        sample_arrows[2].add_updater(
            lambda mob: mob.put_start_and_end_on(
                start=sample_center,
                end=(
                    sample_center[0] + o_trackers[2].get_value() * dd,
                    sample_center[1],
                    0,
                ),
            )
        )
        sample_arrows[3].add_updater(
            lambda mob: mob.put_start_and_end_on(
                start=sample_center,
                end=(
                    sample_center[0],
                    sample_center[1] - o_trackers[3].get_value() * dd,
                    0,
                ),
            )
        )

        # TODO, change offsets multiple times
        # TODO, maybe a final regular series?
        for _ in range(3):
            self.play(AnimationGroup(
                *(tracker.animate.set_value(np.random.uniform(2,8))
                  for tracker in o_trackers),
            ))
            self.wait(0.3)
        self.wait()

        # ************************************************************
        self.next_section(
            'sample anchor, single dddd(640/32) representation',
            skip_animations=True,
        )
        # ************************************************************
        # remove updaters of distance for preparation
        for dis in sample_diss:
            dis.clear_updaters()

        # TODO, maybe crawling lines to signify UNIT concept?
        # append /32 for each distance
        divs_32 = VGroup(
            MathTex(
                '/32',
                font_size=int(32*(1-i*0.1)),
                color=GRAY,
            ).next_to(sample_diss[i],RIGHT,buff=0).shift(DOWN*0.03).set_opacity(1-i*0.2).set_z_index(1)
            for i in range(4)
        )
        self.play(Write(divs_32))
        self.wait()

        # transform x/32 into result
        _inputs = VGroup(
            VGroup(
                left,
                right,
            ) for left, right in zip(sample_diss,divs_32)
        )
        _outputs = VGroup(
            DecimalNumber(
                o_trackers[0].get_value(),
                num_decimal_places=2,
            ).move_to(sample_center+DL*_offset_scale*1.5).set_opacity(1.0).scale(0.9).set_color(distance_colors[0]).set_z_index(4),
            DecimalNumber(
                o_trackers[1].get_value(),
                num_decimal_places=2,
            ).move_to(sample_center + DL * _offset_scale * 0.5).set_opacity(0.8).scale(0.8).set_color(distance_colors[1]).set_z_index(3),
            DecimalNumber(
                o_trackers[2].get_value(),
                num_decimal_places=2,
            ).move_to(sample_center + DL * _offset_scale * -0.5).set_opacity(0.6).scale(0.7).set_color(distance_colors[2]).set_z_index(2),
            DecimalNumber(
                o_trackers[3].get_value(),
                num_decimal_places=2,
            ).move_to(sample_center + DL * _offset_scale * -1.5).set_opacity(0.4).scale(0.6).set_color(distance_colors[3]).set_z_index(1),
        )
        self.play(AnimationGroup(
            ReplacementTransform(_input, _output) for _input,_output in zip(_inputs,_outputs)
        ))
        self.wait()

        # add updaters to decimals
        _outputs[0].add_updater(
            lambda mob: mob.set_value(
                o_trackers[0].get_value(),
            ),
        )
        _outputs[1].add_updater(
            lambda mob: mob.set_value(
                o_trackers[1].get_value(),
            ),
        )
        _outputs[2].add_updater(
            lambda mob: mob.set_value(
                o_trackers[2].get_value(),
            ),
        )
        _outputs[3].add_updater(
            lambda mob: mob.set_value(
                o_trackers[3].get_value(),
            ),
        )

        # TODO, change offsets multiple times
        for _ in range(3):
            self.play(AnimationGroup(
                *(tracker.animate.set_value(np.random.uniform(2, 8))
                  for tracker in o_trackers),
            ))
            self.wait(0.3)
        self.wait()

        # ************************************************************
        self.next_section(
            'clean job',
            skip_animations=True,
        )
        # ************************************************************
        # FIXME, necessary to clear updater before unwrite?
        for output in _outputs:
            output.clear_updaters()
        for arrow in sample_arrows:
            arrow.clear_updaters()
        sample_rect.clear_updaters()
        
        self.play(AnimationGroup(
            Unwrite(_outputs, run_time=0.5),
            Unwrite(sample_arrows, run_time=0.5),     # unwriting always_redraw object
            anchors.animate.restore(),
        ))

        # TODO, problem with the transformed anchors? thus recreate
        self.remove(anchors)
        anchors = create_anchor_points(
            background,
            20,
            offsets,
        )
        self.add(anchors)
        self.wait()

        # ************************************************************
        self.next_section(
            'dddd(640/32) output representation',
            skip_animations=False,
        )
        # ************************************************************
        # make anchors and background a whole
        whole = Group(background, anchors)

        # make room in the right
        self.play(whole.animate.shift(LEFT*3).scale(0.8))
        self.wait()
        dd = float(background.width) / 20   # update step from now on

        # prepare lf
        lf_output_32_box = LayersFake(
            4,
            width=background.width,
            height=background.height,
            width_nominal=20,
            height_nominal=20,
            expanded=True,
            buff=0.12,
        ).shift(RIGHT*3)
        # self.add(lf_output_32_box)
        self.wait()

        # prepare digit representation, dmobs
        dmobs = []
        data = offsets.transpose(0,1).reshape(4,20,20)
        x_step = dd * RIGHT
        y_step = dd * DOWN
        for i, layer in enumerate(data):
            bg = lf_output_32_box.rects[3-i]    # reversed for layersfake type
            base = bg.get_corner(UL) + x_step * 0.5 + y_step * 0.5
            zidx = 4 - i
            opac = 1.0 - i * 0.25
            color = distance_colors[i]  # color for current layer

            layer_mobs = []
            for j, row in enumerate(layer):
                for k, value in enumerate(row):
                    mob = DecimalNumber(
                        value,
                        color=color,
                        stroke_width=0.5,   # make digits more visible
                        stroke_opacity=opac,
                    ).move_to(base).shift(k * x_step + j * y_step)
                    mob.scale(0.25)

                    mob.set_z_index(zidx)
                    mob.set_fill(opacity=opac)
                    # mobs.append(mob)
                    layer_mobs.append(mob)
            layer_mobs = VGroup(*layer_mobs)
            dmobs.append(layer_mobs)
        dmobs = VGroup(*dmobs)
        dmobs = VGroup(VGroup(*g) for g in list(zip(*dmobs)))   # rearrange

        # self.add(dmobs)
        # self.wait()

        # # sync capture and digit generation
        self.play(AnimationGroup(
            *(AnimationGroup(
                anchor.to_rect(
                    dd,
                    stroke_width=1,
                    stroke_opacity=0.3,
                    stroke_color=WHITE,
                ),
                Write(
                    beam,
                    lag_ratio=0.001,
                    run_time=1.0,          # FIXME, sync
                ),
            ) for anchor, beam in zip(anchors, dmobs)),
            lag_ratio=0.003,
        ))
        self.wait()
        # self.play(AnimationGroup(
        #     *(anchor.to_dot() for anchor in anchors),
        #     lag_ratio=0.003,
        # ))
        # self.wait()

        # sync capture and digits generation

        # replace digits with numberplane

        # ************************************************************
        self.next_section(
            'sample anchor, single dfl-32 representation',
            skip_animations=True,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'dfl-32 output representation',
            skip_animations=True,
        )
        # ************************************************************


        # decode step roughly, before tensor introduction

        # save for next scene

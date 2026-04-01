from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground
from utils.anchor_point import AnchorPoint

import torch

# order:          left   up    right  down
distance_colors = [RED, GREEN, BLUE, YELLOW]

def align_to_top(rect, p):
    return np.array([p[0], rect.get_top()[1], 0])

def align_to_bottom(rect, p):
    return np.array([p[0], rect.get_bottom()[1], 0])

def align_to_left(rect, p):
    return np.array([rect.get_left()[0], p[1], 0])

def align_to_right(rect, p):
    return np.array([rect.get_right()[0], p[1], 0])

align_to_funs = [
    align_to_left,
    align_to_top,
    align_to_right,
    align_to_bottom,
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
        offsets = dist_box[0, :, 8000:].transpose(0,1)
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
            skip_animations=False,
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
        next_dirs = [UP, RIGHT, DOWN, LEFT]
        sample_diss = always_redraw(
            lambda: VGroup(
                *(Integer(
                    v*32,
                ).scale(0.4).next_to(
                    sample_arrows[i],
                    next_dirs[i],
                    buff=0.1,
                )
                for i,v in enumerate([t.get_value() for t in o_trackers])),
            )
        )
        self.play(Write(sample_diss, lag_ratio=0.3))
        self.wait()

        # TODO, change offsets multiple times
        for _ in range(1):
            self.play(AnimationGroup(
                *(tracker.animate.set_value(np.random.randint(2,6))
                  for tracker in o_trackers),
            ))
            self.wait(0.3)
        self.wait()

        # change color of each direction text and rearrange
        self.play(AnimationGroup(
            *(dis.animate.set_color(distance_colors[i]) for i,dis in enumerate(sample_diss)),
            lag_ratio=0.3,
        ))
        self.wait()

        # reset updaters of sample_diss
        copy_base = RIGHT * 5       # TODO, constant
        sample_diss.clear_updaters()
        sample_diss[0].add_updater(
            lambda mob: mob.set_value(
                o_trackers[0].get_value() * 32,
            ).next_to(sample_arrows[0], UP, buff=0.1,),
        )
        sample_diss[1].add_updater(
            lambda mob: mob.set_value(
                o_trackers[1].get_value() * 32,
            ).next_to(sample_arrows[1], RIGHT, buff=0.1, ),
        )
        sample_diss[2].add_updater(
            lambda mob: mob.set_value(
                o_trackers[2].get_value() * 32,
            ).next_to(sample_arrows[2], DOWN, buff=0.1, ),
        )
        sample_diss[3].add_updater(
            lambda mob: mob.set_value(
                o_trackers[3].get_value() * 32,
            ).next_to(sample_arrows[3], LEFT, buff=0.1, ),
        )

        # create copy of sample diss with its own updaters
        diss_copy = sample_diss.copy().clear_updaters()
        self.add(diss_copy)
        self.play(diss_copy.animate.shift(RIGHT*4))
        diss_copy[0].add_updater(
            lambda mob: mob.set_value(o_trackers[0].get_value() * 32),
        )
        diss_copy[1].add_updater(
            lambda mob: mob.set_value(o_trackers[1].get_value() * 32),
        )
        diss_copy[2].add_updater(
            lambda mob: mob.set_value(o_trackers[2].get_value() * 32),
        )
        diss_copy[3].add_updater(
            lambda mob: mob.set_value(o_trackers[3].get_value() * 32),
        )
        self.wait()

        # changing offsets after arranging distances
        for _ in range(1):
            self.play(AnimationGroup(
                *(tracker.animate.set_value(np.random.randint(2,6))
                  for tracker in o_trackers),
            ))
            self.wait(0.3)
        self.wait()

        # ************************************************************
        self.next_section(
            'dddd(640) output representation',
            skip_animations=False,
        )
        # ************************************************************


        # ************************************************************
        self.next_section(
            'sample anchor, single dddd(640/32) representation',
            skip_animations=True,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'dddd(640/32) output representation',
            skip_animations=True,
        )
        # ************************************************************




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

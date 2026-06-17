from manim import *

from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.constants import *
from utils.line_matrix import LineMatrix
from utils.anchor_point import AnchorPoint
from utils.general import tensor_to_line_matrix, import_mobs, export_mobs
from utils.layers_fake import LayersFake

import random

# ---------------- anchor point related -------------------
AP_DOT_CONFIG_FOCUS = {
    'stroke_color': PURE_YELLOW,
    'stroke_opacity': 1.0,
}
AP_DOT_CONFIG_OTHERS = {
    'stroke_color': GRAY,
    'stroke_opacity': 0.5,
}
AP_RECT_CONFIG_FOCUS = {
    'stroke_color': PURE_YELLOW,
    'stroke_opacity': 1.0,
}
AP_RECT_CONFIG_OTHERS = {
    'stroke_color': GRAY,
    'stroke_opacity': 0.3,
    'stroke_width': 1.0,
}

# ---------------- explainer related -------------------
SAMPLE_IDX = 189
N_LOOP_SAMPLES = 3

ARROW_CONFIG = {
    'stroke_width': 1,
    'tip_length': 0.03,
    'buff': 0.0,
    'max_stroke_width_to_length_ratio': 15,         # FIXME: 5 by default
    'max_tip_length_to_length_ratio': 0.85,          # FIXME: 0.25 by default
}

# ---------------- tensor related -------------------
TENSOR_OFFSET_CONFIG = {
    'side_length': 0.15,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'fill_opacity': 0.7,
}
TENSOR_XYXY_CONFIG = {
    'side_length': 0.15,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'fill_opacity': 0.7,
}
TENSOR_BUFF_RATIO = 0.5

# ---------------- computation related -------------------
COMPUTATION_FONT_SIZE = 20
COMPUTATION_LINE_BUFF = 0.5
COMPUTATION_BASE_COLOR = GRAY

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init background and explainer anew',
            skip_animations=True,
        )
        # ************************************************************
        background = ImagePad(padded=True)
        background.scale(1.3)

        explainer = Explainer.from_file(
            background=background,
            version=32,
            sf_nominal=32,
        )

        annotation = YoloAnnotation(
            background=background.image,
            annotation=PATH_LABEL,
        )

        system = Group(background, explainer)
        self.add(system)
        self.wait(wt)

        self.play(background.animate(
            run_time=wt,
        ).set_opacity(0.2))
        self.wait(wt)

        # show shape as a first hint
        self.play(ShowShape(
            background,
            text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            aargs={'run_time': wt},
        ))
        self.wait(wt)
        self.play(HideShape(
            background,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'anchor points capture thinking',
            skip_animations=True,
        )
        # ************************************************************
        # show grid then anchor points
        self.play(explainer.show_grid(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        self.play(explainer.show_anchor_points(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        self.play(explainer.hide_grid(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # anchor points capture
        self.play(explainer.to_rects(
            rect_config={},
            aargs={},
            gargs={
                'lag_ratio':0,
                'run_time':SHORT_DURATION,
            },
        ))
        self.wait(wt)
        self.play(explainer.to_dots(
            dot_config={},
            aargs={},
            gargs={'lag_ratio':0, 'run_time':SHORT_DURATION},
        ))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'inside anchor points capture',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # show true annotation
        # self.play(Write(
        #     annotation,
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # hide labels for now
        # self.play(AnimationGroup(
        #     *(label.animate.set_opacity(opacity=0)
        #         for label in annotation.get_labels()),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # collect inside/outside anchor points
        # aps_in, aps_out = explainer.collect_aps(
        #     func=lambda ap: any(ap.inside_box(box) for box in annotation.get_boxes()),
        # )

        # # focus on important anchor points
        # self.play(AnimationGroup(
        #     AnimationGroup(
        #         *(ap.mob.animate.set_style(
        #             **AP_DOT_CONFIG_FOCUS,
        #         ) for ap in aps_in),
        #         lag_ratio=0,
        #         run_time=wt,
        #     ),
        #     AnimationGroup(
        #         *(ap.mob.animate.set_style(
        #             **AP_DOT_CONFIG_OTHERS,
        #         ) for ap in aps_out),
        #         lag_ratio=0,
        #         run_time=wt,
        #     ),
        # ))
        # self.wait(wt)

        # # important anchor points capture
        # self.play(AnimationGroup(
        #     *(ap.to_rect(rect_config=AP_RECT_CONFIG_FOCUS,
        #     ) for ap in aps_in),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # other anchor points capture
        # self.play(AnimationGroup(
        #     *(ap.to_rect(rect_config=AP_RECT_CONFIG_OTHERS,
        #     ) for ap in aps_out),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # restore all anchor points
        # self.play(explainer.to_dots(
        #     dot_config={},
        #     aargs={},
        #     gargs={'lag_ratio': 0.0, 'run_time': wt},
        # ))
        # self.wait(wt)

        # # remove annotation
        # self.play(Unwrite(
        #     annotation,
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'sample, xyxy output',
            skip_animations=True,
        )
        # ************************************************************
        # focus on sample anchor point
        ap_sample, aps_others = explainer.collect_ap(
            func=lambda ap: ap.index_flatten == SAMPLE_IDX,
        )
        self.play(AnimationGroup(
            *(ap.mob.animate.set_style(
                **AP_DOT_CONFIG_OTHERS,
            ) for ap in aps_others),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # capture
        self.play(ap_sample.to_rect(
            rect_config={},
            run_time=wt,
        ))
        self.wait(wt)

        # show (x1, y1)
        self.play(ap_sample.show_coords(
            position=UL,
            origin=background.get_corner(UL),
            v1=ap_sample.xyxy[0].item() * ap_sample.sf_nominal,
            v2=ap_sample.xyxy[1].item() * ap_sample.sf_nominal,
            num_decimal_places=0,
            run_time=wt,
        ))
        self.wait(wt)

        # show (x2, y2)
        self.play(ap_sample.show_coords(
            position=DR,
            origin=background.get_corner(UL),
            v1=ap_sample.xyxy[2].item() * ap_sample.sf_nominal,
            v2=ap_sample.xyxy[3].item() * ap_sample.sf_nominal,
            num_decimal_places=0,
            run_time=wt,
        ))
        self.wait(wt)

        # clean up
        self.play(ap_sample.hide_coords(
            run_time=wt,
        ))
        self.play(ap_sample.to_dot(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'sample, offset output',
            skip_animations=True,
        )
        # ************************************************************
        # show arrows
        self.play(ap_sample.show_arrows(
            arrow_config={},
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # show absolute offset for arrows
        self.play(ap_sample.show_arrows_offset_abs(
            text_config={},
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)

        # show anchor point coords (+0.5 version)
        self.play(ap_sample.show_coords(
            position=ORIGIN,
            origin=background.get_corner(UL),
            v1=ap_sample.index[0] + 0.5,
            v2=ap_sample.index[1] + 0.5,
            num_decimal_places=1,
            text_config={'color': GRAY},
            run_time=wt,
        ))
        self.wait(wt)

        # make room in the right
        self.play(system.animate(
            run_time=wt,
        ).shift(LEFT * 2.5))
        self.wait(wt)

        # show computation from absolute offset to position
        cps_abs = ap_sample.create_computation_abs_to_position(
            buff=COMPUTATION_LINE_BUFF,
            text_config={
                'font_size': COMPUTATION_FONT_SIZE,
                'color': COMPUTATION_BASE_COLOR,
            },
        ).shift(RIGHT*3.5)
        self.play(Succession(
            *(Create(cp) for cp in cps_abs),
            run_time=wt,
        ))
        self.wait(wt)

        # hide anchor point coords (+0.5 version)
        self.play(ap_sample.hide_coords(
            run_time=wt,
        ))
        self.wait(wt)

        # show (x1, y1) (x2, y2) again, reversed path
        self.play(ap_sample.show_coords(
            position=UL,
            origin=background.get_corner(UL),
            v1=ap_sample.xyxy[0].item() * ap_sample.sf_nominal,
            v2=ap_sample.xyxy[1].item() * ap_sample.sf_nominal,
            num_decimal_places=0,
            reversed=True,
            run_time=wt,
        ))
        self.play(ap_sample.show_coords(
            position=DR,
            origin=background.get_corner(UL),
            v1=ap_sample.xyxy[2].item() * ap_sample.sf_nominal,
            v2=ap_sample.xyxy[3].item() * ap_sample.sf_nominal,
            num_decimal_places=0,
            reversed=True,
            run_time=wt,
        ))
        self.wait(wt)

        # show capture rect again
        self.play(ap_sample.to_rect(
            rect_config={},
            run_time=wt,
        ))
        self.wait(wt)

        # hide xyxy coords
        self.play(AnimationGroup(
            ap_sample.hide_coords(
                run_time=wt,
            ),
            ap_sample.to_dot(
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'sample, normed offset output',
            skip_animations=True,
        )
        # ************************************************************
        # show divides for arrow offsets
        self.play(ap_sample.show_arrows_divide(
            text_config={},
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)

        # convert absolute offsets into relative offset
        self.play(ap_sample.arrows_abs_to_rela(
            text_config={},
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)

        # show computation from relative offset to position
        cps_rela = ap_sample.create_computation_rela_to_position(
            buff=COMPUTATION_LINE_BUFF,
            text_config={
                'font_size': COMPUTATION_FONT_SIZE,
                'color': COMPUTATION_BASE_COLOR,
            },
        ).shift(RIGHT*3.5)  # variable constant?

        # FIXME: cool but failed
        # self.play(Succession(
        #     *(TransformMatchingShapes(cp1, cp2) for cp1, cp2 in zip(cps_abs, cps_rela)),
        #     run_time=wt,
        # ))
        # self.wait(wt)
        self.play(Transform(
            cps_abs,
            cps_rela,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # rect capture again
        self.play(ap_sample.to_rect(
            rect_config={},
            run_time=wt,
        ))
        self.wait(wt)

        # clean up offsets, arrows, rects
        self.play(ap_sample.hide_arrows_offset_rela(
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.play(ap_sample.hide_arrows(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(ap_sample.to_dot(
            dot_config={},
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'OPTIONAL: loop through several samples',
            skip_animations=True,
        )
        # ************************************************************
        sample_idxs = random.sample(
            range(explainer.shape[0] * explainer.shape[1]),
            k=N_LOOP_SAMPLES,
        )

        for sample_idx in sample_idxs:
            ap_sample, aps_others = explainer.collect_ap(
                func=lambda ap: ap.index_flatten == sample_idx,
            )

            # highlight sample anchor point
            self.play(AnimationGroup(
                ap_sample.to_dot(),
                *(ap.mob.animate.set_style(
                    **AP_DOT_CONFIG_OTHERS,
                ) for ap in aps_others),
                lag_ratio=0.0,
                run_time=wt,
            ))

            # show arrows
            self.play(ap_sample.show_arrows(
                arrow_config={},
                lag_ratio=0.5,
                run_time=wt,
            ))

            # update computations, based on abs (NOT rela)
            cps_new = ap_sample.create_computation_rela_to_position(
                buff=COMPUTATION_LINE_BUFF,
                text_config={
                    'font_size': COMPUTATION_FONT_SIZE,
                    'color': COMPUTATION_BASE_COLOR,
                },
            ).align_to(cps_abs, RIGHT)
            # self.play(Succession(
            #     *(TransformMatchingShapes(cp1, cp2) for cp1, cp2 in zip(cps_abs, cps_new)),
            #     run_time=wt,
            # ))
            self.play(Transform(
                cps_abs,
                cps_new,
                lag_ratio=0.5,
                run_time=wt,
            ))

            # show captures
            self.play(ap_sample.to_rect(
                rect_config={},
                run_time=wt,
            ))

            # clean arrows, rects
            self.play(ap_sample.hide_arrows(
                lag_ratio=0.5,
                run_time=wt,
            ))
            self.play(ap_sample.to_dot(
                dot_config={},
                run_time=wt,
            ))

        self.wait(wt)

        # fade sample ap, remove computations
        self.play(ap_sample.mob.animate(
            run_time=wt,
        ).set_style(**AP_DOT_CONFIG_OTHERS))
        self.play(Unwrite(
            cps_abs,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'offset: explainer to tensor mapping',
            skip_animations=False,
        )
        # ************************************************************
        # scale and shift system
        self.play(system.animate(
            run_time=wt,
        ).scale(0.5).shift(UP*2))
        self.wait(wt)

        # create arrows and related tensor
        tensor_offset = explainer.create_tensor_offset(
            cell_config=TENSOR_OFFSET_CONFIG,
            buff_ratio=TENSOR_BUFF_RATIO,
        )
        tensor_offset.shift(DOWN*4)
        self.play(AnimationGroup(
            *(AnimationGroup(
                ap.show_arrows(
                    arrow_config=ARROW_CONFIG,
                ),
                Write(series),
            ) for ap, series in zip(
                explainer.anchor_points,
                tensor_offset,
            )),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'xyxy: explainer to tensor mapping',
            skip_animations=False,
        )
        # ************************************************************

        # # sync distance generation
        # self.play(explainer_dist_bg.animate(run_time=SHORT_DURATION).scale(0.8).shift(LEFT*.5))
        # self.wait(SHORT_DURATION)

        # tensor_dist = explainer_dist.create_distance_tensor(font_size=8)
        # tensor_dist.center().shift(RIGHT*3)
        # self.play(AnimationGroup(
        #     explainer_dist.show_arrows(
        #         arrow_config={'stroke_width':1, 'tip_length':0.03,},
        #         gargs={'run_time':SHORT_DURATION, 'lag_ratio':0.02},
        #     ),
        #     Write(tensor_dist, run_time=SHORT_DURATION, lag_ratio=0.02),
        # ))  # TODO, 3 seconds looks good
        # self.wait(SHORT_DURATION)

        # # ************************************************************
        # self.next_section(
        #     'global, generate xyxy tensor',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # scale and make room in the right
        # manager = Group(explainer_dist_bg, tensor_dist)
        # manager.generate_target()
        # manager.target.scale(0.7).arrange(DOWN,buff=0.5).shift(LEFT*3)
        # manager.target[1].align_to(manager.target[0][0].background, LEFT)
        # self.play(MoveToTarget(manager, run_time=SHORT_DURATION))
        # self.wait(SHORT_DURATION)

        # # make copy of distance
        # explainer_xyxy_bg = explainer_dist_bg.copy()
        # self.add(explainer_xyxy_bg)
        # self.play(explainer_xyxy_bg.animate(run_time=1.0).shift(RIGHT*5.5))
        # self.wait(SHORT_DURATION)

        # explainer_xyxy = explainer_xyxy_bg[0]

        # # sync position generation
        # tensor_xyxy = explainer_xyxy.create_xyxy_tensor(font_size=6)
        # tensor_xyxy.align_to(tensor_dist, UP)
        # self.play(AnimationGroup(
        #     explainer_xyxy.to_rects(
        #         rect_config={'width':0.5,},
        #         aargs={},
        #         gargs={'lag_ratio':0.01, 'run_time': SHORT_DURATION},
        #     ),
        #     explainer_xyxy.hide_arrows(
        #         aargs={},
        #         gargs={'lag_ratio':0.01, 'run_time': SHORT_DURATION},
        #     ),
        #     Write(tensor_xyxy, run_time=SHORT_DURATION, lag_ratio=0.01),
        # ))  # TODO, 3 seconds looks good
        # self.wait(SHORT_DURATION)

        # # # TODO, generate comment labels for layers of tensors

        # # ************************************************************
        # self.next_section(
        #     'reshape xyxy tensor to 2d',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # make room for reshaped xyxy tensor
        # self.play(AnimationGroup(
        #     explainer_dist_bg.animate(run_time=SHORT_DURATION).shift(LEFT*1),
        #     tensor_dist.animate(run_time=SHORT_DURATION).shift(LEFT*1),
        #     explainer_xyxy_bg.animate(run_time=SHORT_DURATION).shift(LEFT*2),
        #     tensor_xyxy.animate(run_time=SHORT_DURATION).shift(LEFT*2),
        # ))
        # self.wait(SHORT_DURATION)

        # # transform xyxy into reshaped 2d version
        # tensor_xyxy_2d = tensor_xyxy.copy()     # make a copy as target 2d tensor
        # self.add(tensor_xyxy_2d)
        # line_matrix = explainer_xyxy.create_line_matrix(n=4).scale(0.07).shift(RIGHT*4.3)
        # self.play(tensor_to_line_matrix(
        #     tensor=tensor_xyxy_2d,
        #     lmatrix=line_matrix,
        #     targs={},
        #     gargs={'lag_ratio':0.02, 'run_time':0.1,},
        #     ggargs={'lag_ratio':0.05, 'run_time':SHORT_DURATION,},
        # ))
        # self.wait(SHORT_DURATION)

        # # ************************************************************
        # self.next_section(
        #     'simplify tensor_dist/tensor_xyxy/tensor_xyxy_2d' \
        #     'into lf_output_32_dist/lf_output_32_xyxy/lf_output_32_xyxy_2d',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # create lf_output_32_dist
        # lf_output_32_dist = LayersFake(
        #     n=4,
        #     ref=tensor_dist,
        #     width_nominal=20,
        #     height_nominal=20,
        #     buff=0.05,
        #     expanded=True,
        # ).move_to(tensor_dist).scale(0.95)

        # # create lf_output_32_xyxy
        # lf_output_32_xyxy = lf_output_32_dist.copy()
        # lf_output_32_xyxy.move_to(tensor_xyxy)

        # # create lf_output_32_xyxy_2d
        # lf_output_32_xyxy_2d = LayersFake(
        #     n=1,
        #     ref=tensor_xyxy_2d,
        #     width_nominal=4,
        #     height_nominal=400,
        #     expanded=True,
        # ).move_to(tensor_xyxy_2d)

        # # simplify tensor_dist/tensor_xyxy/tensor_xyxy_2d
        # self.play(AnimationGroup(
        #     Unwrite(tensor_dist, lag_ratio=0, run_time=1.0),
        #     Write(lf_output_32_dist, run_time=1.0),
        #     Unwrite(tensor_xyxy, lag_ratio=0, run_time=1.0),
        #     Write(lf_output_32_xyxy, run_time=1.0),
        #     Unwrite(tensor_xyxy_2d, lag_ratio=0, run_time=1.0),
        #     Write(lf_output_32_xyxy_2d, run_time=1.0),
        # ))
        # self.wait(0.3)


        # # ************************************************************
        # self.next_section(
        #     'simplify explainer_dist and explainer_xyxy ' \
        #     'into 4x4 mini version',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # clean explainer_dist and explainer_xyxy
        # self.play(AnimationGroup(
        #     explainer_dist.hide_arrows(
        #         aargs={},
        #         gargs={'lag_ratio':0, 'run_time':0.5},
        #     ),
        #     explainer_xyxy.to_dots(
        #         aargs={},
        #         gargs={'lag_ratio':0, 'run_time':0.5},
        #     ),
        # ))
        # self.wait(0.3)
        # self.play(AnimationGroup(
        #     explainer_dist.hide_anchor_points(
        #         lag_ratio=0, run_time=0.5,
        #     ),
        #     explainer_xyxy.hide_anchor_points(
        #         lag_ratio=0, run_time=0.5,
        #     ),
        # ))
        # self.wait(0.3)
        # self.remove(explainer_dist, explainer_xyxy)
        
        # # create mini version explainer_dist and explainer_xyxy
        # # data_cls is not used here
        # explainer_dist = ExplainerBbox(
        #     background=background,
        #     data=np.load(MINI_32_DIST_PATH),
        #     data_cls=np.load(MINI_32_PROB_PATH),
        #     sf_nominal=32,
        # )
        # explainer_xyxy = ExplainerBbox(
        #     background=explainer_xyxy_bg[1],
        #     data=np.load(MINI_32_DIST_PATH),
        #     data_cls=np.load(MINI_32_PROB_PATH),
        #     sf_nominal=32,
        # )
        # explainer_dist_bg = Group(explainer_dist, background)
        # explainer_xyxy_bg = Group(explainer_xyxy, explainer_xyxy_bg[1])

        # # show content for explainer_dist and explainer_xyxy
        # self.play(AnimationGroup(
        #     explainer_dist.show_anchor_points(
        #         lag_ratio=0, run_time=0.5,
        #     ),
        #     explainer_xyxy.show_anchor_points(
        #         lag_ratio=0, run_time=0.5,
        #     ),
        # ))
        # self.wait(0.5)
        # self.play(AnimationGroup(
        #     explainer_dist.show_arrows(
        #         arrow_config={'stroke_width':2, 'tip_length':0.06,},
        #         aargs={},
        #         gargs={'lag_ratio':0, 'run_time':0.5},
        #     ),
        #     explainer_xyxy.to_rects(
        #         rect_config={'width':1,},
        #         aargs={},
        #         gargs={'lag_ratio':0, 'run_time':0.5},
        #     ),
        # ))
        # self.wait(0.5)

        # # # ************************************************************
        # # self.next_section(
        # #     'generate explainer_xyxy_2d from explainer_xyxy',
        # #     skip_animations=True,
        # # )
        # # # ************************************************************

        # # ************************************************************
        # self.next_section(
        #     'save for next scene which go back to big map',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # everything = Group(
        #     explainer_dist_bg,
        #     explainer_xyxy_bg,
        #     lf_output_32_dist,
        #     lf_output_32_xyxy,
        #     lf_output_32_xyxy_2d,
        # )
        # save_everything(S013_EVERYTHING, everything)
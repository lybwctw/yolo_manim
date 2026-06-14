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

SAMPLE_IDX = 189

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

        # ************************************************************
        self.next_section(
            'inside anchor points capture',
            skip_animations=True,
        )
        # ************************************************************
        # show true annotation
        self.play(Write(
            annotation,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide labels for now
        self.play(AnimationGroup(
            *(label.animate.set_opacity(opacity=0)
                for label in annotation.get_labels()),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # collect inside/outside anchor points
        aps_in, aps_out = explainer.collect_aps(
            func=lambda ap: any(ap.inside_box(box) for box in annotation.get_boxes()),
        )

        # focus on important anchor points
        self.play(AnimationGroup(
            AnimationGroup(
                *(ap.mob.animate.set_style(
                    **AP_DOT_CONFIG_FOCUS,
                ) for ap in aps_in),
                lag_ratio=0,
                run_time=wt,
            ),
            AnimationGroup(
                *(ap.mob.animate.set_style(
                    **AP_DOT_CONFIG_OTHERS,
                ) for ap in aps_out),
                lag_ratio=0,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # important anchor points capture
        self.play(AnimationGroup(
            *(ap.to_rect(rect_config=AP_RECT_CONFIG_FOCUS,
            ) for ap in aps_in),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # other anchor points capture
        self.play(AnimationGroup(
            *(ap.to_rect(rect_config=AP_RECT_CONFIG_OTHERS,
            ) for ap in aps_out),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # restore all anchor points
        self.play(explainer.to_dots(
            dot_config={},
            aargs={},
            gargs={'lag_ratio': 0.0, 'run_time': wt},
        ))
        self.wait(wt)

        # remove annotation
        self.play(Unwrite(
            annotation,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'sample, from distance to position thinking',
            skip_animations=False,
        )
        # ************************************************************
        # focus on sample anchor point
        aps_sample, aps_others = explainer.collect_aps(
            func=lambda ap: ap.index_flatten == SAMPLE_IDX,
        )
        ap_sample = aps_sample[0]
        self.play(AnimationGroup(
            ap_sample.mob.animate.set_style(
                **AP_DOT_CONFIG_FOCUS,
            ),
            *(ap.mob.animate.set_style(
                **AP_DOT_CONFIG_OTHERS,
            ) for ap in aps_others),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        
        # from distance to position, thinking
        self.play(ap_sample.show_arrows(
            arrow_config={},
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)
        self.play(ap_sample.to_rect(
            rect_config={},
            run_time=wt,
        ))
        self.wait(wt)
        # self.play(ap_sample.to_dot(
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'sample, from absolute distance to relative distance',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # from distance to position, details
        # self.play(sample_ap.show_distance_abs(lag_ratio=0.1, run_time=SHORT_DURATION))
        # self.wait(SHORT_DURATION)
        # self.play(AnimationGroup(
        #     sample_ap.arrows.animate(run_time=SHORT_DURATION).set_opacity(0.3),
        #     sample_ap.show_divide(run_time=SHORT_DURATION),
        # ))
        # self.wait(SHORT_DURATION)
        # self.play(AnimationGroup(
        #     sample_ap.arrows.animate(run_time=SHORT_DURATION).set_opacity(1.0),
        #     sample_ap.abs_to_rela(
        #         aargs={'run_time':0.3,},
        #         gargs={'lag_ratio':0.1, 'run_time':SHORT_DURATION,},
        #     ),
        # ))
        # self.wait(SHORT_DURATION)

        # # ************************************************************
        # self.next_section(
        #     'sample, detailed computation from distance to position',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # make room for equations
        # self.play(explainer_dist_bg.animate(run_time=SHORT_DURATION).shift(LEFT*2).scale(0.9))
        # self.wait(SHORT_DURATION)

        # # create equations for sample
        # sample_eq = sample_ap.create_decode_equations(
        #     buff=0.3,
        # ).shift(RIGHT*3)
        # self.play(Create(sample_eq))
        # self.wait(SHORT_DURATION)

        # # show point from x1y1
        # self.play(explainer_dist.show_point_from_xy(
        #     sample_idx,
        #     direction=UL,
        #     pargs={'run_time':SHORT_DURATION, 'time_width':2},
        #     targs={},
        #     gargs={'lag_ratio':SHORT_DURATION,},
        # ))
        # self.wait(SHORT_DURATION)
        # self.play(explainer_dist.hide_xy_txts(run_time=SHORT_DURATION))

        # # show point from x2y2
        # self.play(explainer_dist.show_point_from_xy(
        #     sample_idx,
        #     direction=DR,
        #     pargs={'run_time':1, 'time_width':2},
        #     targs={},
        #     gargs={'lag_ratio':SHORT_DURATION,},
        # ))
        # self.wait(SHORT_DURATION)
        # self.play(explainer_dist.hide_xy_txts(run_time=SHORT_DURATION))
        # self.wait(SHORT_DURATION)

        # # to rect
        # self.play(AnimationGroup(
        #     sample_ap.hide_distance(run_time=SHORT_DURATION, lag_ratio=0),
        #     sample_ap.to_rect(run_time=SHORT_DURATION),
        # ))
        # self.wait(SHORT_DURATION)

        # # clean
        # self.play(AnimationGroup(
        #     sample_ap.hide_arrows(run_time=SHORT_DURATION),
        #     sample_ap.to_dot(run_time=SHORT_DURATION),
        #     Uncreate(sample_eq, run_time=SHORT_DURATION),
        # ))
        # self.wait(SHORT_DURATION)

        # # ************************************************************
        # self.next_section(
        #     'loop, from distance to position',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # TODO, more natural way of looping
        # k=1         # TODO, proper loop number
        # idxs = random.sample(
        #     range(data_dist.shape[0]*data_dist.shape[1]),
        #     k=k,
        # )
        # for idx in idxs:
        #     # highlight one target point
        #     sample_ap, other_aps = explainer_dist.collect_focus_ap(idx)
        #     self.play(AnimationGroup(
        #         sample_ap.animate(run_time=SHORT_DURATION).set_pattern(opacity=1.0),
        #         AnimationGroup(
        #             *(ap.animate.set_pattern(opacity=0.3) for ap in other_aps),
        #             lag_ratio=0, run_time=SHORT_DURATION,
        #         )
        #     ))
        #     self.wait(SHORT_DURATION)

        #     # show arrows
        #     self.play(sample_ap.show_arrows(lag_ratio=0.0, run_time=SHORT_DURATION))
        #     self.wait(SHORT_DURATION)

        #     # show equations
        #     sample_eq = sample_ap.create_decode_equations(
        #         buff=0.3,
        #     ).shift(RIGHT*3)
        #     self.play(Create(sample_eq, run_time=SHORT_DURATION))
        #     self.wait(SHORT_DURATION)

        #     # to rect
        #     self.play(sample_ap.to_rect(run_time=SHORT_DURATION))
        #     self.wait(SHORT_DURATION)

        #     # restore
        #     self.play(AnimationGroup(
        #         sample_ap.hide_arrows(run_time=SHORT_DURATION),
        #         sample_ap.to_dot(run_time=SHORT_DURATION),
        #         Uncreate(sample_eq, run_time=SHORT_DURATION),
        #     ))
        #     self.wait(SHORT_DURATION)
        
        # # make all aps opacity 1.0
        # self.play(AnimationGroup(
        #     *(ap.animate.set_pattern(opacity=1.0)
        #     for ap in explainer_dist.anchor_points),
        #     lag_ratio=0.0,
        #     run_time=SHORT_DURATION,
        # ))
        # self.wait(SHORT_DURATION)

        # # ************************************************************
        # self.next_section(
        #     'global, generate distance tensor',
        #     skip_animations=True,
        # )
        # # ************************************************************
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
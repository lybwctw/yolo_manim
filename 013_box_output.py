from manim import *

from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.general import export_mobs
from utils.layers_fake import LayersFake
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.constants import *

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

AP_RECT_CONFIG_THIN = {
    'stroke_color': WHITE,
    'stroke_opacity': 0.3,
    'stroke_width': 1.0,
}

# ---------------- explainer related -------------------
SAMPLE_IDX = 189
N_LOOP_SAMPLES = 3

ARROW_CONFIG_20x20 = {
    'stroke_width': 1,
    'tip_length': 0.03,
    'buff': 0.0,
    'max_stroke_width_to_length_ratio': 15,         # FIXME: 5 by default
    'max_tip_length_to_length_ratio': 0.85,          # FIXME: 0.25 by default
}
ARROW_CONFIG_4x4 = {
    'stroke_width': 3,
    'tip_length': 0.2,
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
TENSOR_XYXY_2D_CONFIG = {
    'line_width': 0.3,
    'stroke_width': 1.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
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
            skip_animations=False,
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
            skip_animations=False,
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
                'run_time':wt,
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
            skip_animations=False,
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
            'sample, xyxy output',
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
            'explainer: two initial explainers',
            skip_animations=False,
        )
        # ************************************************************
        # scale and shift explainer
        self.play(system.animate(
            run_time=wt,
        ).scale(0.5).shift(UP*2))
        self.wait(wt)

        # renaming
        system_offset = system
        system_xyxy = system_offset.copy()
        background_offset = system_offset[0]
        explainer_offset = system_offset[1]
        background_xyxy = system_xyxy[0]
        explainer_xyxy = system_xyxy[1]

        # create a explainer copy representing position
        self.play(system_xyxy.animate(
            run_time=wt,
        ).shift(RIGHT*5))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'offset: explainer to tensor',
            skip_animations=False,
        )
        # ************************************************************
        # synced creation: arrows + tensors
        tensor_offset = explainer_offset.create_tensor_offset(
            cell_config=TENSOR_OFFSET_CONFIG,
            buff_ratio=TENSOR_BUFF_RATIO,
        )
        tensor_offset.shift(DOWN*4)
        self.play(AnimationGroup(
            *(AnimationGroup(
                ap.show_arrows(
                    arrow_config=ARROW_CONFIG_20x20,
                ),
                Write(series),
            ) for ap, series in zip(
                explainer_offset.anchor_points,
                tensor_offset,
            )),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'xyxy: explainer to tensor',
            skip_animations=False,
        )
        # ************************************************************
        # synced creation: rects + tensors
        tensor_xyxy = explainer_xyxy.create_tensor_xyxy(
            cell_config=TENSOR_XYXY_CONFIG,
            buff_ratio=TENSOR_BUFF_RATIO,
        )
        tensor_xyxy.shift(DOWN*4)
        self.play(AnimationGroup(
            *(AnimationGroup(
                ap.to_rect(
                    rect_config=AP_RECT_CONFIG_THIN,
                ),
                Write(series),
            ) for ap, series in zip(
                explainer_xyxy.anchor_points,
                tensor_xyxy,
            )),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'reshape xyxy tensor to 2d version',
            skip_animations=False,
        )
        # ************************************************************
        # make room for reshaped xyxy tensor
        self.play(AnimationGroup(
            system_offset.animate.shift(LEFT*1),
            tensor_offset.animate.shift(LEFT*1),
            system_xyxy.animate.shift(LEFT*2),
            tensor_xyxy.animate.shift(LEFT*2),
            run_time=wt,
        ))
        self.wait(wt)

        # create 2d version xyxy tensor
        tensor_xyxy_2d_target = explainer_xyxy.create_tensor_xyxy_2d(
            line_config=TENSOR_XYXY_2D_CONFIG,
            w_buff_ratio=0.1,               # buff between rows
            h_buff_ratio=0.017,             # buff between cols
        ).move_to(RIGHT*4.5)

        # transform xyxy into 2d version
        tensor_xyxy_2d = tensor_xyxy.copy()
        self.play(AnimationGroup(
            *(Transform(stack, row) for stack, row in zip(
                tensor_xyxy_2d, tensor_xyxy_2d_target
            )),
            lag_ratio=0.5,
            run_time=wt,                    # NOTE: make this long
            rate_func=rate_functions.ease_in_circ,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'simplify tensor_offset/tensor_xyxy/tensor_xyxy_2d' \
            'into t32_offset/t32_xyxy/t32_xyxy_2d',
            skip_animations=False,
        )
        # ************************************************************
        # replace tensor_offset with t32_offset
        t32_offset = LayersFake(
            n=4,
            ref=VGroup(tensor_offset[0][0], tensor_offset[-1][0]),
            expanded=True,
            buff=0.075,         # based on tensor_offset's buff
            width_nominal=20,
            height_nominal=20,
            depth_nominal=4,
            rect_config={},
        ).move_to(tensor_offset)
        self.play(AnimationGroup(
            Unwrite(tensor_offset),
            Write(t32_offset),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.play(ReplacementTransform(
        #     tensor_offset,
        #     t32_offset,
        #     run_time=wt,
        # ))
        self.wait(wt)

        # replace tensor_xyxy with t32_xyxy
        t32_xyxy = LayersFake(
            n=4,
            ref=VGroup(tensor_xyxy[0][0], tensor_xyxy[-1][0]),
            expanded=True,
            buff=0.075,         # based on tensor_offset's buff
            width_nominal=20,
            height_nominal=20,
            depth_nominal=4,
            rect_config={},
        ).move_to(tensor_xyxy)
        self.play(AnimationGroup(
            Unwrite(tensor_xyxy),
            Write(t32_xyxy),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.play(ReplacementTransform(
        #     tensor_xyxy,
        #     t32_xyxy,
        #     run_time=wt,
        # ))
        self.wait(wt)

        # replace tensor_xyxy_2d with t32_xyxy_2d
        t32_xyxy_2d = LayersFake(
            n=1,
            width=1.0,
            height=3.0,
            expanded=True,
            # buff=0.075,
            width_nominal=4,
            height_nominal=400,
            depth_nominal=1,
            rect_config={},
        ).set_x(
            tensor_xyxy_2d.get_x(),
        ).set_y(
            t32_xyxy.get_y(),
        )
        # self.play(AnimationGroup(
        #     Unwrite(tensor_xyxy_2d),
        #     Write(t32_xyxy_2d),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        self.play(ReplacementTransform(
            tensor_xyxy_2d,
            t32_xyxy_2d,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'simplify system_offset and system_xyxy ' \
            'into s32_offset and s32_xyxy' \
            '4x4 mini version',
            skip_animations=False,
        )
        # ************************************************************
        # clean up system_offset and system_xyxy
        self.play(AnimationGroup(
            explainer_offset.hide_arrows(
                aargs={},
                gargs={'lag_ratio':0.0},
            ),
            explainer_xyxy.to_dots(
                aargs={},
                gargs={'lag_ratio':0.0},
            ),
            run_time=wt,
        ))
        self.play(AnimationGroup(
            explainer_offset.hide_anchor_points(
                lag_ratio=0.0,
            ),
            explainer_xyxy.hide_anchor_points(
                lag_ratio=0.0,
            ),
            run_time=wt,
        ))
        self.wait(wt)
        self.remove(explainer_offset, explainer_xyxy)
        
        # create e32_offset+e32_xyxy -> t32_offset+t32_xyxy
        e32_offset = Explainer.from_file(
            background=background_offset,
            version=160,
            dot_config={},
            rect_config={},
        )
        e32_xyxy = Explainer.from_file(
            background=background_xyxy,
            version=160,
            dot_config={},
            rect_config={},
        )
        s32_offset = Group(background_offset, e32_offset)
        s32_xyxy = Group(background_xyxy, e32_xyxy)
        self.add(e32_offset, e32_xyxy)

        # show anchor points of new explainers
        self.play(AnimationGroup(
            e32_offset.show_anchor_points(
                lag_ratio=0.5,
            ),
            e32_xyxy.show_anchor_points(
                lag_ratio=0.5,
            ),
            run_time=wt,
        ))
        self.wait(wt)

        # show arrows and rects separately
        self.play(AnimationGroup(
            e32_offset.show_arrows(
                arrow_config=ARROW_CONFIG_4x4,
            ),
            e32_xyxy.to_rects(
                rect_config={},
                aargs={},
                gargs={
                    'lag_ratio':0,
                    'run_time':wt,
                },
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'into big map',
            skip_animations=False,
        )
        # ************************************************************
        ac_game = ArrowComment(False, RIGHT).scale(0.8).move_to(LEFT*10).set_color(PURE_RED)
        aci_8 = ArrowComment(False, RIGHT).scale(0.8).move_to(UP*5)
        act_8 = ArrowComment(False, RIGHT).scale(0.8).move_to(DOWN*5)
        act_9 = ArrowComment(False, RIGHT).scale(0.8).move_to(DOWN*5)
        acm_7 = ArrowComment(True, DOWN).scale(0.8).move_to(LEFT*10)
        acm_8 = ArrowComment(True, DOWN).scale(0.8).move_to(RIGHT*10)

        # show big map without s32_xyxy_2d
        mobs = Group(
            Mobject(), s32_offset, aci_8,     s32_xyxy, Mobject(), Mobject(),
            Mobject(), acm_7,      Mobject(), acm_8,    Mobject(), Mobject(),
            ac_game,   t32_offset, act_8,     t32_xyxy, act_9,     t32_xyxy_2d,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=6,
            buff=0.5,
        ).scale(0.5).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # introduce s32_xyxy_2d
        aci_9 = aci_8.copy().move_to(UP*5)
        acm_9 = acm_8.copy().move_to(RIGHT*5)
        s32_xyxy_2d = s32_xyxy.copy().move_to(UP*5)
        mobs = Group(
            Mobject(), s32_offset, aci_8,     s32_xyxy, aci_9,     s32_xyxy_2d,
            Mobject(), acm_7,      Mobject(), acm_8,    Mobject(), acm_9,
            ac_game,   t32_offset, act_8,     t32_xyxy, act_9,     t32_xyxy_2d,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=6,
            buff=0.5,
        ).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # show shapes for tensors
        ac_all = VGroup(
            aci_8, aci_9,
            acm_7, acm_8, acm_9,
            ac_game, act_8, act_9,
        ).save_state()
        self.play(ac_all.animate(
            run_time=wt,
        ).fade(0.8))
        self.play(AnimationGroup(
            ShowShape(t32_offset, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_xyxy, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_xyxy_2d, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes for tensors
        self.play(AnimationGroup(
            HideShape(t32_offset),
            HideShape(t32_xyxy),
            HideShape(t32_xyxy_2d),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(ac_all.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        export_mobs(__file__, mobs)     # NOTE: used by ???
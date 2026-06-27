from manim import *

from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs
from utils.constants import *

# TODO: adjust layer gaps for previous scenes
# TODO: layer gap as a series of constants: small / medium / big

GAP_POSTPROCESS = 0.2
MERGED_SCALE_FACTOR = 1/1.1         # NOTE: reverse of 015

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs from 015',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('015')
        (
            s32_offset, aci_7,         s32_xyxy,    aci_8, s32_xyxy_2d,
            s32_prob,   aci_9,         s32_prob_2d,
            mas_2,      s32_merged_2d,
            mat_1,
            t32_offset, act_7,         t32_xyxy,    act_8, t32_xyxy_2d,
            t32_prob,   act_9,         t32_prob_2d,
            mat_2,      t32_merged_2d,
        ) = mobs

        # reference
        ac_all = VGroup(
                   aci_7, aci_8, aci_9, mas_2,
            mat_1, act_7, act_8, act_9, mat_2,
        )
        
        self.add(mobs)
        self.wait()

        # make room in the right
        self.play(mobs.animate.shift(LEFT*10.))
        self.wait()

        # ************************************************************
        self.next_section(
            "[1a] intuition view: max class select",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        aci_10 = aci_9.copy().next_to(
            s32_merged_2d,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        ac_all.add(aci_10)
        self.play(Write(
            aci_10,
            run_time=wt,
        ))

        # copy system
        s32_max = s32_merged_2d.copy()
        self.play(s32_max.animate(
            run_time=1.0,
        ).next_to(
            aci_10,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))

        # apply max select on copy
        s32_max[-1].apply_max_select(
            self,
            run_time_ratio=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[1b] tensor view: max class select",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        act_10 = act_9.copy().next_to(
            t32_merged_2d,
            RIGHT,
            buff=GAP_POSTPROCESS
        ).align_to(aci_10, LEFT)
        ac_all.add(act_10)
        self.play(Write(
            act_10,
            run_time=wt,
        ))

        # copy system
        t32_max = t32_merged_2d.copy()
        self.play(t32_max.animate(
            run_time=wt,
        ).next_to(
            act_10,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_max.get_x()))

        # apply max select on copy
        self.play(t32_max.animate(
            run_time=wt,
        ).stretch_to_fit_width(
            t32_merged_2d.width * 0.8
        ))
        t32_max.width_nominal = 6   # width: 4+3 -> 4+2
        self.wait(wt)

        # show shapes
        ac_all.save_state()
        self.play(AnimationGroup(
            ac_all.animate.fade(0.7),
            AnimationGroup(
                ShowShape(t32_merged_2d, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
                ShowShape(t32_max, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_merged_2d),
                HideShape(t32_max),
            ),
            ac_all.animate.restore(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[2a] intuition view: conf filter",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        aci_11 = aci_10.copy().next_to(
            s32_max,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        ac_all.add(aci_11)
        self.play(Write(
            aci_11,
            run_time=wt,
        ))

        # copy system
        s32_conf = s32_max.copy()
        self.play(s32_conf.animate(
            run_time=wt,
        ).next_to(
            aci_11,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))
        # TODO: use hardcoded removal
        s32_conf[-1].apply_keep_random(
            scene=self,
            ratio=0.5,
            run_time_ratio=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[2b] tensor view: conf filter",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        act_11 = act_10.copy().next_to(
            t32_max,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).align_to(aci_11, LEFT)
        ac_all.add(act_11)
        self.play(Write(
            act_11,
            run_time=wt,
        ))

        # copy system
        t32_conf = t32_max.copy()
        self.play(t32_conf.animate(
            run_time=wt,
        ).next_to(
            act_11,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_conf.get_x()))

        # apply conf filter on copy
        self.play(t32_conf.animate(
            run_time=wt,
        ).stretch_to_fit_height(
            t32_max.height * 0.6
        ))
        t32_conf.height_nominal = 'k'   # height: 400 -> k
        self.wait(wt)

        # show shapes
        ac_all.save_state()
        self.play(AnimationGroup(
            ac_all.animate.fade(0.7),
            AnimationGroup(
                ShowShape(t32_max, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
                ShowShape(t32_conf, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_max),
                HideShape(t32_conf),
            ),
            ac_all.animate.restore(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[3a] intuition view: nms filter",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        aci_12 = aci_11.copy().next_to(
            s32_conf,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        ac_all.add(aci_12)
        self.play(Write(
            aci_12,
            run_time=wt,
        ))

        # copy system
        s32_nms = s32_conf.copy()
        self.play(s32_nms.animate(
            run_time=wt,
        ).next_to(
            aci_12,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))
        # TODO: use hardcoded removal
        s32_nms[-1].apply_keep_random(
            scene=self,
            ratio=0.7,
            run_time_ratio=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[3b] tensor view: nms filter",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        act_12 = act_11.copy().next_to(
            t32_conf,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).align_to(aci_12, LEFT)
        ac_all.add(act_12)
        self.play(Write(
            act_12,
            run_time=wt,
        ))

        # copy system
        t32_nms = t32_conf.copy()
        self.play(t32_nms.animate(
            run_time=wt,
        ).next_to(
            act_12,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_nms.get_x()))

        # apply nms filter on copy
        self.play(t32_nms.animate(
                run_time=wt,
            ).stretch_to_fit_height(
            t32_conf.height * 0.6
        ))
        t32_nms.height_nominal = 'm'      # height: k -> m
        self.wait(wt)

        # show shapes
        ac_all.save_state()
        self.play(AnimationGroup(
            ac_all.animate.fade(0.7),
            AnimationGroup(
                ShowShape(t32_conf, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
                ShowShape(t32_nms, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_conf),
                HideShape(t32_nms),
            ),
            ac_all.animate.restore(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[4a] intuition view: scale back",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        aci_13 = aci_12.copy().next_to(
            s32_nms,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        ac_all.add(aci_13)
        self.play(Write(
            aci_13,
            run_time=wt,
        ))

        # copy system
        s32_back = s32_nms.copy() # FIXME: HERE EHRHERERERE
        self.play(s32_back.animate(
            run_time=wt,
        ).next_to(
            aci_13,
            RIGHT,
            buff=GAP_POSTPROCESS+0.3,   # more for scale up later
        ))

        s32_back[-1].apply_scale_back(
            scene=self,
            scale_factor=1.5,
            run_time_ratio=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "[4b] tensor view: scale back",
            skip_animations=False,
        )
        # ************************************************************
        # new arrow
        act_13 = act_12.copy().next_to(
            t32_nms,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).align_to(aci_13, LEFT)
        ac_all.add(act_13)
        self.play(Write(
            act_13,
            run_time=wt,
        ))

        # copy system
        t32_back = t32_nms.copy()
        self.play(t32_back.animate(
            run_time=wt,
        ).next_to(
            act_13,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_back.get_x()))

        # apply scale back on copy
        self.play(t32_back.animate(
            run_time=wt,
        ).stretch_to_fit_height(
            t32_nms.height * 0.9
        ))
        t32_back.height_nominal = 'n'      # height: m -> n(m)
        self.wait(wt)

        # show shapes
        ac_all.save_state()
        self.play(AnimationGroup(
            ac_all.animate.fade(0.7),
            AnimationGroup(
                ShowShape(t32_nms, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
                ShowShape(t32_back, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_nms),
                HideShape(t32_back),
            ),
            ac_all.animate.restore(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back to output big map',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            s32_offset, aci_7,         s32_xyxy,    aci_8,   s32_xyxy_2d,
            s32_prob,   aci_9,         s32_prob_2d,
            mas_2,      s32_merged_2d, aci_10,      s32_max, aci_11,      s32_conf, aci_12, s32_nms, aci_13, s32_back,
            mat_1,      
            t32_offset, act_7,         t32_xyxy,    act_8, t32_xyxy_2d,
            t32_prob,   act_9,         t32_prob_2d,
            mat_2,      t32_merged_2d, act_10,      t32_max, act_11,      t32_conf, act_12, t32_nms, act_13, t32_back,
        )
        self.play(mobs.animate(
            run_time=wt,
        ).scale(0.6).center())
        self.wait(wt)

        # show shapes
        ac_all.save_state()
        self.play(ac_all.animate(
            run_time=wt,
        ).fade(0.7))
        # FIXME: or medium shape text?
        self.play(AnimationGroup(
            *(ShowShape(tensor, text_config=SMALL_SHAPE_TEXT_CONFIG)
             for tensor in (
                t32_offset, t32_xyxy, t32_xyxy_2d,
                t32_prob, t32_prob_2d,
                t32_merged_2d, t32_max, t32_conf, t32_nms, t32_back,
            )),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape(tensor) for tensor in (
                t32_offset, t32_xyxy, t32_xyxy_2d,
                t32_prob, t32_prob_2d,
                t32_merged_2d, t32_max, t32_conf, t32_nms, t32_back,
            )),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.play(ac_all.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        export_mobs(__file__, mobs)         # NOTE: used by 023

        # ************************************************************
        self.next_section(
            "decode part and postprocess part",
            skip_animations=False,
        )
        # ************************************************************
        s32_mid_decode = Group(
            aci_7, s32_xyxy, aci_8, s32_xyxy_2d, mas_2,
            aci_9, s32_prob_2d,
        )
        s32_mid_postprocess = Group(
            aci_10, s32_max, aci_11, s32_conf, aci_12, s32_nms, aci_13,
        )
        t32_mid_decode = Group(
            act_7, t32_xyxy, act_8, t32_xyxy_2d, mat_2,
            act_9, t32_prob_2d,
        )
        t32_mid_postprocess = Group(
            act_10, t32_max, act_11, t32_conf, act_12, t32_nms, act_13,
        )

        self.play(AnimationGroup(
            *(mob.animate.fade(0.9)
               for mob in (
                mat_1, s32_mid_decode, s32_mid_postprocess,
                t32_mid_decode, t32_mid_postprocess,
               )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'simplify into two steps on raw output',
            skip_animations=False,
        )
        # ************************************************************
        # new arrows
        aci_14 = ArrowComment(False, RIGHT).scale(0.2).move_to(UP*5.0)
        aci_15 = ArrowComment(False, RIGHT).scale(0.2).move_to(UP*5.0)
        act_game = ArrowComment(False, RIGHT).scale(0.2).move_to(LEFT*10.0)
        act_14 = ArrowComment(False, RIGHT).scale(0.2).move_to(DOWN*5.0)
        act_15 = ArrowComment(False, RIGHT).scale(0.2).move_to(DOWN*5.0)

        mobs = Group(
            Mobject(), s32_offset, s32_prob, aci_14, s32_merged_2d, aci_15, s32_back,
            act_game,  t32_offset, t32_prob, act_14, t32_merged_2d, act_15, t32_back,
        )
        mobs.generate_target()
        mobs.target[4].scale(MERGED_SCALE_FACTOR)   # merged was scaled up
        mobs.target[6].scale(MERGED_SCALE_FACTOR)   # merged was scaled up
        mobs.target.arrange_in_grid(
            rows=2,
            cols=7,
            buff=0.3,
        ).center().scale(1.5)
        self.play(AnimationGroup(
            *(FadeOut(mob) for mob in (
                mat_1,
                s32_mid_decode, s32_mid_postprocess,
                t32_mid_decode, t32_mid_postprocess,
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'into bigger map: from input to output',
            skip_animations=False,
        )
        # ************************************************************
        aci_1 = aci_14.copy().move_to(LEFT*10)
        act_1 = act_14.copy().move_to(LEFT*10)
        sin_raw = s32_back[0].copy().set_opacity(1.0).move_to(LEFT*10)
        sin_norm = s32_merged_2d[0].copy().set_opacity(1.0).move_to(LEFT*10)
        tin_raw = LayersFake(
            n=3,
            ref=sin_raw,
            expanded=True,
            width_nominal=sin_raw.width_nominal,
            height_nominal=sin_raw.height_nominal,
            buff=0.05,              # TODO, natural buff?
        ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?
        tin_norm = LayersFake(
            n=3,
            ref=sin_norm,
            expanded=True,
            width_nominal=sin_norm.width_nominal,
            height_nominal=sin_norm.height_nominal,
            buff=0.05,              # TODO, natural buff?
        ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?

        mobs = Group(
            sin_raw, aci_1, sin_norm, Mobject(), s32_offset, s32_prob, aci_14, s32_merged_2d, aci_15, s32_back,
            tin_raw, act_1, tin_norm, act_game,  t32_offset, t32_prob, act_14, t32_merged_2d, act_15, t32_back,
        )
        mobs.generate_target()

        # make output tensors smaller to match input tensors
        mobs.target[14].scale(0.6)
        mobs.target[15].scale(0.6)
        mobs.target[17].scale(0.7)
        mobs.target[19].scale(0.7)
        mobs.target.arrange_in_grid(
            rows=2,
            cols=10,
            # buff=0.5,
        ).center().scale(0.95)

        # FIXME: more gap on output tensor layers
        mobs.target[14].adjust_gap(buff=0.05)
        mobs.target[15].adjust_gap(buff=0.05)
        # orig_center = mobs.target[14].get_center()
        # mobs.target[14].rects.arrange(
        #     UR,
        #     buff=-mobs.target[14][0].width + 0.09,
        # ).move_to(orig_center)
        # orig_center = mobs.target[15].get_center()
        # mobs.target[15].rects.arrange(
        #    UR,
        #     buff=-mobs.target[15][0].width + 0.08,
        # ).move_to(orig_center)

        # back to big map
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait()

        # show shape on tensors

        # ************************************************************
        self.next_section(
            'show shape on simplified output map',
            skip_animations=False,
        )
        # ************************************************************
        ac_all = VGroup(
            aci_1,           aci_14, aci_15,
            act_1, act_game, act_14, act_15
        )
        tensor_mobs = (
            tin_raw, tin_norm, t32_offset, t32_prob, t32_merged_2d, t32_back,
        )

        # show shapes for tensor mobs
        ac_all.save_state()
        self.play(ac_all.animate(
            run_time=wt,
        ).fade(0.8))
        self.play(AnimationGroup(
            *(ShowShape(mob, text_config=SMALL_SHAPE_TEXT_CONFIG)
              for mob in tensor_mobs),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait()

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape(mob)
              for mob in tensor_mobs),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(ac_all.animate(
            run_time=wt,
        ).restore())

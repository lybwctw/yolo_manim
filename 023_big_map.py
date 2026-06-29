from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs

GAP_POSTPROCESS = 0.2
MERGED_SCALE_FACTOR = 1/1.1

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        mobs = import_mobs('020')
        (
            s32_offset, aci_7,         s32_xyxy,    aci_8,   s32_xyxy_2d,
            s32_prob,   aci_9,         s32_prob_2d,
            mas_2,      s32_merged_2d, aci_10,      s32_max, aci_11,      s32_conf, aci_12, s32_nms, aci_13, s32_back,
            mat_1,      
            t32_offset, act_7,         t32_xyxy,    act_8, t32_xyxy_2d,
            t32_prob,   act_9,         t32_prob_2d,
            mat_2,      t32_merged_2d, act_10,      t32_max, act_11,      t32_conf, act_12, t32_nms, act_13, t32_back,
        ) = mobs

        self.add(mobs)
        self.wait(wt)

        # scale down to make root in the left
        self.play(mobs.animate(
            run_time=0.5,
        ).scale(0.93).shift(RIGHT*0.5))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert s32_reg in intuition view',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of s32_offset
        aci_6 = aci_7.copy().rotate(180*DEGREES).next_to(
            s32_offset,
            LEFT,
            buff=0.08,              # manual offset
        )
        s32_distrib = s32_offset.copy()
        self.play(Write(
            aci_6,
            run_time=wt,
        ))
        self.play(s32_distrib.animate(
            run_time=wt,
        ).next_to(s32_offset, LEFT, buff=0.55))   # manual offset
        self.wait(wt)

        # remove original arrows
        self.play(s32_distrib[-1].hide_arrows(
            gargs={
                'lag_ratio': 0.5,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        # show shrinked pcells
        self.play(s32_distrib[-1].show_pcells(
            sf_pcell=0.5,
            box_config={},
            gargs={
                'lag_ratio': 0.5,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert t32_distrib in tensor view',
            skip_animations=True,
        )
        # ************************************************************
        # shift mat_1 to make room
        self.play(mat_1.animate(
            run_time=wt,
        ).shift(LEFT*1.55))                 # manual offset
        self.wait(wt)

        act_6 = act_7.copy().rotate(180*DEGREES).align_to(
            aci_6,
            LEFT,
        )
        # create mini t32_distrib
        t32_distrib = LayersFake(
            n=8,                            # fake 64
            ref=t32_offset,
            buff=0.05,                  # TODO: make this constant
            width_nominal=20,
            height_nominal=20,
            depth_nominal=64,
            expanded=True,
        ).next_to(
            t32_offset,
            LEFT,
            buff=0.60,
        )

        self.play(Write(
            act_6,
            run_time=wt,
        ))
        self.play(Write(
            t32_distrib,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # adjust new arrows
        self.play(AnimationGroup(
            mat_1.output[1].animate.put_start_and_end_on(
                start=mat_1.output[1].get_start(),
                end=t32_prob.get_corner(LEFT)+LEFT*0.3,
            ),
            Rotate(aci_6, PI),
            Rotate(act_6, PI),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            "highlight decode stage and postprocess stage",
            skip_animations=False,
        )
        # ************************************************************
        s32_mid_decode = Group(
            aci_6, s32_offset, aci_7, s32_xyxy, aci_8, s32_xyxy_2d, mas_2,
            aci_9, s32_prob_2d,
        )
        s32_mid_postprocess = Group(
            aci_10, s32_max, aci_11, s32_conf, aci_12, s32_nms, aci_13,
        )
        t32_mid_decode = Group(
            act_6, t32_offset, act_7, t32_xyxy, act_8, t32_xyxy_2d, mat_2,
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
            Mobject(), s32_distrib, s32_prob, aci_14, s32_merged_2d, aci_15, s32_back,
            act_game,  t32_distrib, t32_prob, act_14, t32_merged_2d, act_15, t32_back,
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
            sin_raw, aci_1, sin_norm, Mobject(), s32_distrib, s32_prob, aci_14, s32_merged_2d, aci_15, s32_back,
            tin_raw, act_1, tin_norm, act_game,  t32_distrib, t32_prob, act_14, t32_merged_2d, act_15, t32_back,
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

        # TODO: make gaps a series of variables
        mobs.target[14].adjust_gap(buff=0.05)
        mobs.target[15].adjust_gap(buff=0.05)

        # back to big map
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

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
            tin_raw, tin_norm, t32_distrib, t32_prob, t32_merged_2d, t32_back,
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

        mobs = Group(
            sin_raw, aci_1, sin_norm,            s32_distrib, s32_prob, aci_14, s32_merged_2d, aci_15, s32_back,
            tin_raw, act_1, tin_norm, act_game,  t32_distrib, t32_prob, act_14, t32_merged_2d, act_15, t32_back,
        )
        export_mobs(__file__, mobs)         # NOTE: used by 025
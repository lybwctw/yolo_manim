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
            skip_animations=False,
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
            # acb_aa.animate.rotate(180*DEGREES),
            # acb_11.animate.rotate(180*DEGREES),
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

        # # ************************************************************
        # # NOTE: a copy from 020
        # self.next_section(
        #     "highlight decode stage and postprocess stage",
        #     skip_animations=False,
        # )
        # # ************************************************************
        # s32_mid_decode = Group(
        #     acb_aa, s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, marrow_out_iview,
        #     acc_ab, s32_prob_2d,
        # )
        # s32_mid_postprocess = Group(
        #     ac_a, s32_max, ac_b, s32_conf, ac_c, s32_nms, ac_d,
        # )
        # t32_mid_decode = Group(
        #     acb_11, t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d, marrow_out_tview,
        #     acc_12, t32_prob_2d,
        # )
        # t32_mid_postprocess = Group(
        #     ac_1, t32_max, ac_2, t32_conf, ac_3, t32_nms, ac_4,
        # )

        # self.play(AnimationGroup(
        #     marrow_in_tview.animate.fade(0.9),
        #     s32_mid_decode.animate.fade(0.9),
        #     s32_mid_postprocess.animate.fade(0.9),
        #     t32_mid_decode.animate.fade(0.9),
        #     t32_mid_postprocess.animate.fade(0.9),
        #     run_time=0.5,
        #     lag_ratio=0.0,
        # ))

        # # ************************************************************
        # # NOTE: a copy from 020
        # self.next_section(
        #     'simplify into two steps on raw output',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # aco_a = ArrowComment(False, RIGHT).scale(0.2).shift(UP*10)
        # aco_b = ArrowComment(False, RIGHT).scale(0.2).shift(UP*10)
        # ac_game = ArrowComment(False, RIGHT).scale(0.2).shift(LEFT*10)
        # aco_1 = ArrowComment(False, RIGHT).scale(0.2).shift(DOWN*10)
        # aco_2 = ArrowComment(False, RIGHT).scale(0.2).shift(DOWN*10)

        # mobs = Group(
        #     Mobject(), s32_reg, s32_prob, aco_a, s32_merged_2d, aco_b, s32_back,
        #     ac_game,   t32_reg, t32_prob, aco_1, t32_merged_2d, aco_2, t32_back,
        # )

        # mobs.generate_target()
        # mobs.target[4].scale(MERGED_SCALE_FACTOR)   # merged was scaled up
        # mobs.target[6].scale(MERGED_SCALE_FACTOR)   # merged was scaled up
        # mobs.target.arrange_in_grid(
        #     rows=2,
        #     cols=7,
        #     buff=0.3,
        # ).center().scale(1.5)
        # self.play(AnimationGroup(
        #     FadeOut(s32_mid_decode),
        #     FadeOut(s32_mid_postprocess),
        #     FadeOut(marrow_in_tview),
        #     FadeOut(t32_mid_decode),
        #     FadeOut(t32_mid_postprocess),
        #     run_time=0.5,
        #     lag_ratio=0.5,
        # ))
        # self.play(MoveToTarget(
        #     mobs,
        #     run_time=0.5,
        # ))
        # self.wait()


        # # ************************************************************
        # # NOTE: a copy from 020
        # self.next_section(
        #     'into bigger map: from input to output',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # aci_a = aco_a.copy().move_to(LEFT*10)
        # aci_1 = aco_a.copy().move_to(LEFT*10)
        # sin_raw = s32_back[0].copy().set_opacity(1.0).move_to(LEFT*10)
        # sin_pad = s32_merged_2d[0].copy().set_opacity(1.0).move_to(LEFT*10)
        # tin_raw = LayersFake(
        #     n=3,
        #     ref=sin_raw,
        #     expanded=True,
        #     width_nominal=sin_raw.width_nominal,
        #     height_nominal=sin_raw.height_nominal,
        #     buff=0.05,              # TODO, natural buff?
        # ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?
        # tin_pad = LayersFake(
        #     n=3,
        #     ref=sin_pad,
        #     expanded=True,
        #     width_nominal=sin_pad.width_nominal,
        #     height_nominal=sin_pad.height_nominal,
        #     buff=0.05,              # TODO, natural buff?
        # ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?

        # mobs = Group(
        #     sin_raw, aci_a, sin_pad, Mobject(), s32_reg, s32_prob, aco_a, s32_merged_2d, aco_b, s32_back,
        #     tin_raw, aci_1, tin_pad, ac_game,   t32_reg, t32_prob, aco_1, t32_merged_2d, aco_2, t32_back,
        # )
        # mobs.generate_target()
        # # make output smaller to match input tensors
        # mobs.target[14].scale(0.6)
        # mobs.target[15].scale(0.6)
        # mobs.target[17].scale(0.7)
        # mobs.target[19].scale(0.7)
        # mobs.target.arrange_in_grid(
        #     rows=2,
        #     cols=10,
        #     # buff=0.5,
        # ).center().scale(0.95)
        # self.play(MoveToTarget(mobs))
        # self.wait()

        # # TODO, pop out comments from acs

        # # ************************************************************
        # # NOTE: a copy from 020
        # self.next_section(
        #     'show shape on simplified output map',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # tensor_mobs = VGroup(
        #     tin_raw, tin_pad, t32_reg, t32_prob, t32_merged_2d, t32_back,
        # )
        # other_mobs = Group(
        #     *(mob for mob in mobs if mob not in tensor_mobs),
        # )

        # # fade non-tensor mobs
        # other_mobs.save_state()
        # self.play(other_mobs.animate(
        #     run_time=0.5,
        # ).fade(0.9))

        # # show shapes on tensor mobs
        # self.play(AnimationGroup(
        #     *(ShowShape(mob, text_config=MINI_SHAPE_TEXT_CONFIG)
        #       for mob in tensor_mobs),
        #     lag_ratio=0.5,
        #     run_time=1.0,
        # ))
        # self.wait()

        # # hide shape
        # self.play(AnimationGroup(
        #     *(HideShape(mob)
        #       for mob in tensor_mobs),
        #     lag_ratio=0.5,
        #     run_time=1.0,
        # ))

        # # fade back non-tensor mobs
        # self.play(Transform(
        #     other_mobs,
        #     other_mobs.saved_state,
        #     run_time=0.5,
        # ))
        # self.wait()

        # # ************************************************************
        # self.next_section(
        #     "save everything, used by 025",
        #     skip_animations=False,
        # )
        # # ************************************************************
        # mobs = Group(
        #     sin_raw, aci_a, sin_pad,          s32_reg, s32_prob, aco_a, s32_merged_2d, aco_b, s32_back,
        #     tin_raw, aci_1, tin_pad, ac_game, t32_reg, t32_prob, aco_1, t32_merged_2d, aco_2, t32_back,
        # )
        # export_mobs(__file__, mobs)
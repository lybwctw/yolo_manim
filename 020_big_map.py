from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs

GAP_POSTPROCESS = 0.2
MERGED_SCALE_FACTOR = 1/1.1

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs according to 017',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('017')
        (
            s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, marrow_out_iview, s32_merged_2d,
            s32_prob, acc_ab, s32_prob_2d,
            marrow_in_tview,
            t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d, marrow_out_tview, t32_merged_2d,
            t32_prob, acc_12, t32_prob_2d,
        ) = mobs

        # reference
        ac_all = VGroup(
            acb_ab, acb_bc, marrow_out_iview,
            acc_ab,
            marrow_in_tview, acb_12, acb_23, marrow_out_tview,
            acc_12,
        )
        
        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            "Make room in the right",
            skip_animations=False,
        )
        # ************************************************************
        self.play(mobs.animate.shift(LEFT*10.))
        self.wait()


        # ************************************************************
        self.next_section("""
            [1] max class selection
                (6400,7) -> (6400,6) [xyxy, conf, cls]
                [option] multi-label
            """,
            skip_animations=False,
        )
        # ************************************************************
        # intuition view append new
        ac_a = acb_ab.copy().next_to(
            s32_merged_2d,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        self.play(Write(ac_a))
        s32_max = s32_merged_2d.copy()
        self.play(s32_max.animate(
            run_time=1.0,
        ).next_to(
            ac_a,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))
        # TODO: show comment on ac_a
        s32_max[-1].apply_max_select(
            self,
            run_time_ratio=0.5,
        )
        self.wait()

        # tensor view append new
        ac_1 = ac_a.copy().next_to(
            t32_merged_2d,
            RIGHT,
            buff=GAP_POSTPROCESS
        ).align_to(ac_a, LEFT)
        self.play(Write(ac_1))
        t32_max = t32_merged_2d.copy()
        self.play(t32_max.animate(
            run_time=1.0,
        ).next_to(
            ac_1,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_max.get_x()))
        # TODO: show comment on ac_1
        self.play(t32_max.animate(
            run_time=0.5,
        ).stretch_to_fit_width(
            t32_merged_2d.width * 0.8
        ))
        t32_max.width_nominal = 6   # width: 4+3 -> 4+2
        self.wait()

        # show shapes after max selection
        ac_1.save_state()
        marrow_out_tview.save_state()     # marrow_out already changed, save again for later restore
        self.play(AnimationGroup(
            AnimationGroup(
                marrow_out_tview.animate.fade(0.8),
                ac_1.animate.fade(0.8),
            ),
            AnimationGroup(
                ShowShape(t32_merged_2d, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_max, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_merged_2d),
                HideShape(t32_max),
            ),
            AnimationGroup(
                marrow_out_tview.animate.restore(),
                ac_1.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section("""
            [2] conf filter
                (6400,6) -> (k,6) [xyxy, conf, cls]
                [value] conf = ?
            """,
            skip_animations=False,
        )
        # ************************************************************
        # intuition view append new
        ac_b = ac_a.copy().next_to(
            s32_max,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        self.play(Write(ac_b))
        s32_conf = s32_max.copy()
        self.play(s32_conf.animate(
            run_time=1.0,
        ).next_to(
            ac_b,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))
        # TODO: show comment on ac_b
        # TODO: use hardcoded removal
        s32_conf[-1].apply_keep_random(
            scene=self,
            ratio=0.5,
            run_time_ratio=0.5,
        )
        self.wait()

        # tensor view append new
        ac_2 = ac_b.copy().next_to(
            t32_max,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).align_to(ac_b, LEFT)
        self.play(Write(ac_2))
        t32_conf = t32_max.copy()
        self.play(t32_conf.animate(
            run_time=1.0,
        ).next_to(
            ac_2,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_conf.get_x()))
        # TODO: show comment on ac_2
        self.play(t32_conf.animate(
            run_time=0.5,
        ).stretch_to_fit_height(
            t32_max.height * 0.6
        ))
        t32_conf.height_nominal = 'k'   # height: 400 -> k
        self.wait()

        # show shapes after conf filter
        ac_1.save_state()
        ac_2.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                ac_1.animate.fade(0.8),
                ac_2.animate.fade(0.8),
            ),
            AnimationGroup(
                ShowShape(t32_max, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_conf, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_max),
                HideShape(t32_conf),
            ),
            AnimationGroup(
                ac_1.animate.restore(),
                ac_2.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section("""
            [3] NMS filter
                (k,6) -> (m,6) [xyxy, conf, cls]
                [value] iou = ?
                [option] agnostic_nms
            """,
            skip_animations=False,
        )
        # ************************************************************
        # intuition view append new
        ac_c = ac_b.copy().next_to(
            s32_conf,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        self.play(Write(ac_c))
        s32_nms = s32_conf.copy()
        self.play(s32_nms.animate(
            run_time=1.0,
        ).next_to(
            ac_c,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))
        # TODO: show comment on ac_c
        # TODO: use hardcoded removal
        s32_nms[-1].apply_keep_random(
            scene=self,
            ratio=0.7,
            run_time_ratio=0.5,
        )
        self.wait()

        # tensor view append new
        ac_3 = ac_c.copy().next_to(
            t32_conf,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).align_to(ac_c, LEFT)
        self.play(Write(ac_3))
        t32_nms = t32_conf.copy()
        self.play(t32_nms.animate(
            run_time=1.0,
        ).next_to(
            ac_3,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_nms.get_x()))
        # TODO: show comment on ac_3
        self.play(t32_nms.animate(
                run_time=0.5,
            ).stretch_to_fit_height(
            t32_conf.height * 0.6
        ))
        t32_nms.height_nominal = 'm'      # height: k -> m
        self.wait()

        # show shapes after NMS
        ac_2.save_state()
        ac_3.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                ac_2.animate.fade(0.8),
                ac_3.animate.fade(0.8),
            ),
            AnimationGroup(
                ShowShape(t32_conf, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_nms, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_conf),
                HideShape(t32_nms),
            ),
            AnimationGroup(
                ac_2.animate.restore(),
                ac_3.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section("""
            [4] scale back to original image size: (m,6) -> (n,6)
                maybe convert to desired output format (e.g. xywh)
            """,
            skip_animations=False,
        )
        # ************************************************************
        # intuition view append new
        ac_d = ac_c.copy().next_to(
            s32_nms,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        self.play(Write(ac_d))
        s32_back = s32_nms.copy()
        self.play(s32_back.animate(
            run_time=1.0,
        ).next_to(
            ac_d,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ))
        # TODO: show comment on ac_d
        self.play(s32_back[0].hide_paddings(
            updown=True,        # manual
            width_nominal=640,
            height_nominal=360,
            aargs={},
            gargs={},
        ))

        # clip into small background
        s32_back[-1].apply_clip(
            scene=self,
            run_time_ratio=1.0,
        )
        self.wait()
        
        # scale up a bit
        s32_back.generate_target()
        s32_back.target.scale(1.5).next_to(
            ac_d,
            RIGHT,
            buff=GAP_POSTPROCESS,
        )
        self.play(MoveToTarget(
            s32_back,
            run_time=0.5,
        ))
        self.wait()

        # TODO: show comment on ac_d
        # tensor view append new
        ac_4 = ac_d.copy().next_to(
            t32_nms,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).align_to(ac_d, LEFT)
        self.play(Write(ac_4))
        t32_back = t32_nms.copy()
        self.play(t32_back.animate(
            run_time=1.0,
        ).next_to(
            ac_4,
            RIGHT,
            buff=GAP_POSTPROCESS,
        ).set_x(s32_back.get_x()))
        # TODO: show comment on ac_4
        self.play(t32_back.animate(
            run_time=0.5,
        ).stretch_to_fit_height(
            t32_nms.height * 0.9
        ))
        t32_back.height_nominal = 'n'      # height: m -> n(m)
        self.wait()

        # show shapes after scale back
        ac_3.save_state()
        ac_4.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                ac_3.animate.fade(0.8),
                ac_4.animate.fade(0.8),
            ),
            AnimationGroup(
                ShowShape(t32_nms, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_back, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_nms),
                HideShape(t32_back),
            ),
            AnimationGroup(
                ac_3.animate.restore(),
                ac_4.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'back to output big map',
            skip_animations=False,
        )
        # ************************************************************
        # scale down the big map
        # mobs = Group(*self.get_top_level_mobjects())
        mobs = Group(
            s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d,
            s32_prob, acc_ab, s32_prob_2d,
            marrow_out_iview,
            s32_merged_2d, ac_a, s32_max, ac_b, s32_conf, ac_c, s32_nms, ac_d, s32_back,
            marrow_in_tview,
            t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d,
            t32_prob, acc_12, t32_prob_2d,
            marrow_out_tview,
            t32_merged_2d, ac_1, t32_max, ac_2, t32_conf, ac_3, t32_nms, ac_4, t32_back,
        )
        self.play(mobs.animate.scale(0.7).center())
        self.wait()

        ac_all.add(
            ac_a, ac_b, ac_c, ac_d,
            ac_1, ac_2, ac_3, ac_4,
        )
        ac_all.save_state()

        # TODO, also shape text z_index
        self.play(ac_all.animate(
            run_time=1.0
        ).fade(0.8))
        self.play(AnimationGroup(
            ShowShape(t32_dist, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_xyxy, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_xyxy_2d, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_prob, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_prob_2d, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_merged_2d, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_max, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_conf, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_nms, text_config=MINI_SHAPE_TEXT_CONFIG),
            ShowShape(t32_back, text_config=MINI_SHAPE_TEXT_CONFIG),
            lag_ratio=0.2,
        ))
        self.wait()

        self.play(AnimationGroup(
            HideShape(t32_dist),
            HideShape(t32_xyxy),
            HideShape(t32_xyxy_2d),
            HideShape(t32_prob),
            HideShape(t32_prob_2d),
            HideShape(t32_merged_2d),
            HideShape(t32_max),
            HideShape(t32_conf),
            HideShape(t32_nms),
            HideShape(t32_back),
            lag_ratio=0.2,
        ))
        self.play(ac_all.animate(
            run_time=1.0
        ).restore())
        self.wait()

        # ************************************************************
        self.next_section(
            'save everything, used by 023',
            skip_animations=False,
        )
        # ************************************************************
        export_mobs(__file__, mobs)

        # ************************************************************
        self.next_section(
            "highlight decode stage and postprocess stage",
            skip_animations=False,
        )
        # ************************************************************
        s32_mid_decode = Group(
            acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, marrow_out_iview,
            acc_ab, s32_prob_2d,
        )
        s32_mid_postprocess = Group(
            ac_a, s32_max, ac_b, s32_conf, ac_c, s32_nms, ac_d,
        )
        t32_mid_decode = Group(
            acb_12, t32_xyxy, acb_23, t32_xyxy_2d, marrow_out_tview,
            acc_12, t32_prob_2d,
        )
        t32_mid_postprocess = Group(
            ac_1, t32_max, ac_2, t32_conf, ac_3, t32_nms, ac_4,
        )

        self.play(AnimationGroup(
            marrow_in_tview.animate.fade(0.9),
            s32_mid_decode.animate.fade(0.9),
            s32_mid_postprocess.animate.fade(0.9),
            t32_mid_decode.animate.fade(0.9),
            t32_mid_postprocess.animate.fade(0.9),
            run_time=0.5,
            lag_ratio=0.0,
        ))

        # ************************************************************
        self.next_section(
            'simplify into two steps on raw output',
            skip_animations=False,
        )
        # ************************************************************
        # TODO: alignment issue, maybe to do with clipping
        # arrow with comment on output
        aco_a = ArrowComment(False, RIGHT).scale(0.2).shift(UP*10)
        aco_b = ArrowComment(False, RIGHT).scale(0.2).shift(UP*10)
        ac_game = ArrowComment(False, RIGHT).scale(0.2).shift(LEFT*10)
        aco_1 = ArrowComment(False, RIGHT).scale(0.2).shift(DOWN*10)
        aco_2 = ArrowComment(False, RIGHT).scale(0.2).shift(DOWN*10)

        mobs = Group(
            Mobject(), s32_dist, s32_prob, aco_a, s32_merged_2d, aco_b, s32_back,
            ac_game,   t32_dist, t32_prob, aco_1, t32_merged_2d, aco_2, t32_back,
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
            FadeOut(s32_mid_decode),
            FadeOut(s32_mid_postprocess),
            FadeOut(marrow_in_tview),
            FadeOut(t32_mid_decode),
            FadeOut(t32_mid_postprocess),
            run_time=0.5,
            lag_ratio=0.5,
        ))
        self.play(MoveToTarget(
            mobs,
            run_time=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'into bigger map: from input to output',
            skip_animations=False,
        )
        # ************************************************************
        aci_a = aco_a.copy().move_to(LEFT*10)
        aci_1 = aco_a.copy().move_to(LEFT*10)
        sin_raw = s32_back[0].copy().set_opacity(1.0).move_to(LEFT*10)
        sin_pad = s32_merged_2d[0].copy().set_opacity(1.0).move_to(LEFT*10)
        tin_raw = LayersFake(
            n=3,
            ref=sin_raw,
            expanded=True,
            width_nominal=sin_raw.width_nominal,
            height_nominal=sin_raw.height_nominal,
            buff=0.05,              # TODO, natural buff?
        ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?
        tin_pad = LayersFake(
            n=3,
            ref=sin_pad,
            expanded=True,
            width_nominal=sin_pad.width_nominal,
            height_nominal=sin_pad.height_nominal,
            buff=0.05,              # TODO, natural buff?
        ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?

        mobs = Group(
            sin_raw, aci_a, sin_pad, Mobject(), s32_dist, s32_prob, aco_a, s32_merged_2d, aco_b, s32_back,
            tin_raw, aci_1, tin_pad, ac_game,   t32_dist, t32_prob, aco_1, t32_merged_2d, aco_2, t32_back,
        )
        mobs.generate_target()
        # make output smaller to match input tensors
        mobs.target[14].scale(0.6)
        mobs.target[15].scale(0.6)
        mobs.target[17].scale(0.7)
        mobs.target[19].scale(0.7)
        mobs.target.arrange_in_grid(
            rows=2,
            cols=10,
            # buff=0.5,
        ).center().scale(0.95)
        self.play(MoveToTarget(mobs))
        self.wait()

        # TODO, pop out comments from acs

        # ************************************************************
        self.next_section(
            'show shape on simplified output map',
            skip_animations=False,
        )
        # ************************************************************
        tensor_mobs = VGroup(
            tin_raw, tin_pad, t32_dist, t32_prob, t32_merged_2d, t32_back,
        )
        other_mobs = Group(
            *(mob for mob in mobs if mob not in tensor_mobs),
        )

        # fade non-tensor mobs
        other_mobs.save_state()
        self.play(other_mobs.animate(
            run_time=0.5,
        ).fade(0.9))

        # show shapes on tensor mobs
        self.play(AnimationGroup(
            *(ShowShape(mob, text_config=MINI_SHAPE_TEXT_CONFIG)
              for mob in tensor_mobs),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()

        # hide shape
        self.play(AnimationGroup(
            *(HideShape(mob)
              for mob in tensor_mobs),
            lag_ratio=0.5,
            run_time=1.0,
        ))

        # fade back non-tensor mobs
        self.play(Transform(
            other_mobs,
            other_mobs.saved_state,
            run_time=0.5,
        ))
        self.wait()

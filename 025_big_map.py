from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.explainer import Explainer
from utils.general import import_mobs, export_mobs
from utils.image_pad import ImagePad

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs according to 023',
            skip_animations=True,
        )
        # ************************************************************
        mobs = import_mobs('023')
        (
            sin_raw, aci_a, sin_pad,            s32_reg, s32_prob, aco_a_32, s32_merged_2d, aco_b, s32_back,
            tin_raw, aci_1, tin_pad, ac_game,   t32_reg, t32_prob, aco_1_32, t32_merged_2d, aco_2, t32_back,
        ) = mobs
        
        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            'remove tails',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            Unwrite(aco_b),
            Unwrite(aco_2),
            FadeOut(s32_back),
            FadeOut(t32_back),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'insert stride-8 and stride-16 series',
            skip_animations=True,
        )
        # ************************************************************
        # init stride-8 series in intuition view
        b8 = s32_reg[0].copy()
        e8 = Explainer.from_random(
            background=b8,
            reg_max=4,
            dist_range=(0.5, 1),
            prob_range=(0, 1),
            shape=(8, 8),       # 6x6 as stride-8's fake
            sf_pcell=0.5,
        )
        s8_reg = Group(b8, e8).shift(RIGHT*10)
        # FIXME: create aps thus arrange works properly
        self.play(e8.show_anchor_points(run_time=0.02, lag_ratio=0.0))
        s8_prob = s8_reg.copy().shift(RIGHT*10)
        aco_a_8 = aco_a_32.copy().shift(RIGHT*10)
        s8_merged_2d = s8_reg.copy().shift(RIGHT*10)

        # init stride-16 series in intuition view
        b16 = s32_reg[0].copy()
        e16 = Explainer.from_random(
            b16,
            reg_max=4,
            dist_range=(0.5, 1),
            prob_range=(0, 1),
            shape=(6, 6),       # 5x5 as stride-16's fake
            sf_pcell=0.5,
        )
        s16_reg = Group(b16, e16).shift(RIGHT*10)
        # FIXME: create aps thus arrange works properly
        self.play(e16.show_anchor_points(run_time=0.02, lag_ratio=0.0))
        s16_prob = s16_reg.copy().shift(RIGHT*10)
        aco_a_16 = aco_a_32.copy().shift(RIGHT*10)
        s16_merged_2d = s16_reg.copy().shift(RIGHT*10)

        # init stride-8 series in tensor view
        t8_reg = t32_reg.copy().shift(RIGHT*10)
        t8_reg.width_nominal = 80
        t8_reg.height_nominal = 80
        t8_prob = t32_prob.copy().shift(RIGHT*10)
        t8_prob.width_nominal = 80
        t8_prob.height_nominal = 80
        aco_1_8 = aco_1_32.copy().shift(RIGHT*10)
        t8_merged_2d = t32_merged_2d.copy().shift(RIGHT*10)
        t8_merged_2d.height_nominal = 6400

        # init stride-16 series in tensor view
        t16_reg = t32_reg.copy().shift(RIGHT*10)
        t16_reg.width_nominal = 40
        t16_reg.height_nominal = 40
        t16_prob = t32_prob.copy().shift(RIGHT*10)
        t16_prob.width_nominal = 40
        t16_prob.height_nominal = 40
        aco_1_16 = aco_1_32.copy().shift(RIGHT*10)
        t16_merged_2d = t32_merged_2d.copy().shift(RIGHT*10)
        t16_merged_2d.height_nominal = 1600

        # arrange outputs for stride-8/16/32
        mobs = Group(
            Mobject(), Mobject(), Mobject(), Mobject(), s8_reg,  s8_prob,  aco_a_8,  s8_merged_2d,
            sin_raw,   aci_a,     sin_pad,   Mobject(), s16_reg, s16_prob, aco_a_16, s16_merged_2d,
            Mobject(), Mobject(), Mobject(), Mobject(), s32_reg, s32_prob, aco_a_32, s32_merged_2d,
            Mobject(), Mobject(), Mobject(), Mobject(), t8_reg,  t8_prob,  aco_1_8,  t8_merged_2d,
            tin_raw,   aci_1,     tin_pad,   ac_game,   t16_reg, t16_prob, aco_1_16, t16_merged_2d,
            Mobject(), Mobject(), Mobject(), Mobject(), t32_reg, t32_prob, aco_1_32, t32_merged_2d,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=6,
            cols=8,
            # buff=0.1,
        ).scale(0.8).center()

        # adjust mob scales
        # mobs.target[36].scale(0.8)  # t16_reg
        # mobs.target[44].scale(0.6)  # t32_reg
        # mobs.target[37].scale(0.8)  # t16_prob
        # mobs.target[45].scale(0.6)  # t32_prob
        mobs.target[36].scale_layers(0.8)  # t16_reg
        mobs.target[44].scale_layers(0.6)  # t32_reg
        mobs.target[37].scale_layers(0.8)  # t16_prob
        mobs.target[45].scale_layers(0.6)  # t32_prob
        height_2d = mobs.target[39].height
        mobs.target[39].stretch_to_fit_height(height_2d*0.8)
        mobs.target[47].stretch_to_fit_height(height_2d*0.6)

        self.play(MoveToTarget(
            mobs,
            run_time=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'expand systems in intuition view',
            skip_animations=True,
        )
        # ************************************************************
        # realtime label width and height
        label_width = s32_merged_2d[-1].anchor_points[0].labels[0].width
        label_height = s32_merged_2d[-1].anchor_points[0].labels[0].height
        rect_stroke_width = s32_merged_2d[-1].anchor_points[0].mob.stroke_width
        rect_stroke_color = GRAY
        self.play(AnimationGroup(
            s8_reg[-1].show_pcells(
                label_config={},
                box_config={},
                aargs={'lag_ratio': 0.0,},
                gargs={'lag_ratio': 0.2,},
            ),
            s16_reg[-1].show_pcells(
                label_config={},
                box_config={},
                aargs={'lag_ratio': 0.0,},
                gargs={'lag_ratio': 0.2,},
            ),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.0)
                  for ap in s8_prob[-1].anchor_points),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.0)
                  for ap in s16_prob[-1].anchor_points),
                lag_ratio=0.0,
            ),
            s8_prob[-1].show_pbars(
                pbar_config={},
                aargs={},
                gargs={},
                ggargs={'lag_ratio': 0.2},
            ),
            s16_prob[-1].show_pbars(
                pbar_config={},
                aargs={},
                gargs={},
                ggargs={'lag_ratio': 0.2},
            ),
            s8_merged_2d[-1].show_rect_mlabels(
                rect_config={
                    'stroke_width': rect_stroke_width,
                    'stroke_color': rect_stroke_color,
                },
                include_text=False,
                label_config={},
                box_config={
                    'width': label_width,
                    'height': label_height,
                    'fill_opacity': 1.0,
                },
                rargs={},
                largs={},
                gargs={},
                ggargs={'lag_ratio': 0.2},
            ),
            s16_merged_2d[-1].show_rect_mlabels(
                rect_config={
                    'stroke_width': rect_stroke_width,
                    'stroke_color': rect_stroke_color,
                },
                include_text=False,
                label_config={},
                box_config={
                    'width': label_width,
                    'height': label_height,
                    'fill_opacity': 1.0,
                },
                rargs={},
                largs={},
                gargs={},
                ggargs={'lag_ratio': 0.2},
            ),
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'combine multiple systems into one',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of arrow
        aco_b = aco_a_16.copy()
        self.play(aco_b.animate(
            run_time=0.5,
        ).shift(RIGHT*2.0))
        self.wait(0.5)

        # make a copy of background
        bg_copy = s16_merged_2d[0].copy()
        self.play(bg_copy.animate(
            run_time=0.5,
        ).shift(RIGHT*2.0))
        self.wait(0.5)

        # make a copy of explainers
        e8_offset = bg_copy.get_center() - s8_merged_2d[0].get_center()
        e16_offset = bg_copy.get_center() - s16_merged_2d[0].get_center()
        e32_offset = bg_copy.get_center() - s32_merged_2d[0].get_center()
        e8_copy = s8_merged_2d[-1].copy()
        e16_copy = s16_merged_2d[-1].copy()
        e32_copy = s32_merged_2d[-1].copy()
        self.play(AnimationGroup(
            e8_copy.animate(run_time=0.5).shift(e8_offset),
            e16_copy.animate(run_time=0.5).shift(e16_offset),
            e32_copy.animate(run_time=0.5).shift(e32_offset),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait(0.5)

        # combine explainers into one
        e_merged_2d = Explainer.from_explainers(
            background=bg_copy,
            explainers=[e8_copy, e16_copy, e32_copy],
        )
        s_merged_2d = Group(bg_copy, e_merged_2d)

        # ************************************************************
        self.next_section(
            'combine multiple tensors into one',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of arrow
        aco_2 = aco_1_16.copy()
        self.play(aco_2.animate(
            run_time=0.5,
        ).shift(RIGHT*2.0))
        self.wait(0.5)

        # make a copy of tensors
        t8_copy = t8_merged_2d.copy()
        t16_copy = t16_merged_2d.copy()
        t32_copy = t32_merged_2d.copy()
        t_copy_combined = Group(t8_copy, t16_copy, t32_copy)
        t8_copy.generate_target()
        t16_copy.generate_target()
        t32_copy.generate_target()
        t16_copy.target.shift(RIGHT*2.0)
        t8_copy.target.next_to(t16_copy.target, UP, buff=0.0)
        t32_copy.target.next_to(t16_copy.target, DOWN, buff=0.0)

        # align combined to arrow
        tg = VGroup(t8_copy.target, t16_copy.target, t32_copy.target)
        tg.set_y(aco_2.get_y())

        self.play(AnimationGroup(
            MoveToTarget(t8_copy),
            MoveToTarget(t16_copy),
            MoveToTarget(t32_copy),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait(0.5)

        # combine tensors into one
        t_merged_2d = LayersFake(
            n=1,
            ref=t_copy_combined,
            width_nominal=7,
            height_nominal=6400+1600+400,
            expanded=True,
        ).move_to(t_copy_combined)
        self.play(AnimationGroup(
            FadeOut(t_copy_combined),
            FadeIn(t_merged_2d),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'make room in the right',
            skip_animations=True,
        )
        # ************************************************************
        mobs = Group(*self.get_top_level_mobjects())
        self.play(mobs.animate(
            run_time=0.5,
        ).scale(0.98).shift(LEFT*2.5))      # TODO: twick
        self.wait()

        # ************************************************************
        self.next_section(
            'result template in both views',
            skip_animations=True,
        )
        # ************************************************************
        aco_c = aco_b.copy()
        aco_3 = aco_2.copy()
        self.play(AnimationGroup(
            aco_c.animate.shift(RIGHT*2.0),
            aco_3.animate.shift(RIGHT*2.0),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.5)

        s_result = s_merged_2d.copy()
        t_result = t_merged_2d.copy()
        self.play(AnimationGroup(
            s_result.animate.shift(RIGHT*2.5),  # TODO: twick
            t_result.animate.shift(RIGHT*2.5),  # TODO: twick
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'apply max selection in both views',
            skip_animations=True,
        )
        # ************************************************************
        # intuition view
        s_result[-1].apply_max_select(
            self,
            run_time_ratio=0.5,
        )
        self.wait(0.5)

        # tensor view
        self.play(t_result.animate(
            run_time=0.5,
        ).stretch_to_fit_width(
            t_merged_2d.width * 0.8,
        ))
        t_result.width_nominal = 6
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'apply conf filter in both views',
            skip_animations=True,
        )
        # ************************************************************
        # intuition view
        s_result[-1].apply_keep_random(
            scene=self,
            ratio=0.2,
            run_time_ratio=0.5,
        )
        self.wait(0.5)

        # tensor view
        self.play(t_result.animate(
            run_time=0.5,
        ).stretch_to_fit_height(
            t_result.height * 0.3,
        ))
        t_result.height_nominal = 'k'
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'apply nms filter in both views',
            skip_animations=True,
        )
        # ************************************************************
        # intuition view
        s_result[-1].apply_keep_random(
            scene=self,
            ratio=0.3,
            run_time_ratio=0.5,
        )
        self.wait(0.5)

        # tensor view
        self.play(t_result.animate(
            run_time=0.5,
        ).stretch_to_fit_height(
            t_result.height * 0.5,
        ))
        t_result.height_nominal = 'm'
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'apply scale back in both views',
            skip_animations=True,
        )
        # ************************************************************
        # intuition view
        self.play(s_result[0].hide_paddings(
            updown=True,        # manual
            width_nominal=640,
            height_nominal=360,
            aargs={},
            gargs={},
        ))

        s_result[-1].apply_clip(
            scene=self,
            run_time_ratio=0.5,
        )
        self.play(s_result.animate(
            run_time=0.5,
        ).scale(1.5))
        self.wait(0.5)

        # TODO: nothing for tensor view
        t_result.height_nominal = 'n'

        # TODO: simplify decoding step?

        # introduce marrows?

        # ************************************************************
        self.next_section(
            'show tensor shapes',
            skip_animations=True,
        )
        # ************************************************************
        # mobs = Group(*self.get_top_level_mobjects())
        mobs = Group(
            sin_raw, aci_a, sin_pad,
            s8_reg, s8_prob, aco_a_8, s8_merged_2d,
            s16_reg, s16_prob, aco_a_16, s16_merged_2d,
            s32_reg, s32_prob, aco_a_32, s32_merged_2d,
            aco_b, s_merged_2d, aco_c, s_result,
            tin_raw, aci_1, tin_pad, ac_game,
            t8_reg, t8_prob, aco_1_8, t8_merged_2d,
            t16_reg, t16_prob, aco_1_16, t16_merged_2d,
            t32_reg, t32_prob, aco_1_32, t32_merged_2d,
            aco_2, t_merged_2d, aco_3, t_result,
        )
        tensor_mobs = Group(
            tin_raw, tin_pad,
            t8_reg, t8_prob, t8_merged_2d,
            t16_reg, t16_prob, t16_merged_2d,
            t32_reg, t32_prob, t32_merged_2d,
            t_merged_2d, t_result,
        )
        other_mobs = Group(*[m for m in mobs if m not in tensor_mobs])

        # fade non-tensor mobs
        other_mobs.save_state()
        self.play(other_mobs.animate(
            run_time=0.5,
        ).fade(0.9))
        self.wait(0.5)

        # show shapes on tensor mobs
        self.play(AnimationGroup(
            *(ShowShape(mob, text_config=MINI_SHAPE_TEXT_CONFIG)
              for mob in tensor_mobs),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in tensor_mobs),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait(0.5)

        # fade back non-tensor mobs
        self.play(Transform(
            other_mobs,
            other_mobs.saved_state,
            run_time=0.5,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'focus on AI game',
            skip_animations=True,
        )
        # ************************************************************
        focus_mobs = Group(
            tin_pad, ac_game,
            t8_reg, t8_prob,
            t16_reg, t16_prob,
            t32_reg, t32_prob,
        )

        other_mobs = Group(*[m for m in mobs if m not in focus_mobs])
        self.play(AnimationGroup(
            FadeOut(other_mobs),
            focus_mobs.animate(
                lag_ratio=0.0,
            ).scale(1.5).center(),
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'show shapes on AI game',
            skip_animations=False,
        )
        # ************************************************************
        ac_game.save_state()
        t_mobs = Group(
            tin_pad,
            t8_reg, t8_prob,
            t16_reg, t16_prob,
            t32_reg, t32_prob,
        )
        self.play(AnimationGroup(
            ac_game.animate.fade(0.8),
            AnimationGroup(
                *(ShowShape(mob, text_config=MINI_SHAPE_TEXT_CONFIG)
                  for mob in t_mobs),
                lag_ratio=0.5,
            ),
            run_time=0.5,
        ))
        self.wait(0.5)

        self.play(AnimationGroup(
            ac_game.animate.restore(),
            AnimationGroup(
                *(HideShape(mob) for mob in t_mobs),
                lag_ratio=0.5,
            ),
            run_time=0.5,
        ))
        self.wait(0.5)
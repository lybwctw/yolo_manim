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
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        mobs = import_mobs('023')
        (
            sin_raw, aci_1, sin_norm,            s32_distrib, s32_prob, aci_14, s32_merged_2d, aci_15, s32_back,
            tin_raw, act_1, tin_norm, act_game,  t32_distrib, t32_prob, act_14, t32_merged_2d, act_15, t32_back,
        ) = mobs
        
        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'remove tails',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            Unwrite(aci_15),
            Unwrite(act_15),
            FadeOut(s32_back),
            FadeOut(t32_back),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert stride-8 and stride-16 series',
            skip_animations=True,
        )
        # ************************************************************
        # init stride-8 series in intuition view
        b8 = s32_distrib[0].copy()
        e8 = Explainer.from_random(
            background=b8,
            shape=(8,8),
            n_distrib=4,
            offsets_range=(0,2),     # not used in big map
            prob_range=(0,1),
            dot_config={},
            rect_config={},
        )
        s8_distrib = Group(b8, e8).shift(RIGHT*10)
        # NOTE: create aps thus arrange works properly
        self.play(e8.show_anchor_points(run_time=0.02, lag_ratio=0.0))
        s8_prob = s8_distrib.copy().shift(RIGHT*10)
        aci_12 = aci_14.copy().shift(RIGHT*10)
        s8_merged_2d = s8_distrib.copy().shift(RIGHT*10)

        # init stride-16 series in intuition view
        b16 = s32_distrib[0].copy()
        e16 = Explainer.from_random(
            background=b16,
            shape=(6,6),
            n_distrib=4,
            offsets_range=(0,2),     # not used in big map
            prob_range=(0,1),
            dot_config={},
            rect_config={},
        )
        s16_distrib = Group(b16, e16).shift(RIGHT*10)
        # FIXME: create aps thus arrange works properly
        self.play(e16.show_anchor_points(run_time=0.02, lag_ratio=0.0))
        s16_prob = s16_distrib.copy().shift(RIGHT*10)
        aci_13 = aci_14.copy().shift(RIGHT*10)
        s16_merged_2d = s16_distrib.copy().shift(RIGHT*10)

        # init stride-8 series in tensor view
        t8_distrib = t32_distrib.copy().shift(RIGHT*10)
        t8_distrib.width_nominal = 80
        t8_distrib.height_nominal = 80
        t8_prob = t32_prob.copy().shift(RIGHT*10)
        t8_prob.width_nominal = 80
        t8_prob.height_nominal = 80
        act_12 = act_14.copy().shift(RIGHT*10)
        t8_merged_2d = t32_merged_2d.copy().shift(RIGHT*10)
        t8_merged_2d.height_nominal = 6400

        # init stride-16 series in tensor view
        t16_distrib = t32_distrib.copy().shift(RIGHT*10)
        t16_distrib.width_nominal = 40
        t16_distrib.height_nominal = 40
        t16_prob = t32_prob.copy().shift(RIGHT*10)
        t16_prob.width_nominal = 40
        t16_prob.height_nominal = 40
        act_13 = act_14.copy().shift(RIGHT*10)
        t16_merged_2d = t32_merged_2d.copy().shift(RIGHT*10)
        t16_merged_2d.height_nominal = 1600

        # arrange outputs for 8/16/32
        mobs = Group(
            Mobject(), Mobject(), Mobject(), Mobject(), s8_distrib,  s8_prob,  aci_12,  s8_merged_2d,
            sin_raw,   aci_1,     sin_norm,  Mobject(), s16_distrib, s16_prob, aci_13, s16_merged_2d,
            Mobject(), Mobject(), Mobject(), Mobject(), s32_distrib, s32_prob, aci_14, s32_merged_2d,
            Mobject(), Mobject(), Mobject(), Mobject(), t8_distrib,  t8_prob,  act_12,  t8_merged_2d,
            tin_raw,   act_1,     tin_norm,  act_game,  t16_distrib, t16_prob, act_13, t16_merged_2d,
            Mobject(), Mobject(), Mobject(), Mobject(), t32_distrib, t32_prob, act_14, t32_merged_2d,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=6,
            cols=8,
            # buff=0.1,
        ).scale(0.8).center()

        # adjust mob scales
        mobs.target[36].scale_layers(0.8)  # t16_distrib
        mobs.target[44].scale_layers(0.6)  # t32_distrib
        mobs.target[37].scale_layers(0.8)  # t16_prob
        mobs.target[45].scale_layers(0.6)  # t32_prob
        height_2d = mobs.target[39].height
        mobs.target[39].stretch_to_fit_height(height_2d*0.8)
        mobs.target[47].stretch_to_fit_height(height_2d*0.6)

        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'expand everything',
            skip_animations=True,
        )
        # ************************************************************
        # realtime label width and height
        label_width = s32_merged_2d[-1].anchor_points[0].labels[0].width
        label_height = s32_merged_2d[-1].anchor_points[0].labels[0].height
        rect_stroke_width = s32_merged_2d[-1].anchor_points[0].mob.stroke_width
        rect_stroke_color = WHITE

        # expand distrib for 8/16
        self.play(AnimationGroup(
            s8_distrib[-1].show_pcells(
                sf_pcell=0.5,
                box_config={},
                gargs={'lag_ratio': 0.5},
            ),
            s16_distrib[-1].show_pcells(
                sf_pcell=0.5,
                box_config={},
                gargs={'lag_ratio': 0.5},
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # expand prob for 8/16
        self.play(AnimationGroup(
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
                random=False,
                pbar_config={},
                aargs={},
                gargs={'lag_ratio': 0.0},
            ),
            s16_prob[-1].show_pbars(
                random=False,
                pbar_config={},
                aargs={},
                gargs={'lag_ratio': 0.0},
            ),
        ))
        self.wait(wt)

        # expand rect and labels for 8/16
        self.play(AnimationGroup(
            s8_merged_2d[-1].show_rect_labels(
                rect_config={
                    'stroke_width': rect_stroke_width,
                    'stroke_color': rect_stroke_color,
                },
                include_text=False,
                label_txt_config={},
                label_bg_config={
                    'width': label_width,
                    'height': label_height,
                    'fill_opacity': 1.0,
                },
                aargs={},
                gargs={'lag_ratio': 0.0},
            ),
            s16_merged_2d[-1].show_rect_labels(
                rect_config={
                    'stroke_width': rect_stroke_width,
                    'stroke_color': rect_stroke_color,
                },
                include_text=False,
                label_txt_config={},
                label_bg_config={
                    'width': label_width,
                    'height': label_height,
                    'fill_opacity': 1.0,
                },
                aargs={},
                gargs={'lag_ratio': 0.0},
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'combine multiple systems into one',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of arrow
        aci_15 = aci_13.copy()
        self.play(aci_15.animate(
            run_time=wt,
        ).shift(RIGHT*2.2))             # TODO: twick
        self.wait(wt)

        # make a copy of background
        bg_copy = s16_merged_2d[0].copy()
        self.play(bg_copy.animate(
            run_time=wt,
        ).shift(RIGHT*2.2))             # TODO: twick
        self.wait(wt)

        # make copies of explainers
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
            run_time=wt,
        ))
        self.wait(wt)

        # combine multiple explainers into one
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
        act_15 = act_13.copy()
        self.play(act_15.animate(
            run_time=wt,
        ).shift(RIGHT*2.2))                 # TODO: twick
        self.wait(wt)

        # make a copy of tensors
        t8_copy = t8_merged_2d.copy()
        t16_copy = t16_merged_2d.copy()
        t32_copy = t32_merged_2d.copy()
        t_copy_combined = Group(t8_copy, t16_copy, t32_copy)
        t8_copy.generate_target()
        t16_copy.generate_target()
        t32_copy.generate_target()
        t16_copy.target.shift(RIGHT*2.2)    # TODO: twick
        t8_copy.target.next_to(t16_copy.target, UP, buff=0.0)
        t32_copy.target.next_to(t16_copy.target, DOWN, buff=0.0)

        # align combined to arrow
        tg = VGroup(t8_copy.target, t16_copy.target, t32_copy.target)
        tg.set_y(act_15.get_y())

        self.play(AnimationGroup(
            MoveToTarget(t8_copy),
            MoveToTarget(t16_copy),
            MoveToTarget(t32_copy),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # combine tensors into one
        t_merged_2d = LayersFake(
            n=1,
            ref=t_copy_combined,
            expanded=True,
            width_nominal=7,
            height_nominal=6400+1600+400,
            rect_config={},
        ).move_to(t_copy_combined)
        self.play(AnimationGroup(
            FadeOut(t_copy_combined),
            FadeIn(t_merged_2d),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'result after decode and before postprocess',
            skip_animations=True,
        )
        # ************************************************************
        # make room in the right
        mobs = Group(*self.get_top_level_mobjects())
        self.play(mobs.animate(
            run_time=0.5,
        ).scale(1.0).shift(LEFT*2.3))      # TODO: twick
        self.wait(wt)

        aci_16 = aci_15.copy()
        act_16 = act_15.copy()
        self.play(AnimationGroup(
            aci_16.animate.shift(RIGHT*2.0),
            act_16.animate.shift(RIGHT*2.0),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # results before postprocess
        s_result = s_merged_2d.copy()
        t_result = t_merged_2d.copy()
        self.play(AnimationGroup(
            s_result.animate.shift(RIGHT*2.2),  # TODO: twick
            t_result.animate.shift(RIGHT*2.2),  # TODO: twick
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply max selection',
            skip_animations=True,
        )
        # ************************************************************
        # intuition view
        s_result[-1].apply_max_select(
            self,
            run_time_ratio=0.5,
        )
        self.wait(wt)

        # tensor view
        self.play(t_result.animate(
            run_time=wt,
        ).stretch_to_fit_width(
            t_merged_2d.width * 0.8,
        ))
        t_result.width_nominal = 6
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply conf, nms, scale back',
            skip_animations=True,
        )
        # ************************************************************
        # conf filter
        s_result[-1].apply_keep_random(
            scene=self,
            ratio=0.2,
            run_time_ratio=wt,
        )
        self.play(t_result.animate(
            run_time=wt,
        ).stretch_to_fit_height(
            t_result.height * 0.3,
        ))
        t_result.height_nominal = 'k'
        self.wait(wt)

        # nms filter
        s_result[-1].apply_keep_random(
            scene=self,
            ratio=0.3,
            run_time_ratio=wt,
        )
        self.play(t_result.animate(
            run_time=0.5,
        ).stretch_to_fit_height(
            t_result.height * 0.5,
        ))
        t_result.height_nominal = 'm'
        self.wait(wt)

        # scale back
        s_result[-1].apply_scale_back(
            scene=self,
            scale_factor=1.5,
            width_nominal=960,
            height_nominal=540,
            run_time_ratio=wt,
        )
        t_result.height_nominal = 'n'

        # ************************************************************
        self.next_section(
            'tensor shapes',
            skip_animations=True,
        )
        # ************************************************************
        # mobs = Group(
        #                                         s8_distrib,  s8_prob,  aci_12,  s8_merged_2d,
        #     sin_raw, aci_1, sin_norm,           s16_distrib, s16_prob, aci_13, s16_merged_2d, aci_15, s_merged_2d, aci_16, s_result,
        #                                         s32_distrib, s32_prob, aci_14, s32_merged_2d,
        #                                         t8_distrib,  t8_prob,  act_12,  t8_merged_2d,
        #     tin_raw, act_1, tin_norm, act_game, t16_distrib, t16_prob, act_13, t16_merged_2d, act_15, t_merged_2d, act_16, t_result,
        #                                         t32_distrib, t32_prob, act_14, t32_merged_2d,
        # )
        tensor_mobs = VGroup(
            tin_raw, tin_norm,
            t8_distrib, t8_prob, t8_merged_2d,
            t16_distrib, t16_prob, t16_merged_2d,
            t32_distrib, t32_prob, t32_merged_2d,
            t_merged_2d, t_result,
        )
        ac_all = VGroup(
            aci_1, aci_12, aci_13, aci_14, aci_15, aci_16,
            act_1, act_12, act_13, act_14, act_15, act_16,
        )

        # show shapes
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
        self.wait(wt)

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

        # ************************************************************
        self.next_section(
            'focus on core game',
            skip_animations=False,
        )
        # ************************************************************
        # first time focus
        focus_mobs = Group(
                            s8_distrib,  s8_prob,
        sin_norm,           s16_distrib, s16_prob,
                            s32_distrib, s32_prob,
                            t8_distrib,  t8_prob,
        tin_norm, act_game, t16_distrib, t16_prob,
                            t32_distrib, t32_prob,
        )
        left_mobs = Group(
            sin_raw, aci_1,
            tin_raw, act_1,
        )
        right_mobs = Group(
            aci_12,  s8_merged_2d,
            aci_13, s16_merged_2d, aci_15, s_merged_2d, aci_16, s_result,
            aci_14, s32_merged_2d,
            act_12,  t8_merged_2d,
            act_13, t16_merged_2d, act_15, t_merged_2d, act_16, t_result,
            act_14, t32_merged_2d,
        )
        self.play(AnimationGroup(
            left_mobs.animate.shift(LEFT*10),
            right_mobs.animate.shift(RIGHT*10),
            focus_mobs.animate.center(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # second time focus
        focus_mobs = Group(
                            t8_distrib,  t8_prob,
        tin_norm, act_game, t16_distrib, t16_prob,
                            t32_distrib, t32_prob,
        )
        other_mobs = Group(
                  s8_distrib,  s8_prob,
        sin_norm, s16_distrib, s16_prob,
                  s32_distrib, s32_prob,
        )
        self.play(AnimationGroup(
            other_mobs.animate.shift(UP*10),
            focus_mobs.animate.center().scale(2.0),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes for tensors
        self.play(AnimationGroup(
            *(ShowShape(mob, text_config=MEDIUM_SHAPE_TEXT_CONFIG)
             for mob in (t8_distrib,  t8_prob,
               tin_norm, t16_distrib, t16_prob,
                         t32_distrib, t32_prob,)),
             lag_ratio=0.0,
             run_time=wt*4,
        ))
        self.wait(wt)
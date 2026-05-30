from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.explainer import Explainer
from utils.general import import_mobs, export_mobs
from utils.image_pad import ImagePad

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
            skip_animations=False,
        )
        # ************************************************************
        # init stride-8 series in intuition view
        b8 = s32_reg[0].copy()
        e8 = Explainer.from_random(
            background=b8,
            reg_max=4,
            dist_range=(0.5, 1),
            prob_range=(0, 1),
            shape=(6, 6),       # 6x6 as stride-8's fake
            sf_pcell=0.5,
        )
        # FIXME: create aps thus arrange works properly
        self.play(e8.show_anchor_points(run_time=0.02, lag_ratio=0.0))
        s8_reg = Group(b8, e8).shift(RIGHT*10)
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
            shape=(5, 5),       # 5x5 as stride-16's fake
            sf_pcell=0.5,
        )
        # FIXME: create aps thus arrange works properly
        self.play(e16.show_anchor_points(run_time=0.02, lag_ratio=0.0))
        s16_reg = Group(b16, e16).shift(RIGHT*10)
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
        t8_merged_2d = t32_merged_2d.copy()
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

        # # ************************************************************
        # self.next_section(
        #     'insert stride-8 and stride-16 series',
        #     skip_animations=False,
        # )
        # # ************************************************************
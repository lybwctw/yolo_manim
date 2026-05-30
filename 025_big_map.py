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
            'init stride-8 and stride-16 series',
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
        # s8_reg = Group(b8, e8).shift(RIGHT*10)
        s8_reg = Group(b8, e8).shift(RIGHT*100)
        s8_prob = s8_reg.copy().shift(RIGHT*10)
        aco_a_8 = aco_a_32.copy().shift(RIGHT*10)
        s8_merged_2d = s8_reg.copy().shift(RIGHT*10)

        text = '{:.2f}'.format(s8_reg.width)
        text = Text(text)
        self.play(Write(text))
        self.wait(0.5)

        # # init stride-16 series in intuition view
        # b16 = s32_reg[0].copy()
        # e16 = Explainer.from_random(
        #     b16,
        #     reg_max=4,
        #     dist_range=(0.5, 1),
        #     prob_range=(0, 1),
        #     shape=(5, 5),       # 5x5 as stride-16's fake
        #     sf_pcell=0.5,
        # )
        # s16_reg = Group(b16, e16).shift(RIGHT*10)
        # s16_prob = s16_reg.copy().shift(RIGHT*10)
        # aco_a_16 = aco_a_32.copy().shift(RIGHT*10)
        # s16_merged_2d = s16_reg.copy().shift(RIGHT*10)

        # # init stride-8 series in tensor view
        # t8_reg = LayersFake(
        #     n=8,            # fake 64
        #     ref=t32_reg,
        #     buff=0.015,     # TODO: make this variable
        #     width_nominal=80,
        #     height_nominal=80,
        #     depth_nominal=64,
        #     expanded=True,
        # ).shift(RIGHT*10)
        # t8_prob = LayersFake(
        #     n=3,
        #     ref=t32_prob,
        #     width_nominal=80,
        #     height_nominal=80,
        #     depth_nominal=3,
        #     buff=0.05,      # TODO: make this variable
        #     expanded=True,
        # ).shift(RIGHT*10)
        # aco_1_8 = aco_1_32.copy().shift(RIGHT*10)
        # t8_merged_2d = LayersFake(
        #     n=1,
        #     ref=t32_merged_2d,
        #     width_nominal=7,
        #     height_nominal=6400,
        #     expanded=True,
        # ).shift(RIGHT*10)

        # # init stride-16 series in tensor view
        # t16_reg = LayersFake(
        #     n=8,            # fake 64
        #     ref=t32_reg,
        #     buff=0.015,     # TODO: make this variable
        #     width_nominal=40,
        #     height_nominal=40,
        #     depth_nominal=64,
        #     expanded=True,
        # ).shift(RIGHT*10)
        # t16_prob = LayersFake(
        #     n=3,
        #     ref=t32_prob,
        #     buff=0.05,      # TODO: make this variable
        #     width_nominal=40,
        #     height_nominal=40,
        #     depth_nominal=3,
        #     expanded=True,
        # ).shift(RIGHT*10)
        # aco_1_16 = aco_1_32.copy().shift(RIGHT*10)
        # t16_merged_2d = LayersFake(
        #     n=1,
        #     ref=t32_merged_2d,
        #     width_nominal=7,
        #     height_nominal=1600,
        #     expanded=True,
        # ).shift(RIGHT*10)

        # # mobs = Group(
        # #     # Mobject(), Mobject(), Mobject(), Mobject(),  
        # #     sin_raw,   aci_a,     sin_pad,   s8_reg,
        # #     # Mobject(), Mobject(), Mobject(), s32_reg, 
        # #     # Mobject(), Mobject(), Mobject(), Mobject(), s8_reg,  s8_prob,  aco_a_8,  s8_merged_2d,
        # #     # sin_raw,   aci_a,     sin_pad,   Mobject(), s16_reg, s16_prob, aco_a_16, s16_merged_2d,
        # #     # Mobject(), Mobject(), Mobject(), Mobject(), s32_reg, s32_prob, aco_a_32, s32_merged_2d,
        # #     # Mobject(), Mobject(), Mobject(), Mobject(), t8_reg,  t8_prob,  aco_1_8,  t8_merged_2d,
        # #     # tin_raw,   aci_1,     tin_pad,   ac_game,   t16_reg, t16_prob, aco_1_16, t16_merged_2d,
        # #     # Mobject(), Mobject(), Mobject(), Mobject(), t32_reg, t32_prob, aco_1_32, t32_merged_2d,
        # # )
        # # mobs.generate_target()
        # # # mobs.target.arrange().center()
        # # mobs.target.arrange_in_grid(
        # #     rows=1,
        # #     cols=4,
        # #     # buff=0.1,
        # # ).center()
        # # self.play(MoveToTarget(
        # #     mobs,
        # #     run_time=0.5,
        # # ))
        # # self.wait()

        # # # self.play(s8_reg[-1].animate.set_opacity(1.0))
        # # # self.wait()
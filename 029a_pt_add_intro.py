from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.general import import_mobs, export_mobs
from utils.constants import *
from utils.constants_3d import *

from modules.pt_add import create_ic_add

import torch

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # modules
        cards_module = import_mobs('028')
        (
            ic_add, ic_split, ic_cat,
            ic_Conv2d, ic_MaxPool2d, ic_Sigmoid, ic_ReLU, ic_SiLU, ic_Softmax, ic_Linear, ic_BatchNorm2d,
            ic_Conv, ic_Bottleneck, ic_C2f, ic_SPPF, ic_Detect,
        ) = cards_module
        card_module = ic_add
        card_others = VGroup(card for card in cards_module if card is not card_module)

        # input/output
        card_i1 = InfoCard('input_1').to_edge(LEFT, buff=CARD_EDGE_BUFF).set_y(CARD_INIT_UP)
        card_i2 = InfoCard('input_2').to_edge(LEFT, buff=CARD_EDGE_BUFF).set_y(CARD_INIT_UP)
        card_o1 = InfoCard('output_2').to_edge(LEFT, buff=CARD_EDGE_BUFF).set_y(CARD_INIT_DOWN)

        cards = VGroup(card_i1, card_i2, card_module, card_o1)

        self.add_fixed_in_frame_mobjects(
            cards_module, card_i1, card_i2, card_o1,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on current module',
            skip_animations=False,
        )
        # ************************************************************
        # focus on current card
        self.play(card_others.animate.fade(CARD_FADE_VALUE), run_time=wt)
        card_others.save_state()
        self.play(AnimationGroup(
            card_others.animate.shift(LEFT*CARD_OUT_OFFSET),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # introduce input/output
        self.play(cards.animate(
            run_time=wt,
            rate_func=rate_functions.ease_out_cubic,
        ).arrange(
            DOWN,
            buff=CARD_GAP,
            aligned_edge=LEFT,
        ).to_edge(
            LEFT,
            buff=CARD_EDGE_BUFF,
        ))
        self.wait(wt)

        export_mobs(__file__, cards)
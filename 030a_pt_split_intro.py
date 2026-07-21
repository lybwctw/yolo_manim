from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.general import import_mobs, export_mobs
from utils.constants import *
from utils.constants_3d import *

from modules.pt_add import create_ic_add

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
        card_list = import_mobs('028')
        (
            ic_add, ic_split, ic_cat,
            ic_Conv2d, ic_MaxPool2d, ic_Sigmoid, ic_ReLU, ic_SiLU, ic_Softmax, ic_Linear, ic_BatchNorm2d,
            ic_Conv, ic_Bottleneck, ic_C2f, ic_SPPF, ic_Detect,
        ) = card_list
        card_focus = ic_split
        card_others = VGroup(card for card in card_list if card is not card_focus)

        # input/output
        card_i1 = InfoCard('in_1').to_edge(LEFT, buff=CARD_EDGE_BUFF).set_y(CARD_INIT_UP)
        card_o1 = InfoCard('out_1').to_edge(LEFT, buff=CARD_EDGE_BUFF).set_y(CARD_INIT_DOWN)
        card_o2 = InfoCard('out_2').to_edge(LEFT, buff=CARD_EDGE_BUFF).set_y(CARD_INIT_DOWN)

        cards = VGroup(
            card_i1,
            card_focus,
            card_o1,
            card_o2,
        )

        self.add_fixed_in_frame_mobjects(
            cards, card_others,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on current module',
            skip_animations=False,
        )
        # ************************************************************
        # focus on current card
        card_list.save_state()
        self.play(card_others.animate.fade(CARD_FADE_VALUE), run_time=wt)
        self.play(AnimationGroup(
            card_others.animate.shift(LEFT*CARD_OUT_OFFSET),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # to edge center
        self.play(card_focus.animate(
            run_time=wt,
        ).set_y(
            CARD_CENTER_Y,
        ))
        self.wait(wt)

        # expand card params
        self.play(card_focus.expand_for_detail(
            aligned_edge=LEFT,
            run_time=wt,
        ))
        self.play(card_focus.write_detail(
            run_time=wt,
        ))
        # self.wait(wt)

        # introduce 2 inputs and 1 output
        cards.generate_target()
        cards.target.arrange(
            DOWN,
            buff=CARD_GAP,
            aligned_edge=LEFT,
        ).to_edge(
            LEFT,
            buff=CARD_EDGE_BUFF,
        )
        offset = card_focus.get_y() - cards.target[1].get_y()
        cards.target.shift(offset*UP)
        self.play(MoveToTarget(
            cards,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = VGroup(cards, card_list)     # used by b/c/d/e...
        export_mobs(__file__, mobs)
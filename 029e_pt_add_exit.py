from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor_3D
from utils.general import *
from utils.constants import *
from utils.constants_3d import *

import torch

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # cards
        cards, card_list = import_mobs('029a')
        (
            card_i1,
            card_i2,
            card_module,
            card_o1,
        ) = cards

        self.add_fixed_in_frame_mobjects(
            cards
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back to module card list',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            card_i1.animate.set_y(CARD_INIT_UP),
            card_i2.animate.set_y(CARD_INIT_UP),
            card_o1.animate.set_y(CARD_INIT_DOWN),
            card_list.animate.restore(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
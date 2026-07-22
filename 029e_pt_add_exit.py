from manim import *

from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # cards
        cards, card_modules = import_mobs('029a')
        (
            card_i1,
            card_i2,
            card_m,
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
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_i2, UP),
            detach_to_ref(card_o1, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(card_modules.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)
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
        card_focus, cards_module = import_mobs('038a')

        self.add_fixed_in_frame_mobjects(cards_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back to module list',
            skip_animations=False,
        )
        # ************************************************************
        # module list
        self.play(cards_module.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

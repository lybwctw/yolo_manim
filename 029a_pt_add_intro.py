from manim import *

from utils.general import import_mobs, export_mobs
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

wt = 1.0
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
        card_focus, cards_other = collect_idx_card(cards_module, 0)

        self.add_fixed_in_frame_mobjects(cards_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on current module',
            skip_animations=False,
        )
        # ************************************************************
        cards_module.save_state()

        # exit and focus
        self.play(AnimationGroup(
            cards_other.animate.set_x(CARD_EXIT_X),
            card_focus.animate.set_y(CARD_FOCUS_Y),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # no expansion

        # export
        mobs = VGroup(card_focus, cards_module)     # NOTE: used by next
        export_mobs(__file__, mobs)
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
        card_focus, cards_module = import_mobs('041a')
        cards_sample = import_mobs('041h')

        self.add_fixed_in_frame_mobjects(cards_sample)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back to module list',
            skip_animations=False,
        )
        # ************************************************************
        # shrink samples
        self.play(AnimationGroup(
            *(card.shrink_summary() for card in cards_sample),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # replace all samples with a single
        self.play(Succession(
            AnimationGroup(
                *(Unwrite(card) for card in cards_sample),
                lag_ratio=0.0,
                run_time=wt,
            ),
            Write(card_focus, run_time=wt),
        ))
        self.wait(wt)
        self.add_fixed_in_frame_mobjects(cards_module)

        # module list
        self.play(cards_module.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

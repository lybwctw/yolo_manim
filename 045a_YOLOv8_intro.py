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
        cards_focus, cards_other = collect_idx_cards(
            cards_module,
            (15,16,17,18,19),
        )

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
        for card in cards_focus:
            card.generate_target()
        for card in cards_other:
            card.generate_target()
        focus_target = VGroup(card.target for card in cards_focus)
        other_target = VGroup(card.target for card in cards_other)
        focus_target.set_y(CARD_FOCUS_Y)
        other_target.set_x(CARD_EXIT_X)
        self.play(AnimationGroup(
            AnimationGroup(
                *(MoveToTarget(
                    card,
                ) for card in cards_other),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(MoveToTarget(
                    card,
                ) for card in cards_focus),
                lag_ratio=0.2,
            ),
            lag_ratio=0.8,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(cards_focus, cards_module)     # NOTE: used by next
        export_mobs(__file__, mobs)


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

        # input/output
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        card_i2 = InfoCard('in_2').hide_to_corner(UP)
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        card_is = VGroup(card_i1, card_i2)

        self.add_fixed_in_frame_mobjects(
            cards_module, card_is, card_o1,
        )
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

        # introduce intput/output
        self.play(AnimationGroup(
            attach_to_ref(card_is, card_focus, UP,
                rate_func=rate_functions.exponential_decay),
            attach_to_ref(card_o1, card_focus, DOWN,
                rate_func=rate_functions.exponential_decay),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        cards = VGroup(
            card_i1,
            card_i2,
            card_focus,
            card_o1,
        )
        mobs = VGroup(cards, cards_module)     # NOTE: used by b/c/d/e...
        export_mobs(__file__, mobs)
from manim import *

from utils.general import import_mobs, export_mobs
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

MODULE_PARAMS = {
    'split_size': UNKNOWN,
    'dim': UNKNOWN,
}

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
        card_focus, cards_other = collect_idx_card(cards_module, 1)
        
        # # input/output
        # card_i1 = InfoCard('in_1').hide_to_corner(UP)
        # card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        # card_o2 = InfoCard('out_2').hide_to_corner(DOWN)
        # card_os = VGroup(card_o1, card_o2)

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
        self.wait(wt)

        # expand
        self.play(card_focus.expand_params(
            params=MODULE_PARAMS,
            run_time=wt,
        ))
        card_focus.add(card_focus.line_mobs)    # FIXME

        # # introduce intput/output
        # self.play(AnimationGroup(
        #     attach_to_ref(card_i1, card_focus, UP,
        #         rate_func=rate_functions.exponential_decay),
        #     attach_to_ref(card_os, card_focus, DOWN,
        #         rate_func=rate_functions.exponential_decay),
        #     lag_ratio=0.0,
        #     run_time=wt*2,
        # ))
        # self.wait(wt)

        # export
        mobs = VGroup(card_focus, cards_module)     # NOTE: used by b/c/d/e...
        export_mobs(__file__, mobs)
from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

from modules.pt_Conv2d import *

import torch

# TODO: reference image

EMPTY_CONFIG = {
    'in_channels': UNKNOWN,
    'out_channels': UNKNOWN,
    'kernel_size': UNKNOWN,
    'stride': UNKNOWN,
    'padding': UNKNOWN,
    'bias': UNKNOWN,
    'dilation': UNKNOWN,
    'groups': UNKNOWN,
    'padding_mode': UNKNOWN,
}

INIT_CONFIG = {
    'in_channels': 6,
    'out_channels': 5,
    'kernel_size': 3,
    'stride': 1,
    'padding': 1,
    'bias': False,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # cards
        card_gallery = import_mobs('028')
        card_module, cards_other = collect_idx_card(card_gallery, 3)

        self.add_fixed_in_frame_mobjects(card_gallery)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on current module',
            skip_animations=True,
        )
        # ************************************************************
        card_gallery.save_state()

        # focus
        self.play(AnimationGroup(
            cards_other.animate.set_x(CARD_EXIT_X),
            card_module.animate.set_y(CARD_FOCUS_Y),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # expand empty
        self.play(card_module.expand_params(
            params=EMPTY_CONFIG,
            run_time=wt,
        ))
        card_module.add(card_module.line_mobs)    # FIXME
        self.wait(wt)


        # ************************************************************
        self.next_section(
            'init config and params',
            skip_animations=True,
        )
        # ************************************************************
        # intro view
        self.set_camera_orientation(
            **VIEW_INTRO,
        )

        # raw module
        t_module = torch.nn.Conv2d(
            **INIT_CONFIG,
        )

        # mob module
        m_module = PT_Conv2d(
            module=t_module,
            module_config=INIT_CONFIG,
        )

        # options
        self.play(card_module.update_params(
            INIT_CONFIG,
            run_time=wt,
        ))

        # params
        self.play(m_module.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={
                'lag_ratio': 0.1,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'param shapes',
            skip_animations=True,
        )
        # ************************************************************
        # show shapes on weight (no bias)
        self.play(ShowShape3D(
            scene=self,
            mob=m_module.mobs_weight,
            facing='left',
            aargs={
                'lag_ratio': 0.5,
                'run_time': wt*4,
            },
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'config value vs param shapes',
            skip_animations=False,
        )
        # ************************************************************
        # out_channels vs block dimension
        value_mob = card_module.value_objs['out_channels']
        shape_mob = m_module.mobs_weight.shape_texts[0]
        self.play(AnimationGroup(
            *(AnimationGroup(mob.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_fill(color=PURE_RED))
             for mob in [value_mob, shape_mob]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight in_channels and layer dimension
        value_mob = card_module.value_objs['in_channels']
        shape_mob = m_module.mobs_weight.shape_texts[1]
        self.play(AnimationGroup(
            *(AnimationGroup(mob.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_fill(color=PURE_RED))
             for mob in [value_mob, shape_mob]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight kernel_size and w/h dimensions
        value_mob = card_module.value_objs['kernel_size']
        shape_mob1 = m_module.mobs_weight.shape_texts[2]
        shape_mob2 = m_module.mobs_weight.shape_texts[3]
        self.play(AnimationGroup(
            *(AnimationGroup(mob.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_fill(color=PURE_RED))
             for mob in [value_mob, shape_mob1, shape_mob2]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes on weights
        self.play(HideShape3D(
            mob=m_module.mobs_weight,
            aargs={
                'lag_ratio': 0.5,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        # mobs = Group(card, m_module)
        # export_mobs(__file__, mobs)     # NOTE, used by 029


        # # export
        # mobs = VGroup(card_module, card_gallery)     # NOTE: used by b/c/d/e...
        # export_mobs(__file__, mobs)

        # self.move_camera(
        #     **VIEW_COMPUTE,
        #     run_time=wt,
        # )
        # self.wait(wt)
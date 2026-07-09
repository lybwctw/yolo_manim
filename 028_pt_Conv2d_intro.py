from manim import *

from utils.name_card import NameCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.general import export_mobs
from utils.constants import *
from utils.constants_3d import *

from modules.pt_Conv2d import *

import torch

# TODO: reference image

PT_Conv2d_CONFIG = {
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

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        self.set_camera_orientation(
            **VIEW_INTRO,
        )

        card = NameCard(
            name='Conv2d',
            params=PT_Conv2d_CONFIG,
            levels=DEFAULT_PT_Conv2d_LEVELS,
        )

        t_module = torch.nn.Conv2d(
            **PT_Conv2d_CONFIG,
        )

        m_module = PT_Conv2d(
            module=t_module,
            module_config=PT_Conv2d_CONFIG,
        )

        # ************************************************************
        self.next_section(
            'introduce module',
            skip_animations=False,
        )
        # ************************************************************
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

        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce name card',
            skip_animations=False,
        )
        # ************************************************************
        self.camera.add_fixed_in_frame_mobjects(card)
        self.play(Create(
            card,
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes on weight (bias later)
        self.play(ShowShape3D(
            scene=self,
            mob=m_module.mobs_weight,
            facing='right',
            aargs={
                'lag_ratio': 0.5,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'highlight option and module mapping',
            skip_animations=False,
        )
        # ************************************************************
        # highlight out_channels and block dimension
        op1 = card.value_mob('in_channels')
        st1 = m_module.mobs_weight.shape_texts[1]
        self.play(AnimationGroup(
            op1.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st1.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight in_channels and layer dimension
        op2 = card.value_mob('out_channels')
        st2 = m_module.mobs_weight.shape_texts[0]
        self.play(AnimationGroup(
            op2.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st2.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight kernel_size and w/h dimension
        op3 = card.value_mob('kernel_size')
        st3a = m_module.mobs_weight.shape_texts[2]
        st3b = m_module.mobs_weight.shape_texts[3]
        self.play(AnimationGroup(
            op3.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st3a.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st3b.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(HideShape3D(
            mob=m_module.mobs_weight,
            aargs={
                'lag_ratio': 0.5,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        mobs = Group(card, m_module)
        export_mobs(__file__, mobs)     # NOTE, used by 029
from manim import *

from utils.mtensor import MTensor_1D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_1D = 1.5
TENSOR_HGAP_1D = 1.0

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
        card_m, _ = import_mobs('031a')

        # input raw tensor
        t_i1 = torch.randn(5)
        t_i2 = torch.randn(5)

        # input tensor mob
        tensor_is = VGroup(
            MTensor_1D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ).shift(UP*TENSOR_VGAP_1D)
            for t in [t_i1, t_i2]
        )
        tensor_is.arrange(
            RIGHT,
            buff=TENSOR_HGAP_1D,
        ).align_to(
            UP*TENSOR_VGAP_1D,
            DOWN,
        )

        # input card mob
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        card_i2 = InfoCard('in_2').hide_to_corner(UP)
        
        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_i2,
            card_m,
        )   # tensor not added while it's ok
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'input tensor and card',
            skip_animations=False,
        )
        # ************************************************************
        # input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                direction=RIGHT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={'lag_ratio': 0.5},
            ) for tmob in tensor_is),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # input card
        self.play(attach_to_ref(
            VGroup(card_i1, card_i2),
            card_m,
            UP,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(cmob.expand_summary(
                t2s(t_i1),
            ) for cmob, t in zip(
                [card_i1, card_i2],
                [t_i1, t_i2]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
from manim import *

from utils.mtensor import MTensor_2D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_2D = 1.5
TENSOR_HGAP_2D = 1.0

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # cards
        card_m, _ = import_mobs('030a')

        # input raw tensor
        t_i1 = torch.randn(6,8)

        # input tensor mob
        tensor_i1 = MTensor_2D(
            array=t_i1,
            z_style='erect',
            **MEDIUM_CUBE_CONFIG,
        ).rotate(
            90*DEGREES,
            RIGHT,
        ).shift(UP*TENSOR_VGAP_2D)

        # input card mob
        card_i1 = InfoCard('in_1').hide_to_corner(UP)

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_m,
            card_i1,
        )   # tensor not added while it's ok
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'input tensor and card',
            skip_animations=False,
        )
        # ************************************************************
        # input tensor
        self.play(tensor_i1.create(
            direction=RIGHT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))

        # input card
        self.play(attach_to_ref(
            card_i1,
            card_m,
            UP,
            run_time=wt,
        ))
        self.play(card_i1.expand_summary(
            t2s(t_i1),
            run_time=wt,
        ))
        self.wait(wt)
from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.general import *
from utils.mtensor import MTensor_3D
from utils.constants import *
from utils.constants_3d import *

from modules.pt_add import create_ic_add

import torch

TENSOR_EGAP_3D = 0.8

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
        cards, _ = import_mobs('030a')
        (
            card_i1,
            card_module,
            card_o1,
            card_o2,
        ) = cards

        # raw torch arrays
        t_i1 = torch.randn(6,3,4)
        # t_o1, t_o2 = torch.split(t_i1, 3)

        # tensor mobs
        tensor_i1 = MTensor_3D(
            array=t2n(t_i1),
            **MEDIUM_CUBE_CONFIG,
        ).center()

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce inputs',
            skip_animations=False,
        )
        # ************************************************************
        # # show input tensor
        # self.play(AnimationGroup(
        #     tensor_i1.create(
        #         style='beam',
        #         direction=OUT,
        #         anim=GrowFromCenter,
        #         aargs={'rate_func': rate_functions.ease_out_back},
        #         gargs={},
        #     ),
        #     card_i1.expand_summary(t2s(t_i1)),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait()

        self.play(card_module.update_value(
            name='split_size',
            value=3,
            run_time=wt,
        ))
        self.wait(wt)
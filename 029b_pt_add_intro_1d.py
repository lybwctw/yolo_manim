from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor_1D
from utils.general import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_OFFSET = 1.5

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # perspective
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        # cards
        cards = import_mobs('029')
        (
            card_i1,
            card_i2,
            card_module,
            card_o1,
        ) = cards

        # sample tensors
        t_i1 = np.random.randn(8)
        t_i2 = np.random.randn(8)
        t_o1 = t_i1 + t_i2

        # tensor mobs
        tensor_i1 = MTensor_1D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).shift(UP*TENSOR_OFFSET*2)
        tensor_i2 = MTensor_1D(
            array=t_i2,
            **MEDIUM_CUBE_CONFIG,
        ).shift(UP*TENSOR_OFFSET)
        tensor_o1 = MTensor_1D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).shift(DOWN*TENSOR_OFFSET)
        VGroup(tensor_i1, tensor_i2, tensor_o1).center()

        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce cube inputs',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            AnimationGroup(
                card_i1.expand_summary(summary=shape_str(t_i1)),
                tensor_i1.create(
                    direction=RIGHT,
                    anim=GrowFromCenter,
                    aargs={'rate_func': rate_functions.ease_out_back},
                    gargs={'lag_ratio': 0.5},
                ),
            ),
            AnimationGroup(
                card_i2.expand_summary(summary=shape_str(t_i2)),
                tensor_i2.create(
                    direction=RIGHT,
                    anim=GrowFromCenter,
                    aargs={'rate_func': rate_functions.ease_out_back},
                    gargs={'lag_ratio': 0.5},
                ),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output',
            skip_animations=False,
        )
        # ************************************************************
        # TODO: highlight loop
        self.play(AnimationGroup(
            card_o1.expand_summary(summary=shape_str(t_o1)),
            tensor_o1.create(
                direction=RIGHT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={'lag_ratio': 0.5},
            ),
            run_time=wt,
        ))
        self.wait(wt)

# ************************************************************
# Visualize several Conv samples from yolov8 series (3 classes).
# ************************************************************
from manim import *
import csv
from pathlib import Path

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *
import torch
import numpy as np

from modules.ut_Conv import *
from modules.pt_Conv2d import *
from modules.pt_BatchNorm2d import *

from ultralytics.nn.modules import Conv

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

wt = 0.5

class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        cards = import_mobs('040f')

        # show initial reference card
        self.set_camera_orientation(
            **VIEW_COMPUTE,
            zoom=0.6,
            focal_distance=80,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on [3 16 3 2 1]',
            skip_animations=False,
        )
        # ************************************************************
        # TODO: highlight current card

        # assets
        config_module = {
            'c1': 3,
            'c2': 16,
            'k': 3,
            's': 2,
            'p': 1,
        }
        config_conv = Conv_2_conv_config(config_module)
        # config_bn =  Conv_2_bn_config(config_module)

        ut_module = Conv(**config_module)
        pt_conv = ut_module.conv
        pt_bn = ut_module.bn

        mm_conv = PT_Conv2d(
            module=pt_conv,
            module_config=config_conv,
            block_gap=0.5,
            bias_offset=0.5,
        )
        # manual 4 aligned erect 1d tensor
        mm_bn = VGroup(
            *(MTensor1D(
                array=np.random.randn(4), # value doesn't matter
                mode='cube',
                style='erect',
                **SMALL_TENSOR_CONFIG,
            ) for _ in range(config_module['c2'])),
        )
        for idx, beam in enumerate(mm_bn):
            beam.next_to(
                mm_conv.mt_weight[idx],
                DOWN,
                TENSOR_VGAP_SMALL,
            )

        VGroup(mm_conv, mm_bn).center()

        # show conv and bn
        self.play(AnimationGroup(
            mm_conv.mt_weight.create(
                style='beam',
                direction=OUT,
                lag_ratio=0.1,
                run_time=wt*2,
            ),
            AnimationGroup(
                *(beam.create(
                    style='series',
                    direction=LEFT,
                ) for beam in mm_bn),
                lag_ratio=0.1,
                run_time=wt*2,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)
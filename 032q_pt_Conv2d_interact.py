from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *

from modules.pt_Conv2d import *

import torch

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0
BIAS_GAP_BIG = 2.0
BIAS_GAP_SMALL = 0.8

CONFIG_1 = {
    'in_channels': 4,
    'out_channels': 7,
    'kernel_size': 2,
    'stride': 1,
    'padding': 1,
    'bias': True,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

CONFIG_2 = {
    'in_channels': 5,           # updated
    'out_channels': 4,          # updated
    'kernel_size': 3,           # updated
    'stride': 1,
    'padding': 1,
    'bias': True,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

CONFIG_2 = {
    'in_channels': 6,           # updated
    'out_channels': 5,          # updated
    'kernel_size': 3,           # updated
    'stride': 1,
    'padding': 1,
    'bias': False,              # updated
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load cards and input
        (
            card_i1,
            card_module,
            card_o1,
        ) = import_mobs('032p')

        # raw module and manim module
        module_config = CONFIG_1
        torch_module = torch.nn.Conv2d(**module_config)
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=module_config,
            block_gap=0.5,
            bias_offset=BIAS_GAP_BIG,
        ).center()
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.wait(wt)

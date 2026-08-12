from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

from modules.pt_Conv2d import *

import torch

# EMPTY_CONFIG = {
#     'in_channels': UNKNOWN,
#     'out_channels': UNKNOWN,
#     'kernel_size': UNKNOWN,
#     'stride': UNKNOWN,
#     'padding': UNKNOWN,
#     'bias': UNKNOWN,
#     'dilation': UNKNOWN,
#     'groups': UNKNOWN,
#     'padding_mode': UNKNOWN,
# }

# INIT_CONFIG = {
#     'in_channels': 6,
#     'out_channels': 5,
#     'kernel_size': 3,
#     'stride': 1,
#     'padding': 1,
#     'bias': False,
#     'dilation': 1,
#     'groups': 1,
#     'padding_mode': 'zeros',
# }

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
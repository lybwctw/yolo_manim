# ************************************************************
# Input/output for SPPF.
# ************************************************************
from manim import *

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
from modules.ut_Bottleneck import *

from ultralytics.nn.modules import SPPF

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load cards, modules, tensors, graph
        (
            tc_i, mc, tc_o,
            mm_cv1, mm_cv2,
            mts,
            mg,
        ) = import_mobs('043c')
        module_config = mg.module_config

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.7)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mts, mm_cv1, mm_cv2)
        self.wait(wt)
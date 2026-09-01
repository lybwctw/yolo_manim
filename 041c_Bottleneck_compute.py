# ************************************************************
# Detailed Compute loop for Bottleneck (shortcut=False).
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

from ultralytics.nn.modules import Bottleneck

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
    # 'c1': 8,
    # 'c2': 8,
    # 'shortcut': False,
    # 'k': (3,3),
    # 'e': 0.5,
# }

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load card and graph
        mc, mg = import_mobs('041b')
        module_config = mg.module_config

        # raw modules
        m_module = Bottleneck(**module_config)
        m_cv1 = m_module.cv1
        m_cv2 = m_module.cv2

        # raw tensor
        t_i = torch.randn(1, 8, 40, 40)
        t_m1 = m_cv1(t_i)
        t_o = m_cv2(t_m1)

        # module mobs (cv1 and cv2)
        mm_cv1 = UT_Conv(
            module_config=Bottleneck_2_cv1_config(module_config),
        )
        mm_cv2 = UT_Conv(
            module_config=Bottleneck_2_cv2_config(module_config),
        )
        VGroup(mm_cv1, mm_cv2).arrange(
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        # # tensor mobs
        # mts = VGroup(
        #     MTensor3D(
        #         array=t.detach()[0],
        #         mode='cube',
        #         **SMALL_TENSOR_CONFIG,
        #     ) for t in [
        #         t_i, t_m1, t_o,
        #     ]
        # )

        # increase_z_index_in_batch([
        #     mts[0],
        #     mm_cv1.mt_weight,
        #     mts[1],
        #     mm_cv2.mt_bias,
        #     mts[2],
        # ])

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(mc, mg)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show sub modules',
            skip_animations=False,
        )
        # ************************************************************
        # highlight conv in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[0],
            run_time=wt,
        ))
        # self.wait(wt)

        # show cv1 params (4d)
        self.play(mm_cv1.create(
            run_time=wt,
        ))
        # self.wait(wt)
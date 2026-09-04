# ************************************************************
# Detailed Compute loop for C2f.
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

from ultralytics.nn.modules import C2f

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
    # 'c1': 8,
    # 'c2': 8,
    # 'n': 3,
    # 'shortcut': False,
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
        mc, mg = import_mobs('042b')
        module_config = mg.module_config

        # raw modules
        m_module = C2f(**module_config)
        m_cv1 = m_module.cv1
        m_cv2 = m_module.cv2
        m_m = m_module.m

        # raw tensors
        t_i = torch.randn(1, 8, 5, 6)
        t_m1 = m_cv1(t_i)
        t_m2, t_m3 = torch.split(t_m1, 4, dim=1)
        t_m4 = m_m[0](t_m3)
        t_m5 = m_m[1](t_m4)
        t_m6 = m_m[2](t_m5)
        t_m7 = torch.concat([t_m2, t_m3, t_m4, t_m5, t_m6], dim=1)
        t_o = m_cv2(t_m7)

        # module mobs (cv1, m, cv2)
        mm_cv1 = UT_Conv(
            module_config=C2f_2_cv1_config(module_config),
            init_scale=0.8,
            opaque=True,
        )
        mm_cv2 = UT_Conv(
            module_config=C2f_2_cv2_config(module_config),
            init_scale=0.8,
            opaque=True,
        )
        mm_m = VGroup(
            UT_Bottleneck(
                module_config=C2f_2_bottleneck_config(module_config),
                init_scale=0.8,
                opaque=True,
            ) for _ in range(module_config['n'])
        )
        mm_m1, mm_m2, mm_m3 = mm_m
        VGroup(mm_cv1, mm_m1, mm_m2, mm_m3, mm_cv2).arrange(
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        # TODO: tensor mobs

        # increase_z_index_in_batch([ # ])

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
        # highlight cv1 in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[0],
            run_time=wt,
        ))
        # self.wait(wt)

        # show cv1
        self.play(mm_cv1.create(
            ref='center',
            run_time=wt,
        ))
        # self.wait(wt)

        # show m
        self.play(Succession(
            *(mb.create(
                ref='center',
                run_time=wt,
            ) for mb in mm_m),
            run_time=wt*3,
        ))
        # self.wait(wt)

        # show cv2
        self.play(mm_cv2.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)
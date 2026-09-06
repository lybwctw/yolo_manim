# ************************************************************
# shortcut=True for C2f.
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

TENSOR_VGAP_SMALL = 0.5
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0


# INIT_CONFIG = {
    # 'c1': 16,
    # 'c2': 16,
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
        # load cards, modules, tensors, graph
        (
            tc_i, mc, tc_o,
            mm_cv1, mm_m, mm_cv2,
            mts,
            mg,
        ) = import_mobs('042e')
        module_config = mg.module_config

        # for convenience
        mm_m1, mm_m2, mm_m3 = mm_m

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.7)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mm_m, mm_cv1, mm_cv2, mts)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'shortcut: False -> True',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'shortcut': True},
                run_time=wt,
            )
        )

        # update graph
        self.play(AnimationGroup(
            mg.mobs_card[2].update_summary(
                summary='8 8 T',
                run_time=wt,
            ),
            mg.mobs_card[3].update_summary(
                summary='8 8 T',
                run_time=wt,
            ),
            mg.mobs_card[4].update_summary(
                summary='8 8 T',
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'export',
            skip_animations=False,
        )
        # ************************************************************
        # export
        mobs = VGroup(
            tc_i, mc, tc_o,
            mm_cv1, mm_m, mm_cv2,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
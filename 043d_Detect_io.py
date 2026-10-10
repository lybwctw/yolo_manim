# ************************************************************
# Input/output for Detect.
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

# from ultralytics.nn.modules import Detect

# INIT_CONFIG = {
#     'ch': 8,
#     'c2': 4,
#     'c3': 4,
#     'reg_max': 5,      # 5 probs for each direction (16 by default)
#     'nc': 3,           # 3 classes
# }

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
            tc_i, mc, card_o1, card_o2,
            mm_bs, mm_cs,
            mts,
            mg,
        ) = import_mobs('044c')
        module_config = mg.module_config

        # for convenience
        mm_b1, mm_b2, mm_b3 = mm_bs
        mm_c1, mm_c2, mm_c3 = mm_cs
        series_box = VGroup(
            *mm_bs,
            *mts[1:13],
        )
        series_cls = VGroup(
            *mm_cs,
            *mts[13:],
        )

        # show initial mobs
        camera_config = {
            **VIEW_COMPUTE,
            'phi': 40*DEGREES,
            'zoom': 0.6,
            # 'frame_center': DOWN*1.5,
        }

        # FIXME: initial camera setup hack
        self.set_camera_orientation(**camera_config)
        self.add_fixed_in_frame_mobjects(tc_i, mc, card_o1, card_o2, mg)
        self.add(mts, mm_bs, mm_cs)
        self.wait(wt*0.1)
        self.set_camera_orientation(frame_center=DOWN*1.5)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on modules',
            skip_animations=False,
        )
        # ************************************************************
        # use (?, h, w) in tensor cards
        self.play(AnimationGroup(
            tc_i.update_summary(summary='(8,h,w)'),
            card_o1.update_summary(summary='(20,h,w)'),
            card_o2.update_summary(summary='(3,h,w)'),
            lag_ratio=0.5,
            run_time=wt*3,
        ))

        # clean shapes in graph
        self.play(mg.hide_shapes(
            lag_ratio=0.5,
            run_time=wt,
        ))

        # fade tensor mobs
        self.play(AnimationGroup(
            *(mt.tarnish() for mt in mts),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            tc_i, mc, card_o1, card_o2,
            mm_bs, mm_cs,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
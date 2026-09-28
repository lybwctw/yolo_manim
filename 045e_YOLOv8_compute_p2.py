# ************************************************************
# Compute steps for fake yolov8n, part 2.
# ************************************************************
from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.ftensor import *
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *
import torch
import numpy as np

from modules.ut_Conv import UT_Conv
from modules.ut_Bottleneck import UT_Bottleneck
from modules.ut_C2f import UT_C2f
from modules.ut_SPPF import UT_SPPF
from modules.ut_Detect import UT_Detect

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

INIT_SCALE = 0.5

RUNNING_X = 6.0
FAKE_HALF = 2/3

# for reference
# [0]  16 -> 8
# [1]  32 -> 12
# [2]  32 -> 12
# [3]  64 -> 16
# [4]  64 -> 16
# [5]  128 -> 20
# [6]  128 -> 20
# [7]  256 -> 24
# [8]  256 -> 24
# [9]  256 -> 24
# [10] 256 -> 24
# [11] 384 -> 26
# [12] 128 -> 20
# [13] 128 -> 20
# [14] 192 -> 22
# [15] 64 -> 16
# [16] 64 -> 16
# [17] 192 -> 22
# [18] 128 -> 20
# [19] 128 -> 20
# [20] 384 -> 26
# [21] 256 -> 24
# [22] 
# [23]
# [24]

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
        mobs = import_mobs('045d')
        (
            mm_modules, card, graph,
            mt_running,
            mt_c9, mt_c12,
        ) = mobs

        cam_args = {
            **VIEW_COMPUTE,
            'theta': -125*DEGREES,
            'focal_distance': 100,
            'zoom': 0.35,
        }
        self.set_camera_orientation(
            **cam_args,
        )
        self.add_fixed_in_frame_mobjects(card, graph)
        self.add(mm_modules, mt_running, mt_c9, mt_c12)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[15] apply C2f, backup',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[15]
        mask_module = np.eye(len(mm_modules), dtype=bool)[15]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[15],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[15].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(64,80,80),
            scale_factor=(16/36, 1.0, 1.0),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c15 = mt_running.copy()
        mt_c15.set_opacity(0.3)
        self.play(FadeIn(mt_c15, run_time=wt*0.1))
        self.play(mt_c15.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[15],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)
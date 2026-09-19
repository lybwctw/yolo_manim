# ************************************************************
# Visualize fake modules for YOLOv8n.
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

from modules.ut_Conv import *
from modules.ut_C2f import UT_C2f
from modules.ut_SPPF import MGraph_SPPF
from modules.ut_Detect import *

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

INIT_SCALE = 0.5

MODULE_CONFIG = {
    0: {'c1': 3, 'c2': 8, 'k': 2, 's': 2, 'p': 1},
}

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
        mobs = import_mobs('045b')
        card, graph = mobs

        module_config = graph.module_config

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(card, graph)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'test',
            skip_animations=False,
        )
        # ************************************************************
        # mobs = VGroup(
        #     UT_Conv(
        #         module_config=MODULE_CONFIG[0],
        #         opaque=True,
        #     ).scale(INIT_SCALE) for _ in range(5)
        # ).arrange(DOWN, buff=0.5)

        # self.play(AnimationGroup(
        #     *(mob.create(
        #         lag_ratio=0.5,
        #         run_time=wt,
        #     ) for mob in mobs),
        #     lag_ratio=0.5,
        #     run_time=wt*5,
        # ))
        # self.wait(wt)

        # cfg = {'c1': 8, 'c2': 8, 'shortcut': True, 'k': (3,3), 'e': 1.0}
        # mob = UT_Bottleneck(
        #     module_config=cfg,
        # ).scale(INIT_SCALE)
        # self.play(mob.create(
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        cfg = {'c1': 16, 'c2': 8, 'n': 3, 'shortcut': True, 'e': 0.5}
        mob = UT_C2f(
            module_config=cfg,
        ).scale(INIT_SCALE)
        self.play(mob.create(
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)
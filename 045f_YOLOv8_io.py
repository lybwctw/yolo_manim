# ************************************************************
# input and output shapes for YOLOv8n with 3 classes.
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

wt = 0.5
# TODO: show shape text into (n, h, w)
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('045e')
        (
            mm_modules, card, graph,
            mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        ) = mobs

        cam_args = {
            **VIEW_COMPUTE,
            'theta': -125*DEGREES,
            'focal_distance': 100,
            'zoom': 0.25,
        }
        self.set_camera_orientation(
            **cam_args,
        )
        self.add_fixed_in_frame_mobjects(card, graph)
        self.add(
            mm_modules, mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,640,640) -> (3,640,1280)',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mt_input.stretch_3d(
            new_shape=(3,640,1280),
            scale_factor=(1.0, 1.0, 3/2),
            run_time=wt*0.5,
        ))
        self.play(AnimationGroup(
            mt_22_box.stretch_3d(
                new_shape=(64,80,160),
                scale_factor=(1.0, 1.0, 3/2),
                run_time=wt*0.5,
            ),
            mt_22_cls.stretch_3d(
                new_shape=(3,80,160),
                scale_factor=(1.0, 1.0, 3/2),
                run_time=wt*0.5,
            ),
            mt_23_box.stretch_3d(
                new_shape=(64,40,80),
                scale_factor=(1.0, 1.0, 3/2),
                run_time=wt*0.5,
            ),
            mt_23_cls.stretch_3d(
                new_shape=(3,40,80),
                scale_factor=(1.0, 1.0, 3/2),
                run_time=wt*0.5,
            ),
            mt_24_box.stretch_3d(
                new_shape=(64,20,40),
                scale_factor=(1.0, 1.0, 3/2),
                run_time=wt*0.5,
            ),
            mt_24_cls.stretch_3d(
                new_shape=(3,20,40),
                scale_factor=(1.0, 1.0, 3/2),
                run_time=wt*0.5,
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,640,1280) -> (3,1280,1280)',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mt_input.stretch_3d(
            new_shape=(3,1280,1280),
            scale_factor=(1.0, 3/2, 1.0),
            run_time=wt*0.5,
        ))
        self.play(AnimationGroup(
            mt_22_box.stretch_3d(
                new_shape=(64,160,160),
                scale_factor=(1.0, 3/2, 1.0),
                run_time=wt*0.5,
            ),
            mt_22_cls.stretch_3d(
                new_shape=(64,160,160),
                scale_factor=(1.0, 3/2, 1.0),
                run_time=wt*0.5,
            ),
            mt_23_box.stretch_3d(
                new_shape=(64,80,80),
                scale_factor=(1.0, 3/2, 1.0),
                run_time=wt*0.5,
            ),
            mt_23_cls.stretch_3d(
                new_shape=(64,80,80),
                scale_factor=(1.0, 3/2, 1.0),
                run_time=wt*0.5,
            ),
            mt_24_box.stretch_3d(
                new_shape=(64,40,40),
                scale_factor=(1.0, 3/2, 1.0),
                run_time=wt*0.5,
            ),
            mt_24_cls.stretch_3d(
                new_shape=(3,40,40),
                scale_factor=(1.0, 3/2, 1.0),
                run_time=wt*0.5,
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,1280,1280) -> (3,640,640)',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mt_input.stretch_3d(
            new_shape=(3,640,640),
            scale_factor=(1.0, 2/3, 2/3),
            run_time=wt*0.5,
        ))
        self.play(AnimationGroup(
            mt_22_box.stretch_3d(
                new_shape=(64,80,80),
                scale_factor=(1.0, 2/3, 2/3),
                run_time=wt*0.5,
            ),
            mt_22_cls.stretch_3d(
                new_shape=(64,80,80),
                scale_factor=(1.0, 2/3, 2/3),
                run_time=wt*0.5,
            ),
            mt_23_box.stretch_3d(
                new_shape=(64,40,40),
                scale_factor=(1.0, 2/3, 2/3),
                run_time=wt*0.5,
            ),
            mt_23_cls.stretch_3d(
                new_shape=(64,40,40),
                scale_factor=(1.0, 2/3, 2/3),
                run_time=wt*0.5,
            ),
            mt_24_box.stretch_3d(
                new_shape=(64,20,20),
                scale_factor=(1.0, 2/3, 2/3),
                run_time=wt*0.5,
            ),
            mt_24_cls.stretch_3d(
                new_shape=(64,20,20),
                scale_factor=(1.0, 2/3, 2/3),
                run_time=wt*0.5,
            ),
        ))
        self.wait(wt)
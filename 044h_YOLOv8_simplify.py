# ************************************************************
# Simplified view on YOLOv8n with 3 classes.
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

SCALE_FACTOR = 0.25

UNIT_BUFF = 0.7

RUNNING_X = 6.0
FAKE_HALF = 2/3

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('045g')
        (
            mm_modules, card, graph,
            mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        ) = mobs
        mt_outputs = VGroup(
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )

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
        self.add(
            mm_modules, mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean cards and extra modules',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            Unwrite(graph, run_time=wt),
            Unwrite(card, run_time=wt),
            Unwrite(mm_modules[:-3], run_time=wt),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'arrange input, modules and output',
            skip_animations=True,
        )
        # ************************************************************
        mm_modules = mm_modules[-3:]

        mm_modules.generate_target()
        mm_modules.target.center()
        offset = mm_modules.target.get_center() - mm_modules.get_center()

        mt_outputs.generate_target()
        mt_outputs.target.shift(offset)

        mt_input.generate_target()
        mt_input.target.next_to(
            mm_modules.target,
            UP,
            buff=4.0,
        )

        self.play(AnimationGroup(
            MoveToTarget(mm_modules),
            MoveToTarget(mt_input),
            MoveToTarget(mt_outputs),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'new perspective and arrange again',
            skip_animations=False,
        )
        # ************************************************************
        mm_modules.generate_target()
        mm_modules.target.rotate(
            90*DEGREES,
            axis=OUT,
        ).center().scale(SCALE_FACTOR)

        mt_input.generate_target()
        mt_input.target.scale(SCALE_FACTOR).next_to(
            mm_modules.target,
            LEFT,
            buff=UNIT_BUFF,
        )

        mt_outputs.generate_target()
        mt_outputs.target.scale(SCALE_FACTOR).next_to(
            mm_modules.target,
            RIGHT,
            buff=UNIT_BUFF,
        )

        cam_args = {
            **VIEW_INTRO,
            'focal_distance': 20,
            'zoom': 1.0,
        }
        self.move_camera(
            **cam_args,
            added_anims=[
                AnimationGroup(
                    MoveToTarget(mm_modules),
                    MoveToTarget(mt_input),
                    MoveToTarget(mt_outputs),
                    lag_ratio=0.0,
                    run_time=wt,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # export
        mobs = VGroup(
            mt_input, mm_modules,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        export_mobs(__file__, mobs)     # used by next
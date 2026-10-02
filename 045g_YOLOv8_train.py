# ************************************************************
# Training intuition for YOLOv8.
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

def collect_ut_convs(mob):
    if isinstance(mob, UT_Conv):
        return [mob]
    if isinstance(mob, UT_Bottleneck):
        return [mob.ut_cv1, mob.ut_cv2]
    if isinstance(mob, UT_C2f):
        convs = [mob.ut_cv1]
        for bottleneck in mob.ut_m:
            convs.extend(collect_ut_convs(bottleneck))
        convs.append(mob.ut_cv2)
        return convs
    if isinstance(mob, UT_SPPF):
        return [mob.ut_cv1, mob.ut_cv2]
    if isinstance(mob, UT_Detect):
        return [
            mob.ut_b1,
            mob.ut_b2,
            mob.ut_b3,
            mob.ut_c1,
            mob.ut_c2,
            mob.ut_c3,
        ]
    raise TypeError(f'Unsupported module type: {type(mob).__name__}')

class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('045f')
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
            'backprop intuition',
            skip_animations=False,
        )
        # ************************************************************
        io_mobs = (
            mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        self.play(AnimationGroup(
            *(mob.tarnish(run_time=wt) for mob in io_mobs),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        conv_units = []
        for module in mm_modules:
            conv_units.extend(collect_ut_convs(module))
        conv_units.reverse()

        self.play(AnimationGroup(
            *(conv.translate_convs(run_time=wt) for conv in conv_units),
            lag_ratio=0.1,
            rate_func=rate_functions.ease_in_out_quad,
            run_time=wt*5,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            *(mob.lightup(run_time=wt) for mob in io_mobs),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            mm_modules, card, graph,
            mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        export_mobs(__file__, mobs)     # used by next
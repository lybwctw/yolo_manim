# ************************************************************
# Simpler compute loop for Conv. (skip SiLU animation)
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
from modules.pt_Conv2d import *
from modules.pt_BatchNorm2d import *

from ultralytics.nn.modules import Conv

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
#     'c1': 4,
#     'c2': 5,
#     'k': 3,
#     's': 2,
#     'p': 1,
# }

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
        (
            tc_i, mc, tc_o,
            mt_i, mm_conv, mm_bn, mt_o,
            mg,
        ) = import_mobs('040d')

        module_config = mg.module_config

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            tc_i, mc, tc_o, mg,
        )
        self.add(
            mt_i, mm_conv, mm_bn, mt_o,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'clean output',
            skip_animations=True,
        )
        # ************************************************************
        mt_o.save_state()
        self.play(AnimationGroup(
            mt_o.uncreate(
                style='whole',
                anim=Unwrite,
            ),
            tc_o.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        mt_o.restore()      # reuse later

        # remove shapes in graph?

        # ************************************************************
        self.next_section(
            'apply conv bn act together',
            skip_animations=True,
        )
        # ************************************************************
        # loop
        self.play(AnimationGroup(
            mm_conv.mt_weight.breath(
                style='whole',
                rate_func=smooth,           # sync with default
                lag_ratio=0.5,              # sync with default
                run_time=wt*3,
            ),
            AnimationGroup(
                *(AnimationGroup(
                    *(cube.breath() for cube in beam),
                    lag_ratio=0.0,
                ) for beam in mm_bn),
                rate_func=smooth,
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            mt_o.create(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))

        # expand summary
        self.play(tc_o.expand_summary(
            t2s(mt_o.array),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean job',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output and graph
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='whole',
                    anim=ShrinkToCenter,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [mt_i, mt_o],
                [tc_i, tc_o],
            )),
            Unwrite(mg),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # remove input/output cards
        self.play(AnimationGroup(
            detach_to_ref(tc_i, UP),
            detach_to_ref(tc_o, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(mc.shrink_params(
            run_time=wt,
        ))

        # expand module summary
        self.play(mc.expand_summary(
            '4 5 3 2 1',
            direction='right',
            run_time=wt,
        ))
        self.wait(wt)

        # remove module mob
        self.play(AnimationGroup(
            mm_conv.mt_weight.uncreate(
                style='whole',
                anim=ShrinkToCenter,
                lag_ratio=0.0,
                run_time=wt,
            ),
            AnimationGroup(
                *(AnimationGroup(
                    *(ShrinkToCenter(cube) for cube in beam),
                    lag_ratio=0.0,
                ) for beam in mm_bn),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        # self.wait(wt)

        # shrink module card
        self.play(mc.shrink_summary(
            run_time=wt,
        ))
        self.wait(wt)

        # export
        export_mobs(__file__, mc)     # NOTE: used by next
# ************************************************************
# Simplified view on SPPF.
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

from ultralytics.nn.modules import SPPF

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
    # 'c1': 16,
    # 'c2': 16,
    # 'k': 5,
# }

wt = SHORT_DURATION
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
            mm_cv1, mm_cv2,
            mts,
            mg,
        ) = import_mobs('042e')
        module_config = mg.module_config

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mm_cv1, mm_cv2, mts)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'ignore mid tensors',
            skip_animations=False,
        )
        # ************************************************************
        # lightup all tensors
        self.play(AnimationGroup(
            *(mt.lightup() for mt in mts),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # remove mid tensors
        self.play(AnimationGroup(
            *(mt.uncreate(ref='center') for mt in mts[1:-1]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'rearrange input/module/output',
            skip_animations=False,
        )
        # ************************************************************
        mobs = VGroup(mts[0], mm_cv1, mm_cv2, mts[-1])
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=TENSOR_VGAP_SMALL)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output and graph
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(ref='bottom'),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [mts[0], mts[-1]],
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
            '16 16',
            direction='right',
            run_time=wt,
        ))
        self.wait(wt)

        # shrink module card
        self.play(mc.shrink_summary(
            run_time=wt,
        ))
        # self.wait(wt)

        # remove module mob
        self.play(AnimationGroup(
            mm_cv1.uncreate(
                ref='center',
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_cv2.uncreate(
                ref='center',
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # export
        export_mobs(__file__, mc)     # NOTE: used by next, samples
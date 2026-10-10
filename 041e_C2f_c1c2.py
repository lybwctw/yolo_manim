# ************************************************************
# c1 and c2 for C2f.
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
    # 'c1': 8,
    # 'c2': 8,
    # 'n': 3,
    # 'shortcut': False,
    # 'e': 0.5,
# }


wt = 0.5

# TODO: make graph smaller??
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
        ) = import_mobs('042d')
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
            '[8 8] -> [16 8]',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c1': 16},
                run_time=wt,
            )
        )

        # update graph
        self.play(
            mg.mobs_card[0].update_summary(
                summary='16 8 1 1 1',
                run_time=wt,
            )
        )

        # update modules
        self.play(
            mm_cv1.stretch_3d(
                new_shape=(16,1,1),
                scale_factor=(2.0, 1.0, 1.0),
                run_time=wt,
            )
        )

        # update tensors
        self.play(
            mts[0].stretch_3d(
                new_shape=(16,5,6),
                scale_factor=(2.0, 1.0, 1.0),
                run_time=wt,
            )
        )

        # update tensor cards
        self.play(
            tc_i.update_summary(
                '(16,h,w)',
                run_time=wt,
            ),
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[16 8] -> [16 16]',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c2': 16},
                run_time=wt,
            )
        )

        # update graph
        self.play(AnimationGroup(
            mg.mobs_card[0].update_summary(
                summary='16 16 1 1 1',
                run_time=wt,
            ),
            mg.mobs_card[1].update_summary(
                summary='8 0',
                run_time=wt,
            ),
            mg.mobs_card[2].update_summary(
                summary='8 8 F',
                run_time=wt,
            ),
            mg.mobs_card[3].update_summary(
                summary='8 8 F',
                run_time=wt,
            ),
            mg.mobs_card[4].update_summary(
                summary='8 8 F',
                run_time=wt,
            ),
            mg.mobs_card[6].update_summary(
                summary='40 16 1 1 1',
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
        ))

        # update modules: stretch blocks
        self.play(AnimationGroup(
            mm_cv1.stretch_blocks(
                new_shape=(16,16,1,1),      # FIXME: not verified
                direction='out',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_m1.stretch_blocks(
                new_shape=(8,4,3,3),
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_m2.stretch_blocks(
                new_shape=(8,4,3,3),
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_m3.stretch_blocks(
                new_shape=(8,4,3,3),
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.stretch_blocks(
                new_shape=(16,20,1,1),
                direction='out',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        # self.wait(wt)

        # update modules: stretch 3d
        self.play(AnimationGroup(
            mm_m1.stretch_3d(
                new_shape=(8,8,3,3),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_m2.stretch_3d(
                new_shape=(8,8,3,3),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_m3.stretch_3d(
                new_shape=(8,8,3,3),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_cv2.stretch_3d(
                new_shape=(16,40,1,1),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # update tensors
        mts[2].generate_target()
        mts[2].target.stretch_to_fit_depth(mts[2].depth*2.0).align_to(mts[2],IN)
        mts[3].generate_target()
        mts[3].target.stretch_to_fit_depth(mts[3].depth*2.0).align_to(mts[3],OUT)
        self.play(AnimationGroup(
            mts[1].stretch_3d(
                new_shape=(16,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            MoveToTarget(mts[2], run_time=wt),
            MoveToTarget(mts[3], run_time=wt),
            mts[4].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[5].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[6].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[7].stretch_3d(
                new_shape=(40,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[8].stretch_3d(
                new_shape=(16,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # update tensor cards
        self.play(
            tc_o.update_summary(
                '(16,h,w)',
                run_time=wt,
            ),
        )
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
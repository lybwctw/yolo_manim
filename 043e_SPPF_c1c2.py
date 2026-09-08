# ************************************************************
# c1 and c2 for SPPF.
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
    # 'c1': 8,
    # 'c2': 8,
    # 'k': 5,
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
            mm_cv1, mm_cv2,
            mts,
            mg,
        ) = import_mobs('043d')
        module_config = mg.module_config

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.7)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mm_cv1, mm_cv2, mts)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[8 4 1 1] -> [16 8 1 1]',
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

        # update graph modules
        self.play(
            mg.mobs_card[0].update_summary(
                summary='16 8 1 1',
                run_time=wt,
            ),
            mg.mobs_card[5].update_summary(
                summary='32 8 1 1',
                run_time=wt,
            ),
        )

        # update modules: stretch blocks
        self.play(mm_cv1.stretch_blocks(
            new_shape=(16,8,1,1),
            direction='out',
            diff=2,
            ref='center',
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update modules: stretch 3d
        self.play(AnimationGroup(
            mm_cv1.stretch_3d(
                new_shape=(16,1,1),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_cv2.stretch_3d(
                new_shape=(32,1,1),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update tensors
        self.play(AnimationGroup(
            mts[0].stretch_3d(
                new_shape=(16,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[1].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[2].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[3].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[4].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[5].stretch_3d(
                new_shape=(32,5,6),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update graph shapes
        self.play(AnimationGroup(
            mg.update_shape(text='(16,h,w)', index=0),
            mg.update_shape(text='(8,h,w)', index=1),
            mg.update_shape(text='(8,h,w)', index=2),
            mg.update_shape(text='(8,h,w)', index=3),
            mg.update_shape(text='(8,h,w)', index=4),
            mg.update_shape(text='(32,h,w)', index=5),
            mg.update_shape(text='(8,h,w)', index=6),
            lag_ratio=0.5,
            run_time=wt*3,
        ))

        # update tensor cards
        self.play(tc_i.update_summary(
            summary='(16,h,w)',
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[16 8 1 1] -> [16 16 1 1]',
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

        # update graph modules
        self.play(mg.mobs_card[5].update_summary(
            summary='32 16 1 1',
            run_time=wt,
        ))

        # update modules: stretch blocks
        self.play(mm_cv2.stretch_blocks(
            new_shape=(16,16,1,1),
            direction='out',
            diff=4,
            ref='center',
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update tensors
        self.play(mts[6].stretch_3d(
            new_shape=(16,5,6),
            scale_factor=(2.0,1.0,1.0),
            run_time=wt,
        ))

        # update graph shapes
        self.play(mg.update_shape(
            text='(16,h,w)',
            index=6,
            run_time=wt,
        ))

        # update tensor cards
        self.play(tc_o.update_summary(
            summary='(16,h,w)',
            run_time=wt,
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
            mm_cv1, mm_cv2,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
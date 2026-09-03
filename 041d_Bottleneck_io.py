# ************************************************************
# Input/output for Bottleneck.
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

from ultralytics.nn.modules import Bottleneck

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
    # 'c1': 8,
    # 'c2': 8,
    # 'shortcut': False,
    # 'k': (3,3),
    # 'e': 0.5,
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
        # load cards, modules, tensors, graph
        (
            tc_i, mc, tc_o,
            mt_1, mm_cv1, mt_2, mm_cv2, mt_3,
            mg,
        ) = import_mobs('041c')
        module_config = mg.module_config

        # # raw modules
        # m_module = Bottleneck(**module_config)
        # m_cv1 = m_module.cv1
        # m_cv2 = m_module.cv2

        # for convenience
        mts = VGroup(mt_1, mt_2, mt_3)

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mts, mm_cv1, mm_cv2)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '856 -> 456 -> 856',
            skip_animations=True,
        )
        # ************************************************************
        # fade modules
        self.play(AnimationGroup(
            mm_cv1.tarnish(),
            mm_cv2.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '896 -> 496 -> 896',
            skip_animations=True,
        )
        # ************************************************************
        # tensors stretch
        self.play(AnimationGroup(
            mts[0].stretch_3d(
                new_shape=(8,9,6),
            ),
            mts[1].stretch_3d(
                new_shape=(4,9,6),
            ),
            mts[2].stretch_3d(
                new_shape=(8,9,6),
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # manual graph update
        self.play(AnimationGroup(
            mg.update_shape(
                text='(8,9,6)',
                index=0,
            ),
            mg.update_shape(
                text='(4,9,6)',
                index=1,
            ),
            mg.update_shape(
                text='(8,9,6)',
                index=2,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # manual cards update
        self.play(AnimationGroup(
            tc_i.update_summary(
                summary='(8,9,6)',
            ),
            tc_o.update_summary(
                summary='(8,9,6)',
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '8912 -> 4912 -> 8912',
            skip_animations=True,
        )
        # ************************************************************
        # tensors stretch
        self.play(AnimationGroup(
            mts[0].stretch_3d(
                new_shape=(8,9,12),
            ),
            mts[1].stretch_3d(
                new_shape=(4,9,12),
            ),
            mts[2].stretch_3d(
                new_shape=(8,9,12),
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # manual graph update
        self.play(AnimationGroup(
            mg.update_shape(
                text='(8,9,12)',
                index=0,
            ),
            mg.update_shape(
                text='(4,9,12)',
                index=1,
            ),
            mg.update_shape(
                text='(8,9,12)',
                index=2,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # manual cards update
        self.play(AnimationGroup(
            tc_i.update_summary(
                summary='(8,9,12)',
            ),
            tc_o.update_summary(
                summary='(8,9,12)',
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '856 -> 456 -> 856',
            skip_animations=False,
        )
        # ************************************************************
        # tensors stretch
        self.play(AnimationGroup(
            mts[0].stretch_3d(
                new_shape=(8,5,6),
            ),
            mts[1].stretch_3d(
                new_shape=(4,5,6),
            ),
            mts[2].stretch_3d(
                new_shape=(8,5,6),
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # manual graph update
        self.play(AnimationGroup(
            mg.update_shape(
                text='(8,5,6)',
                index=0,
            ),
            mg.update_shape(
                text='(4,5,6)',
                index=1,
            ),
            mg.update_shape(
                text='(8,5,6)',
                index=2,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # manual cards update
        self.play(AnimationGroup(
            tc_i.update_summary(
                summary='(8,5,6)',
            ),
            tc_o.update_summary(
                summary='(8,5,6)',
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # lightup modules
        self.play(AnimationGroup(
            mm_cv1.lightup(),
            mm_cv2.lightup(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean tensors',
            skip_animations=False,
        )
        # ************************************************************
        # fade tensors
        self.play(AnimationGroup(
            mts[0].tarnish(),
            mts[1].tarnish(),
            mts[2].tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # remove shapes in graph
        self.play(mg.hide_shapes(
            lag_ratio=0.5,
            run_time=wt,
        ))

        # shrink tensor cards
        self.play(AnimationGroup(
            *(card.shrink_summary() for card in [tc_i, tc_o]),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            tc_i, mc, tc_o,
            mts[0], mm_cv1, mts[1], mm_cv2, mts[2],
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
# ************************************************************
# cls series args for Detect.
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

# from ultralytics.nn.modules import Detect

# INIT_CONFIG = {
#     'ch': 8,
#     'c2': 4,
#     'c3': 4,
#     'reg_max': 4,      # 4 probs for each direction (16 by default)
#     'nc': 3,           # 3 classes
# }

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

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
            tc_i, mc, card_o1, card_o2,
            mm_bs, mm_cs,
            mts,
            mg,
        ) = import_mobs('044e')
        module_config = mg.module_config

        # for convenience
        mm_b1, mm_b2, mm_b3 = mm_bs
        mm_c1, mm_c2, mm_c3 = mm_cs
        series_box = VGroup(
            *mm_bs,
            *mts[1:13],
        )
        series_cls = VGroup(
            *mm_cs,
            *mts[13:],
        )

        # show initial mobs
        camera_config = {
            **VIEW_COMPUTE,
            'phi': 40*DEGREES,
            'zoom': 0.6,
            # 'frame_center': DOWN*1.5,
        }

        # FIXME: initial camera setup hack
        self.set_camera_orientation(**camera_config)
        self.add_fixed_in_frame_mobjects(tc_i, mc, card_o1, card_o2, mg)
        self.add(mts, mm_bs, mm_cs)
        self.wait(wt*0.1)
        self.set_camera_orientation(frame_center=DOWN*1.5)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'c3: 4 -> 8',
            skip_animations=True,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c3': 8},
                run_time=wt,
            )
        )

        # update graph modules
        # FIXME: width issue on update_summary
        # FIXME: start with scaled raw info_card?
        self.play(AnimationGroup(
            mg.cards_cls[0].update_summary(
                summary='16 8 3 1 1',
                run_time=wt,
            ),
            mg.cards_cls[1].update_summary(
                summary='8 8 3 1 1',
                run_time=wt,
            ),
            mg.cards_cls[2].update_summary(
                summary='8 3 1 1 0 T',
                run_time=wt,
            ),
        ))

        # update modules: stretch blocks
        self.play(AnimationGroup(
            mm_c1.stretch_blocks(
                new_shape=(8,16,3,3),
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_c2.stretch_blocks(
                new_shape=(8,4,3,3),
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        # self.wait(wt)

        # update modules: stretch 3d
        self.play(AnimationGroup(
            mm_c2.stretch_3d(
                new_shape=(8,3,3),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_c3.stretch_3d(
                new_shape=(8,1,1),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        # self.wait(wt)

        # update tensors
        self.play(AnimationGroup(
            mts[13].stretch_3d(
                new_shape=(8,7,9),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            mts[14].stretch_3d(
                new_shape=(8,7,9),
                scale_factor=(2.0,1.0,1.0),
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'nc: 3 -> 10(3+3+4)',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'nc': 10},
                run_time=wt,
            )
        )

        # update graph modules
        self.play(AnimationGroup(
            mg.cards_cls[2].update_summary(
                summary='8 10 1 1 0 T',
                run_time=wt,
            ),
        ))

        # update modules: stretch blocks
        self.play(
            mm_c3.stretch_blocks(
                new_shape=(10,8,1,1),
                direction='out',
                diff=(3,4),
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
        )

        # update tensors
        self.play(AnimationGroup(
            mts[15].stretch_3d(
                new_shape=(10,7,9),
                scale_factor=(10/3,1.0,1.0),
                run_time=wt,
            ),
            mts[16].stretch_3d(
                new_shape=(10,7,9),
                scale_factor=(10/3,1.0,1.0),
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        # self.wait(wt)

        # update tensor cards
        self.play(card_o2.update_summary(
            summary='(10,h,w)',
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back: c3->4, nc->3',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c3': 4, 'nc': 3},
                run_time=wt,
            ),
        )

        # update graph modules
        self.play(AnimationGroup(
            mg.cards_cls[0].update_summary(
                summary='16 4 3 1 1',
                run_time=wt,
            ),
            mg.cards_cls[1].update_summary(
                summary='4 4 3 1 1',
                run_time=wt,
            ),
            mg.cards_cls[2].update_summary(
                summary='4 3 1 1 0 T',
                run_time=wt,
            ),
        ))

        # update modules: stretch 3d
        self.play(AnimationGroup(
            mm_c2.stretch_3d(
                new_shape=(4,3,3),
                scale_factor=(0.5,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_c3.stretch_3d(
                new_shape=(4,1,1),
                scale_factor=(4/8,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        # self.wait(wt)

        # update modules: stretch blocks
        self.play(AnimationGroup(
            mm_c1.stretch_blocks(
                new_shape=(4,16,3,3),
                direction='in',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_c2.stretch_blocks(
                new_shape=(4,4,3,3),
                direction='in',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_c3.stretch_blocks(
                new_shape=(3,4,1,1),
                direction='in',
                diff=(3,4),
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        # self.wait(wt)

        # update tensors
        self.play(AnimationGroup(
            mts[13].stretch_3d(
                new_shape=(4,7,9),
                scale_factor=(0.5,1.0,1.0),
                run_time=wt,
            ),
            mts[14].stretch_3d(
                new_shape=(4,7,9),
                scale_factor=(0.5,1.0,1.0),
                run_time=wt,
            ),
            mts[15].stretch_3d(
                new_shape=(3,7,9),
                scale_factor=(3/10,1.0,1.0),
                run_time=wt,
            ),
            mts[16].stretch_3d(
                new_shape=(3,7,9),
                scale_factor=(3/10,1.0,1.0),
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # update tensor cards
        self.play(card_o2.update_summary(
            summary='(3,h,w)',
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            tc_i, mc, card_o1, card_o2,
            mm_bs, mm_cs,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
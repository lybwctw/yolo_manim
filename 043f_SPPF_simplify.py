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
            mm_cv1, mm_cv2,
            mts,
            mg,
        ) = import_mobs('043e')
        module_config = mg.module_config

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mm_cv1, mm_cv2, mts)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'get rid of mid tensors',
            skip_animations=True,
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
            '[16 16 5] -> [8 8 5]',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c1': 8, 'c2': 8},
                run_time=wt,
            )
        )

        # update graph modules
        self.play(
            mg.mobs_card[0].update_summary(
                summary='8 4 1 1',
                run_time=wt,
            ),
            mg.mobs_card[5].update_summary(
                summary='16 8 1 1',
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        )

        # update module: stretch blocks
        self.play(AnimationGroup(
            mm_cv1.stretch_blocks(
                new_shape=(4,8,1,1),
                direction='in',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.stretch_blocks(
                new_shape=(8,32,1,1),
                direction='in',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # update modules: stretch 3d
        self.play(AnimationGroup(
            mm_cv1.stretch_3d(
                new_shape=(8,1,1),
                scale_factor=(0.5,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_cv2.stretch_3d(
                new_shape=(16,1,1),
                scale_factor=(0.5,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update tensors
        self.play(AnimationGroup(
            mts[0].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(0.5,1.0,1.0),
                run_time=wt,
            ),
            mts[-1].stretch_3d(
                new_shape=(8,5,6),
                scale_factor=(0.5,1.0,1.0),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update graph shapes
        self.play(AnimationGroup(
            mg.update_shape(text='(8,h,w)', index=0),
            mg.update_shape(text='(4,h,w)', index=1),
            mg.update_shape(text='(4,h,w)', index=2),
            mg.update_shape(text='(4,h,w)', index=3),
            mg.update_shape(text='(4,h,w)', index=4),
            mg.update_shape(text='(16,h,w)', index=5),
            mg.update_shape(text='(8,h,w)', index=6),
            lag_ratio=0.5,
            run_time=wt*3,
        ))

        # update tensor cards
        self.play(AnimationGroup(
            tc_i.update_summary(
                summary='(8,h,w)',
                run_time=wt,
            ),
            tc_o.update_summary(
                summary='(8,h,w)',
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean everything',
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
            '8 8',
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
# ************************************************************
# Simplified view on C2f.
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

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0


# INIT_CONFIG = {
    # 'c1': 16,
    # 'c2': 16,
    # 'n': 1,
    # 'shortcut': True,
    # 'e': 0.25,
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
            mm_cv1, mm_m, mm_cv2,
            mts,
            mg,
        ) = import_mobs('042h')
        module_config = mg.module_config

        # for convenience
        mm_m1 = mm_m[0]

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.9)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mm_m, mm_cv1, mm_cv2, mts)
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
        # FIXME: occlusion issue between mm_cv2 and input
        # FIXME: due to stretch blocks z_index setup
        mts[-2].set_z_index(0)
        self.play(AnimationGroup(
            *(mt.uncreate(ref='center') for mt in mts[1:-1]),
            # *(FadeOut(mt) for mt in mts[1:-1]),
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
        mobs = VGroup(mts[0], mm_cv1, mm_m, mm_cv2, mts[-1])
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=TENSOR_VGAP_SMALL)
        self.move_camera(
            zoom=1.0,
            added_anims=[
                MoveToTarget(mobs, run_time=wt),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'e: 0.25 -> 0.5 (default)',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'e': 0.5},
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
                summary='8 8 T',
                run_time=wt,
            ),
            mg.mobs_card[4].update_summary(
                summary='24 16 1 1 1',
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # update modules: stretch blocks
        self.play(AnimationGroup(
            mm_cv1.stretch_blocks(
                new_shape=(16,16,1,1),
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
            lag_ratio=0.5,
            run_time=wt*3,
        ))

        # update modules: stretch blocks
        self.play(AnimationGroup(
            mm_m1.stretch_3d(
                new_shape=(8,8,3,3),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_cv2.stretch_3d(
                new_shape=(16,24,1,1),
                scale_factor=(2.0,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt*3,
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
        # FIXME: end with e=0.5?
        self.play(mc.expand_summary(
            '16 16 1 T',
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
            mm_m1.uncreate(
                ref='center',
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # export
        export_mobs(__file__, mc)     # NOTE: used by next, samples
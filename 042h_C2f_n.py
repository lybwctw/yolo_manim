# ************************************************************
# n for C2f.
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
    # 'c1': 16,
    # 'c2': 16,
    # 'n': 3,
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
        ) = import_mobs('042g')
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
            'n: 3 -> 2',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'n': 2},
                run_time=wt,
            )
        )

        # update graph
        self.play(mg.pop_bottleneck(
            run_time=wt*2,
        ))
        self.play(mg.animate(
            run_time=wt,
        ).set_y(0.0))
        self.play(mg.mobs_card[5].update_summary(
            summary='16 16 1 1 1',
            run_time=wt,
        ))
        # self.wait(wt)

        # update modules: remove mm_m3 and mts[6]
        mt_pop = mts[6]
        self.play(AnimationGroup(
            mm_m3.uncreate(ref='center', run_time=wt),
            mt_pop.uncreate(ref='center', run_time=wt),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        mm_m.remove(mm_m3)
        mts.remove(mt_pop)

        # update modules: stretch mm_cv2
        self.play(
            mm_cv2.stretch_3d(
                new_shape=(16,16,1,1),
                scale_factor=(16/20,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            )
        )

        # update tensors
        self.play(
            mts[6].stretch_3d(
                new_shape=(16,5,6),
                scale_factor=(16/20,1.0,1.0),
                run_time=wt,
            )
        )

        # rearrange
        vg1 = VGroup(mts[0], mm_cv1, mts[1], mts[2], mts[3], mm_m1, mts[4], mm_m2, mts[5])
        vg2 = VGroup(mts[6], mm_cv2, mts[7])
        vg1_z, vg2_z = vg1.get_z(), vg2.get_z()
        mobs = VGroup(vg1, vg2)
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=TENSOR_VGAP_SMALL)
        mobs.target.shift(UP*1.2)       # NOTE: shifted center in 042c
        mobs.target[0].set_z(vg1_z)
        mobs.target[1].set_z(vg2_z)
        self.move_camera(
            zoom=0.8,
            added_anims=[
                MoveToTarget(
                    mobs,
                    run_time=wt,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'n: 2 -> 1',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'n': 1},
                run_time=wt,
            )
        )

        # update graph
        self.play(mg.pop_bottleneck(
            run_time=wt*2,
        ))
        self.play(mg.animate(
            run_time=wt,
        ).set_y(0.0))
        self.play(mg.mobs_card[4].update_summary(
            summary='12 16 1 1 1',
            run_time=wt,
        ))
        # self.wait(wt)

        # update modules: remove mm_m2 and mts[5]
        mt_pop = mts[5]
        self.play(AnimationGroup(
            mm_m2.uncreate(ref='center', run_time=wt),
            mt_pop.uncreate(ref='center', run_time=wt),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        mm_m.remove(mm_m2)
        mts.remove(mt_pop)

        # update modules: stretch mm_cv2
        self.play(
            mm_cv2.stretch_3d(
                new_shape=(12,16,1,1),
                scale_factor=(12/16,1.0,1.0),
                lag_ratio=0.0,
                run_time=wt,
            )
        )

        # update tensors
        self.play(
            mts[5].stretch_3d(
                new_shape=(12,5,6),
                scale_factor=(12/16,1.0,1.0),
                run_time=wt,
            )
        )

        # rearrange
        vg1 = VGroup(mts[0], mm_cv1, mts[1], mts[2], mts[3], mm_m1, mts[4])
        vg2 = VGroup(mts[5], mm_cv2, mts[6])
        vg1_z, vg2_z = vg1.get_z(), vg2.get_z()
        mobs = VGroup(vg1, vg2)
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=TENSOR_VGAP_SMALL)
        mobs.target.shift(UP*0.5)       # NOTE: shifted center in 042c
        mobs.target[0].set_z(vg1_z)
        mobs.target[1].set_z(vg2_z)
        self.move_camera(
            zoom=0.9,                   # NOTE: final zoom
            added_anims=[
                MoveToTarget(
                    mobs,
                    run_time=wt,
                ),
            ],
            run_time=wt,
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
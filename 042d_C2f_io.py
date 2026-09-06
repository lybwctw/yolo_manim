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

from ultralytics.nn.modules import C2f

TENSOR_VGAP_SMALL = 0.5
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

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
        ) = import_mobs('042c')
        module_config = mg.module_config

        # for convenience
        mm_m1, mm_m2, mm_m3 = mm_m

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.7)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mts, mm_cv1, mm_m, mm_cv2)
        self.wait(wt)

        # self.begin_ambient_camera_rotation(
        #     rate=0.02,
        # )
        # self.wait(10.0)         # slow rotation and talking....
        # self.stop_ambient_camera_rotation()

        # self.move_camera(
        #     **VIEW_COMPUTE,
        #     run_time=wt,
        # )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on tensors',
            skip_animations=False,
        )
        # ************************************************************
        # fade all sub modules
        self.play(AnimationGroup(
            mm_cv1.tarnish(),
            mm_m1.tarnish(),
            mm_m2.tarnish(),
            mm_m3.tarnish(),
            mm_cv2.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(c,5,6) -> (c,6,9)',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            AnimationGroup(
                *(mt.stretch_3d(
                    new_shape=mt.shape[:1]+(6,9),
                    scale_factor=[
                        1.0, 6/5, 9/6,
                    ],
                ) for mt in mts),
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            AnimationGroup(
                mg.update_shape(text='(8,6,9)', index=0),
                mg.update_shape(text='(8,6,9)', index=1),
                mg.update_shape(text='(4,6,9)', index=8, direction=UP, buff=0.03),
                mg.update_shape(text='(4,6,9)', index=2),
                mg.update_shape(text='(4,6,9)', index=3),
                mg.update_shape(text='(4,6,9)', index=4),
                mg.update_shape(text='(4,6,9)', index=5),
                mg.update_shape(text='(20,6,9)', index=6),
                mg.update_shape(text='(8,6,9)', index=7),
                lag_ratio=0.5,
                run_time=wt*3,
            ),
        ))
        self.play(AnimationGroup(
            tc_i.update_summary(summary='(8,6,9)'),
            tc_o.update_summary(summary='(8,6,9)'),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back: (c,6,9) -> (c,5,6)',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            AnimationGroup(
                *(mt.stretch_3d(
                    new_shape=mt.shape[:1]+(5,6),
                    scale_factor=[
                        1.0, 5/6, 6/9,
                    ],
                ) for mt in mts),
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            AnimationGroup(
                mg.update_shape(text='(8,5,6)', index=0),
                mg.update_shape(text='(8,5,6)', index=1),
                mg.update_shape(text='(4,5,6)', index=8, direction=UP, buff=0.03),
                mg.update_shape(text='(4,5,6)', index=2),
                mg.update_shape(text='(4,5,6)', index=3),
                mg.update_shape(text='(4,5,6)', index=4),
                mg.update_shape(text='(4,5,6)', index=5),
                mg.update_shape(text='(20,5,6)', index=6),
                mg.update_shape(text='(8,5,6)', index=7),
                lag_ratio=0.5,
                run_time=wt*3,
            ),
        ))
        self.play(AnimationGroup(
            tc_i.update_summary(summary='(8,5,6)'),
            tc_o.update_summary(summary='(8,5,6)'),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'fade tensors, focus on modules',
            skip_animations=False,
        )
        # ************************************************************
        # fade tensors
        self.play(AnimationGroup(
            *(mt.tarnish() for mt in mts),
            *(mm.lightup() for mm in [
                mm_cv1, mm_m1, mm_m2, mm_m3, mm_cv2,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # remove shapes in graph
        self.play(mg.hide_shapes(
            lag_ratio=0.0,
            run_time=wt,
        ))

        # use general tensor cards
        self.play(AnimationGroup(
            tc_i.update_summary('(8,h,w)'),
            tc_o.update_summary('(8,h,w)'),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # export
        mobs = VGroup(
            tc_i, mc, tc_o,
            mm_cv1, mm_m, mm_cv2,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
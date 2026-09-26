# ************************************************************
# Visualize fake modules for YOLOv8n.
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

from modules.ut_Conv import UT_Conv
from modules.ut_Bottleneck import UT_Bottleneck
from modules.ut_C2f import UT_C2f
from modules.ut_SPPF import UT_SPPF
from modules.ut_Detect import UT_Detect

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

INIT_SCALE = 0.5

MODULE_MAP = {
    'Conv': UT_Conv,
    'C2f': UT_C2f,
    'SPPF': UT_SPPF,
    'Detect': UT_Detect,
}

FAKE_MAP = {
    # 3: 3,
    # 16: 4,
    # 32: 4,
    # 64: 4,
    # 128: 4,
    # 192: 4,
    # 256: 4,
    # 384: 4,
    3: 3,
    16: 8,
    32: 12,
    64: 16,
    128: 20,
    192: 22,
    256: 24,
    384: 26,
}

MODULE_CONFIG = {
    0:  ['Conv', {'c1': 3, 'c2': 16, 'k': 3, 's': 2, 'p': 1}],
    1:  ['Conv', {'c1': 16, 'c2': 32, 'k': 3, 's': 2, 'p': 1 }],
    2:  ['C2f', {'c1': 32, 'c2': 32, 'n': 1, 'shortcut': True}],
    3:  ['Conv', {'c1': 32, 'c2': 64, 'k': 3, 's': 2, 'p': 1 }],
    4:  ['C2f', {'c1': 64, 'c2': 64, 'n': 2, 'shortcut': True}],
    5:  ['Conv', {'c1': 64, 'c2': 128, 'k': 3, 's': 2, 'p': 1 }],
    6:  ['C2f', {'c1': 128, 'c2': 128, 'n': 2, 'shortcut': True}],
    7:  ['Conv', {'c1': 128, 'c2': 256, 'k': 3, 's': 2, 'p': 1 }],
    8:  ['C2f', {'c1': 256, 'c2': 256, 'n': 1, 'shortcut': True}],
    9:  ['SPPF', {'c1': 256, 'c2': 256}],
    10: ['Upsample', {'scale_factor': 2}],
    11: ['concat', {'dim': 0}],
    12: ['C2f', {'c1': 384, 'c2': 128, 'n': 1, 'shortcut': False}],
    13: ['Upsample', {'scale_factor': 2}],
    14: ['concat', {'dim': 0}],
    15: ['C2f', {'c1': 192, 'c2': 64, 'n': 1, 'shortcut': False}],
    16: ['Conv', {'c1': 64, 'c2': 64, 'k': 3, 's': 2, 'p': 1 }],
    17: ['concat', {'dim': 0}],
    18: ['C2f', {'c1': 192, 'c2': 128, 'n': 1, 'shortcut': False}],
    19: ['Conv', {'c1': 128, 'c2': 128, 'k': 3, 's': 2, 'p': 1 }],
    20: ['concat', {'dim': 0}],
    21: ['C2f', {'c1': 384, 'c2': 256, 'n': 1, 'shortcut': False}],
    22: ['Detect', {'ch': 64, 'c2': 64, 'c3': 64, 'reg_max': 16, 'nc': 3}],
    23: ['Detect', {'ch': 128, 'c2': 64, 'c3': 64, 'reg_max': 16, 'nc': 3}],
    24: ['Detect', {'ch': 256, 'c2': 64, 'c3': 64, 'reg_max': 16, 'nc': 3}],
}

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
        mobs = import_mobs('045b')
        card, graph = mobs

        module_config = graph.module_config

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(card, graph)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show fake modules',
            skip_animations=True,
        )
        # ************************************************************
        # init visible modules
        mm_modules = VGroup()
        for idx, (name, args) in MODULE_CONFIG.items():
            if name not in MODULE_MAP:
                continue

            # apply fake values to genuine args
            for k in args:
                if k in ('c1', 'c2', 'c3', 'ch', 'reg_max'):
                    args[k] = FAKE_MAP[args[k]]

            # create manim module
            if MODULE_MAP[name] is UT_Conv:
                mm_module = UT_Conv(
                    module_config=args,
                    opaque=True,
                ).scale(INIT_SCALE)
            else:
                mm_module = MODULE_MAP[name](
                    module_config=args,
                ).scale(INIT_SCALE)

            mm_modules.add(mm_module)
        mm_modules.arrange(DOWN, buff=0.3)

        # positions
        fc_start = mm_modules[0].get_top() + DOWN * 2
        fc_end = mm_modules[-1].get_bottom() + UP * 5
        ls_offset = LEFT*7 + DOWN*9 + OUT*10
        ls_start = fc_start + ls_offset
        ls_end = fc_end + ls_offset
        light_source = self.camera.light_source        # (-7,-9,10) by default

        # init lightsource and camera
        light_source.move_to(ls_start)
        self.set_camera_orientation(
            frame_center=fc_start,
        )

        # modules generation
        self.move_camera(
            added_anims=[
                AnimationGroup(
                    *(mm_module.create_convs(
                        lag_ratio=0.5,
                        run_time=wt,
                    ) for mm_module in mm_modules),
                    lag_ratio=1.0,
                    run_time=wt*10,
                    # run_time=wt*1,
                    rate_func=smooth,
                ),
                light_source.animate(
                    run_time=wt*10,
                    # run_time=wt*1,
                ).move_to(ls_end),
            ],
            frame_center=fc_end,
            run_time=wt*10,
            # run_time=wt*1,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'new perspective',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            added_anims=[
                # mm_modules.animate(
                #     run_time=wt*2,
                # ).scale(0.3),
                light_source.animate(
                    run_time=wt*2,
                ).move_to(ls_offset),
            ],
            frame_center=ORIGIN,
            # phi=60*DEGREES,
            # theta=-75*DEGREES,
            focal_distance=100,     # TODO: change back later
            zoom=0.35,               # TODO: chnage back later
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'connect module cards',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME: need shorter root line
        self.play(graph.connect(
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)
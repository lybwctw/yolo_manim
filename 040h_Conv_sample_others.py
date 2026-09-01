# ************************************************************
# Visualize other Conv samples from yolov8 series (3 classes).
# ************************************************************
from manim import *
import csv
from pathlib import Path

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
from modules.pt_Conv2d import *
from modules.pt_BatchNorm2d import *
from modules.ut_Conv import *

from ultralytics.nn.modules import Conv

SIDE_LENGTH_MINI = 0.2

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
        # load sample cards
        cards, ut_conv = import_mobs('040g')

        # show initial reference card
        self.set_camera_orientation(
            **VIEW_COMPUTE,
            zoom=1.0,
            focal_distance=80,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.add(ut_conv)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[3 16 3 2 1] -> [3 32 3 2 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[1] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # visualize new Conv
        self.move_camera(
            zoom=0.55,
            theta=-152*DEGREES,
            focal_distance=90,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=8,
                    direction='bottom',
                    shape=(32,3,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[3 32 3 2 1] -> [3 48 3 2 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[2] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 48
        self.move_camera(
            zoom=0.40,
            theta=-150*DEGREES,
            focal_distance=100,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=8,
                    direction='bottom',
                    shape=(48,3,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[3 48 3 2 1] -> [3 64 3 2 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[3] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 64
        self.move_camera(
            zoom=0.30,
            theta=-146*DEGREES,
            focal_distance=110,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=8,
                    direction='bottom',
                    shape=(64,3,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[3 64 3 2 1] -> [3 80 3 2 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[4] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 80
        self.move_camera(
            zoom=0.25,
            theta=-142*DEGREES,
            focal_distance=120,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=8,
                    direction='bottom',
                    shape=(80,3,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[3 80 3 2 1] -> [16 16 3 1 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[5] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 16
        self.move_camera(
            zoom=1.0,           # back
            focal_distance=80,  # back
            **VIEW_COMPUTE,     # back
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=-32,
                    direction='bottom',
                    shape=(16,3,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # stretch erect to 16
        self.move_camera(
            zoom=0.8,
            **VIEW_COMPUTE,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='erect',
                    size_scale=16/3,
                    shape=(16,16,3,3),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[16 16 3 1 1] -> [16 32 3 2 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[6] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 32
        self.move_camera(
            zoom=0.53,
            theta=-150*DEGREES,
            focal_distance=90,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=8,
                    direction='bottom',
                    shape=(32,16,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[16 32 3 2 1] -> [32 32 1 1 0]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[7] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch horizontal to 1x1
        self.move_camera(
            # zoom=0.45,
            # theta=-145*DEGREES,
            # focal_distance=100,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='horizontal',
                    size_scale=1/3,
                    shape=(32,16,1,1),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # stretch erect to 32
        self.move_camera(
            zoom=0.45,
            theta=-145*DEGREES,
            focal_distance=100,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='erect',
                    size_scale=2.0,
                    shape=(32,32,1,1),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[32 32 1 1 0] -> [32 32 3 1 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[8] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch horizontal to 3x3
        self.move_camera(
            zoom=0.45,
            theta=-145*DEGREES,
            focal_distance=100,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='horizontal',
                    size_scale=3.0,
                    shape=(32,32,3,3),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[32 32 3 1 1] -> [32 64 3 2 1]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[9] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 64
        self.move_camera(
            zoom=0.25,
            theta=-145*DEGREES,
            focal_distance=110,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=16,
                    direction='bottom',
                    shape=(64,32,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[32 64 3 2 1] -> [48 32 1 1 0]',
            skip_animations=True,
        )
        # ************************************************************
        # highlight new card
        mask = np.zeros(len(cards), dtype=bool)
        mask[10] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch blocks to 32
        self.move_camera(
            zoom=0.45,
            theta=-145*DEGREES,
            focal_distance=100,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=-16,
                    direction='bottom',
                    shape=(32,32,3,3),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # stretch horizontal to 1x1
        self.move_camera(
            # zoom=0.45,
            # theta=-145*DEGREES,
            # focal_distance=100,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='horizontal',
                    size_scale=1/3,
                    shape=(32,32,1,1),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # stretch erect to 48
        self.move_camera(
            zoom=0.43,
            theta=-145*DEGREES,
            focal_distance=100,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='erect',
                    size_scale=48/32,
                    shape=(48,32,1,1),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'final test',
            skip_animations=False,
        )
        # ************************************************************
        # highlight all cards
        mask = np.ones(len(cards), dtype=bool)
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        # self.wait(wt)

        # stretch erect to 8
        self.move_camera(
            zoom=0.43,
            theta=-145*DEGREES,
            focal_distance=100,
            added_anims=[
                ut_conv.stretch_direction(
                    direction='erect',
                    size_scale=8/48,
                    shape=(32,8,1,1),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # stretch blocks to 8
        self.move_camera(
            zoom=1.0,
            focal_distance=80,
            **VIEW_COMPUTE,
            added_anims=[
                ut_conv.stretch_blocks(
                    diff=-12,
                    direction='bottom',
                    shape=(8,8,1,1),
                    lag_ratio=0.5,
                ),
            ],
            run_time=wt*2,
        )
        # self.wait(wt)

        # stretch horizontal to 3x3
        self.play(ut_conv.stretch_direction(
            direction='horizontal',
            size_scale=3.0,
            shape=(32,32,3,3),
            lag_ratio=0.0,
            run_time=wt*2,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        # remove module
        self.play(ut_conv.uncreate(
            direction='center',
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        export_mobs(__file__, cards)        # NOTE: used by next
# ************************************************************
# C2f samples from yolov8 series for 3 classes.
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

from ultralytics.nn.modules import Conv

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

wt = 0.5

SCALE_FACTOR = 1.0

with open(Path(__file__).with_name('.csv'), newline='') as csv_file:
    args = [
        # f"{row['c1']} {row['c2']} {row['shortcut']} {row['k']} {row['e']}"
        f"{row['c1']} {row['c2']} {row['shortcut'][0]}"
        for row in csv.DictReader(csv_file)
    ]

class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # # load card and graph
        # card_ref = import_mobs('041g')
        # cards = VGroup(card_ref.copy() for _ in range(21))

        # # show initial reference card
        # self.set_camera_orientation(
        #     **VIEW_COMPUTE,
        # )
        # self.add_fixed_in_frame_mobjects(cards[0])
        # self.wait(wt)


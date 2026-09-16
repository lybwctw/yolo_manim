from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

from utils.mgraph import *

# ------------- info card ---------------------
# 'nc': 3,          # by default
# 'scale': UNKNOWN, # model size
# ---------------------------------------------

LINE_BUFF = 0.5             # connection node to edge distance
LINE_GAP = 0.22              # gap between input/output lines for softmax

CARD_BUFF_V_SMALL = 0.08
CARD_BUFF_H_SMALL = 0.5
CARD_BUFF_H_MEDIUM = 1.0

CURVE_BUFF_SMALL = 0.25
CURVE_BUFF_MEDIUM = 0.5

LAYER_COLORS = {
    'Conv': PURE_BLUE,
    'C2f': PURE_BLUE,
    'SPPF': PURE_BLUE,
    'Upsample': ORANGE,
    'concat': TEAL,
    'Detect': PURE_BLUE,
}

def create_curve(
    p1,
    p2,
    buff: float = CURVE_BUFF_SMALL,
) -> VMobject:
    pm_x = min(p1[0], p2[0]) - buff
    pm_seg = (p1[1] - p2[1]) / 5
    pm_y1 = p1[1] - pm_seg
    pm_y2 = p2[1] + pm_seg

    # pm_y = (p1[1]+p2[1]) / 2
    # pm = (pm_x, pm_y, 0.0)
    # curve = VMobject(**LINE_CONFIG_THIN).set_points_smoothly(
    #     [p1, pm, p2]
    # )

    pm1 = (pm_x, pm_y1, 0.0)
    pm2 = (pm_x, pm_y2, 0.0)
    curve = VMobject(**LINE_CONFIG_THIN).set_points_smoothly(
        [p1, pm1, pm2, p2]
    )
    return curve

LAYER_ARGS = {
    'n': {
        0:  ['Conv', '3 16 3 2 1'],
        1:  ['Conv', '16 32 3 2 1'],
        2:  ['C2f', '32 32 1 T'],
        3:  ['Conv', '32 64 3 2 1'],
        4:  ['C2f', '64 64 2 T'],
        5:  ['Conv', '64 128 3 2 1'],
        6:  ['C2f', '128 128 2 T'],
        7:  ['Conv', '128 256 3 2 1'],
        8:  ['C2f', '256 256 1 T'],
        9:  ['SPPF', '256 256'],
        10: ['Upsample', '2'],
        11: ['concat', '0'],
        12: ['C2f', '384 128 1 F'],
        13: ['Upsample', '2'],
        14: ['concat', '0'],
        15: ['C2f', '192 64 1 F'],
        16: ['Conv', '64 64 3 2 1'],
        17: ['concat', '0'],
        18: ['C2f', '192 128 1 F'],
        19: ['Conv', '128 128 3 2 1'],
        20: ['concat', '0'],
        21: ['C2f', '384 256 1 F'],
        22: ['Detect', '64 64 64 16 3'],
        23: ['Detect', '128 64 64 16 3'],
        24: ['Detect', '256 64 64 16 3'],
    },
    's': {
        0:  ['Conv', '3 32 3 2 1'],
        1:  ['Conv', '32 64 3 2 1'],
        2:  ['C2f', '64 64 1 T'],
        3:  ['Conv', '64 128 3 2 1'],
        4:  ['C2f', '128 128 2 T'],
        5:  ['Conv', '128 256 3 2 1'],
        6:  ['C2f', '256 256 2 T'],
        7:  ['Conv', '256 512 3 2 1'],
        8:  ['C2f', '512 512 1 T'],
        9:  ['SPPF', '512 512'],
        10: ['Upsample', '2'],
        11: ['concat', '0'],
        12: ['C2f', '768 256 1 F'],
        13: ['Upsample', '2'],
        14: ['concat', '0'],
        15: ['C2f', '384 128 1 F'],
        16: ['Conv', '128 128 3 2 1'],
        17: ['concat', '0'],
        18: ['C2f', '384 256 1 F'],
        19: ['Conv', '256 256 3 2 1'],
        20: ['concat', '0'],
        21: ['C2f', '768 512 1 F'],
        22: ['Detect', '128 64 128 16 3'],
        23: ['Detect', '256 64 128 16 3'],
        24: ['Detect', '512 64 128 16 3'],
    },
    'm': {
        0:  ['Conv', '3 48 3 2 1'],
        1:  ['Conv', '48 96 3 2 1'],
        2:  ['C2f', '96 96 2 T'],
        3:  ['Conv', '96 192 3 2 1'],
        4:  ['C2f', '192 192 4 T'],
        5:  ['Conv', '192 384 3 2 1'],
        6:  ['C2f', '384 384 4 T'],
        7:  ['Conv', '384 576 3 2 1'],
        8:  ['C2f', '576 576 2 T'],
        9:  ['SPPF', '576 576'],
        10: ['Upsample', '2'],
        11: ['concat', '0'],
        12: ['C2f', '960 384 2 F'],
        13: ['Upsample', '2'],
        14: ['concat', '0'],
        15: ['C2f', '576 192 2 F'],
        16: ['Conv', '192 192 3 2 1'],
        17: ['concat', '0'],
        18: ['C2f', '576 384 2 F'],
        19: ['Conv', '384 384 3 2 1'],
        20: ['concat', '0'],
        21: ['C2f', '960 576 2 F'],
        22: ['Detect', '192 64 192 16 3'],
        23: ['Detect', '384 64 192 16 3'],
        24: ['Detect', '576 64 192 16 3'],
    },
    'l': {
        0:  ['Conv', '3 64 3 2 1'],
        1:  ['Conv', '64 128 3 2 1'],
        2:  ['C2f', '128 128 3 T'],
        3:  ['Conv', '128 256 3 2 1'],
        4:  ['C2f', '256 256 6 T'],
        5:  ['Conv', '256 512 3 2 1'],
        6:  ['C2f', '512 512 6 T'],
        7:  ['Conv', '512 512 3 2 1'],
        8:  ['C2f', '512 512 3 T'],
        9:  ['SPPF', '512 512'],
        10: ['Upsample', '2'],
        11: ['concat', '0'],
        12: ['C2f', '1024 512 3 F'],
        13: ['Upsample', '2'],
        14: ['concat', '0'],
        15: ['C2f', '768 256 3 F'],
        16: ['Conv', '256 256 3 2 1'],
        17: ['concat', '0'],
        18: ['C2f', '768 512 3 F'],
        19: ['Conv', '512 512 3 2 1'],
        20: ['concat', '0'],
        21: ['C2f', '1024 512 3 F'],
        22: ['Detect', '256 64 256 16 3'],
        23: ['Detect', '512 64 256 16 3'],
        24: ['Detect', '512 64 256 16 3'],
    },
    'x': {
        0:  ['Conv', '3 80 3 2 1'],
        1:  ['Conv', '80 160 3 2 1'],
        2:  ['C2f', '160 160 3 T'],
        3:  ['Conv', '160 320 3 2 1'],
        4:  ['C2f', '320 320 6 T'],
        5:  ['Conv', '320 640 3 2 1'],
        6:  ['C2f', '640 640 6 T'],
        7:  ['Conv', '640 640 3 2 1'],
        8:  ['C2f', '640 640 3 T'],
        9:  ['SPPF', '640 640'],
        10: ['Upsample', '2'],
        11: ['concat', '0'],
        12: ['C2f', '1280 640 3 F'],
        13: ['Upsample', '2'],
        14: ['concat', '0'],
        15: ['C2f', '960 320 3 F'],
        16: ['Conv', '320 320 3 2 1'],
        17: ['concat', '0'],
        18: ['C2f', '960 640 3 F'],
        19: ['Conv', '640 640 3 2 1'],
        20: ['concat', '0'],
        21: ['C2f', '1280 640 3 F'],
        22: ['Detect', '320 80 320 16 3'],
        23: ['Detect', '640 80 320 16 3'],
        24: ['Detect', '640 80 320 16 3'],
    },
}

class UT_YOLOv8(VMobject):
    pass

class MGraph_YOLOv8(MGraph):
    def __init__(
        self,
        module_config: dict = {},
    ):
        super().__init__(module_config)
        self.mode = 'linear'

    # def create(
    #     self,
    #     **aargs,
    # ) -> Animation:
        # pass

    def create_cards(
        self,
    ) -> tuple:
        objs = []

        scale = self.module_config['scale']

        args = LAYER_ARGS[scale]
        for idx in args:
            card = InfoCard(
                args[idx][0],
                summary=args[idx][1],
                frame_config={
                    'fill_color': LAYER_COLORS[args[idx][0]],
                },
            ).scale(0.8)    # smaller than normal
            objs.append(card)

        mobs = VGroup(*objs).arrange(
            DOWN,
            buff=CARD_BUFF_V_SMALL,
        )

        # reposition 3 Detect
        mobs[-3].next_to(mobs[15], RIGHT, buff=CARD_BUFF_H_SMALL)
        mobs[-2].next_to(mobs[18], RIGHT, buff=CARD_BUFF_H_SMALL)
        mobs[-1].next_to(mobs[21], RIGHT, buff=CARD_BUFF_H_SMALL)

        mobs.center()

        return objs, mobs

    def connect(
        self,
        **aargs,
    ) -> Animation:
        line_head = Line(
            self.objs_card[0].get_top() + UP*LINE_BUFF,
            self.objs_card[0].get_top(),
            **LINE_CONFIG_THIN,
        )
        lines_mid = VGroup(
            Line(
                self.objs_card[idx].get_bottom(),
                self.objs_card[idx+1].get_top(),
                **LINE_CONFIG_THIN,
            ) for idx in range(0, 21)
        )
        cps = [
            (self.objs_card[6].get_left(), self.objs_card[11].get_left()),
            (self.objs_card[4].get_left(), self.objs_card[14].get_left()),
            (self.objs_card[12].get_left(), self.objs_card[17].get_left()),
            (self.objs_card[9].get_left(), self.objs_card[20].get_left()),
        ]
        lines_concat = VGroup(
            create_curve(cps[0][0], cps[0][1], buff=CURVE_BUFF_SMALL),
            create_curve(cps[1][0], cps[1][1], buff=CURVE_BUFF_MEDIUM),
            create_curve(cps[2][0], cps[2][1], buff=CURVE_BUFF_SMALL),
            create_curve(cps[3][0], cps[3][1], buff=CURVE_BUFF_MEDIUM),
        )

        lines = VGroup(
            line_head,
            *lines_mid,
            *lines_concat,
            # *lines_tail,
        )

        lines.set_z_index(999)
        self.lines = lines

        def finish_connect(scene):
            self.add(self.lines)
            scene.add_fixed_in_frame_mobjects(self.lines)

        return AnimationGroup(
            *(Write(
                line,
                fixed=True,
            ) for line in self.lines),
            **aargs,
            _on_finish=finish_connect,
        )

    def switch_arrange(
        self,
    ):
        if self.mode == 'linear':
            self.mode = 'network'

        elif self.mode == 'network':
            self.mode = 'linear'
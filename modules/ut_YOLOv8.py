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
    color: ManimColor = WHITE,
) -> VMobject:
    cfg = {**LINE_CONFIG_THIN, 'stroke_color': color}

    pm_x = min(p1[0], p2[0]) - buff
    pm_seg = (p1[1] - p2[1]) / 5
    pm_y1 = p1[1] - pm_seg
    pm_y2 = p2[1] + pm_seg

    pm1 = (pm_x, pm_y1, 0.0)
    pm2 = (pm_x, pm_y2, 0.0)
    curve = VMobject(**cfg).set_points_smoothly(
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

        mobs.center()

        return objs, mobs

    def connect(
        self,
        **aargs,
    ) -> Animation:
        # 1 head line
        line_head = Line(
            self.objs_card[0].get_top() + UP*LINE_BUFF,
            self.objs_card[0].get_top(),
            **LINE_CONFIG_THIN,
        )

        # 21 mid lines
        lines_mid = VGroup(
            Line(
                self.objs_card[idx].get_bottom(),
                self.objs_card[idx+1].get_top(),
                **LINE_CONFIG_THIN,
            ) for idx in range(0, 21)
        )

        # 4 concat lines
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

        # 3 head input lines from [15, 18, 21]
        cps = [
            (self.objs_card[15].get_left(), self.objs_card[-3].get_left()),
            (self.objs_card[18].get_left(), self.objs_card[-2].get_left()),
            (self.objs_card[21].get_left(), self.objs_card[-1].get_left()),
        ]
        lines_hin = VGroup(
            create_curve(cps[0][0], cps[0][1], buff=CURVE_BUFF_SMALL),
            create_curve(cps[1][0], cps[1][1], buff=CURVE_BUFF_SMALL),
            create_curve(cps[2][0], cps[2][1], buff=CURVE_BUFF_SMALL),
        )

        # 6 head output lines
        lines_hout = VGroup(
            Line(
                self.objs_card[-3].get_right() + UP * 0.05,
                self.objs_card[-3].get_right() + UP * 0.05 + RIGHT * LINE_BUFF,
                **LINE_CONFIG_THIN,
            ),
            Line(
                self.objs_card[-3].get_right() + DOWN * 0.05,
                self.objs_card[-3].get_right() + DOWN * 0.05 + RIGHT * LINE_BUFF,
                **LINE_CONFIG_THIN,
            ),
            Line(
                self.objs_card[-2].get_right() + UP * 0.05,
                self.objs_card[-2].get_right() + UP * 0.05 + RIGHT * LINE_BUFF,
                **LINE_CONFIG_THIN,
            ),
            Line(
                self.objs_card[-2].get_right() + DOWN * 0.05,
                self.objs_card[-2].get_right() + DOWN * 0.05 + RIGHT * LINE_BUFF,
                **LINE_CONFIG_THIN,
            ),
            Line(
                self.objs_card[-1].get_right() + UP * 0.05,
                self.objs_card[-1].get_right() + UP * 0.05 + RIGHT * LINE_BUFF,
                **LINE_CONFIG_THIN,
            ),
            Line(
                self.objs_card[-1].get_right() + DOWN * 0.05,
                self.objs_card[-1].get_right() + DOWN * 0.05 + RIGHT * LINE_BUFF,
                **LINE_CONFIG_THIN,
            ),
        )

        lines = VGroup(
            line_head,
            *lines_mid,
            *lines_concat,
            *lines_hin,
            *lines_hout,
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

    def reposition_heads(
        self,
        **aargs,
    ):
        ms1 = VGroup(self.mobs_card[-3], self.lines[-6], self.lines[-5])
        ms2 = VGroup(self.mobs_card[-2], self.lines[-4], self.lines[-3])
        ms3 = VGroup(self.mobs_card[-1], self.lines[-2], self.lines[-1])
        ms1.generate_target()
        ms2.generate_target()
        ms3.generate_target()
        ms1.target.next_to(self.mobs_card[15], RIGHT, buff=0.5)
        ms2.target.next_to(self.mobs_card[18], RIGHT, buff=0.5)
        ms3.target.next_to(self.mobs_card[21], RIGHT, buff=0.5)

        c1, c2, c3 = self.lines[-9], self.lines[-8], self.lines[-7]
        c1t = Line(
            self.mobs_card[15].get_right(),
            ms1.target.get_left(),
            **LINE_CONFIG_THIN,
        )
        c2t = Line(
            self.mobs_card[18].get_right(),
            ms2.target.get_left(),
            **LINE_CONFIG_THIN,
        )
        c3t = Line(
            self.mobs_card[21].get_right(),
            ms3.target.get_left(),
            **LINE_CONFIG_THIN,
        )

        return AnimationGroup(
            MoveToTarget(ms1),
            MoveToTarget(ms2),
            MoveToTarget(ms3),
            Transform(c1, c1t),
            Transform(c2, c2t),
            Transform(c3, c3t),
            **aargs,
        )

    def reposition_all(
        self,
        **aargs,
    ):
        hcard = self.mobs_card[0].height
        mbuff = 0.3

        s1 = self.mobs_card[:10]
        s2 = self.mobs_card[10:16]
        s3 = self.mobs_card[16:22]
        s4 = self.mobs_card[-3:]

        s1.generate_target()
        s2.generate_target()
        s3.generate_target()
        s4.generate_target()

        # setup s1 target cards
        s1.target.arrange(DOWN, buff=mbuff).shift(LEFT*3).shift(UP*0.5)

        # setup s2 target cards
        sbuff = (s1.target[4:7].height - 4*hcard) / 3
        s2.target[1:5].arrange(UP, buff=sbuff)
        s2.target[0].next_to(s2.target[1], DOWN, buff=mbuff)
        s2.target[5].next_to(s2.target[4], UP, buff=mbuff)
        offset_y = s1.target[4].get_top()[1] - s2.target[4].get_top()[1]
        s2.target.shift(UP*offset_y + LEFT)

        # setup s3 target cards
        bbuff = (s2.target[2].get_top()[1] - s1.target[-1].get_bottom()[1] - 4*hcard)/3
        s3.target[1:5].arrange(DOWN, buff=bbuff)
        s3.target[0].next_to(s3.target[1], UP, buff=mbuff)
        s3.target[-1].next_to(s3.target[4], DOWN, buff=mbuff)
        offset_y = s2.target[2].get_top()[1] - s3.target[1].get_top()[1]
        s3.target.shift(UP*offset_y, RIGHT)

        # setup s4 target cards
        s4.target[0].center().align_to(s2.target[-1], UP)
        s4.target[1].center().align_to(s3.target[2], UP)
        s4.target[2].center().align_to(s3.target[-1], UP)
        s4.target.shift(RIGHT*3)

        # setup head line target
        slines = self.lines
        for line in slines:
            line.generate_target()
        tlines = VGroup(line.target for line in slines)
        tlines[0].next_to(s1.target[0], UP, buff=0.0)

        # setup mid lines target
        for idx, line in enumerate(tlines[1:10]):
            line.put_start_and_end_on(
                start=s1.target[idx].get_bottom(),
                end=s1.target[idx+1].get_top(),
            )
        node_start = s2.target[0].get_bottom()
        node_start[1] = s1.target[-1].get_y()
        tlines[10].put_start_and_end_on(
            start=node_start,
            end=s2.target[0].get_bottom(),
        )
        for idx, line in enumerate(tlines[11:16]):
            line.put_start_and_end_on(
                start=s2.target[idx].get_top(),
                end=s2.target[idx+1].get_bottom(),
            )
        node_start = s3.target[0].get_top()
        node_start[1] = s2.target[-1].get_y()
        tlines[16].put_start_and_end_on(
            start=node_start,
            end=s3.target[0].get_top(),
        )
        for idx, line in enumerate(tlines[17:22]):
            line.put_start_and_end_on(
                start=s3.target[idx].get_bottom(),
                end=s3.target[idx+1].get_top(),
            )

        # setup concat lines target
        tlines[22].become(Line(
            start=s1.target[6].get_right(),
            end=s2.target[1].get_left(),
            **LINE_CONFIG_THIN,
        ))
        tlines[23].become(Line(
            start=s1.target[4].get_right(),
            end=s2.target[4].get_left(),
            **LINE_CONFIG_THIN,
        ))
        tlines[24].become(Line(
            start=s2.target[2].get_right(),
            end=s3.target[1].get_left(),
            **LINE_CONFIG_THIN,
        ))
        tlines[25].become(Line(
            start=s1.target[-1].get_right(),
            end=s3.target[-2].get_left(),
            **LINE_CONFIG_THIN,
        ))

        # setup head input lines target
        tlines[26].put_start_and_end_on(
            start=s2.target[-1].get_right(),
            end=s4.target[0].get_left(),
        )
        tlines[27].put_start_and_end_on(
            start=s3.target[2].get_right(),
            end=s4.target[1].get_left(),
        )
        tlines[28].put_start_and_end_on(
            start=s3.target[-1].get_right(),
            end=s4.target[2].get_left(),
        )

        # setup head output lines target
        tlines[29:31].next_to(s4.target[0], RIGHT, buff=0.0)
        tlines[31:33].next_to(s4.target[1], RIGHT, buff=0.0)
        tlines[33:35].next_to(s4.target[2], RIGHT, buff=0.0)

        anims = AnimationGroup(
            MoveToTarget(s1),
            MoveToTarget(s2),
            MoveToTarget(s3),
            MoveToTarget(s4),
            *(MoveToTarget(line) for line in slines),
            **aargs,
        )

        return anims

    def expand(
        self,
        summaries: list | None = None,
        **aargs,
    ) -> Animation:
        if summaries is None:
            return AnimationGroup(
                *(card.expand_summary(
                    direction='center',
                ) for card in self.mobs_card),
                **aargs,
            )
        else:
            return AnimationGroup(
                *(card.expand_summary(
                    summary=summary,
                    direction='center',
                ) for card, summary in zip(
                    self.mobs_card,
                    summaries,
                )),
                **aargs,
            )
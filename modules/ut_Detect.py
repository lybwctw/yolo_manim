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
# 'ch': UNKNOWN,    # input channels
# 'c2': UNKNOWN,    # mid channels for cv2
# 'c3': UNKNOWN,    # mid channels for cv3
# 'reg_max': UNKNOWN,    # max regression, for cv2
# 'nc': UNKNOWN,    # number of classes, for cv3
# ---------------------------------------------

LINE_BUFF = 0.5             # connection node to edge distance
LINE_GAP = 0.22              # gap between input/output lines for softmax

class UT_Detect(VMobject):
    pass

class MGraph_Detect(MGraph):
    def __init__(
        self,
        module_config: dict = {},
    ):
        super().__init__(module_config)

    def create_cards(
        self,
    ) -> tuple:
        objs = {}

        ch = self.module_config['ch']
        c2 = self.module_config['c2']
        c3 = self.module_config['c3']
        reg_max = self.module_config['reg_max']
        nc = self.module_config['nc']

        objs['box'] = VGroup(
            InfoCard('Conv', summary=f'{ch} {c2} 3 1 1', frame_config={'fill_color': PURE_BLUE}),
            InfoCard('Conv', summary=f'{c2} {c2} 3 1 1', frame_config={'fill_color': PURE_BLUE}),
            InfoCard('Conv2d', summary=f'{c2} {reg_max*4} 1 1 0 T', frame_config={'fill_color': ORANGE}),
            InfoCard('split', summary=f'0 {reg_max}', frame_config={'fill_color': TEAL}),
            InfoCard('Softmax', summary=f'0', frame_config={'fill_color': TEAL}),
            InfoCard('concat', summary=f'0', frame_config={'fill_color': TEAL}),
        )
        objs['cls'] = VGroup(
            InfoCard('Conv', summary=f'{ch} {c3} 3 1 1', frame_config={'fill_color': PURE_BLUE}),
            InfoCard('Conv', summary=f'{c3} {c3} 3 1 1', frame_config={'fill_color': PURE_BLUE}),
            InfoCard('Conv2d', summary=f'{c3} {nc} 1 1 0 T', frame_config={'fill_color': ORANGE}),
            InfoCard('Sigmoid', frame_config={'fill_color': TEAL}),
        )

        mobs_box = VGroup(
            *objs['box'],
        ).arrange(DOWN, buff=MCARD_BUFF_MINI, aligned_edge=RIGHT)
        mobs_cls = VGroup(
            *objs['cls'],
        ).arrange(DOWN, buff=MCARD_BUFF_MINI, aligned_edge=LEFT)
        mobs = VGroup(
            mobs_box,
            mobs_cls,
        ).arrange(RIGHT, buff=MCARD_BUFF_MINI, aligned_edge=UP)

        return objs, mobs

    def more_space(
        self,
        **aargs,
    ) -> Animation:
        center_box = self.mobs_card[0].get_center()
        center_cls = self.mobs_card[1].get_center()

        mobs_box = self.mobs_card[0]
        mobs_cls = self.mobs_card[1]
        mobs_box.generate_target()
        mobs_cls.generate_target()
        mobs_box.target.arrange(
            DOWN,
            buff=MCARD_BUFF_MEDIUM,
            aligned_edge=RIGHT,
        ).move_to(
            center_box,
        )
        mobs_cls.target.arrange(
            DOWN,
            buff=MCARD_BUFF_MEDIUM,
            aligned_edge=LEFT,
        ).move_to(
            center_cls,
        ).align_to(
            mobs_box.target,
            UP,
        )

        anims = AnimationGroup(
            MoveToTarget(
                mobs_box,
                **aargs,
            ),
            MoveToTarget(
                mobs_cls,
                **aargs,
            ),
            lag_ratio=0.0,
        )

        return anims

    def expand(
        self,
        **aargs,
    ) -> Animation:
        return AnimationGroup(
            *(card.expand_summary(
                direction='left',
            ) for card in self.mobs_card[0]),
            *(card.expand_summary(
                direction='right',
            ) for card in self.mobs_card[1]),
            **aargs,
        )

    def connect(
        self,
        **aargs,
    ) -> Animation:
        # common root line
        p1_root = (self.objs_card['box'][0].get_right() + self.objs_card['cls'][0].get_left()) / 2
        p1_root[1] = (self.objs_card['box'][0].get_top()[1] + UP*MCARD_BUFF_MEDIUM*2)[1]
        p2_root = p1_root + DOWN*MCARD_BUFF_MEDIUM
        line_root = Line(
            p1_root,
            p2_root,
            **LINE_CONFIG_DEFAULT,
        )

        # root line for box series
        p3_box = self.objs_card['box'][0].get_corner(UR) + LEFT*LINE_BUFF
        p2_box = p3_box.copy()
        p2_box[1] = p2_root[1]
        line_root_box = VMobject(**LINE_CONFIG_DEFAULT).set_points_as_corners([
            p2_root,
            p2_box,
            p3_box,
        ])

        # root line for cls series
        p3_cls = self.objs_card['cls'][0].get_corner(UL) + RIGHT*LINE_BUFF
        p2_cls = p3_cls.copy()
        p2_cls[1] = p2_root[1]
        line_root_cls = VMobject(**LINE_CONFIG_DEFAULT).set_points_as_corners([
            p2_root,
            p2_cls,
            p3_cls,
        ])

        # mids and tail for box
        n_box = 6
        lines_box = VGroup(
            Line(
                self.objs_card['box'][i].get_corner(DR) + LEFT*LINE_BUFF,
                self.objs_card['box'][i+1].get_corner(UR) + LEFT*LINE_BUFF,
                **LINE_CONFIG_DEFAULT,
            ) for i in range(n_box-1)
        )
        # x4 for input/output lines for softmax
        in_softmax, out_softmax = lines_box[3], lines_box[4]
        in_center = in_softmax.get_center()
        out_center = out_softmax.get_center()
        ins_softmax = VGroup(in_softmax.copy() for _ in range(4)).arrange(RIGHT, buff=LINE_GAP).move_to(in_center)
        outs_softmax = VGroup(out_softmax.copy() for _ in range(4)).arrange(RIGHT, buff=LINE_GAP).move_to(out_center)
        lines_box = VGroup(
            *lines_box[:3],
            *ins_softmax,
            *outs_softmax,
            *lines_box[5:],
        )
        line_tail_box = Line(
            self.objs_card['box'][n_box-1].get_corner(DR) + LEFT*LINE_BUFF,
            self.objs_card['box'][n_box-1].get_corner(DR) + LEFT*LINE_BUFF + DOWN*MCARD_BUFF_MEDIUM,
            **LINE_CONFIG_DEFAULT,
        )

        # mids and tail for cls
        n_cls = 4
        lines_cls = VGroup(
            Line(
                self.objs_card['cls'][i].get_corner(DL) + RIGHT*LINE_BUFF,
                self.objs_card['cls'][i+1].get_corner(UL) + RIGHT*LINE_BUFF,
                **LINE_CONFIG_DEFAULT,
            ) for i in range(n_cls-1)
        )
        line_tail_cls = Line(
            self.objs_card['cls'][n_cls-1].get_corner(DL) + RIGHT*LINE_BUFF,
            self.objs_card['cls'][n_cls-1].get_corner(DL) + RIGHT*LINE_BUFF + DOWN*MCARD_BUFF_MEDIUM,
            **LINE_CONFIG_DEFAULT,
        )

        lines = VGroup(
            line_root,
            line_root_box,
            *lines_box,
            line_tail_box,
            line_root_cls,
            *lines_cls,
            line_tail_cls,
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
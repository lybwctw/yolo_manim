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
# 'c1': UNKNOWN,
# 'c2': UNKNOWN,
# 'k': UNKNOWN,

class UT_C2f(VMobject):
    pass

class MGraph_SPPF(MGraph):
    def __init__(
        self,
        module_config: dict = {},
    ):
        super().__init__(module_config)

    def create_cards(
        self,
    ) -> tuple:
        objs = {}

        c1 = self.module_config['c1']
        c2 = self.module_config['c2']
        k = self.module_config['k']

        c_ = int(c2//2)

        objs['cv1'] = InfoCard(
            'Conv',
            summary=f'{c1} {c_} 1 1',
            frame_config={'fill_color': PURE_BLUE},
        )
        objs['cv2'] = InfoCard(
            'Conv',
            summary=f'{c_*4} {c2} 1 1',
            frame_config={'fill_color': PURE_BLUE},
        )
        objs['m'] = VGroup(
            InfoCard(
                'MaxPool2d',
                summary=f'{k} 1 {k//2}',
            frame_config={'fill_color': ORANGE},
            ) for _ in range(3)
        )
        objs['concat'] = InfoCard(
            'concat',
            summary=f'0',
            frame_config={'fill_color': TEAL},
        )

        mobs = VGroup(
            objs['cv1'],
            *objs['m'],
            objs['concat'],
            objs['cv2'],
        )
        mobs.arrange(DOWN, buff=MCARD_BUFF_MINI)
        return objs, mobs

    def more_space(
        self,
        **aargs,
    ) -> Animation:
        # TODO, even more space in mid ones?
        orig_center = self.get_center()
        anim = self.mobs_card.animate(
            **aargs,
        ).arrange(
            DOWN,
            buff=MCARD_BUFF_MEDIUM,
        ).move_to(
            orig_center
        )

        return anim

    def expand(
        self,
        **aargs,
    ) -> Animation:
        return AnimationGroup(
            *(card.expand_summary(
                direction='center',
            ) for card in self.mobs_card),
            **aargs,
        )

    def connect(
        self,
        **aargs,
    ) -> Animation:
        lines = VGroup(
            Line(
                self.card_cv1.get_top() + UP*MCARD_BUFF_MEDIUM,
                self.card_cv1.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_cv1.get_bottom(),
                self.cards_m[0].get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.cards_m[0].get_bottom(),
                self.cards_m[1].get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.cards_m[1].get_bottom(),
                self.cards_m[2].get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.cards_m[2].get_bottom(),
                self.card_concat.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_concat.get_bottom(),
                self.card_cv2.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_cv2.get_bottom(),
                self.card_cv2.get_bottom() + DOWN*MCARD_BUFF_MEDIUM,
                **LINE_CONFIG_DEFAULT,
            ),
        )

        # connect cv1 output to concat
        x_left = (self.get_left() + MCARD_BUFF_MEDIUM*LEFT)[0]
        p1 = lines[1].get_center() + DOWN*MCARD_BUFF_MINI
        p2 = p1.copy()
        p2[0] = x_left
        p4 = self.card_concat.get_left()
        p3 = p4.copy()
        p3[0] = x_left
        path = VMobject(**LINE_CONFIG_DEFAULT).set_points_as_corners([
            p1, p2, p3, p4,
        ])
        lines.add(path)

        # horizontal lines to connection
        hlines = VGroup()
        for i in range(2):
            p1 = lines[2+i].get_center() + DOWN*MCARD_BUFF_MINI
            p2 = p1.copy()
            p2[0] = x_left
            line = Line(p1, p2, **LINE_CONFIG_DEFAULT)
            hlines.add(line)
        lines.add(*hlines)

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


    @property
    def card_cv1(self):
        return self.objs_card['cv1']
    @property
    def card_cv2(self):
        return self.objs_card['cv2']
    @property
    def card_concat(self):
        return self.objs_card['concat']
    @property
    def cards_m(self):
        return self.objs_card['m']
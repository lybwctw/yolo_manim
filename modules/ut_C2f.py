from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

from modules.ut_Conv import *
from modules.ut_Bottleneck import *

# ------------- info card ---------------------
# 'c1': UNKNOWN,
# 'c2': UNKNOWN,
# 'n': UNKNOWN,
# 'shortcut': UNKNOWN,
# 'e': UNKNOWN,
# ---------------------------------------------

class UT_C2f(VMobject):
    pass

class MGraph_C2f(MGraph):
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
        n = self.module_config['n']
        shortcut = self.module_config['shortcut']
        e = self.module_config['e']

        c_ = int(c2*e)

        objs['cv1'] = InfoCard(
            'Conv',
            summary=f'{c1} {c_*2} 1 1 1',
            frame_config={'fill_color': PURE_BLUE},
        )
        objs['cv2'] = InfoCard(
            'Conv',
            summary=f'{(2+n)*c_} {c2} 1 1 1',
            frame_config={'fill_color': PURE_BLUE},
        )
        objs['split'] = InfoCard(
            'split',
            summary=f'{c_} 0',
            frame_config={'fill_color': TEAL},
        )
        # TODO: update cat with concat in previous chapters
        objs['concat'] = InfoCard(
            'concat',
            summary=f'0',
            frame_config={'fill_color': TEAL},
        )
        objs['m'] = VGroup(
            InfoCard(
                'Bottleneck',
                summary=f'{c_} {c_} {str(shortcut)[0]}',
                frame_config={'fill_color': PURE_BLUE},
            ) for _ in range(n)
        )

        mobs = VGroup(
            objs['cv1'],
            objs['split'],
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
                self.card_split.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_split.get_bottom(),
                self.cards_m[0].get_top(),
                **LINE_CONFIG_DEFAULT,
            ),

            *(Line(
                self.cards_m[i].get_bottom(),
                self.cards_m[i+1].get_top(),
                **LINE_CONFIG_DEFAULT,
            ) for i in range(self.module_config['n']-1)),

            Line(
                self.cards_m[-1].get_bottom(),
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

        # connection between split and concat
        x_left = (self.get_left() + MCARD_BUFF_MEDIUM*LEFT)[0]
        p1 = self.card_split.get_left()
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
        for i in range(self.module_config['n']):
            # a bit down for showing shape text on top
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

    def pop_bottleneck(
        self,
        **aargs,
    ) -> AnimationGroup:
        n = self.module_config['n']
        card_pop = self.mobs_card[n+1]
        line_pop1 = self.lines[n+1]
        line_pop2 = self.lines[2*n+5]

        self.mobs_card.remove(card_pop)
        self.objs_card['m'].remove(card_pop)
        self.lines.remove(line_pop1)
        self.lines.remove(line_pop2)

        mobs_tail = VGroup(
            self.mobs_card[n+1:],
            self.lines[n+1:n+4],
        )
        mobs_tail.generate_target()
        mobs_tail.target.next_to(self.mobs_card[n], DOWN, buff=0.0)

        # new multi-segment path
        path = self.lines[n+4]
        x_left = path.get_left()[0]
        p1 = self.card_split.get_left()
        p2 = p1.copy()
        p2[0] = x_left
        # p4 = self.card_concat.get_left()
        p4 = mobs_tail.target[0][0].get_left()
        p3 = p4.copy()
        p3[0] = x_left
        path_new = VMobject(**LINE_CONFIG_DEFAULT).set_points_as_corners([
            p1, p2, p3, p4,
        ])

        # update module_config
        self.module_config['n'] = self.module_config['n'] - 1

        return Succession(
            Unwrite(card_pop),
            Unwrite(line_pop1),
            Unwrite(line_pop2),
            AnimationGroup(
                MoveToTarget(mobs_tail),
                Transform(path, path_new),
                lag_ratio=0.0,
            ),
            **aargs,
        )


    @property
    def card_cv1(self):
        return self.objs_card['cv1']
    @property
    def card_cv2(self):
        return self.objs_card['cv2']
    @property
    def card_split(self):
        return self.objs_card['split']
    @property
    def card_concat(self):
        return self.objs_card['concat']
    @property
    def cards_m(self):
        return self.objs_card['m']
from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *
from utils.mgraph import *
from utils.ftensor import *
from utils.show_shape_3d import *
from utils.general import *

# ------------- info card ---------------------
# 'c1': UNKNOWN,
# 'c2': UNKNOWN,
# 'shortcut': UNKNOWN,
# 'k': UNKNOWN,
# 'e': UNKNOWN,
# ---------------------------------------------


class UT_Bottleneck(VMobject):
    pass

class MGraph_Bottleneck(MGraph):
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
        shortcut = self.module_config['shortcut']
        k = self.module_config['k']
        e = self.module_config['e']

        c_ = int(c2*e)
        p1_ = int((k[0]-1)/2)
        p2_ = int((k[1]-1)/2)

        objs['cv1'] = InfoCard(
            'Conv',
            summary=f'{c1} {c_} {k[0]} 1 {p1_}',
            frame_config={'fill_color': PURE_BLUE},
        )
        objs['cv2'] = InfoCard(
            'Conv',
            summary=f'{c_} {c2} {k[1]} 1 {p2_}',
            frame_config={'fill_color': PURE_BLUE},
        )
        objs['add'] = InfoCard(
            'Add',
            frame_config={'fill_color': TEAL},
        )

        if shortcut:
            mobs = VGroup(
                objs['cv1'],
                objs['cv2'],
                objs['add'],
            )
        else:
            mobs = VGroup(
                objs['cv1'],
                objs['cv2'],
            )
        mobs.arrange(DOWN, buff=MCARD_BUFF_MINI)
        return objs, mobs

    def expand(
        self,
        **aargs,
    ) -> Animation:
        orig_center = self.get_center()
        anims = self.mobs_card.animate(
            **aargs,
        ).arrange(
            DOWN,
            buff=MCARD_BUFF_MEDIUM,
        ).move_to(
            orig_center
        )
        return anims

    def connect(
        self,
        **aargs,
    ) -> Animation:
        # FIXME: shortcut=False by default
        lines = VGroup(
            Line(
                self.card_cv1.get_top() + UP*MCARD_BUFF_MEDIUM,
                self.card_cv1.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_cv1.get_bottom(),
                self.card_cv2.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_cv2.get_bottom(),
                self.card_cv2.get_bottom() + DOWN*MCARD_BUFF_MEDIUM,
                **LINE_CONFIG_DEFAULT,
            ),
        )

        self.lines = lines

        def finish_connect(scene):
            self.add(self.lines)
            scene.add_fixed_in_frame_mobjects(self.lines)

        return AnimationGroup(
            *(GrowFromCenter(
                line,
                fixed=True,
            ) for line in self.lines),
            *(card.expand_summary(
                direction='center',
            ) for card in [self.card_cv1, self.card_cv2]),
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
    def card_add(self):
        return self.objs_card['add']
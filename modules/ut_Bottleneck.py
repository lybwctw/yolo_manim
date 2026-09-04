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

from modules.ut_Conv import *

# ------------- info card ---------------------
# 'c1': UNKNOWN,
# 'c2': UNKNOWN,
# 'shortcut': UNKNOWN,
# 'k': UNKNOWN,
# 'e': UNKNOWN,
# ---------------------------------------------

# CONFIG_NORMAL = {}
# CONFIG_OPAQUE = {'fill_opacity': 1.0, 'stroke_width': 1.5}

class UT_Bottleneck(VMobject):
    """(c1, c2, shortcut)
       Only consider when c1==c2.
       shortcut not visible.
    """
    def __init__(
        self,
        module_config: dict = {},               # c1, c2, shortcut
        z_index: float = 0.0,
        ut_gap: float = UNIT_FTENSOR_SIZE*1.0,  # gap between cv1 and cv2
        init_scale: float = 1.0,
        opaque: bool = False,
    ):
        super().__init__()
        self.module_config = module_config

        ut_cv1 = UT_Conv(
            module_config=Bottleneck_2_cv1_config(self.module_config),
            z_index=z_index,
            tensor_gap=UNIT_FTENSOR_SIZE,   # closer from bottleneck
            init_scale=init_scale,
            opaque=opaque,
        )
        ut_cv2 = UT_Conv(
            module_config=Bottleneck_2_cv2_config(self.module_config),
            z_index=z_index,
            tensor_gap=UNIT_FTENSOR_SIZE,   # closer from bottleneck
            init_scale=init_scale,
            opaque=opaque,
        )
        VGroup(ut_cv1, ut_cv2).arrange(DOWN, buff=ut_gap)

        self.ut_cv1 = ut_cv1
        self.ut_cv2 = ut_cv2

        self.add(self.ut_cv1, self.ut_cv2)
        self.center()
        
    def create(
        self,
        ref: str = 'center',
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ut_cv1.create(ref=ref, **aargs),
            self.ut_cv2.create(ref=ref, **aargs),
            lag_ratio=0.0,
            _on_finish=lambda s: s.add(self),
        )

    def breath(
        self,
        **aargs,
    ):
        return AnimationGroup(
            self.ut_cv1.breath(**aargs),
            self.ut_cv2.breath(**aargs),
            lag_ratio=0.0,
        )

    def tarnish(
        self,
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ut_cv1.tarnish(),
            self.ut_cv2.tarnish(),
            **aargs,
        )

    def lightup(
        self,
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ut_cv1.lightup(),
            self.ut_cv2.lightup(),
            **aargs,
        )
    
    def uncreate(
        self,
        ref: str = 'center',
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ut_cv1.uncreate(ref=ref, **aargs),
            self.ut_cv2.uncreate(ref=ref, **aargs),
            lag_ratio=0.0,
            _on_finish=lambda s: s.remove(self),
        )
    

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

        # lines.set_z_index(999)
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

    def append_add(
        self,
        **aargs,
    ):
        # init card
        card_add = self.objs_card['add']
        card_add.next_to(self.lines[-1], DOWN, buff=0.0)

        # init first extra path
        path = VMobject(**LINE_CONFIG_DEFAULT)
        p1 = self.lines[0].get_top()
        p2 = [self.get_left()[0]-MCARD_BUFF_SMALL, p1[1], 0]
        p4 = card_add.get_left()
        p3 = [p2[0], p4[1], 0]
        path.set_points_as_corners([p1, p2, p3, p4])

        # init second extra line
        line = Line(
            card_add.get_bottom(),
            card_add.get_bottom() + DOWN*MCARD_BUFF_MEDIUM,
            **LINE_CONFIG_DEFAULT,
        )

        def finish_append(scene):
            self.mobs_card.add(card_add)
            self.lines.add(path, line)

        return Succession(
            self.lines[0].animate.put_start_and_end_on(
                start=self.lines[0].get_start() + UP*MCARD_BUFF_SMALL,
                end=self.lines[0].get_end(),
            ),
            GrowFromCenter(card_add, fixed=True),
            Write(path, fixed=True),
            Write(line, fixed=True),
            **aargs,
            _on_finish=finish_append,
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


class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        module_config = {
            'c1': 4,
            'c2': 4,
            'shortcut': False,
            'k': (3,3),
            'e': 1.0,
        }

        bottleneck = UT_Bottleneck(
            module_config=module_config,
            init_scale=0.8,
            opaque=True,
        )

        self.play(bottleneck.create(
            ref='center',
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait()

        self.play(bottleneck.breath(
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait()
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
# 's': UNKNOWN,
# 'p': UNKNOWN,

class UT_Conv(VMobject):
    """Visualization of ultralytics.nn.modules.Conv.
    """
    def __init__(
        self,
    ):
        super().__init__()


class MGraph_Conv(MGraph):
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
        s = self.module_config['s']
        p = self.module_config['p']
        objs['conv'] = InfoCard(
            'Conv2d',
            summary=f'{c1} {c2} {k} {s} {p} F',
            frame_config={'fill_color': ORANGE},
        )
        objs['bn'] = InfoCard(
            'BatchNorm2d',
            summary=f'{c2}',
            frame_config={'fill_color': ORANGE},
        )
        objs['act'] = InfoCard(
            'SiLU',
            frame_config={'fill_color': ORANGE},
        )

        mobs = VGroup(v for v in objs.values())
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
        lines = VGroup(
            Line(
                self.card_conv.get_top() + UP*MCARD_BUFF_MEDIUM,
                self.card_conv.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_conv.get_bottom(),
                self.card_bn.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_bn.get_bottom(),
                self.card_act.get_top(),
                **LINE_CONFIG_DEFAULT,
            ),
            Line(
                self.card_act.get_bottom(),
                self.card_act.get_bottom() + DOWN*MCARD_BUFF_MEDIUM,
                **LINE_CONFIG_DEFAULT,
            ),
        )

        self.lines = lines

        # FIXME: why simply fixed=True failed
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
            ) for card in [self.card_conv, self.card_bn]),
            **aargs,
            _on_finish=finish_connect,
        )

    @property
    def card_conv(self):
        return self.objs_card['conv']
    @property
    def card_bn(self):
        return self.objs_card['bn']
    @property
    def card_act(self):
        return self.objs_card['act']

    @property
    def config_conv(self):
        return {
            'in_channels': self.module_config['c1'],
            'out_channels': self.module_config['c2'],
            'kernel_size': self.module_config['k'],
            'stride': self.module_config['s'],
            'padding': self.module_config['p'],
            'bias': False,
            'dilation': 1,
            'groups': 1,
            'padding_mode': 'zeros',
        }

    @property
    def config_bn(self):
        return {
            'num_features': self.module_config['c2'],
            'eps': 1e-5,
            'momentum': 0.1,
            'affine': True,
            'track_running_stats': True,
        }

class Demo(ThreeDScene):
    def construct(self):
        graph = MGraph_Conv(
            module_config = {
                'c1': 10,
                'c2': 20,
                'k': 3,
                's': 1,
                'p': 1,
            },
        )
        self.play(graph.create(
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait()

        self.play(graph.animate(
            run_time=1.0,
        ).shift(RIGHT*3))

        cube = Cube(
            stroke_width=3,
            stroke_color=WHITE,
            stroke_opacity=1.0,
            fill_color=GRAY,
            fill_opacity=0.6,
        )
        self.move_camera(
            phi=60*DEGREES,
            theta=-75*DEGREES,
            added_anims=[
                Write(cube),
            ],
            run_time=1.0,
        )
        self.wait()

        self.play(graph.expand(run_time=0.5))
        self.play(graph.connect(lag_ratio=0.0, run_time=0.5))
        self.wait()

        self.play(AnimationGroup(
            Unwrite(cube),
            graph.animate.center(),
            run_time=1.0,
        ))
        self.wait()

        self.play(graph.show_shape(
            '(12,3,4)',
            index=0,
            direction=RIGHT,
            buff=0.1,
            run_time=1.0,
        ))
        self.wait()

        self.play(graph.show_shape(
            '(12,3,4)',
            index=1,
            direction=RIGHT,
            buff=0.1,
            run_time=1.0,
        ))
        self.wait()

        self.play(graph.show_shape(
            '(12,4,5)',
            index=2,
            direction=RIGHT,
            buff=0.1,
            run_time=1.0,
        ))
        self.wait()

        self.play(graph.show_shape(
            '(12,5,6)',
            index=3,
            direction=RIGHT,
            buff=0.1,
            run_time=1.0,
        ))
        self.wait()

        self.play(graph.animate(
            run_time=1.0,
        ).shift(RIGHT*3))
        self.wait()
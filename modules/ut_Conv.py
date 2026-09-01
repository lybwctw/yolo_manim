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
# 'k': UNKNOWN,
# 's': UNKNOWN,
# 'p': UNKNOWN,
# ---------------------------------------------

DEFAULT_N = 8
DEFAULT_BLOCK_GAP = 0.3,
DEFAULT_TENSOR_GAP = 0.8

DEFAULT_CUBE_CONFIG_CONV = {
    'fill_color': GRAY,
    'fill_opacity': 1.0,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_CUBE_CONFIG_BN = {
    'fill_color': GRAY,
    'fill_opacity': 1.0,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_SIZE_CONFIG_CONV = {
    'width': 0.2,
    'height': 0.2,
    'depth': 0.8,
}
DEFAULT_SIZE_CONFIG_BN = {
    'width': 0.1,
    'height': 0.1,
    'depth': 0.4,
}

class UT_Conv(VMobject):
    """Visualization of ultralytics.nn.modules.Conv.
    """
    def __init__(
        self,
        module_config: dict = {},                   # c1, c2, k
        z_index: float = 0.0,                       # used by conv directly
        cube_config_conv: dict = {},
        cube_config_bn: dict = {},
        ref_conv: MTensor4D | None = None,
        ref_bn: MTensor4D | None = None,
        size_config_conv: dict = {},
        size_config_bn: dict = {},
        n: int | None = None,                       # shared by conv and bn
        block_gap: float = DEFAULT_BLOCK_GAP,       # used by conv directly
        tensor_gap: float = DEFAULT_TENSOR_GAP,     # gap between conv and bn
    ):
        super().__init__()
        self.module_config = module_config
        self.z_index = z_index
        self.cube_config_conv = {**DEFAULT_CUBE_CONFIG_CONV, **cube_config_conv}
        self.cube_config_bn = {**DEFAULT_CUBE_CONFIG_BN, **cube_config_bn}
        self.size_config_conv = {**DEFAULT_SIZE_CONFIG_CONV, **size_config_conv}
        self.size_config_bn = {**DEFAULT_SIZE_CONFIG_BN, **size_config_bn}
        if n is not None:
            self.n = n                              # explicit visual blocks
        else:
            self.n = module_config['c2']            # implicit visual blocks
        self.block_gap = block_gap
        # self.tensor_gap = tensor_gap

        mobs_conv = FTensor4D(
            ref_4d=ref_conv,
            shape=(
                self.module_config['c2'],
                self.module_config['c1'],
                self.module_config['k'],
                self.module_config['k'],
            ),
            z_index=self.z_index,
            cube_config=self.cube_config_conv,
            size_config=self.size_config_conv,
            n=self.n,
            block_gap=self.block_gap,
        )
        mobs_bn = FTensor4D(
            ref_4d=ref_bn,
            shape=(
                self.module_config['c2'],
                4,
                1,
                1,
            ),
            z_index=mobs_conv.z_index_end,
            cube_config=self.cube_config_bn,
            size_config=self.size_config_bn,
            n=self.n,
        )
        if ref_conv is None and ref_bn is None:
            for mb, mc in zip(mobs_bn.mobs, mobs_conv.mobs):
                mb.next_to(mc, DOWN, buff=tensor_gap)
        self.mobs_conv = mobs_conv
        self.mobs_bn = mobs_bn
        self.add(self.mobs_conv, self.mobs_bn)
        self.center()

    def create(
        self,
        direction: str = 'center',
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.mobs_conv.create(direction=direction, **aargs),
            self.mobs_bn.create(direction=direction, **aargs),
            lag_ratio=0.0,
            _on_finish=lambda s: s.add(self),
        )

    def uncreate(
        self,
        direction: str = 'center',
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.mobs_conv.uncreate(direction=direction, **aargs),
            self.mobs_bn.uncreate(direction=direction, **aargs),
            lag_ratio=0.0,
            _on_finish=lambda s: s.remove(self),
        )
    
    def stretch_direction(
        self,
        direction: str = 'erect',           # horizontal/erect
        size_scale: float | None = None,    # for mobs_conv
        size_target: float | None = 2.0,    # for mobs_conv
        shape: tuple | None = None,         # for mobs_conv
        **aargs,
    ) -> AnimationGroup:
        """Apply stretch_direction on mobs_conv.
           Regap mobs_bn if kernel_size is changed.
        """
        return self.mobs_conv.stretch_direction(
            direction=direction,
            size_scale=size_scale,
            size_target=size_target,
            keep_gap=False,
            shape=shape,
            rate_func=smooth,
            **aargs,
        )

    def stretch_blocks(
        self,
        diff: int = 1,                      # -n / n
        direction: str = 'center',          # top/center/bottom
        shape: tuple | None = None,         # for mobs_conv
        **aargs,
    ) -> AnimationGroup:
        """Apply stretch_blocks on mobs_conv and mobs_bn.
        """
        return AnimationGroup(
            self.mobs_conv.stretch_blocks(
                diff=diff,
                direction=direction,
                shape=shape,
                **aargs,
            ),
            self.mobs_bn.stretch_blocks(
                diff=diff,
                direction=direction,
                shape=shape[:1]+self.mobs_bn.shape[1:],
                **aargs,
            ),
            lag_ratio=0.0,
        )


    @property
    def conv_bn(self):
        return VGroup(self.mobs_conv, self.mobs_bn)

    @property
    def tensor_gap(self):
        return self.mobs_conv[0].get_bottom()[1] - self.mobs_bn[0].get_top()[1]

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

wt = 1.0
class Demo(ThreeDScene):
    def construct(self):
        # graph = MGraph_Conv(
        #     module_config = {
        #         'c1': 10,
        #         'c2': 20,
        #         'k': 3,
        #         's': 1,
        #         'p': 1,
        #     },
        # )
        # self.play(graph.create(
        #     lag_ratio=0.0,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(graph.animate(
        #     run_time=1.0,
        # ).shift(RIGHT*3))

        # cube = Cube(
        #     stroke_width=3,
        #     stroke_color=WHITE,
        #     stroke_opacity=1.0,
        #     fill_color=GRAY,
        #     fill_opacity=0.6,
        # )
        # self.move_camera(
        #     phi=60*DEGREES,
        #     theta=-75*DEGREES,
        #     added_anims=[
        #         Write(cube),
        #     ],
        #     run_time=1.0,
        # )
        # self.wait()

        # self.play(graph.expand(run_time=0.5))
        # self.play(graph.connect(lag_ratio=0.0, run_time=0.5))
        # self.wait()

        # self.play(AnimationGroup(
        #     Unwrite(cube),
        #     graph.animate.center(),
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(graph.show_shape(
        #     '(12,3,4)',
        #     index=0,
        #     direction=RIGHT,
        #     buff=0.1,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(graph.show_shape(
        #     '(12,3,4)',
        #     index=1,
        #     direction=RIGHT,
        #     buff=0.1,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(graph.show_shape(
        #     '(12,4,5)',
        #     index=2,
        #     direction=RIGHT,
        #     buff=0.1,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(graph.show_shape(
        #     '(12,5,6)',
        #     index=3,
        #     direction=RIGHT,
        #     buff=0.1,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(graph.animate(
        #     run_time=1.0,
        # ).shift(RIGHT*3))
        # self.wait()

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        uconv = UT_Conv(
            module_config={
                'c1': 128,
                'c2': 256,
                'k': 3,
            },
            n=8,
        )
        self.play(uconv.create(
            direction='bottom',
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()

        # self.move_camera(
        #     **VIEW_INTRO,
        # )
        # self.wait()

        self.play(uconv.conv_bn.animate(
            run_time=0.5,
        ).arrange(DOWN, buff=3.0))
        self.wait(wt)

        self.play(AnimationGroup(
            ShowShape3D(
                self,
                uconv.mobs_conv,
                view='compute',
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            ShowShape3D(
                self,
                uconv.mobs_bn,
                view='compute',
                lag_ratio=0.3,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            HideShape3D(
                uconv.mobs_conv,
                lag_ratio=0.0,
                run_time=wt,
            ),
            HideShape3D(
                uconv.mobs_bn,
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        self.play(uconv.conv_bn.animate(
            run_time=0.5,
        ).arrange(DOWN, buff=uconv.tensor_gap))
        self.wait(wt)
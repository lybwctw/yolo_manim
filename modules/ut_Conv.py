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

# DEFAULT_N = 8
# DEFAULT_BLOCK_GAP = 0.3,
# DEFAULT_TENSOR_GAP = 0.8

DEFAULT_CUBE_CONFIG_CONV = {
    'fill_color': ORANGE,
    'fill_opacity': 0.8,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_CUBE_CONFIG_BN = {
    'fill_color': RED_C,
    'fill_opacity': 0.8,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}

class UT_Conv(VMobject):
    """Visualization of ultralytics.nn.modules.Conv.
    """
    def __init__(
        self,
        ref_conv: MTensor4D | None = None,
        ref_bn: MTensor4D | None = None,
        module_config: dict = {},                   # c1, c2, k, (s, p)
        z_index: float = 0.0,                       # used by conv directly
        cube_config_conv: dict = {},
        cube_config_bn: dict = {},
        size_config_conv: dict = {},                # override that from module_config
        size_config_bn: dict = {},                  # override that from module_config
        n: int | None = None,                       # override that from module_config
        block_gap: float = UNIT_FTENSOR_SIZE,       # for conv
        tensor_gap: float = UNIT_FTENSOR_SIZE*2,    # gap between conv and bn
    ):
        super().__init__()
        self.module_config = module_config
        self.z_index = z_index
        self.cube_config_conv = {**DEFAULT_CUBE_CONFIG_CONV, **cube_config_conv}
        self.cube_config_bn = {**DEFAULT_CUBE_CONFIG_BN, **cube_config_bn}
        self.size_config_conv = size_config_conv
        self.size_config_bn = size_config_bn
        self.n = n if n is not None else self.module_config['c2']
        self.block_gap = block_gap
        # self.tensor_gap = tensor_gap

        ft_conv = FTensor4D(
            ref_4d=ref_conv,
            shape=Conv_2_conv_shape(self.module_config),
            z_index=self.z_index,
            cube_config=self.cube_config_conv,
            size_config=self.size_config_conv,
            n=self.n,
            block_gap=self.block_gap,
        )
        ft_bn = FTensor4D(
            ref_4d=ref_bn,
            shape=(self.module_config['c2'], 4, 1, 1),
            z_index=ft_conv.z_index_end,
            cube_config=self.cube_config_bn,
            size_config=self.size_config_bn,
            n=self.n,
        )
        if ref_conv is None and ref_bn is None:
            for mb, mc in zip(ft_bn.mobs, ft_conv.mobs):
                mb.next_to(mc, DOWN, buff=tensor_gap)
        self.ft_conv = ft_conv
        self.ft_bn = ft_bn
        self.add(self.ft_conv, self.ft_bn)
        self.center()

    def create(
        self,
        ref: str = 'center',
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ft_conv.create(ref=ref, **aargs),
            self.ft_bn.create(ref=ref, **aargs),
            lag_ratio=0.0,
            _on_finish=lambda s: s.add(self),
        )

    def breath(
        self,
        **aargs,
    ):
        return AnimationGroup(
            self.ft_conv.breath(**aargs),
            self.ft_bn.breath(**aargs),
            lag_ratio=0.0,
        )

    def tarnish(
        self,
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ft_conv.tarnish(),
            self.ft_bn.tarnish(),
            **aargs,
        )

    def lightup(
        self,
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ft_conv.lightup(),
            self.ft_bn.lightup(),
            **aargs,
        )
    
    def uncreate(
        self,
        ref: str = 'center',
        **aargs,
    ) -> AnimationGroup:
        return AnimationGroup(
            self.ft_conv.uncreate(ref=ref, **aargs),
            self.ft_bn.uncreate(ref=ref, **aargs),
            lag_ratio=0.0,
            _on_finish=lambda s: s.remove(self),
        )
    
    # def stretch_direction(
    #     self,
    #     direction: str = 'erect',           # horizontal/erect
    #     size_scale: float | None = None,    # for mobs_conv
    #     size_target: float | None = 2.0,    # for mobs_conv
    #     shape: tuple | None = None,         # for mobs_conv
    #     **aargs,
    # ) -> AnimationGroup:
    #     """Apply stretch_direction on mobs_conv.
    #        Regap mobs_bn if kernel_size is changed.
    #     """
    #     return self.mobs_conv.stretch_direction(
    #         direction=direction,
    #         size_scale=size_scale,
    #         size_target=size_target,
    #         keep_gap=False,
    #         shape=shape,
    #         rate_func=smooth,
    #         **aargs,
    #     )

    # def stretch_blocks(
    #     self,
    #     diff: int = 1,                      # -n / n
    #     direction: str = 'center',          # top/center/bottom
    #     shape: tuple | None = None,         # for mobs_conv
    #     **aargs,
    # ) -> AnimationGroup:
    #     """Apply stretch_blocks on mobs_conv and mobs_bn.
    #     """
    #     return AnimationGroup(
    #         self.mobs_conv.stretch_blocks(
    #             diff=diff,
    #             direction=direction,
    #             shape=shape,
    #             **aargs,
    #         ),
    #         self.mobs_bn.stretch_blocks(
    #             diff=diff,
    #             direction=direction,
    #             shape=shape[:1]+self.mobs_bn.shape[1:],
    #             **aargs,
    #         ),
    #         lag_ratio=0.0,
    #     )

    @property
    def conv_bn(self):
        return VGroup(self.ft_conv, self.ft_bn)

    @property
    def mobs(self):
        return VGroup(*self.ft_conv.mobs, *self.ft_bn.mobs)

    @property
    def tensor_gap(self):
        return self.ft_conv[0].get_bottom()[1] - self.ft_bn[0].get_top()[1]

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

wt = 0.5
class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        uconv = UT_Conv(
            module_config={
                'c1': 16,
                'c2': 16,
                'k': 3,
            },
            size_config_conv={
                'depth': 8*UNIT_FTENSOR_SIZE,
            },
        )
        self.play(uconv.create(
            ref='bottom',
            rate_func=smooth,
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()

        self.play(uconv.breath(
            rate_func=smooth,
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()
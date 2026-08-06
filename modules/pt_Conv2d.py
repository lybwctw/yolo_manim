from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

import numpy as np

# ----------------- config --------------------
# 'in_channels': UNKNOWN,
# 'out_channels': UNKNOWN,
# 'kernel_size': UNKNOWN,
# 'stride': UNKNOWN,
# 'padding': UNKNOWN,
# 'bias': UNKNOWN,
# 'dilation': UNKNOWN,
# 'groups': UNKNOWN,
# 'padding_mode': UNKNOWN,
# ---------------------------------------------

DEFAULT_WEIGHT_CONFIG = SMALL_4D_CUBE_CONFIG
DEFAULT_BIAS_CONFIG = SMALL_1D_CUBE_CONFIG

class PT_Conv2d(VMobject):
    def __init__(
        self,
        module,                         # torch module
        module_config: dict = {},       # torch module config
        weight_config: dict = {},       # weight, 4d
        bias_config: dict = {},         # bias, 1d
        bias_offset: float = 1.0,       # bias offset to weight
    ):
        super().__init__()
        self.module = module
        self.module_config = module_config
        self.weight_config = weight_config
        self.bias_config = bias_config
        self.bias_offset = bias_offset

        # init weight mobs
        mobs_weight = MTensor4D(
            array=self.module.weight.detach().numpy(),
            **{**DEFAULT_WEIGHT_CONFIG, **weight_config},
        )
        self.mobs_weight = mobs_weight
        self.add(self.mobs_weight)

        # maybe init bias mobs
        if self.module_config['bias']:
            mobs_bias = MTensor1D(
                array=self.module.bias.detach().numpy(),
                **{**DEFAULT_BIAS_CONFIG, **bias_config},
            )
            # align bias to weight
            for i, mob in enumerate(mobs_bias.get_mobs()):
                mob.next_to(self.mobs_weight[i], DOWN, self.bias_offset)
            self.mobs_bias = mobs_bias
            self.add(self.mobs_bias)
    
    def create(
        self,
        style='layer',
        direction=OUT,
        anim=Create,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> AnimationGroup:
        anims = []
        anims.append(self.mobs_weight.create(
            style=style,
            direction=direction,
            anim=anim,
            aargs=aargs,
            gargs=gargs,
            ggargs=ggargs,
        ))
        if self.module_config['bias']:
            anims.append(self.mobs_bias.create(
                direction=RIGHT,        # always right direction
                anim=anim,
                aargs=aargs,
                gargs=ggargs,
            ))
        return Succession(*anims)
    
    # def switch_mode(
    #     self,
    #     style: str = 'layer',
    #     direction: np.ndarray = OUT,
    #     aargs: dict = {},
    #     gargs: dict = {},
    #     ggargs: dict = {},
    # ) -> Animation:
    #     anims = []
    #     anims.append(AnimationGroup(
    #         *(tensor.switch_mode(
    #             style=style,
    #             direction=direction,
    #             aargs=aargs,
    #             gargs=gargs,
    #         ) for tensor in self.mobs_weight),
    #         **ggargs,
    #     ))

    #     if self.module_config['bias']:
    #         anims.append(AnimationGroup(
    #             *(tensor.switch_mode(
    #                 style=style,
    #                 direction=direction,
    #                 aargs=aargs,
    #                 gargs=gargs,
    #             ) for tensor in self.mobs_bias),
    #             **ggargs,
    #         ))
    #     return Succession(*anims)
    
    # def get_shape_path(
    #     self,
    #     **path_config,
    # ) -> VMobject:
    #     path = VMobject().set_z_index(self.shape[0])
    #     path.set_points_as_corners([
    #         self.mobs[-1].get_corner(DOWN + RIGHT + IN),
    #         self.mobs[0].get_corner(DOWN + LEFT + IN),
    #         self.mobs[0].get_corner(DOWN + LEFT + OUT),
    #         self.mobs[0].get_corner(UP + LEFT + OUT),
    #         self.mobs[0].get_corner(UP + RIGHT + OUT),
    #     ]).set_stroke(**path_config)
    #     return path

    # def get_shape_text(
    #     self,
    #     **text_config,
    # ) -> VGroup:
    #     buff = text_config.pop('buff', 0.25)

    #     texts = VGroup()
    #     for i in range(4):
    #         text = Text(
    #             str(self.shape[i]),
    #             **text_config,
    #         ).next_to(
    #             self.ref_point(i),
    #             self.ref_direction(i),
    #             buff=self.ref_buff(i, buff),
    #         )
    #         self.rotate_shape(text, i)
    #         texts.add(text)
    #     return texts
    
    # def ref_point(
    #     self,
    #     index: int,     # 0/1/2/3
    # ) -> Point:
    #     if index == 0:
    #         p1 = self.mobs[0].get_corner(DL + IN)
    #         p2 = self.mobs[-1].get_corner(DR + IN)
    #         pm = (p1 + p2) / 2
    #     elif index == 1:
    #         pm = self.mobs[0].get_corner(DL)
    #     elif index == 2:
    #         pm = self.mobs[0].get_corner(LEFT + OUT)
    #     elif index == 3:
    #         pm = self.mobs[0].get_corner(UP + OUT)
    #     return pm

    # def ref_direction(
    #     self,
    #     index: int,     # 0/1/2/3
    # ):
    #     if index == 0:
    #         direction = DOWN
    #     elif index == 1:
    #         direction = LEFT
    #     elif index == 2:
    #         direction = OUT + LEFT
    #     elif index == 3:
    #         direction = OUT + UP
    #     return direction
    
    # def ref_buff(
    #     self,
    #     index: int,     # 0/1/2/3
    #     buff: float,
    # ) -> float:
    #     if index == 0:
    #         return buff
    #     elif index == 1:
    #         return buff
    #     elif index == 2:
    #         return buff*.8
    #     elif index == 3:
    #         return buff*.8

    # def rotate_shape(
    #     self,
    #     mob,
    #     index: int,     # 0/1/2/3
    # ):
    #     if index == 1:
    #         mob.rotate(90*DEGREES, axis=RIGHT)
    #     elif index == 2:
    #         mob.rotate(90*DEGREES, axis=RIGHT)
    #         # mob.rotate(90*DEGREES, axis=OUT)
    #     elif index == 3:
    #         mob.rotate(90*DEGREES, axis=RIGHT)
    
    # @property
    # def weight(self) -> np.ndarray:
    #     return self.module.weight.numpy()
    
    # @property
    # def bias(self) -> np.ndarray:
    #     return self.module.bias.numpy()

    # @property
    # def weight_shape(self):
    #     return self.weight.shape

    # @property
    # def bias_shape(self):
    #     return self.bias.shape

class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=75*DEGREES,
            theta=-75*DEGREES,
        )
        # self.begin_ambient_camera_rotation(
        #     rate=0.1,
        # )

        pt_conv2d = PT_Conv2d(
            array=np.random.rand(5, 4, 3, 3),
            size=0.3,
            mode='cube',
            padding=0.0,
        )
        self.play(pt_conv2d.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={
                'lag_ratio': 0.1,
                'run_time': 1.0,
            },
        ))
        self.add(pt_conv2d)     # FIXME, manual add after creation
        pt_conv2d.add_updater(
            lambda m, dt: m.rotate(5 * DEGREES * dt)
        )
        self.wait(1.0)
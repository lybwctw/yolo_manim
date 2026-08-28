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

DEFAULT_WEIGHT_CREATE_ARGS = {
    'style': 'beam',
    'direction': OUT,
    'lag_ratio': 0.5,
}
DEFAULT_BIAS_CREATE_ARGS = {
    'style': 'series',
    'direction': RIGHT,
}

class PT_Conv2d(VMobject):
    """Visualization of torch.nn.Conv2d.
    """
    def __init__(
        self,
        module,                         # torch module
        module_config: dict = {},       # torch module config
        weight_config: dict = {},       # weight, 4d
        bias_config: dict = {},         # bias, 1d
        block_gap: float = 1.0,         # weight block gap
        bias_offset: float = 1.0,       # bias offset to weight
        init_mode: str = 'cube',
    ):
        super().__init__()
        self.module = module
        self.module_config = module_config
        self.weight_config = weight_config
        self.bias_config = bias_config
        self.block_gap = block_gap
        self.bias_offset = bias_offset

        # init weight
        rt_weight = self.module.weight.detach()
        mt_weight = MTensor4D(
            block_gap=self.block_gap,
            array=rt_weight,
            mode=init_mode,
            style='horizontal',
            **{**SMALL_TENSOR_CONFIG, **self.weight_config},
        )
        self.rt_weight = rt_weight
        self.mt_weight = mt_weight
        self.add(self.mt_weight)

        # init bias (maybe)
        if self.module_config['bias']:
            rt_bias = self.module.bias.detach()
            mt_bias = MTensor1D(
                array=rt_bias,
                mode=init_mode,
                style='horizontal',
                **{**SMALL_TENSOR_CONFIG, **self.bias_config},
            )
            # align bias to weight
            for i, mob in enumerate(mt_bias.mobs):
                mob.next_to(self.mt_weight[i], DOWN, self.bias_offset)
            self.mt_bias = mt_bias
            self.add(self.mt_bias)
    
    def create(
        self,
        wargs: dict = {},       # 4d weight mtensor create args
        bargs: dict = {},       # 1d bias mtensor create args
        **aargs,                # lag_ratio, run_time
    ) -> AnimationGroup:
        anims = []
        anims.append(self.mt_weight.create(
            **{**DEFAULT_WEIGHT_CREATE_ARGS, **wargs},
        ))
        if self.module_config['bias']:
            anims.append(self.mt_bias.create(
                **{**DEFAULT_BIAS_CREATE_ARGS, **bargs},
            ))
        return AnimationGroup(
            *anims,
            **aargs,
        )
    
class Demo(ThreeDScene):
    def construct(self):
        conv2d_config = {
            'in_channels': 5,
            'out_channels': 4,
            'kernel_size': 3,
            'stride': 1,
            'padding': 1,
            'bias': True,
        }

        self.set_camera_orientation(
            **VIEW_INTRO,
        )

        rm_conv2d = torch.nn.Conv2d(**conv2d_config)
        mm_conv2d = PT_Conv2d(
            module=rm_conv2d,
            module_config=conv2d_config,
            block_gap=0.5,
            bias_offset=0.5,
        )

        self.play(mm_conv2d.create(
            lag_ratio=0.5,
            run_time=1.0,
        ))

        self.move_camera(
            **VIEW_COMPUTE,
        )
        self.wait()
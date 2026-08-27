from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

# ----------------- config --------------------
# 'num_features': UNKNOWN,
# 'eps': UNKNOWN,
# 'momentum': UNKNOWN,
# 'affine': UNKNOWN,
# 'track_running_stats': UNKNOWN,
# ---------------------------------------------

DEFAULT_MTENSOR_CREATE_ARGS = {
    'style': 'series',
    'direction': RIGHT,
}

class PT_BatchNorm2d(VMobject):
    def __init__(
        self,
        module,                         # torch module
        module_config: dict = {},       # torch module config
        running_mean_config: dict = {}, # running_mean, 1d
        running_var_config: dict = {},  # running_var, 1d
        weight_config: dict = {},       # weight, 1d
        bias_config: dict = {},         # bias, 1d
        mtensor_dir: np.ndarray = RIGHT,# arrange direction
        mtensor_gap: float = 0.5,       # arrange buff
    ):
        super().__init__()
        self.module = module
        self.module_config = module_config
        self.running_mean_config = running_mean_config
        self.running_var_config = running_var_config
        self.weight_config = weight_config
        self.bias_config = bias_config
        self.mtensor_dir = mtensor_dir
        self.mtensor_gap = mtensor_gap

        # init buffers
        rt_running_mean = self.module.running_mean
        rt_running_var = self.module.running_var
        mt_running_mean = MTensor1D(
            array=rt_running_mean,
            mode='cube',
            style='erect',
            **{**SMALL_TENSOR_CONFIG, **self.running_mean_config},
        )
        mt_running_var = MTensor1D(
            array=rt_running_var,
            mode='cube',
            style='erect',
            **{**SMALL_TENSOR_CONFIG, **self.running_var_config},
        )
        self.rt_running_mean = rt_running_mean
        self.rt_running_var = rt_running_var
        self.mt_running_mean = mt_running_mean
        self.mt_running_var = mt_running_var
        self.add(self.mt_running_mean)
        self.add(self.mt_running_var)

        # init parameters
        rt_weight = self.module.weight.detach()
        rt_bias = self.module.bias.detach()
        mt_weight = MTensor1D(
            array=rt_weight,
            mode='cube',
            style='erect',
            **{**SMALL_TENSOR_CONFIG, **self.weight_config},
        )
        mt_bias = MTensor1D(
            array=rt_bias,
            mode='cube',
            style='erect',
            **{**SMALL_TENSOR_CONFIG, **self.bias_config},
        )
        self.rt_weight = rt_weight
        self.rt_bias = rt_bias
        self.mt_weight = mt_weight
        self.mt_bias = mt_bias
        self.add(self.mt_weight)
        self.add(self.mt_bias)

        # arrange 4 mtensors
        VGroup(
            self.mt_running_mean,
            self.mt_running_var,
            self.mt_weight,
            self.mt_bias,
        ).arrange(
            direction=self.mtensor_dir,
            buff=self.mtensor_gap,
        )

    def create(
        self,
        targs: dict = {},       # 1d mtensor create args
        **aargs,                # lag_ratio, run_time
    ) -> AnimationGroup:
        anims = AnimationGroup(
            *(mt.create(
                **{**DEFAULT_MTENSOR_CREATE_ARGS, **targs},
            ) for mt in [
                self.mt_running_mean,
                self.mt_running_var,
                self.mt_weight,
                self.mt_bias,
            ]),
            **aargs,
        )
        return anims

class Demo(ThreeDScene):
    def construct(self):
        bn2_config = {
            'num_features': 9,
            'eps': 1e-5,
            'momentum': 0.1,
            'affine': True,
            'track_running_stats': True,
        }

        self.set_camera_orientation(
            **VIEW_INTRO,
        )

        rm_bn2 = torch.nn.BatchNorm2d(**bn2_config)
        mm_bn2 = PT_BatchNorm2d(
            module=rm_bn2,
            module_config=bn2_config,
            mtensor_dir=RIGHT,
        )

        self.play(mm_bn2.create(
            lag_ratio=0.5,
            run_time=1.0,
        ))

        self.move_camera(
            **VIEW_COMPUTE,
        )
        self.wait()
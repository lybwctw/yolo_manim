from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *

from modules.pt_Conv2d import *

import torch

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0
BIAS_GAP_BIG = 2.0
BIAS_GAP_SMALL = 0.8

NEW_CONFIG = {
    'in_channels': 4,
    'out_channels': 7,          # updated
    'kernel_size': 2,           # updated
    'stride': 1,
    'padding': 1,
    'bias': True,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load cards and input
        (
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        ) = import_mobs('032o')

        # raw module and manim module
        module_config = NEW_CONFIG
        torch_module = torch.nn.Conv2d(**module_config)
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=module_config,
            block_gap=0.5,
            bias_offset=BIAS_GAP_SMALL,
        ).center()
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # raw tensor
        t_i1 = mob_i1.tensor[None,:]        # manual new dim
        t_o1 = torch_module(t_i1)           # final output

        # new output tensor mob
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_module,
            DOWN,
            TENSOR_VGAP_3D,
        )

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.add(mob_i1)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show new module (weight+bias) and card',
            skip_animations=False,
        )
        # ************************************************************
        # new module params
        # NOTE: assert that only out_channels/kernel_size changes
        self.play(card_module.update_params(
            params={
                'out_channels': module_config['out_channels'],
                'kernel_size': module_config['kernel_size'],
            },
            run_time=wt,
        ))

        # show new module
        self.play(AnimationGroup(
            mob_module.create(
                wargs={'run_time': wt},
                bargs={'run_time': wt},
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute loop, breath style',
            skip_animations=False,
        )
        # ************************************************************
        # NOTE: pad and unpad skipped

        # apply weight and bias
        self.play(AnimationGroup(
            mob_weight.breath(
                style='whole',
                rate_func=smooth,       # sync with default
                lag_ratio=0.5,          # sync with default
                run_time=wt*3,
            ),
            mob_bias.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_o1.create(
                style='layer',
                direction=IN,
                # rate_func=smooth,     # smooth by default
                # lag_ratio=1.0,        # 0.5 by default
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))

        # output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean input/output',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output
        self.play(AnimationGroup(
            *(AnimationGroup(
                mob.uncreate(
                    style='beam',
                    direction=IN,
                    anim=Unwrite,
                ),
                card.shrink_summary(),
                lag_ratio=0.5,
            ) for mob, card in zip(
                [mob_i1, mob_o1],
                [card_i1, card_o1],
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_module,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
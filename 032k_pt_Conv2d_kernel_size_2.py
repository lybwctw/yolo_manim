from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *

from modules.pt_Conv2d import *

import torch

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

NEW_CONFIG = {
    'in_channels': 3,
    'out_channels': 7,
    'kernel_size': 4,
    'stride': 1,
    'padding': 1,
    'bias': False,
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
            skip_animations=True,
        )
        # ************************************************************
        # load cards and input
        (
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        ) = import_mobs('032j')

        # raw module and manim module
        module_config = NEW_CONFIG
        torch_module = torch.nn.Conv2d(**module_config)
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=module_config,
            block_gap=0.5,
            bias_offset=0.5,
        )
        mob_weight = mob_module.mt_weight

        # new raw output tensor
        t_i1 = mob_i1.tensor[None,:]    # FIXME: manual new dim
        t_o1 = torch_module(t_i1)

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
            'show new module weight and card',
            skip_animations=True,
        )
        # ************************************************************
        # new module params
        # NOTE: assert that only kernel_size changes
        self.play(card_module.update_params(
            params={
                'kernel_size': module_config['kernel_size'],
            },
            run_time=wt,
        ))

        # show new weight
        self.play(mob_module.create(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'pad before compute',
            skip_animations=True,
        )
        # ************************************************************
        self.play(mob_i1.pad(
            pad_width=(
                0,
                module_config['padding'],
                module_config['padding'],
            ),
            pad_value=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'layer compute loop (breath style)',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_weight.breath(
                style='whole',
                rate_func=smooth,           # sync with default
                lag_ratio=0.5,              # sync with default
            ),
            mob_o1.create(
                style='layer',
                direction=IN,
                # rate_func=smooth,         # smooth by default
                # lag_ratio=1.0,            # 0.5 by default
            ),
            lag_ratio=0.1,
            run_time=wt*3,
        ))
        self.wait(wt)

        # unpad input tensor
        self.play(mob_i1.unpad(
            run_time=wt,
        ))
        self.wait(wt)

        # output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean module weight and output',
            skip_animations=False,
        )
        # ************************************************************
        # clean output and summary
        self.play(AnimationGroup(
            mob_o1.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean module weight
        self.play(mob_weight.uncreate(
            style='beam',
            direction=IN,
            anim=Unwrite,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
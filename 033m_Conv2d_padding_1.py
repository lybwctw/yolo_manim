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
    'out_channels': 5,
    'kernel_size': 3,
    'stride': 2,
    'padding': 2,
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
            mob_module,     # reuse module mob
        ) = import_mobs('032l')

        # raw module and manim module
        module_config = NEW_CONFIG
        torch_module = torch.nn.Conv2d(**module_config)
        mob_module.module_config = module_config
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
        self.add(
            mob_i1,
            mob_module,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'new module card',
            skip_animations=True,
        )
        # ************************************************************
        # new module params
        # NOTE: assert that only padding changes
        self.play(card_module.update_params(
            params={
                'padding': module_config['padding'],
            },
            run_time=wt,
        ))

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
            'beam compute loop',
            skip_animations=True,
        )
        # ************************************************************
        masks_input = mob_i1.conv2d_masks(
            kh=module_config['kernel_size'],
            kw=module_config['kernel_size'],
            sh=module_config['stride'],
            sw=module_config['stride'],
        )
        c, h, w = mob_o1.shape
        masks_output = np.eye(
            h*w,
            dtype=bool,
        ).reshape(
            h*w,
            h,
            w,
        )[:,None,...].repeat(
            c,
            1,
        )
        beams_output = mob_o1.get_vgs(masks_output)

        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input,
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in beam),
                    lag_ratio=0.0,
                ) for beam in beams_output),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*5,
        ))

        # ************************************************************
        self.next_section(
            'restore input',
            skip_animations=True,
        )
        # ************************************************************
        # restore input
        self.play(mob_i1.highlight(
            run_time=wt,
        ))

        # unpad input
        self.play(mob_i1.unpad(
            run_time=wt,
        ))
        self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean output',
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

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_i1,
            mob_module,         # reuse
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
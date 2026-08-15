from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
import torch

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load mobs and torch module
        (
            card_i1,
            card_module,
            card_o1,
            mob_module,
        ) = import_mobs('032c')
        mob_weight = mob_module.mt_weight
        torch_module = mob_module.module
        module_config = mob_module.module_config

        # raw tensor
        t_i1 = torch.randn(1, 6, 5, 8)
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_weight,
            UP,
            TENSOR_VGAP_3D,
        )

        # output tensor mob
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
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(6,5,8) -[Conv2d]- (5,5,8)',
            skip_animations=True,
        )
        # ************************************************************
        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        self.wait(wt)

        # show input summary
        self.play(card_i1.expand_summary(
            t2s(t_i1.detach()[0]),
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
            'layer compute loop',
            skip_animations=True,
        )
        # ************************************************************
        b, c, h, w = mob_weight.shape
        masks_weight = np.tile(
            np.eye(b, dtype=bool)[:, :, None, None, None],
            (1, c, h, w),
        )
        layers_output = mob_o1.get_layers(
            direction=IN,
        )

        self.play(AnimationGroup(
            mob_weight.highlight_loop(
                masks=masks_weight,
                back=False,
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in layer),
                    lag_ratio=0.0,
                ) for layer in layers_output),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'restore weight / input',
            skip_animations=True,
        )
        # ************************************************************
        # restore weight
        self.play(mob_weight.highlight(
            run_time=wt,
        ))

        # unpad input
        self.play(mob_i1.unpad(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'output summary',
            skip_animations=True,
        )
        # ************************************************************
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
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
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
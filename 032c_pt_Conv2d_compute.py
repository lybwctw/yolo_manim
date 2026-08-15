from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
import torch
import numpy as np

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load mobs and torch module
        card_module, mob_module = import_mobs('032b')
        mob_weight = mob_module.mt_weight
        torch_module = mob_module.module
        module_config = mob_module.module_config

        # raw tensor
        t_i1 = torch.randn(1, 6, 4, 7)
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
        self.add_fixed_in_frame_mobjects(card_module)
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(6,4,7) -[Conv2d]- (5,4,7)',
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
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i1)
        self.play(attach_to_ref(
            card_i1,
            card_module,
            UP,
            run_time=wt,
        ))
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

        # NOTE: switch mode to show exact pad value?

        # ************************************************************
        self.next_section(
            'first compute',
            skip_animations=True,
        )
        # ************************************************************
        b, c, h, w = mob_weight.shape
        masks_weight = np.tile(
            np.eye(b, dtype=bool)[:, :, None, None, None],
            (1, c, h, w),
        )
        masks_input = mob_i1.conv2d_masks(
            kh=module_config['kernel_size'],
            kw=module_config['kernel_size'],
            sh=module_config['stride'],
            sw=module_config['stride'],
        )
        layers_output = mob_o1.get_layers(
            direction=IN,
        )

        # highlight first weight block
        self.play(mob_weight.highlight(
            mask=masks_weight[0],
            run_time=wt,
        ))
        self.wait(wt)

        # highlight first input subblock
        self.play(mob_i1.highlight(
            mask=masks_input[0],
            run_time=wt,
        ))
        self.wait(wt)

        # generate first output
        self.play(GrowFromCenter(
            layers_output[0][0],
            rate_func=rate_functions.ease_out_back,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'the rest of compute loop for first layer',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input[1:],
                rate_func=smooth,
            ),
            Succession(
                *(GrowFromCenter(
                    mob,
                    rate_func=rate_functions.ease_out_back,
                ) for mob in layers_output[0][1:]),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute loop for other layers',
            skip_animations=True,
        )
        # ************************************************************
        for b_idx in range(1, b):
            # fade previous output layer
            self.play(AnimationGroup(
                *(mob.tarnish() for mob in layers_output[b_idx-1]),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

            # highlight current weights block
            self.play(mob_weight.highlight(
                mask=masks_weight[b_idx],
                run_time=wt,
            ))

            # generation loop
            self.play(AnimationGroup(
                mob_i1.highlight_loop(
                    masks=masks_input,
                    rate_func=smooth,
                ),
                Succession(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in layers_output[b_idx]),
                    rate_func=smooth,
                ),
                lag_ratio=0.0,
                run_time=wt*3,
            ))
            self.wait(wt)

        # ************************************************************
        self.next_section(
            'restore output / weight / input',
            skip_animations=True,
        )
        # ************************************************************
        # restore output
        self.play(AnimationGroup(
            *(mob.lightup() for mob in mob_o1[:-1]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # restore weight
        self.play(mob_weight.highlight(
            run_time=wt,
        ))

        # restore input
        self.play(mob_i1.highlight(
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
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1)
        self.play(attach_to_ref(
            card_o1,
            card_module,
            DOWN,
            run_time=wt,
        ))
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'shape matching again',
            skip_animations=False,
        )
        # ************************************************************
        # shape of input/weight/output
        self.play(AnimationGroup(
            *(ShowShape3D(
                scene=self,
                mob=mob,
                view='compute',
                lag_ratio=0.5,
            ) for mob in [
                mob_i1,
                mob_weight,
                mob_o1,
            ]),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # in_channels
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                 card_module.value_objs['in_channels'],
                 mob_i1.shape_texts[0],
                 mob_weight.shape_texts[1],
             ]),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # out_channels
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                 card_module.value_objs['out_channels'],
                 mob_weight.shape_texts[0],
                 mob_o1.shape_texts[0],
             ]),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape3D(
                mob=mob,
                lag_ratio=0.0,
            ) for mob in [
                mob_i1,
                mob_weight,
                mob_o1,
            ]),
            lag_ratio=0.0,
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
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

TENSOR_VGAP_3D = 1.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

EMPTY_CONFIG = {
    'kernel_size': UNKNOWN,
    'stride': UNKNOWN,
    'padding': UNKNOWN,
    'dilation': UNKNOWN,
}

INIT_CONFIG = {
    'kernel_size': 2,
    'stride': 1,
    'padding': 1,
    'dilation': 1,
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('033a')

        # raw module, no visible module
        module_config = INIT_CONFIG
        torch_module = torch.nn.MaxPool2d(**module_config)

        # raw tensor
        t_i1 = torch.randn(1, 6, 4, 7)
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            TENSOR_VGAP_3D*UP,
            DOWN,
        )

        # output tensor mob
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            TENSOR_VGAP_3D*DOWN,
            UP,
        )

        # ************************************************************
        self.next_section(
            'starting module card',
            skip_animations=True,
        )
        # ************************************************************
        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # expand empty module card
        self.play(card_module.expand_params(
            params=EMPTY_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # update module card config
        self.play(card_module.update_params(
            module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=True,
        )
        # ************************************************************
        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        # self.wait(wt)

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
            pad_value=-np.inf,
            stroke_color=PURPLE,
            run_time=wt,
        ))
        self.wait(wt)

        # # focus on input tensor
        # self.move_camera(
        #     **VIEW_INTRO,
        #     frame_center=mob_i1.get_center(),
        #     zoom=1.7,
        # )
        # self.wait(wt)

        # # switch to show -inf
        # self.play(mob_i1.switch(
        #     style='beam',
        #     direction=IN,
        #     run_time=wt*3,
        # ))
        # self.wait(wt)

        # # switch back
        # self.play(mob_i1.switch(
        #     style='beam',
        #     direction=OUT,
        #     run_time=wt*3,
        # ))
        # self.wait(wt)

        # # focus back
        # self.move_camera(
        #     **VIEW_COMPUTE,
        #     frame_center=ORIGIN,
        #     zoom=1.0,
        # )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'first compute',
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
        masks_output = np.eye(h*w, dtype=bool).reshape(h*w,h,w)[:,None,:,:].repeat(c,1)
        beams_output = mob_o1.get_vgs(masks_output)

        # highlight first input subblock
        self.play(mob_i1.highlight(
            mask=masks_input[0],
            run_time=wt,
        ))
        self.wait(wt)

        # generate first output beam
        self.play(AnimationGroup(
            *(GrowFromCenter(
                mob,
                rate_func=rate_functions.ease_out_back,
            ) for mob in beams_output[0]),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'the rest of compute loop',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input[1:],
                rate_func=smooth,
                run_time=wt*5,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in beam),
                    lag_ratio=0.5,
                ) for beam in beams_output[1:]),
                rate_func=smooth,
                run_time=wt*5,
            ),
            lag_ratio=0.0,
            # run_time=wt*5,
        ))
        self.wait(wt)

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
            'clean output',
            skip_animations=False,
        )
        # ************************************************************
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
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
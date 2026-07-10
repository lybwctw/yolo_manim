from manim import *

from utils.general import import_mobs, export_mobs
from utils.mtensor import MTensor_3D
from utils.constants_3d import *
from utils.constants import *
import torch

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        mobs = import_mobs('028')
        (
            card, m_module
        ) = mobs

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card)
        self.add(m_module)
        self.wait(wt)

        # fade module card
        card.save_state()
        self.play(card.animate(
            run_time=wt,
        ).fade(0.5))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=True,
        )
        # ************************************************************
        t_input = torch.randn(1, 6, 3, 3)
        m_input = MTensor_3D(
            array=t_input[0].numpy(),
            **BIG_3D_CONFIG,
        ).shift(UP*3.5)
        self.play(m_input.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop compute into output',
            skip_animations=False,
        )
        # ************************************************************
        t_output = m_module.module(t_input)
        m_output = MTensor_3D(
            array=t_output.detach().numpy()[0],
            **BIG_3D_CONFIG,
        ).shift(DOWN*3.5)

        # pad input
        self.play(m_input.pad(
            padding=m_module.module_config['padding'],
            pad_value=0.0,
            aargs={'run_time': wt},
        ))
        self.wait()

        # prepare masks of input
        masks = m_input.create_conv2d_masks(
            conv2d_config=m_module.module_config,
        )

        # loop into output
        layers_output = []
        for i in range(m_output.shape[0]):
            # highlight module part
            self.play(m_module.mobs_weight.highlight_block(
                direction=RIGHT,
                n=i,
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

            for mask, (j,k) in zip(masks, np.ndindex(m_output.shape[1:])):
                # highlight input part
                self.play(m_input.highlight(
                    mask=mask,
                    run_time=0.2,
                ))
                self.wait(0.2)

                # create output part
                self.play(Write(
                    m_output[i,j,k],
                    run_time=0.2,
                ))
                self.wait(0.2)

            # fade current layer except the last
            if i != m_output.shape[0]-1:
                layer = m_output[i].save_state()
                self.play(layer.animate(
                    run_time=wt,
                ).fade(0.9))
                layers_output.append(layer)
        
        # unfade output layers
        self.play(AnimationGroup(
            *(layer.animate.restore() for layer in layers_output[::-1]),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # unfade module blocks
        self.play(m_module.highlight(
            mask=None,
            run_time=wt,
        ))

        # unpad input tensor
        self.play(m_input.unpad(
            aargs={'lag_ratio': 0.0, 'run_time': wt},
        ))

        self.wait(wt)
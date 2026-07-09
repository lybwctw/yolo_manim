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
            skip_animations=False,
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
            skip_animations=False,
        )
        # ************************************************************
        t_input = torch.randn(1, 6, 7, 7)
        m_input = MTensor_3D(
            array=t_input[0],
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
            'introduce output',
            skip_animations=False,
        )
        # ************************************************************
        t_output = m_module.module(t_input)
        m_output = MTensor_3D(
            array=t_output[0],
            **BIG_3D_CONFIG,
        ).shift(DOWN*3.5)
        self.play(m_output.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
        ))
        self.wait(wt)
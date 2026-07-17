from manim import *

from utils.general import import_mobs, export_mobs
from utils.mtensor import MTensor_3D
from utils.info_card import NameCard
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
        mobs = import_mobs('029')
        (
            card_module,
            m_input,
            m_module,
            m_output,
        ) = mobs

        card_input = NameCard(
            name='Input',
            params={
                'channels': m_input.array.shape[0],
                'height': m_input.array.shape[1],
                'weight': m_input.array.shape[2],
            },
            levels={
                'channels': 0,
                'height': 0,
                'weight': 0,
            },
        ).next_to(
            card_module,
            UP,
        ).align_to(
            card_module,
            LEFT,
        )

        card_output = NameCard(
            name='Output',
            params={
                'channels': m_output.array.shape[0],
                'height': m_output.array.shape[1],
                'weight': m_output.array.shape[2],
            },
            levels={
                'channels': 0,
                'height': 0,
                'weight': 0,
            },
        ).next_to(
            card_module,
            DOWN,
        ).align_to(
            card_module,
            LEFT,
        )

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        self.add_fixed_in_frame_mobjects(
            card_module,
        )
        self.add(m_input, m_module, m_output)
        self.wait(wt)

        self.play(card_module.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        self.add_fixed_in_frame_mobjects(
            card_input, card_output,
        )
        self.play(AnimationGroup(
            Create(card_input),
            Create(card_output),
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait(wt)

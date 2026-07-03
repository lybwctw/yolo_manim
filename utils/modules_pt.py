from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import MTensor

class PT_conv2d(VMobject):
    def __init__(
        self,
        array: np.ndarray,      # 4d np array
        size: float = 0.5,
        mode: str = 'card',
        padding: float = 0.1,
        buff: float = 0.3,
        cube_config: dict = {},
        square_config: dict = {},
        decimal_config: dict = {},
    ):
        super().__init__()
        mobs = VGroup(
            MTensor(
                array=x,
                size=size,
                mode=mode,
                padding=padding,
                cube_config=cube_config,
                square_config=square_config,
                decimal_config=decimal_config,
            ) for x in array
        ).arrange(RIGHT, buff=buff).center()

        self.mobs = mobs
        self.add(self.mobs)
    
    def create(
        self,
        style='layer',
        direction=OUT,
        anim=Create,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> AnimationGroup:
        return AnimationGroup(
            *(mob.create(
                style=style,
                direction=direction,
                anim=anim,
                aargs=aargs,
                gargs=gargs,
            ) for mob in self.mobs),
            **ggargs,
        )

class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=75*DEGREES,
            theta=-75*DEGREES,
        )
        # self.begin_ambient_camera_rotation(
        #     rate=0.1,
        # )

        pt_conv2d = PT_conv2d(
            array=np.random.rand(5, 4, 3, 3),
            size=0.3,
            mode='cube',
            padding=0.0,
        )
        self.play(pt_conv2d.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={
                'lag_ratio': 0.1,
                'run_time': 1.0,
            },
        ))
        self.add(pt_conv2d)     # FIXME, manual add after creation
        pt_conv2d.add_updater(
            lambda m, dt: m.rotate(5 * DEGREES * dt)
        )
        self.wait(1.0)
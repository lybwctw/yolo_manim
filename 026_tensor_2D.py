from manim import *
from utils.mtensor import MCube, MTensor_3D

class MainScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=60*DEGREES,
            theta=-75*DEGREES,
        )

        tensor = MTensor_3D(
            array=np.random.randn(5,3,3),
            mode='cube',
            size=0.3,
            padding=0.00,
        )

        self.play(tensor.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': 1.0},
        ))
        self.wait()

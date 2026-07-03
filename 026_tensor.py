from manim import *
from utils.mtensor import MCube, MTensor

class MainScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=60*DEGREES,
            theta=-75*DEGREES,
        )

        mtensor = MTensor(
            array=np.random.rand(3, 4, 5),
            size=0.6,
            mode='cube',
            padding=0.1,                   
        )
        # self.play(mtensor.create(
        #     style='beam',
        #     direction=OUT,
        #     anim=GrowFromCenter,
        #     aargs={'rate_func': rate_functions.ease_out_back},
        #     gargs={'run_time': 1.0},
        # ))
        self.add(mtensor)
        self.wait()

        # self.play(mtensor.uncreate(
        #     style='beam',
        #     direction=IN,
        #     anim=ShrinkToCenter,
        #     # aargs={'rate_func': rate_functions.ease_out_back},
        #     gargs={'run_time': 1.0},
        # ))
        # self.wait()

        # self.play(mtensor.highlight(
        #     mask=np.random.rand(3, 4, 5) > 0.5,
        #     lag_ratio=0.0,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(mtensor.highlight(
        #     mask=np.random.rand(3, 4, 5) < 0.3,
        #     lag_ratio=0.0,
        #     run_time=1.0,
        # ))
        # self.wait()
        self.play(mtensor.highlight_layer(
            direction=UP,
            n=1,
        ))
        self.wait()

        self.play(mtensor.highlight_beam(
            direction=DOWN,
            ij=(1, 2),
        ))
        self.wait()

        # mask = np.zeros((3, 4, 5), dtype=bool)
        # mask[2,3,4] = True
        # self.play(mtensor.highlight(
        #     mask=mask,
        # ))
        # self.wait()
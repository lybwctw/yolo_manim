from manim import *
from utils.mcube import MCube, CCMode

from manim.utils.rate_functions import ease_in_quart

class CubesFlash(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        cube_config = {'fill_color': BLACK}
        square_config = {'fill_color': BLACK}
        mcubes = MCube(
            np.random.randn(10,3,3),
            size=0.5,
            padding=0.01,
            mode=CCMode.CARD,
            cube_config=cube_config,
            square_config=square_config,
        )
        self.add(mcubes)
        self.wait()

        self.play(Succession(
            *(mcubes.highlight_channel(n) for n in range(mcubes.shape[0])),
            run_time=3,
            rate_func=ease_in_quart,
        ))

        self.play(Succession(
            *(mcubes.highlight((n,0,0),mcubes.shape) for n in range(mcubes.shape[0]-2,-1,-1)),
            run_time=1,
            rate_func=ease_in_quart,
        ))

        self.wait()

        self.stop_ambient_camera_rotation()
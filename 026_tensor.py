from manim import *
from utils.mcube import MCube, CCMode

class MainScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)

        cube_config = {'fill_color': BLACK}
        square_config = {'fill_color': BLACK}
        mcubes = MCube(
            np.random.randn(5,5,5),
            size=0.5,
            padding=0.01,
            mode=CCMode.CUBE,
            cube_config=cube_config,
            square_config=square_config,
        )

        self.play(mcubes.create(type='beam', direction=OUT))
        self.wait()

        self.play(mcubes.switch_mode(
            type='layer',
            direction=IN,
            in_anim=Create,
            out_anim=Uncreate,
        ))
        self.wait()

        self.play(mcubes.uncreate(
            type='layer',
            direction=IN,
            anim=Uncreate,
            run_time=2.0,
        ))
        self.wait()
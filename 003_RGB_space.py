from manim import *
from utils.colorcube import ColorCube
import itertools

# TODO, emphasize beams?
class MainScene(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        axes = ThreeDAxes(
            x_range=[0, 1.2],
            y_range=[0, 1.2],
            z_range=[0, 1.2],
            x_length=4,
            y_length=4,
            z_length=4,
        ).shift(IN * 1)
        axes_labels = axes.get_axis_labels(
            x_label='R',
            y_label='G',
            z_label='B',
        )
        self.play(Create(axes))
        self.play(Write(axes_labels))

        cubes = ColorCube(axis=axes)
        self.play(cubes.create(type='beam', direction=UP))
        self.wait()

        kpoints = np.full(cubes.shape, False, dtype=bool)
        kpoints[0,0,0] = True
        idxs = list(itertools.product([0,cubes.shape[0]-1],repeat=3))
        for idx in idxs:
            kpoints[idx] = True
        _mid = cubes.shape[0]//2
        kpoints[_mid,_mid,_mid] = True
        self.play(cubes.highlight(mask=kpoints))
        self.wait(3)
        self.play(cubes.highlight())

        self.play(cubes.uncreate(type='beam', direction=DOWN))
        self.play(Unwrite(axes), Unwrite(axes_labels))
        self.wait()

        self.stop_ambient_camera_rotation()
from manim import *
from utils.colorcube import ColorCube, SHOW_OPACITY, HIDE_OPACITY
from utils.constants import *
import itertools

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'create 3d axes with RGB labels',
            skip_animations=True,
        )
        # ************************************************************
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        # self.begin_ambient_camera_rotation(rate=0.1)
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
        axes_labels[0].set_color(PURE_RED).next_to(axes.axes[0], RIGHT)
        axes_labels[1].set_color(PURE_GREEN).next_to(axes.axes[1], UP)
        axes_labels[2].set_color(PURE_BLUE).next_to(axes.axes[2], OUT)
        self.play(Create(
            axes,
            run_time=wt,
        ))
        self.play(Write(
            axes_labels,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show cubes',
            skip_animations=True,
        )
        # ************************************************************
        cubes = ColorCube(
            axis=axes,
            shape=7,
            cube_config={
                'side_length': 0.20,
            },
        )
        self.play(cubes.create(
            type='beam',
            direction=UP,
            run_time=1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through red channels',
            skip_animations=False,
        )
        # ************************************************************
        # [1] hide from r=255 into r=0
        self.wait(wt)
        layers = cubes.get_layers(direction=LEFT)[:-1]  # keep r=0
        self.play(AnimationGroup(
            *(ApplyMethod(
                layer.set_fill,
                None,
                HIDE_OPACITY,
            ) for layer in layers),
            lag_ratio=0.5,
            run_time=1.0,
            rate_func=smooth,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'loop through green channels',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'loop through blue channels',
            skip_animations=False,
        )
        # ************************************************************

        # kpoints = np.full(cubes.shape, False, dtype=bool)
        # kpoints[0,0,0] = True
        # idxs = list(itertools.product([0,cubes.shape[0]-1],repeat=3))
        # for idx in idxs:
        #     kpoints[idx] = True
        # _mid = cubes.shape[0]//2
        # kpoints[_mid,_mid,_mid] = True
        # self.play(cubes.highlight(mask=kpoints))
        # self.wait(3)
        # self.play(cubes.highlight())

        # self.play(cubes.uncreate(type='beam', direction=DOWN))
        # self.play(Unwrite(axes), Unwrite(axes_labels))
        # self.wait()

        # self.stop_ambient_camera_rotation()
from manim import *
from utils.colorcube import ColorCube, SHOW_OPACITY, HIDE_OPACITY
from utils.constants import *

N_CUBES = 7

KEY_IDXS = [
    (0, 0, 0),
    (N_CUBES-1, 0, 0),
    (0, N_CUBES-1, 0),
    (0, 0, N_CUBES-1),
    (N_CUBES-1, N_CUBES-1, 0),
    (N_CUBES-1, 0, N_CUBES-1),
    (0, N_CUBES-1, N_CUBES-1),
    (N_CUBES-1, N_CUBES-1, N_CUBES-1),
    ((N_CUBES-1)//2, (N_CUBES-1)//2, (N_CUBES-1)//2),
]
KEY_LABELS = [
    '(0,0,0)',
    '(255,0,0)',
    '(0,255,0)',
    '(0,0,255)',
    '(255,255,0)',
    '(255,0,255)',
    '(0,255,255)',
    '(255,255,255)',
    '(128,128,128)',
]

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        # setup 3d axes and labels
        axes = ThreeDAxes(
            x_range=[0, 1.2],
            y_range=[0, 1.2],
            z_range=[0, 1.2],
            x_length=4,
            y_length=4,
            z_length=4,
        ).shift(IN * 1.5)
        axes_labels = axes.get_axis_labels(
            x_label='R',
            y_label='G',
            z_label='B',
        )
        axes_labels[0].set_color(PURE_RED).next_to(axes.axes[0], RIGHT)
        axes_labels[1].set_color(PURE_GREEN).next_to(axes.axes[1], UP)
        axes_labels[2].set_color(PURE_BLUE).next_to(axes.axes[2], OUT)
        
        # setup cubes
        cubes = ColorCube(
            axis=axes,
            shape=N_CUBES,
            cube_config={
                'side_length': 0.20,
            },
        )

        # setup labels for key cubes
        label_mobs = VGroup(
            Text(
                text=label,
                font='JetBrains Mono',
                font_size=12,
            ).next_to(cubes[idx], OUT*1.0)
             for idx, label in zip(KEY_IDXS, KEY_LABELS)
        ).set_z_index(999)
        # self.add_fixed_orientation_mobjects(
        #     *label_mobs,
        # )

        # ************************************************************
        self.next_section(
            'create 3d axes with RGB labels',
            skip_animations=False,
        )
        # ************************************************************
        self.set_camera_orientation(
            phi=60*DEGREES,
            theta=-60*DEGREES,
            focal_distance=20,
        )
        self.play(Create(
            axes,
            run_time=wt,
        ))
        self.play(Write(
            axes_labels,
            run_time=wt,
        ))
        self.wait(wt)
        self.bring_to_back(axes, axes_labels)

        # ************************************************************
        self.next_section(
            'show cubes',
            skip_animations=False,
        )
        # ************************************************************
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
        self.play(Succession(
            *(ApplyMethod(layer.set_opacity, HIDE_OPACITY)
             for layer in layers),
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        # [2] single layer show from r=0 into r=255
        vg1 = cubes.get_layers(direction=RIGHT)[:-1]
        vg2 = cubes.get_layers(direction=RIGHT)[1:]
        self.play(Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.set_opacity, HIDE_OPACITY),
                ApplyMethod(show_mob.set_opacity, SHOW_OPACITY),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            run_time=wt,
            rate_func=rate_functions.smooth,
        ))
        self.wait(wt)

        # [3] single layer show from r=255 into r=0
        vg1 = cubes.get_layers(direction=LEFT)[:-1]
        vg2 = cubes.get_layers(direction=LEFT)[1:]
        self.play(Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.set_opacity, HIDE_OPACITY),
                ApplyMethod(show_mob.set_opacity, SHOW_OPACITY),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            run_time=wt,
            rate_func=rate_functions.smooth,
        ))
        self.wait(wt)

        # [4] show from r=0 into r=255
        layers = cubes.get_layers(direction=RIGHT)[1:]  # skip r=0
        self.play(Succession(
            *(ApplyMethod(layer.set_opacity, SHOW_OPACITY)
             for layer in layers),
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through green channels',
            skip_animations=False,
        )
        # ************************************************************
        # [1] hide from g=255 into r=0
        self.wait(wt)
        layers = cubes.get_layers(direction=DOWN)[:-1]  # keep g=0
        self.play(Succession(
            *(ApplyMethod(layer.set_opacity, HIDE_OPACITY)
             for layer in layers),
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        # [2] single layer show from g=0 into g=255
        vg1 = cubes.get_layers(direction=UP)[:-1]
        vg2 = cubes.get_layers(direction=UP)[1:]
        self.play(Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.set_opacity, HIDE_OPACITY),
                ApplyMethod(show_mob.set_opacity, SHOW_OPACITY),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            run_time=wt,
            rate_func=rate_functions.smooth,
        ))
        self.wait(wt)

        # [3] single layer show from g=255 into g=0
        vg1 = cubes.get_layers(direction=DOWN)[:-1]
        vg2 = cubes.get_layers(direction=DOWN)[1:]
        self.play(Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.set_opacity, HIDE_OPACITY),
                ApplyMethod(show_mob.set_opacity, SHOW_OPACITY),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            run_time=wt,
            rate_func=rate_functions.smooth,
        ))
        self.wait(wt)

        # [4] show from g=0 into g=255
        layers = cubes.get_layers(direction=UP)[1:]  # skip g=0
        self.play(Succession(
            *(ApplyMethod(layer.set_opacity, SHOW_OPACITY)
             for layer in layers),
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through blue channels',
            skip_animations=False,
        )
        # ************************************************************
        # [1] hide from b=255 into b=0
        self.wait(wt)
        layers = cubes.get_layers(direction=IN)[:-1]  # keep b=0
        self.play(Succession(
            *(ApplyMethod(layer.set_opacity, HIDE_OPACITY)
             for layer in layers),
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        # [2] single layer show from b=0 into b=255
        vg1 = cubes.get_layers(direction=OUT)[:-1]
        vg2 = cubes.get_layers(direction=OUT)[1:]
        self.play(Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.set_opacity, HIDE_OPACITY),
                ApplyMethod(show_mob.set_opacity, SHOW_OPACITY),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            run_time=wt,
            rate_func=rate_functions.smooth,
        ))
        self.wait(wt)

        # [3] single layer show from b=255 into b=0
        vg1 = cubes.get_layers(direction=IN)[:-1]
        vg2 = cubes.get_layers(direction=IN)[1:]
        self.play(Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.set_opacity, HIDE_OPACITY),
                ApplyMethod(show_mob.set_opacity, SHOW_OPACITY),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            run_time=wt,
            rate_func=rate_functions.smooth,
        ))
        self.wait(wt)

        # [4] show from b=0 into b=255
        layers = cubes.get_layers(direction=OUT)[1:]  # skip r=0
        self.play(Succession(
            *(ApplyMethod(layer.set_opacity, SHOW_OPACITY)
             for layer in layers),
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'key colors for practitioner',
            skip_animations=False,
        )
        # FIXME: flicker effect for black cube
        # ************************************************************
        key_mask = np.full(cubes.shape, False, dtype=bool)
        for idx in KEY_IDXS:
            key_mask[idx] = True

        # highlight key cubes
        self.play(AnimationGroup(
            cubes.highlight(mask=key_mask),
            axes.animate.set_opacity(0.2),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show labels for key cubes
        self.camera.add_fixed_orientation_mobjects(
            *label_mobs,
        )
        self.play(Write(
            label_mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # changing perspective and talk..
        self.begin_ambient_camera_rotation(
            rate=0.1,
            about='theta',
        )
        self.wait(1.0)      # TODO: proper duration
        # TODO: rotate R/G/B labels?
        self.stop_ambient_camera_rotation(
            about='theta',
        )
        self.wait(wt)
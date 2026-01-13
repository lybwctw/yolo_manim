from manim import *
from manim.utils.rate_functions import ease_in_out_circ


def simplify_axes_with_graph(axes, graph, name):
    tn_axes = Axes(
        x_range=axes.x_range,
        y_range=axes.y_range,
        x_length=axes.x_length,
        y_length=axes.y_length,
        tips=False,
        axis_config={
            "include_ticks": False,
            "include_numbers": False,
            "stroke_width": 3,
            "color": GRAY_D,
        },
    ).scale(0.12)
    tn_graph = tn_axes.plot(
        graph.underlying_function,
        x_range=(graph.t_min, graph.t_max, graph.t_step),
        color=graph.get_color(),
    )

    tn_name = name.copy().next_to(tn_axes, UP)

    return VGroup(tn_name, tn_axes, tn_graph)

class Sample(ThreeDScene):
    def construct(self) -> None:
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={
                "include_numbers": True,
                'font_size': 24,
                'tip_width': 0.2,
                'tip_height': 0.2,
            },
        )

        graph = axes.plot(
            lambda x: x * np.exp(x) / (1 + np.exp(x)),
            x_range=[-5, 4.5],
            color=MAROON,
            use_smoothing=False,
        )

        name = Text(
            'SiLU',
            font_size=24,
            font='JetBrains Mono',
        ).move_to(axes @ (-3, 3))

        orig_plot = VGroup(name, axes, graph)
        tn_plot = simplify_axes_with_graph(axes, graph, name)
        # tn_plot.to_corner(UR, buff=2)

        self.add(orig_plot)
        # self.play(Transform(orig_plot, tn_plot))
        self.play(AnimationGroup(
            ReplacementTransform(orig_plot[0], tn_plot[0]),
            ReplacementTransform(orig_plot[1], tn_plot[1]),
            ReplacementTransform(orig_plot[2], tn_plot[2]),
            lag_ratio=0.1,
            rate_func=ease_in_out_circ,
            run_time=1.5,
        ))

        bg_rectangle = SurroundingRectangle(tn_plot, color=LOGO_WHITE)
        bg_rectangle.joint_type = LineJointType.ROUND
        tn_plot.add(bg_rectangle)
        self.play(Write(bg_rectangle))
        self.wait()

        self.move_camera(
            phi=60*DEGREES,
            theta=-75*DEGREES,
            # added_anims = [
            #     tn_plot.animate(lag_ratio=0.5).rotate(90 * DEGREES, RIGHT),
            # ],
        )

        self.play(
            tn_plot.animate(lag_ratio=0.5).rotate(90 * DEGREES, RIGHT),
        )

        tn_plot.add_updater(
            lambda m, dt: m.rotate(PI/2 * dt)
        )

        # self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)

        tn_plot.suspend_updating()
        self.wait()
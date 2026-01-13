from manim import *

class Sample(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=0*DEGREES, theta=0*DEGREES)

        sqs = VGroup(
            Square(
                fill_color=color,
                fill_opacity=0.5,
                stroke_width=2,
                grid_xstep=0.2,
                grid_ystep=0.2,
                grid_stroke_width=1,
            ).scale(2).set_z_index(999-i)
            for i, color in enumerate([RED, GREEN, BLUE])
        )

        self.add(sqs)
        self.wait()

        self.move_camera(phi=45*DEGREES, theta=15*DEGREES)

        self.play(sqs.animate.arrange(IN*2))

        self.wait()

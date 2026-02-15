from manim import *

class Slider(VGroup):
    def __init__(
        self,
        tracker: ValueTracker,
        label="",
        width=3,
        color=WHITE,
    ):
        super().__init__()

        self.tracker = tracker
        self.width = width

        self.line = Line(LEFT * width / 2, RIGHT * width / 2)
        self.line.set_color(GREY)

        self.handle = Dot(radius=0.08, color=color)

        self.label = Text(
            label,
            font_size=24,
            font="JetBrains Mono",
        )
        self.label.next_to(self.line, LEFT)

        self.value_text = always_redraw(
            lambda: Text(
                f"{round(self.tracker.get_value())}",
                font_size=24,
                font="JetBrains Mono",
            ).next_to(self.line, RIGHT)
        )

        # Handle follows tracker (0–255)
        self.handle.add_updater(
            lambda m: m.move_to(
                self.line.point_from_proportion(
                    self.tracker.get_value() / 255
                )
            )
        )

        self.add(self.line, self.handle, self.label, self.value_text)


class RGBSliderAnimation(Scene):
    def construct(self):
        r = ValueTracker(0)
        g = ValueTracker(0)
        b = ValueTracker(0)

        r_slider = Slider(r, "R", color=RED)
        g_slider = Slider(g, "G", color=GREEN)
        b_slider = Slider(b, "B", color=BLUE)

        sliders = VGroup(r_slider, g_slider, b_slider)
        sliders.arrange(DOWN, buff=0.6)
        sliders.to_edge(LEFT)

        preview = Square(side_length=2)
        preview.to_edge(RIGHT)

        preview.add_updater(
            lambda m: m.set_fill(
                rgb_to_color([
                    r.get_value() / 255,
                    g.get_value() / 255,
                    b.get_value() / 255,
                ]),
                opacity=1
            ).set_stroke(m.get_fill_color())
        )

        self.add(sliders, preview)

        # --- Animations ---
        self.play(r.animate.set_value(255), run_time=2)
        self.play(g.animate.set_value(255), run_time=2)
        self.play(b.animate.set_value(255), run_time=2)

        self.play(
            r.animate.set_value(64),
            g.animate.set_value(128),
            b.animate.set_value(200),
            run_time=2
        )

        self.wait()

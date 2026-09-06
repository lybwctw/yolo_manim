"""A concise, self-contained Conv2D animation for Manim Community.

Run:
    manim -pqh --renderer=cairo conv2d_3d.py Conv2DIn3D
Quick preview:
    manim -pql --renderer=cairo conv2d_3d.py Conv2DIn3D

Uses Text instead of MathTex: no LaTeX installation required.
The z separation is illustrative; the operation slides over height and width.
"""
from manim import *
import numpy as np


class Conv2DIn3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#101722"
        self.set_camera_orientation(phi=42 * DEGREES, theta=-90 * DEGREES)

        x = np.array([
            [1, 2, 0, 1],
            [3, 1, 2, 2],
            [0, 2, 1, 3],
            [1, 0, 2, 1],
        ])
        w = np.array([[1, 2], [0, -1]])
        bias = 1
        y = np.array([
            [int(np.sum(x[r:r + 2, c:c + 2] * w) + bias)
             for c in range(3)] for r in range(3)
        ])
        size = 0.76
        input_center = np.array([-2.65, 0.0, 0.0])
        output_center = np.array([2.65, 0.0, 0.0])
        colors = [YELLOW, ORANGE, PINK, GREEN]

        def point(center, rows, cols, r, c):
            return center + np.array([
                (c - (cols - 1) / 2) * size,
                ((rows - 1) / 2 - r) * size, 0,
            ])

        def grid(values, center, color, blank=False):
            rows, cols = values.shape
            tiles, numbers = VGroup(), VGroup()
            for r in range(rows):
                for c in range(cols):
                    pos = point(center, rows, cols, r, c)
                    tile = Square(side_length=size - 0.025)
                    tile.set_stroke(color, width=1.5)
                    tile.set_fill(color, opacity=0.12).move_to(pos)
                    tiles.add(tile)
                    label = Text(str(values[r, c]), font_size=26)
                    label.move_to(pos + 0.015 * OUT)
                    if blank:
                        label.set_opacity(0)
                    numbers.add(label)
            return VGroup(tiles, numbers), tiles, numbers

        def hud(text, ypos, font_size=25, color=WHITE):
            obj = Text(text, font_size=font_size, color=color)
            if obj.width > 12.5:
                obj.scale_to_fit_width(12.5)
            obj.move_to([0, ypos, 0])
            self.add_fixed_in_frame_mobjects(obj)
            return obj

        title = hud("Conv2D: slide, multiply, sum", 3.45, 36)
        subtitle = hud("4 x 4 input  |  2 x 2 kernel  |  stride 1  |  padding 0  |  bias +1", 2.88, 22)
        caption = hud("One channel first. Each kernel position produces ONE output value.", -2.65, 23)
        equation = hud("Output = sum of matching products + bias", -3.25, 25)

        def change_text(obj, text, font_size=25, color=WHITE):
            target = Text(text, font_size=font_size, color=color)
            if target.width > 12.5:
                target.scale_to_fit_width(12.5)
            target.move_to(obj.get_center())
            self.play(Transform(obj, target), run_time=0.35)

        input_grid, input_tiles, _ = grid(x, input_center, BLUE)
        output_grid, output_tiles, output_numbers = grid(y, output_center, TEAL)
        # Reveal output numbers only when their calculations finish.
        for label in output_numbers:
            label.set_opacity(0)

        names = VGroup(
            Text("INPUT", font_size=26, color=BLUE).move_to([-2.65, -2.0, 0]),
            Text("OUTPUT", font_size=26, color=TEAL).move_to([2.65, -2.0, 0]),
        )
        self.play(FadeIn(input_grid), FadeIn(output_grid), FadeIn(names))

        def patch_center(r, c):
            return (point(input_center, 4, 4, r, c)
                    + point(input_center, 4, 4, r + 1, c + 1)) / 2

        kernel_center = patch_center(0, 0) + 1.05 * OUT
        kernel, kernel_tiles, kernel_numbers = grid(w, kernel_center, YELLOW)
        for i in range(4):
            kernel_tiles[i].set_stroke(colors[i], width=3)
            kernel_tiles[i].set_fill(colors[i], opacity=0.25)
            kernel_numbers[i].set_color(colors[i])
        self.play(FadeIn(kernel, shift=0.3 * OUT))
        change_text(caption, "The colored grid is the kernel. Its weights stay the same as it slides.", 23)
        self.wait(1.2)

        # Brief orbit makes the floating kernel's depth explicit.
        self.move_camera(phi=52 * DEGREES, theta=-78 * DEGREES, run_time=1.5)
        self.move_camera(phi=42 * DEGREES, theta=-90 * DEGREES, run_time=1.5)

        for r in range(3):
            for c in range(3):
                if (r, c) != (0, 0):
                    self.play(kernel.animate.move_to(patch_center(r, c) + 1.05 * OUT),
                              run_time=0.45)
                selected = [4 * (r + a) + c + b for a in range(2) for b in range(2)]
                guides = VGroup(*[
                    DashedLine(
                        kernel_tiles[i].get_center(),
                        input_tiles[index].get_center(),
                        color=colors[i], stroke_width=2, dash_length=0.08,
                    ) for i, index in enumerate(selected)
                ])
                self.play(
                    FadeIn(guides),
                    *[input_tiles[index].animate.set_fill(colors[i], opacity=0.48)
                      for i, index in enumerate(selected)],
                    run_time=0.25,
                )
                patch = x[r:r + 2, c:c + 2].ravel()
                products = patch * w.ravel()
                out_index = 3 * r + c

                if (r, c) == (0, 0):
                    change_text(caption, "1. Multiply matching entries (colors show the pairs).", 24)
                    terms = []
                    for i in range(4):
                        terms.append(f"{patch[i]} x ({w.ravel()[i]})")
                        change_text(equation, "   +   ".join(terms), 27)
                        self.play(Indicate(kernel_numbers[i], color=colors[i]), run_time=0.5)
                    change_text(caption, "2. Add all four products, then add the bias.", 24)
                    change_text(equation, f"{products[0]} + {products[1]} + {products[2]} + ({products[3]}) + {bias} = {y[r, c]}", 29)
                    self.wait(1)
                else:
                    change_text(equation,
                                f"Y[{r}, {c}] = {products[0]} + {products[1]} + ({products[2]}) + ({products[3]}) + {bias} = {y[r, c]}", 26)

                # Four contributions converge onto the single output cell.
                destination = output_tiles[out_index].get_center() + 0.05 * OUT
                particles = VGroup(*[
                    Dot3D(input_tiles[index].get_center() + 0.06 * OUT,
                          radius=0.055, color=colors[i])
                    for i, index in enumerate(selected)
                ])
                self.add(particles)
                self.play(*[dot.animate.move_to(destination) for dot in particles], run_time=0.55)
                self.remove(particles)
                self.play(output_numbers[out_index].animate.set_opacity(1),
                          output_tiles[out_index].animate.set_fill(TEAL, opacity=0.35),
                          run_time=0.3)
                self.play(FadeOut(guides),
                          *[input_tiles[index].animate.set_fill(BLUE, opacity=0.12)
                            for index in selected], run_time=0.2)
                if (r, c) == (0, 0):
                    change_text(caption, "3. Slide one cell. Repeat with the SAME weights and bias.", 24)
                    self.wait(0.7)

        self.play(FadeOut(kernel))
        change_text(caption, "Output height = output width = (4 - 2) / 1 + 1 = 3", 25)
        change_text(equation, "Kernel is NOT flipped: the usual deep-learning Conv2D convention.", 22)
        self.wait(2)

        self.play(FadeOut(input_grid), FadeOut(output_grid), FadeOut(names))
        change_text(subtitle, "From one channel to many", 28)
        summary = VGroup(*[
            Text(line, font_size=27, color=color) for line, color in [
                ("Input: C_in channels, each H x W", BLUE),
                ("One filter: C_in kernel slices, each kH x kW", YELLOW),
                ("Sum products across ALL slices + one bias", WHITE),
                ("One filter produces ONE output channel", TEAL),
                ("C_out filters produce C_out output channels", TEAL),
            ]
        ]).arrange(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(FadeIn(summary))
        change_text(caption, "Conv2D slides over HEIGHT and WIDTH; channels are summed.", 24)
        change_text(equation, "The 3D spacing in this animation is only for visibility.", 22)
        self.wait(4)

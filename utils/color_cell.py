from manim import *

class ColorCell(VMobject):
    def __init__(self, r, g, b, **kwargs):
        super().__init__(**kwargs)
        _color = rgb_to_color([int(r), int(g), int(b)])
        rect = Square(
            side_length=1,
            fill_color=_color,
            stroke_color=BLACK,
            stroke_width=2,
            stroke_opacity=0.8,
        )
        self.rect = rect
        self.add(self.rect)

class Demo(Scene):
    def construct(self) -> None:
        cell = ColorCell(1,2,3)
        self.add(cell)
        self.wait()
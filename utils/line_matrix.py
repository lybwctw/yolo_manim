from manim import *

class LineMatrix(VMobject):
    """Used as target of 3d-2d transformation.
    """
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        self.m, self.n = self.shape
        
        self.mobs = VGroup(
            VGroup(
                Line(
                    ORIGIN,
                    RIGHT,
                    stroke_width=2,
                ) for _ in range(self.n)
            ).arrange(RIGHT) for _ in range(self.m)
        ).arrange(DOWN)
        self.add(self.mobs)

class Demo(Scene):
    def construct(self):
        lm = LineMatrix((400, 4)).scale(0.06)
        self.play(Write(lm))
        self.wait()
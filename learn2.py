from manim import *
import numpy as np

class TableExamples(ThreeDScene):
    def construct(self):
        sq = Cube(stroke_width=2, stroke_opacity=1.0, fill_color=BLACK)
        self.play(Write(sq))
        self.move_camera(phi=60*DEGREES, theta=-75*DEGREES)
        self.wait()
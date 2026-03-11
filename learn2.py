from manim import *
import numpy as np

class TableExamples(Scene):
    def construct(self):
        axes = Axes(x_range=[0,5,1], y_range=[0,4,1], img_rotate=True)
        self.add(axes)
        self.wait()
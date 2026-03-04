from manim import *
from .constants import INIT_WIDTH_ARROW_COMMENT

class ArrowComment(VMobject):
    def __init__(self, double, direction, comment):
        super().__init__()
        self.scale_factor = 1.0

        if double:
            self.arrow = DoubleArrow(start=-direction, end=direction)
        else:
            self.arrow = Arrow(start=-direction, end=direction)
        self.add(self.arrow)

    def scale(self, scale_factor, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, **kwargs)

    def scale_back(self):
        self.scale(1 / self.scale_factor)
        return self
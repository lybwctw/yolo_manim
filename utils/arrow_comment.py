from manim import *
from .constants import INIT_WIDTH_ARROW_COMMENT

class ArrowComment(VMobject):
    def __init__(self, double, direction, comment):
        super().__init__()
        if double:
            self.arrow = DoubleArrow(start=-direction, end=direction)
        else:
            self.arrow = Arrow(start=-direction, end=direction)
        self.add(self.arrow)
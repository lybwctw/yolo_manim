from manim import *

class ArrowComment(VMobject):
    def __init__(self, double, direction, comment):
        super().__init__()
        if double:
            self.arrow = DoubleArrow(start=-direction, end=direction)
        else:
            self.arrow = Arrow(start=-direction, end=direction)
        self.add(self.arrow)
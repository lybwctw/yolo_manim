from manim import *

class ImageRaw(VGroup):
    def __init__(self, path):
        super().__init__()
        sq = Square()
        sq.stretch_to_fit_width(3.2)
        sq.stretch_to_fit_height(1.8)
        self.sq = sq
        self.add(self.sq)

class Demo(Scene):
    def construct(self):
        img = ImageRaw(None)
        self.add(img)
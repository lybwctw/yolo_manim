from manim import *

class TileComment(VMobject):
    def __init__(self, path):
        super().__init__()
        self.rect = Rectangle(
            fill_color=GRAY,
            fill_opacity=1.0,
            stroke_width=0.0,
        )
        self.add(self.rect)

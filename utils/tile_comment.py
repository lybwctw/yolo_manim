from manim import *

class TileComment(VMobject):
    def __init__(self, text='', init_scale=1.0):
        super().__init__()
        self.rect = Rectangle(
            width=4*init_scale,
            height=3*init_scale,
            fill_color=GRAY,
            fill_opacity=1.0,
            stroke_width=0.0,
        )
        self.add(self.rect)

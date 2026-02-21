from manim import *

class LayersFake(VMobject):
    def __init__(self, obj):
        # init based on obj type
        super().__init__()
        self.rect = Rectangle(
            fill_color=GRAY,
            fill_opacity=0.6,
            stroke_width=0.0,
        )
        self.add(self.rect)

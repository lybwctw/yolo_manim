from manim import *

class LayersFake(VMobject):
    def __init__(self, obj):
        # init based on obj type
        super().__init__()
        self.rect = Rectangle()
        self.add(self.rect)

from manim import *

class GridAnnotationBox(VMobject):
    def __init__(self, path):
        super().__init__()
        self.rect = Rectangle()
        self.add(self.rect)
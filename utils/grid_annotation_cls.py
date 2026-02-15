from manim import *

class GridAnnotationCls(VMobject):
    def __init__(self, path):
        super().__init__()
        self.rect = Rectangle()
        self.add(self.rect)
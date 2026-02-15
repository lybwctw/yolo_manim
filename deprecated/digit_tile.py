from manim import *
from .image_raw import ImageRaw

class DigitTile(VGroup):
    def __init__(self, txt):
        super().__init__()
        text = Text(txt)
        rect = SurroundingRectangle(text)
        rect.set_stroke(color=WHITE, width=2)
        self.rect = rect
        self.text = text
        self.add(self.rect, self.text)

class Demo(Scene):
    def construct(self):
        anno = DigitTile('一堆\n数字')
        self.add(anno)
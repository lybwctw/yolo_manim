from manim import *
from .image_raw import ImageRaw

class ImageAnnotation(VGroup):
    def __init__(self, image, path):
        super().__init__()
        sq = Square(
            fill_color=BLUE_E,
            fill_opacity=0.8,
            stroke_width=0.,
        )
        sq.stretch_to_fit_width(image.width)
        sq.stretch_to_fit_height(image.height)
        self.sq = sq
        self.add(self.sq)

class Demo(Scene):
    def construct(self):
        img = ImageRaw(None)
        anno = ImageAnnotation(img, None)
        VGroup(img, anno).arrange()
        self.add(img, anno)
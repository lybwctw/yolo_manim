from manim import *

class ImageRaw(Mobject):
    def __init__(self, path, init_width=6.4):
        super().__init__()
        self.scale_factor = 1.0
        image = ImageMobject(path)
        image.scale_to_fit_width(init_width)
        self.image = image
        self.add(self.image)
        self.center()

class ImageRepad(VMobject):
    def __init__(self, path, init_scale=1.0):
        super().__init__()
        self.scale_factor = 1.0
        self.rect = Rectangle(
            width=6.4*init_scale,
            height=3.6*init_scale,
            fill_color=GREEN,
            fill_opacity=1.0,
            stroke_width=0.0,
        )
        self.add(self.rect)
        self.center()

class Demo(Scene):
    def construct(self) -> None:
        image = ImageRepad('')
        self.add(image)
        self.wait()
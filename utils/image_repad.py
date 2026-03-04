from manim import *

class ImageRaw(Mobject):
    def __init__(self, path, init_width=6.4):
        super().__init__()
        self.scale_factor = 1.0
        image = ImageMobject(path)
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image.scale_to_fit_width(init_width)
        self.image = image
        self.add(self.image)
        self.center()

    def scale(self, scale_factor, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, **kwargs)

    def scale_back(self):
        self.scale(1/self.scale_factor)
        return self

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

    def scale(self, scale_factor, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, **kwargs)

    def scale_back(self):
        self.scale(1 / self.scale_factor)

class Demo(Scene):
    def construct(self) -> None:
        image = ImageRepad('')
        self.add(image)
        self.wait()
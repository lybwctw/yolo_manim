from manim import *
from utils.show_shape import ShowShape

class ImageRaw(Mobject, ShowShape):
    def __init__(
        self,
        path,
        init_width=6.4,
        width_nominal=960,
        height_nominal=540,
    ):
        super().__init__()
        self.path = path
        self.init_width = init_width
        self._w = width_nominal
        self._h = height_nominal

        self.scale_factor = 1.0     # FIXME, useless?
        image = ImageMobject(path)
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image.scale_to_fit_width(init_width)
        self.image = image
        self.add(self.image)
        self.center()

    def get_shape_path(self):
        path = VMobject()
        path.set_points_as_corners([
            self.image.get_corner(LEFT + DOWN),
            self.image.get_corner(LEFT + UP),
            self.image.get_corner(RIGHT + UP),
        ]).set_stroke(color=BLUE)
        return path

    def get_shape_text(self):
        text_h = Text(str(self._h), font_size=20).next_to(self.image, LEFT)
        text_w = Text(str(self._w), font_size=20).next_to(self.image, UP)
        text = VGroup(text_h, text_w)
        return text

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
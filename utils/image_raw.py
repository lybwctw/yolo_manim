from manim import *
from constants import *
from show_shape import ShowShape

class ImageRaw(Mobject, ShowShape):
    def __init__(
        self,
        path: str = PATH_IMAGE_640,
        width_nominal: int = 960,
        height_nominal: int = 540,
    ):
        super().__init__()
        self.path = path
        self.width_nominal = width_nominal
        self.height_nominal = height_nominal

        image = ImageMobject(path)
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        self.image = image
        self.add(self.image)

    def get_shape_path(self):
        path = VMobject()
        path.set_points_as_corners([
            self.image.get_corner(LEFT + DOWN),
            self.image.get_corner(LEFT + UP),
            self.image.get_corner(RIGHT + UP),
        ]).set_stroke(color=BLUE)
        return path

    def get_shape_text(self):
        text_h = Text(str(self.height_nominal), font_size=20).next_to(self.image, LEFT)
        text_w = Text(str(self.width_nominal), font_size=20).next_to(self.image, UP)
        text = VGroup(text_h, text_w)
        return text

class Demo(Scene):
    def construct(self):
        path = '../assets/images/sample_640_360.jpg'
        img = ImageRaw(
            path=path,
        )
        self.add(img)
        self.wait()

        self.play(img.show_passing_flash())
        self.wait()
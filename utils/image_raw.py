import sys
sys.path.append('..')

from manim import *
from utils.show_shape import ShowShape, HideShape
from utils.constants import *

class ImageRaw(Mobject):
    """
    Example
    -------
    from manim import *
    from utils.image_raw import ImageRaw

    class Demo(Scene):
        def construct(self):
            img = ImageRaw()
            self.add(img)
            self.wait()
    """
    def __init__(
        self,
        path: str = PATH_IMAGE_640,
        width_nominal: int | None = None,
        height_nominal: int | None = None,
    ):
        super().__init__()
        self.path = path

        image = ImageMobject(path)
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        self.image = image

        self.width_nominal = width_nominal or image.get_pixel_array().shape[1]
        self.height_nominal = height_nominal or image.get_pixel_array().shape[0]

        self.add(self.image)

    def get_shape_path(
        self,
        **path_config,
    ):
        path = VMobject()
        path.set_points_as_corners([
            self.image.get_corner(LEFT + DOWN),
            self.image.get_corner(LEFT + UP),
            self.image.get_corner(RIGHT + UP),
        ]).set_stroke(**path_config)
        return path

    def get_shape_text(
        self,
        **text_config,
    ):
        buff = text_config.pop('buff')  # buff SHOULD be provided
        text_h = Text(
            str(self.height_nominal),
            **text_config,
        ).next_to(self.image, LEFT, buff=buff)
        text_w = Text(
            str(self.width_nominal),
            **text_config,
        ).next_to(self.image, UP, buff=buff)
        text = VGroup(text_h, text_w)
        return text
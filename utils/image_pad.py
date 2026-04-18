import sys
sys.path.append('..')

from manim import *

from utils.image_raw import ImageRaw
from utils.show_shape import ShowShape
from utils.constants import *

class ImagePad(Mobject, ShowShape):
    def __init__(
        self,
        image_raw: ImageRaw = None,         # from ImageRaw
        path: str = PATH_IMAGE_640,         # from image path
        width_nominal: int | None = None,   # nominal width
        height_nominal: int | None = None,  # nominal height
        padded: bool = False,               # padded or not 
    ):
        super().__init__()

        if image_raw:
            self.path = None
            self.image = image_raw.image
            self.width_nominal = width_nominal or image_raw.width_nominal or self.image.get_pixel_array().shape[1]
            self.height_nominal = height_nominal or image_raw.height_nominal or self.image.get_pixel_array().shape[0]

        else:
            self.path = path
            image = ImageMobject(path)
            image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
            self.image = image
            self.width_nominal = width_nominal or self.image.get_pixel_array().shape[1]
            self.height_nominal = height_nominal or self.image.get_pixel_array().shape[0]

        self.paddings_config = {
            'stroke_width': 0,
            'fill_opacity': 1.0,
            'fill_color': GRAY,
        }
        self.paddings = None

        self.add(self.image)
        # use natural paddings if init with paddings
        if padded:
            paddings = self.create_natural_paddings(
                paddings=None,          # auto compute
            )
            if paddings:
                self.width_nominal = max(self.width_nominal, self.height_nominal)
                self.height_nominal = max(self.width_nominal, self.height_nominal)
                self.paddings = paddings
                self.add(self.paddings)
    
    def set_opacity(self, alpha):
        """ Override set_opacity because there are 
            different interfaces when setting opacity
            for ImageMobject and VMobject.
        """
        self.image.set_opacity(alpha)

        if self.paddings:
            self.paddings.set_opacity(alpha)

        return self

    def get_shape_path(self):
        path = VMobject()
        path.set_points_as_corners([
            self.get_corner(DL),
            self.get_corner(UL),
            self.get_corner(UR),
        ]).set_stroke(color=YELLOW)
        return path
    
    def get_shape_text(self):
        text_h = Text(str(self.height_nominal), font_size=20).next_to(self, LEFT)
        text_w = Text(str(self.width_nominal), font_size=20).next_to(self, UP)
        text = VGroup(text_h, text_w)
        return text

    def create_paddings(
        self,
        updown: bool = True,
        paddings: tuple = (1,1),
        **config,
    ):
        width, height = self.image.width, self.image.height

        if updown:
            p1 = Rectangle(
                width=width,
                height=paddings[0],
                **config,
            ).next_to(self.image, UP, buff=0)
            p2 = Rectangle(
                width=width,
                height=paddings[1],
                **config,
            ).next_to(self.image, DOWN, buff=0)
        else:
            p1 = Rectangle(
                width=paddings[0],
                height=height,
                **config,
            ).next_to(self.image, LEFT, buff=0)
            p2 = Rectangle(
                width=paddings[1],
                height=height,
                **config,
            ).next_to(self.image, RIGHT, buff=0)

        return VGroup(p1, p2)
    
    def create_natural_paddings(
        self,
        paddings: tuple | None = None,
    ):
        if self.width_nominal == self.height_nominal:
            paddings = None
        elif self.width_nominal > self.height_nominal:
            if paddings is None:
                paddings = (
                    (self.image.width-self.image.height)/2,
                    (self.image.width-self.image.height)/2,
                )
                
            paddings = self.create_paddings(
                updown=True,
                paddings=paddings,
                **self.paddings_config,
            )
        else:
            if paddings is None:
                paddings = (
                    (self.image.height-self.image.width)/2,
                    (self.image.height-self.image.width)/2,
                )
                
            paddings = self.create_paddings(
                updown=False,
                paddings=paddings,
                **self.paddings_config,
            )

        return paddings

    def show_paddings(
        self,
        updown: bool = True,
        paddings: tuple = (1,1),
        width_nominal: int | None = None,       # manual nominal update
        height_nominal: int | None = None,      # manual nominal update
    ):
        # empty animation if already padded
        if self.paddings:
            return Wait()

        paddings_start = self.create_paddings(
            updown=updown,
            paddings=(0,0),
            **self.paddings_config,
        )

        paddings_end = self.create_paddings(
            updown=updown,
            paddings=paddings,
            **self.paddings_config,
        )

        # manually update nominals if provided
        if width_nominal:
            self.width_nominal = width_nominal
        if height_nominal:
            self.height_nominal = height_nominal

        self.paddings = paddings_start
        self.add(self.paddings)

        return AnimationGroup(
            *(Transform(p1, p2) for p1, p2 in zip(paddings_start, paddings_end)),
            lag_ratio=0,
        )

    def show_natural_paddings(
        self,
    ):
        if self.width_nominal == self.height_nominal:
            return Wait()
        elif self.width_nominal > self.height_nominal:
            return self.show_paddings(
                updown=True,
                paddings = (
                    (self.image.width-self.image.height)/2,
                    (self.image.width-self.image.height)/2,
                ),
                height_nominal=self.width_nominal,
            )
        else:
            return self.show_paddings(
                updown=True,
                paddings = (
                    (self.image.height-self.image.width)/2,
                    (self.image.height-self.image.width)/2,
                ),
                width_nominal=self.height_nominal,
            )
        
    def hide_paddings(
        self,
        updown: bool = True,    # user is responsible for providing correct updown
        width_nominal: int | None = None,       # manual nominal update
        height_nominal: int | None = None,      # manual nominal update
        aargs: dict = {},       # transform args
        gargs: dict = {},       # group args
    ) -> Animation:
        if not self.paddings:
            return Wait()

        paddings_start = self.paddings
        paddings_end = self.create_paddings(
            updown=updown,
            paddings=(0,0),
            **self.paddings_config,
        )

        self.paddings = None

        if width_nominal:
            self.width_nominal = width_nominal
        if height_nominal:
            self.height_nominal = height_nominal

        return AnimationGroup(
            *(Transform(p1, p2, **aargs) for p1, p2 in zip(paddings_start, paddings_end)),
            **gargs,
        )

class Demo(Scene):
    def construct(self) -> None:
        path = '../assets/images/sample_640_360.jpg'
        ipad = ImagePad(
            path=path,
            padded=False,
        )

        self.add(ipad)
        self.wait()

        self.play(ipad.show_natural_paddings())
        self.wait()

        self.play(ipad.hide_paddings(
            width_nominal=640,
            height_nominal=360,
        ))
        self.wait()

        self.play(ipad.show_passing_flash())
        self.wait()
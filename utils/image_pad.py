import sys
sys.path.append('..')

from manim import *
from utils.image_raw import ImageRaw
from utils.show_shape import *
from utils.constants import *

class ImagePad(Mobject):
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
        """
        Override set_opacity because there are
            different interfaces when setting opacity
            for ImageMobject and VMobject.


        Example
        -------
        ipad = ImagePad(padded=True)
        ipad.set_opacity(alpha=0.5)
        """
        self.image.set_opacity(alpha)

        if self.paddings:
            self.paddings.set_opacity(alpha)

        return self

    def get_shape_path(
        self,
        **path_config,
    ) -> VMobject:
        """
        Example
        -------
        ipad = ImagePad(padded=True)
        result = ipad.get_shape_path()
        """
        path = VMobject()
        path.set_points_as_corners([
            self.get_corner(DL),
            self.get_corner(UL),
            self.get_corner(UR),
        ]).set_stroke(**path_config)
        return path

    def get_shape_text(
        self,
        **text_config,
    ) -> VGroup:
        """
        Example
        -------
        ipad = ImagePad(padded=True)
        result = ipad.get_shape_text()
        """
        buff = text_config.pop('buff', 0.15)
        text_h = Text(
            str(self.height_nominal),
            **text_config,
        ).next_to(
            self,
            LEFT,
            buff=buff,
        )
        text_w = Text(
            str(self.width_nominal),
            **text_config,
        ).next_to(
            self,
            UP,
            buff=buff,
        )
        text = VGroup(text_h, text_w)
        return text

    def create_paddings(
        self,
        updown: bool = True,
        paddings: tuple = (1,1),
        **config,
    ):
        """
        Example
        -------
        ipad = ImagePad(padded=True)
        result = ipad.create_paddings()
        """
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
        """
        Example
        -------
        ipad = ImagePad(padded=True)
        result = ipad.create_natural_paddings()
        """
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
        **aargs,
    ):
        """Show paddings for backgound image.
        """
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
            **aargs,
        )

    def show_natural_paddings(
        self,
        **aargs,
    ):
        """Show natrual paddings for background image.
        """
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
                **aargs,
            )
        else:
            return self.show_paddings(
                updown=True,
                paddings = (
                    (self.image.height-self.image.width)/2,
                    (self.image.height-self.image.width)/2,
                ),
                width_nominal=self.height_nominal,
                **aargs,
            )

    def hide_paddings(
        self,
        updown: bool = True,    # user is responsible for providing correct updown
        width_nominal: int | None = None,       # manual nominal update
        height_nominal: int | None = None,      # manual nominal update
        **aargs,
    ) -> Animation:
        """Hide paddings for background image.
        """
        if not self.paddings:
            return Wait()

        paddings_start = self.paddings
        paddings_end = self.create_paddings(
            updown=updown,
            paddings=(0,0),
            **self.paddings_config,
        )

        self.paddings = None
        # self.remove(self.paddings)

        if width_nominal:
            self.width_nominal = width_nominal
        if height_nominal:
            self.height_nominal = height_nominal

        return AnimationGroup(
            *(Transform(p1, p2) 
              for p1, p2 in zip(paddings_start, paddings_end)),
            **aargs,
        )

class Demo(Scene):
    def construct(self) -> None:
        image_pad = ImagePad(padded=True)
        self.add(image_pad)
        self.wait()

        self.play(image_pad.animate.set_opacity(0.1))
        self.wait()

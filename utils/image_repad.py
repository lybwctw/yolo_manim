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

class ImageRepad(Mobject, ShowShape):
    def __init__(
        self,
        image_raw,
        padded=False,
    ):
        super().__init__()
        self.scale_factor = 1.0
        self.image = image_raw.image
        self._w = image_raw._w
        self._h = image_raw._h
        self.padded = padded
        self.natural_pad = False # natural means w>h

        if self.padded:
            width, height = self.image.width, self.image.height
            if self._w > self._h:
                self.natural_pad = True
                t_width, t_height = width, (width - height) / 2
                p1 = Rectangle(
                    width=t_width,
                    height=t_height,
                    stroke_width=0,
                    fill_color=GRAY,  # FIXME, using exact 114,114,114
                    fill_opacity=1.0,
                ).next_to(self.image, DOWN, buff=0)
                p2 = p1.copy().next_to(self.image, UP, buff=0)
            else:
                self.natural_pad = False
                t_width, t_height = (height - width) / 2, height
                p1 = Rectangle(
                    width=t_width,
                    height=t_height,
                    stroke_width=0,
                    fill_color=GRAY,  # FIXME, using exact 114,114,114
                    fill_opacity=1.0,
                ).next_to(self.image, LEFT, buff=0)
                p2 = p1.copy().next_to(self.image, RIGHT, buff=0)
            self.paddings = VGroup(p1, p2)
            self.add(self.paddings)
        else:
            self.paddings = None

        self.add(image_raw)

    def get_shape_path(self):
        path = VMobject()
        if self.natural_pad:
            path.set_points_as_corners([
                self.paddings[0].get_corner(LEFT + DOWN),
                self.paddings[1].get_corner(LEFT + UP),
                self.paddings[1].get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
        else:
            path.set_points_as_corners([
                self.paddings[0].get_corner(LEFT + DOWN),
                self.paddings[0].get_corner(LEFT + UP),
                self.paddings[1].get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
        return path
    
    def get_shape_text(self):
        if self.natural_pad:
            text_h = Text(str(self._h), font_size=20).next_to(self.image, LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.paddings[1], UP)
        else:
            text_h = Text(str(self._h), font_size=20).next_to(self.paddings[0], LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.image, UP)
        text = VGroup(text_h, text_w)
        return text

    def show_paddings(self):
        if self.padded:
            return None

        width, height = self.image.width, self.image.height
        if self._w > self._h:
            self.natural_pad = True
            t_width, t_height = width, (width-height)/2
            p1 = Rectangle(
                width=t_width,
                height=0,
                stroke_width=0,
                fill_color=GRAY,  # FIXME, using exact 114,114,114
            ).next_to(self.image, DOWN, buff=0)
            p2 = p1.copy().next_to(self.image, UP, buff=0)
            p1_res = Rectangle(
                width=t_width,
                height=t_height,
                stroke_width=0,
                fill_color=GRAY,
                fill_opacity=1.0,
            ).next_to(p1, DOWN, buff=0)
            p2_res = p1_res.copy().next_to(p2, UP, buff=0)

            self.paddings = VGroup(p1, p2)
            self.add(self.paddings)
            self.padded = True
            self._h = self._w
            return AnimationGroup(
                Transform(p1, p1_res),
                Transform(p2, p2_res),
            )
        else:
            self.natural_pad = False
            t_width, t_height = (height-width)/2, height
            p1 = Rectangle(
                width=0,
                height=t_height,
                stroke_width=0,
                fill_color=GRAY,  # FIXME, using exact 114,114,114
            ).next_to(self.image, LEFT, buff=0)
            p2 = p1.copy().next_to(self.image, RIGHT, buff=0)
            p1_res = Rectangle(
                width=t_width,
                height=t_height,
                stroke_width=0,
                fill_color=GRAY,
                fill_opacity=1.0,
            ).next_to(p1, LEFT, buff=0)
            p2_res = p1_res.copy().next_to(p2, RIGHT, buff=0)

            self.paddings = VGroup(p1, p2)
            self.add(self.paddings)
            self.padded = True
            self._w = self._h
            return AnimationGroup(
                Transform(p1, p1_res),
                Transform(p2, p2_res),
            )


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
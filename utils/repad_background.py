from manim import *
from utils.show_shape import ShowShape

class RepadBackground(Mobject, ShowShape):
    # init from annotation_repad for convenience
    def __init__(self, annotation_repad):
        super().__init__()
        self.natural_pad = annotation_repad.natural_pad
        self._w = annotation_repad._w
        self._h = annotation_repad._h

        background = annotation_repad.annotation.image.copy()
        paddings = annotation_repad.paddings.copy()

        self.background = background
        self.paddings = paddings
        self.add(self.background)
        self.add(self.paddings)

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
            text_h = Text(str(self._h), font_size=20).next_to(self.background, LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.paddings[1], UP)
        else:
            text_h = Text(str(self._h), font_size=20).next_to(self.paddings[0], LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.background, UP)
        text = VGroup(text_h, text_w)
        return text
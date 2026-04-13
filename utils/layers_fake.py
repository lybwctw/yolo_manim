import sys
sys.path.append('..')

from manim import *
from utils.show_shape import ShowShape

from typing import Self

RECT_CONFIG = {
    'fill_color': BLACK,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_color': WHITE,
}

SHAPE_PATH_CONFIG = {
    'color': PURE_YELLOW,
    'width': 3,
    'opacity': 1.0,
}

SHAPE_TEXT_CONFIG = {
    'font_size': 20,
    'font': 'JetBrains Mono',
}

class LayersFake(VMobject, ShowShape):
    def __init__(
        self,
        n: int = 3,                     # layers
        ref: Mobject | None = None,     # width/height reference
        width: float | None = None,     # exact width of single layer
        height: float | None = None,    # exact height of single layer
        expanded: bool = False,         # expanded or not at creation
        buff: float = 0.2,              # buff between layers
        width_nominal: int = 300,       # nominal width
        height_nominal: int = 200,      # nominal height
    ):
        super().__init__()

        self.n = n
        self.width_nominal = width_nominal
        self.height_nominal = height_nominal
        self.expanded=expanded
        self.buff=buff

        # width and height not members
        width = width or ref.width
        height = height or ref.height

        rects = VGroup(
            Rectangle(
                width=width,
                height=height,
                **RECT_CONFIG,
            ).shift(UR*self.buff*i*self.expanded).set_z_index(self.n-i)
            for i in range(self.n)
        )

        self.rects = rects
        self.shape_texts = None

        self.add(self.rects)
        
        # auto center?
        self.center()

    def expand(
        self,
    ) -> Animation:
        if self.expanded or self.n==1:
            return Wait()       # null animation
        orig_center = self.get_center()

        self.rects.generate_target()

        for i, rect in enumerate(self.rects.target):
            rect.shift(UR*self.buff*i)
        self.rects.target.move_to(orig_center)

        self.expanded = True

        return MoveToTarget(self.rects)
    
    def stretch_to_fit(
        self,
        width: float | None = None,     # target width of single layer
        height: float | None = None,    # target height of single layer
        width_nominal: int | None = None,   # new nominal width
        height_nominal: int | None = None,   # new nominal height
        **aargs,
    ) -> Animation:
        """Stretch single layers to target width and height.
        """
        # update nominal width and height
        if width_nominal:
            self.width_nominal = width_nominal
        if height_nominal:
            self.height_nominal = height_nominal

        anims = AnimationGroup(
            *(rect.animate.\
              stretch_to_fit_width(width).\
              stretch_to_fit_height(height)
              for rect in self.rects),
            **aargs,
        )
        return anims
    
    def stretch_to_fit_square(
        self,
        **aargs,
    ) -> Animation:
        """Stretch single layers to square according to nominal width/height.
        """
        if self.width_nominal == self.height_nominal:
            return Wait(1)      # do nothing
        elif self.width_nominal > self.height_nominal:
            width_nominal = self.width_nominal
            height_nominal = width_nominal
            width = self.rects[0].width
            height = width
        else:
            height_nominal = self.height_nominal
            width_nominal = height_nominal
            height = self.rects[0].height
            width = height
        return self.stretch_to_fit(
            width=width,
            height=height,
            width_nominal=width_nominal,
            height_nominal=height_nominal,
            **aargs,
        )

    def get_shape_path(
        self,
    ) -> VMobject:
        # same z_index as the first rect
        path = VMobject().set_z_index(self.n)
        if self.n == 1:
            path.set_points_as_corners([
                self.rects[0].get_corner(DL),
                self.rects[0].get_corner(UL),
                self.rects[0].get_corner(UR),
            ]).set_stroke(**SHAPE_PATH_CONFIG)
        else:
            path.set_points_as_corners([
                self.rects[0].get_corner(DL),
                self.rects[0].get_corner(UL),
                self.rects[-1].get_corner(UL),
                self.rects[-1].get_corner(UR),
            ]).set_stroke(**SHAPE_PATH_CONFIG)
        return path

    def get_shape_text(
        self,
    ) -> VGroup:
        if self.n == 1:
            text_h = Text(
                str(self.height_nominal),
                **SHAPE_TEXT_CONFIG,
            ).next_to(self.rects[0], LEFT)
            text_w = Text(
                str(self.width_nominal),
                **SHAPE_TEXT_CONFIG,
            ).next_to(self.rects[0], UP)
            text = VGroup(text_h, text_w)
        else:
            text_c = Text(
                str(self.n),
                **SHAPE_TEXT_CONFIG,
            ).next_to(self.rects[self.n//2], (LEFT + UP) * .6)
            text_h = Text(
                str(self.height_nominal),
                **SHAPE_TEXT_CONFIG,
            ).next_to(self.rects[0], LEFT)
            text_w = Text(
                str(self.width_nominal),
                **SHAPE_TEXT_CONFIG,
            ).next_to(self.rects[-1], UP)
            text = VGroup(text_h, text_c, text_w)
        return text

class Demo(Scene):
    def construct(self) -> None:
        lf = LayersFake(
            n=1,
            width=0.5,
            height=7,
            width_nominal=4,
            height_nominal=400,
            expanded=True,
        )
        self.play(Write(lf))
        self.wait()
        
        self.play(lf.stretch_to_fit(
            width=1,
            height=3,
        ))
        self.wait()
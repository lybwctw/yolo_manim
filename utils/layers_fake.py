"""Usage
-----
Example inside a scene outside ``utils/``::

    from utils.layers_fake import LayersFake
    from utils.show_shape import ShowShape, HideShape

    lf = LayersFake(n=3, width=3, height=4, width_nominal=300, height_nominal=400, expanded=True)
    self.play(Write(lf))
    self.play(ShowShape(lf, text_config={'buff': 0.2, 'font_size': 25}, path_config={'color': BLUE}))
    self.play(HideShape(lf))
"""

import sys
sys.path.append('..')

from manim import *
from utils.show_shape import *

from typing import Self

RECT_CONFIG = {
    'fill_color': BLACK,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_color': WHITE,
}

class LayersFake(VMobject, ShowShapeMixin):
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
        depth_nominal: int | None = None,   # nominal depth, n by default
        rect_config: dict = {},         # rectangle config
    ):
        """
        Example
        -------
        lf = LayersFake(n=3, width=3, height=4)
        """
        super().__init__()

        self.n = n
        self.width_nominal = width_nominal
        self.height_nominal = height_nominal
        self.depth_nominal = depth_nominal or n
        self.expanded=expanded
        self.buff=buff

        # width and height not members
        if width is None:
            width = ref.rects[0].width if isinstance(ref, LayersFake) else ref.width
        if height is None:
            height = ref.rects[0].height if isinstance(ref, LayersFake) else ref.height
        # width = width or ref.width
        # height = height or ref.height

        cfg = {**RECT_CONFIG, **rect_config}
        rects = VGroup(
            Rectangle(
                width=width,
                height=height,
                **cfg,
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
        """
        Example
        -------
        lf = LayersFake(n=3, width=3, height=4)
        self.play(lf.expand())
        """
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
        """
        Stretch single layers to target width and height.

        Example
        -------
        lf = LayersFake(n=3, width=3, height=4)
        self.play(lf.stretch_to_fit())
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
        """
        Stretch single layers to square according to nominal width/height.

        Example
        -------
        lf = LayersFake(n=3, width=3, height=4)
        self.play(lf.stretch_to_fit_square())
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
        **path_config,
    ) -> VMobject:
        """
        Example
        -------
        lf = LayersFake(n=3, width=3, height=4)
        result = lf.get_shape_path()
        """
        # NOTE: same z_index as the first rect
        path = VMobject().set_z_index(self.n)
        if self.n == 1:
            path.set_points_as_corners([
                self.rects[0].get_corner(DL),
                self.rects[0].get_corner(UL),
                self.rects[0].get_corner(UR),
            ]).set_stroke(**path_config)
        else:
            path.set_points_as_corners([
                self.rects[0].get_corner(DL),
                self.rects[0].get_corner(UL),
                self.rects[-1].get_corner(UL),
                self.rects[-1].get_corner(UR),
            ]).set_stroke(**path_config)
        return path

    def get_shape_text(
        self,
        **text_config,
    ) -> VGroup:
        """
        Example
        -------
        lf = LayersFake(n=3, width=3, height=4)
        result = lf.get_shape_text()
        """
        buff = text_config.pop('buff', 0.15)
        if self.n == 1:
            text_h = Text(
                str(self.height_nominal),
                **text_config,
            ).next_to(self.rects[0], LEFT, buff=buff)
            text_w = Text(
                str(self.width_nominal),
                **text_config,
            ).next_to(self.rects[0], UP, buff=buff)
            text = VGroup(text_h, text_w)
        else:
            text_c = Text(
                str(self.depth_nominal),        # nominal instead of true layers
                **text_config,
            ).next_to(self.rects[self.n//2], (LEFT + UP), buff=buff*.6)
            text_h = Text(
                str(self.height_nominal),
                **text_config,
            ).next_to(self.rects[0], LEFT, buff=buff)
            text_w = Text(
                str(self.width_nominal),
                **text_config,
            ).next_to(self.rects[-1], UP, buff=buff)
            text = VGroup(text_h, text_c, text_w)
        return text

class Demo(Scene):
    def construct(self) -> None:
        lf = LayersFake(
            n=3,
            width=3,
            height=4,
            width_nominal=300,
            height_nominal=400,
            expanded=True,
        )
        self.play(Write(lf))
        self.wait()

        self.play(ShowShape(
            lf,
            text_config={'buff': 0.2, 'font_size': 25,},
            path_config={'color': BLUE,},
        ))
        self.wait()
        self.play(lf.animate(
            rate_func=rate_functions.ease_in_out_back,
        ).scale(0.6).shift(LEFT*2))
        self.wait()
        self.play(HideShape(lf))
        self.wait()
        self.play(lf.animate.shift(RIGHT).scale(2.0))
        self.wait()
        self.play(ShowShape(lf))
        self.wait()
        self.play(HideShape(lf))
        self.wait()

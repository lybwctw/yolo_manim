from manim import *
from utils.show_shape import ShowShape

class LayersFake(VMobject, ShowShape):
    def __init__(
        self,
        n=3,
        width=3,
        height=2,
        expanded=False,
        buff=0.2,
        width_nominal=300,
        height_nominal=200,
        **kwargs,
    ):
        # init based on obj type
        super().__init__(**kwargs)
        self.n = n
        self.w = width
        self.h = height
        self._w = width_nominal
        self._h = height_nominal
        self.expanded=expanded
        self.buff=buff

        rects = []
        for i in range(n):
            rect = Rectangle(
                width=width,
                height=height,
                fill_color=BLACK,
                fill_opacity=0.8,
                stroke_width=2.0,
                stroke_color=WHITE,
            )
            if expanded:
                rect.shift(DL*self.buff*i)
            rects.append(rect)
        self.rects = rects
        self.mobs = VGroup(*rects).center()
        self.shape_texts = VGroup()

        self.add(self.mobs)

    def expand(self):
        if self.expanded:
            return None
        orig_center = self.get_center()

        self.mobs.generate_target()

        for i, rect in enumerate(self.mobs.target):
            rect.shift(DL*self.buff*i)
        self.mobs.target.move_to(orig_center)

        self.expanded = True

        return MoveToTarget(self.mobs)

    def stretch_to_square(self):
        if self._w > self._h:
            self._h = self._w
            anims = AnimationGroup(
                *(rect.animate.stretch_to_fit_height(self.rects[0].width) for rect in self.rects),
                lag_ratio=0,
            )
            return anims
        else:
            self._w = self._h
            anims = AnimationGroup(
                *(rect.animate.stretch_to_fit_width(self.rects[0].height) for rect in self.rects),
                lag_ratio=0,
            )
            return anims

    def get_shape_path(self):
        path = VMobject()
        if self.n == 1:
            path.set_points_as_corners([
                self.rects[0].get_corner(LEFT + DOWN),
                self.rects[0].get_corner(LEFT + UP),
                self.rects[0].get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
        else:
            path.set_points_as_corners([
                self.rects[-1].get_corner(LEFT + DOWN),
                self.rects[-1].get_corner(LEFT + UP),
                self.rects[0].get_corner(LEFT + UP),
                self.rects[0].get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
        return path

    def get_shape_text(self):
        if self.n == 1:
            text_h = Text(str(self._h), font_size=20).next_to(self.rects[0], LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.rects[0], UP)
            text = VGroup(text_h, text_w)
        else:
            text_c = Text(str(self.n), font_size=20).next_to(self.rects[1], (LEFT + UP) * .6)
            text_h = Text(str(self._h), font_size=20).next_to(self.rects[-1], LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.rects[0], UP)
            text = VGroup(text_h, text_c, text_w)
        return text

class Demo(Scene):
    def construct(self) -> None:
        lf = LayersFake(3, 4, 3)
        self.add(lf)
        self.wait()
        self.play(lf.expand())
        self.wait()
        VGroup().arrange_in_grid()
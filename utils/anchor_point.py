from manim import *

def rect_from_point(point, offset, **config):
    left, up, right, down = offset

    x, y, z = point

    x_min = x - left
    x_max = x + right
    y_min = y - down
    y_max = y + up

    rect = Rectangle(
        width=x_max - x_min,
        height=y_max - y_min,
        # stroke_width=3,
        # stroke_opacity=1.0,
        **config,
    )

    rect.move_to([
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        z
    ])

    return rect


class AnchorPointDep(VMobject):
    def __init__(self,
        point,
        offset=(1,1,1,1),
    ):
        super().__init__()
        self.offset = offset
        self.dot = Square(
            side_length=0.01,
            stroke_width=3,
            stroke_opacity=1.0,
            fill_opacity=0.0,
        ).move_to(point)
        self.add(self.dot)

    def to_rect(self, dd, **config):
        self.orig_center = self.dot.get_center()
        rect = rect_from_point(
            self.orig_center,
            (float(d)*dd for d in self.offset),
            **config,
        )
        self.dot.save_state()
        return Transform(self.dot, rect)

    # def get_arrows(self):
    #     # user's responsible for writing and unwriting of arrows
    #     arrows = VGroup(
    #         *(Arrow(
    #             start=self.orig_center,
    #             end=af(self.dot, self.orig_center),
    #             stroke_width=3,
    #             tip_length=0.15,
    #             buff=0,
    #         ) for af in align_to_funs),
    #     )
    #     return arrows

    def to_dot(self):
        return self.dot.animate.restore()

class AnchorPoint(VMobject):
    def __init__(
        self,
        point=ORIGIN,                   # starting position
        offset=(0.8,0.9,1.1,1.2),       # left, up, right, down
        s_xy=(0.5,0.5),              # dx, dy
    ):
        super().__init__()
        if isinstance(offset, np.ndarray):
            self.offset = offset.tolist()
        elif isinstance(offset, (list, tuple)):
            self.offset = offset
        self.s_xy = s_xy

        dot = Square(
            side_length=0.01,
            stroke_width=3,
            stroke_opacity=0.0,
        ).move_to(point)

        left, up, right, down = offset
        left, right = left*self.sx, right*self.sx   # update with sx
        up, down = up*self.sy, down*self.sy         # update with sy
        width, height = left+right, up+down
        center_offset = RIGHT*(right-left)/2 + UP*(up-down)/2
        rect = Rectangle(
            width=width,
            height=height,
            stroke_width=2,
            stroke_opacity=0.0,
            stroke_color=WHITE,
        ).move_to(point + center_offset)

        self.dot = dot
        self.rect = rect
        self.mob = dot.copy().set_stroke(opacity=1.0)
        self.add(self.dot, self.rect, self.mob)

    def to_rect(
        self,
    ):
        target = self.rect.copy().set_stroke(opacity=1.0)
        return Transform(self.mob, target)

    def to_dot(
        self,
    ):
        target = self.dot.copy().set_stroke(opacity=1.0)
        return Transform(self.mob, target)

    @property
    def sx(self):
        return self.s_xy[0]

    @property
    def sy(self):
        return self.s_xy[1]

class Demo(Scene):
    def construct(self):
        ap = AnchorPoint(
            offset=(1,2,3,4),
            s_xy=(0.5,0.5),
        )
        self.play(Create(ap))
        self.wait()

        self.play(ap.to_rect())
        self.wait()

        # self.play(ap.to_dot())
        # self.wait()

        self.play(Write(Square(side_length=3)))
        self.wait()
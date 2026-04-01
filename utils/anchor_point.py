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

# def align_to_top(rect, p):
#     return np.array([p[0], rect.get_top()[1], 0])
#
# def align_to_bottom(rect, p):
#     return np.array([p[0], rect.get_bottom()[1], 0])
#
# def align_to_left(rect, p):
#     return np.array([rect.get_left()[0], p[1], 0])
#
# def align_to_right(rect, p):
#     return np.array([rect.get_right()[0], p[1], 0])
#
# align_to_funs = [
#     align_to_left,
#     align_to_top,
#     align_to_right,
#     align_to_bottom,
# ]

class AnchorPoint(VMobject):
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
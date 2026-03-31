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

class AnchorPoint(VMobject):
    def __init__(self,
        point,
        radius=0.03,
        offset=(1,1,1,1),
    ):
        super().__init__()
        self.offset = offset
        self.dot = Dot(
            point,  # starting position of dot
            radius=radius,
            stroke_width=5,
            stroke_opacity=1.0,
            fill_opacity=0.0,
        )
        self.bg = Dot(
            point,
            radius=radius+0.01,
        )
        self.add(self.dot, self.bg)

    def to_rect(self, dd, **config):
        rect = rect_from_point(
            self.dot.get_center(),
            (float(d)*dd for d in self.offset),
            **config,
        )
        self.dot.save_state()
        self.bg.save_state()
        return AnimationGroup(
            Unwrite(self.bg, run_time=0.1),
            Transform(self.dot, rect),
        )

    def to_dot(self):
        self.bg.restore()
        return AnimationGroup(
            self.dot.animate.restore(),
            Write(self.bg, run_time=0.1),
            lag_ratio=0.9,
        )
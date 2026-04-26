# NOTE: this is for exploration of customized vmobject design
from manim import *

class Slist(VMobject):
    def __init__(
        self,
        n,
    ):
        super().__init__()
        self.squares = VGroup(
            Square(
                side_length=0.5,
                stroke_width=0,
                fill_opacity=1.0,
                fill_color=random_color(),
            ) for _ in range(n)
        ).arrange(RIGHT)
        self.add(self.squares)
    
class Demo(Scene):
    def construct(self):
        banner = ManimBanner()
        self.play(Write(banner))
        self.wait()
        self.play(banner.expand())
        self.wait()
        ApplyFunction
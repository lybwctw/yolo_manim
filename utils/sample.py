from manim import *

class VGSample(VMobject):
    def __init__(self):
        super().__init__()
        sq = Square()
        cr = Circle()
        vg = VGroup(sq, cr).arrange()
        self.add(vg)

class Demo(Scene):
    def construct(self) -> None:
        mob = VGSample()
        self.play(Create(mob))
        self.wait()
        self.play(mob.animate.scale(0.5))

class Demo2(Scene):
    def construct(self) -> None:
        mob = VGSample()
        self.play(Create(mob))
        self.wait()
        self.play(mob.animate.scale(1.5))
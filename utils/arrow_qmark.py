from manim import *

class ArrowQmark(VGroup):
    def __init__(self, adir, tdir, txt='?'):
        super().__init__()
        arrow = Arrow(start=ORIGIN, end=adir*3)
        text = Text(txt).next_to(arrow, tdir)
        self.arrow = arrow
        self.text = text
        self.add(
            self.arrow,
            self.text,
        )
        self.center()

class Demo(Scene):
    def construct(self):
        aq = ArrowQmark(DOWN, RIGHT)
        self.play(Write(aq))
        self.wait()
from manim import *

class MainScene(Scene):
    def construct(self) -> None:
        v = Integer(12.32)
        self.play(Write(v))
        self.wait()
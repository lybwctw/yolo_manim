from manim import *
import numpy as np
from utils.anchor_point import AnchorPoint

class Demo(Scene):
    def construct(self) -> None:
        ap = AnchorPoint((1,1,0), 0.01,(1,2,2,1))
        self.add(ap)
        self.wait()

        self.play(ap.to_rect(1.4))
        self.wait()
        self.play(ap.to_dot())
        self.wait()

        self.play(ap.to_rect(0.8))
        self.wait()
        self.play(ap.to_dot())
        self.wait()

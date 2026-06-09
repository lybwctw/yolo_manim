"""Usage
-----
Example inside a scene outside ``utils/``::

    from utils.prob_bars import ProbBars

    bars = ProbBars(point=UR, probs=[0.2, 0.7, 0.4])
    self.play(Create(bars))
"""

import sys
sys.path.append('..')

from manim import *
import numpy as np

COLOR_MAP = [RED, GREEN, BLUE]

class ProbBars(VGroup):
    def __init__(
        self,
        point: np.ndarray = ORIGIN,         # center of baseline
        space_length: float = 2.0,          # side length of square space
        bar_gap: float = 0.1,               # bar gap as space length ratio
        probs: list | tuple | np.ndarray | None = None,    # assume in the range (0,1)
        color_map: list | None = None,        # color for each bar
    ):
        """
        Example
        -------
        bars = ProbBars()
        """
        super().__init__()

        if isinstance(probs, np.ndarray):
            self.probs = probs.tolist()
        elif isinstance(probs, (list, tuple)):
            self.probs = probs
        self.n_probs = len(self.probs)
        self.space_length = space_length
        self.bar_gap = self.space_length * bar_gap
        self.bar_width = (self.space_length-2*self.bar_gap)/self.n_probs
        self.color_map = color_map

        # create baseline
        self.baseline = Line(LEFT, RIGHT)

        # create bars
        self.bars = VGroup()
        for i, p in enumerate(probs):
            bar = Rectangle(
                width=self.bar_width,
                height=p*self.space_length,
                stroke_width=0,
                fill_color=self.color_map[i],
                fill_opacity=1.0,
            )
            bar.align_to(
                self.baseline,
                LEFT,
            ).shift(
                i*(self.bar_width+self.bar_gap)*RIGHT,
            )
            bar.set_y(
                self.baseline.get_y(),
            )
            self.bars.add(bar)

        # baseline not shown
        self.add(self.bars)

        # move to point
        self.shift(point-self.baseline.get_center())

    # @override_animation(Create)
    # def create(
    #     self,
    #     **(aargs or {}),
    # ) -> Animation:
    #     _bars = self.bars.copy()
    #     for _bar in _bars:
    #         _bar.stretch_to_fit_height(0)
    #     return AnimationGroup(
    #         *(ReplacementTransform(_bar, bar)
    #           for _bar, bar in zip(_bars, self.bars)),
    #         **(aargs or {}),
    #     )

class Demo(Scene):
    def construct(self):
        probs = [0.2, 0.7, 0.4]

        bars = ProbBars(
            point=UR,
            probs=probs,
        )

        self.play(Write(Circle()))
        self.wait()

        self.play(Create(bars))
        self.wait()

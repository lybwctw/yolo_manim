from manim import *

class Loop(Animation):
    def __init__(
        self,
        mob,
        series: list,
        **kwargs,
    ):
        super().__init__(mob, **kwargs)
        self.series = [mob] + series
        self.max_idx = len(self.series) - 1
        self.idx = 0
    
    def interpolate_mobject(self, alpha):
        idx = round(self.rate_func(alpha) * self.max_idx)
        if self.idx != idx:
            self.mobject.become(self.series[idx])
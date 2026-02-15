from manim import *

class Learn(Scene):
    def focus_on(self, idx):
        def _focus_on(vg):
            # vg.save_state()
            vg.arrange_in_grid(buff=3)
            vg[idx].scale(3.)
            vg.shift(-vg[idx].get_center())
            return vg
        return _focus_on
    def construct(self) -> None:
        vg = VGroup(
            Square().scale(.3) for _ in range(6)
        )
        vg[1] = VMobject()
        vg[3] = VMobject()

        vg.arrange_in_grid(rows=3, cols=2)

        self.play(Write(vg, lag_ratio=0.0))
        self.wait()

        extra = VGroup(
            Square().scale(.3) for _ in range(3)
        ).arrange(DOWN).shift(RIGHT*10)

        # make things simple instead of general
        for i, e in zip([2,5,8], extra):
            vg.insert(i, e)
        self.play(vg.animate.arrange_in_grid(rows=3, cols=3).center())
        self.wait()
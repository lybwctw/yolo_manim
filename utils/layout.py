from manim import *

class Learn(Scene):
    def focus_on(self, idx):
        def _focus_on(vg):
            vg.arrange_in_grid(buff=10)
            vg[idx].scale(3.)
            vg.shift(-vg[idx].get_center())
            return vg
        return _focus_on
    def construct(self) -> None:
        vg = VGroup(
            Square().scale(.3) for _ in range(6)
        )
        vg[2] = VMobject()
        vg.arrange_in_grid(rows=2, cols=3)

        self.add(vg)
        vg.save_state()
        self.play(
            ApplyFunction(self.focus_on(0), vg),
        )
        self.wait()
        self.play(
            vg.animate.restore(),
        )
        self.wait()
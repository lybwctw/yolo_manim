import sys
sys.path.append('..')

from manim import *

DEFAULT_AC_CONFIG = {
    'color': WHITE,
}

class ArrowComment(VMobject):
    def __init__(
        self,
        double: bool = False,                   # double arrow or not
        direction: np.ndarray = RIGHT,          # direction of arrow
        comment: str = '',                      # not used for now
        arrow_config: dict = {},                # override default config
    ):
        """
        Example
        -------
        from manim import *
        class Demo(Scene):
            def construct(self):
                a1 = ArrowComment()
                self.play(Write(a1))
                self.wait()
        """
        super().__init__()
        self.comment = comment      # not implemented yet

        mtype = DoubleArrow if double else Arrow

        arrow_config = {**DEFAULT_AC_CONFIG, **arrow_config}

        self.arrow = mtype(
            start=-direction,
            end=direction,
            **arrow_config,
        )

        self.add(self.arrow)

class Demo(Scene):
    def construct(self):
        a1 = ArrowComment()
        self.play(Write(a1))
        self.wait()

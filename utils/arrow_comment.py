"""Usage
-----
Example inside a scene outside ``utils/``::

    from utils.arrow_comment import ArrowComment

    a1 = ArrowComment(double=True, direction=DOWN)
    self.play(Write(a1))
"""

import sys
sys.path.append('..')

from manim import *
from manim.typing import MultiMappingFunction, Point3DLike, Vector3DLike

DOUBLE_AC_CONFIG = {
    'color': GRAY,
}

SINGLE_AC_CONFIG = {
    'color': WHITE,
}

class ArrowComment(VMobject):
    def __init__(
        self,
        double: bool = False,                   # double arrow or not
        direction: np.ndarray = RIGHT,          # direction of arrow
        comment: str = '',                     # pop out comment
    ):
        """
        Example
        -------
        arrow_comment = ArrowComment()
        """
        super().__init__()
        self.comment = comment      # not implemented yet

        if double:
            self.arrow = DoubleArrow(
                start=-direction,
                end=direction,
                **DOUBLE_AC_CONFIG,
            )
        else:
            self.arrow = Arrow(
                start=-direction,
                end=direction,
                **SINGLE_AC_CONFIG,
            )

        self.add(self.arrow)

class Demo(Scene):
    def construct(self):
        a1 = ArrowComment(double=True, direction=DOWN)
        self.play(Write(a1))
        self.wait()

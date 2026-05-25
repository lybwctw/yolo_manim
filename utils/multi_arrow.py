"""Usage
-----
Example inside a scene outside ``utils/``::

    from utils.multi_arrow import MultiArrow

    marrow = MultiArrow(one_to_many=True, p1=UR, p2=DR + LEFT*2)
    self.play(Write(marrow))
    marrow.save_state()
    self.play(marrow.animate.fade(0.9))
    self.play(marrow.animate.restore())
"""

import sys
sys.path.append('..')

from manim import *

# MultiArrow config
RATIO_OUTPUT = 0.3          # output arrow width / vertical distance
RATIO_BRACE = 0.5     # brace width / vertical distance
RATIO_INPUT = 0.3           # input line width / vertical distance

ARROW_CONFIG = {
    'stroke_width': 3,
    'tip_length': 0.15,
    'buff': 0.0,
    'max_stroke_width_to_length_ratio': 25,         # 5 by default
    'max_tip_length_to_length_ratio': 1.0,          # 0.25 by default
}

LINE_CONFIG = {
    'stroke_width': 3,
}

class BraceLike(VMobject):
    def __init__(
        self,
        one_to_many: bool = True,       # single input, multi output
        key: np.ndarray = RIGHT,        # right central point
        width: float = 2,               # width of the brace space
        height: float = 2,              # height of the brace space
        stroke_width: float = 3,        # stroke width
    ):
        """
        Example
        -------
        brace = BraceLike()
        """
        super().__init__()
        self.one_to_many = one_to_many

        if self.one_to_many:
            p1 = key + width*LEFT
            p2 = key + height*UP/2
        else:
            p1 = key + height*UP/2
            p2 = key + width*RIGHT

        b1 = CubicBezier(
            p1,
            p1+RIGHT*0.75*width,
            p2+LEFT*0.75*width,
            p2,
            stroke_width=stroke_width,
        )
        b2 = b1.copy().flip(
            axis=RIGHT,
            about_point=b1.get_bottom(),
        )
        self.b1 = b1
        self.b2 = b2
        self.add(self.b1, self.b2)


class MultiArrow(VMobject):
    def __init__(
        self,
        one_to_many: bool = True,       # single input, multi output
        p1: np.ndarray = UR,            # up corner point
        p2: np.ndarray = DR,            # down corner point
        ratio_input: float = RATIO_INPUT,
        ratio_brace: float = RATIO_BRACE,
        ratio_output: float = RATIO_OUTPUT,
        comment: str = '',
    ):
        """
        Example
        -------
        marrow = MultiArrow()
        """
        super().__init__()
        self.one_to_many = one_to_many
        self.ratio_input = ratio_input
        self.ratio_brace = ratio_brace
        self.ratio_output = ratio_output

        _input, _brace, _output = self._load_ibo(
            one_to_many=self.one_to_many,
            p1=p1,
            p2=p2,
        )

        self.input = _input
        self.brace = _brace
        self.output = _output

        self.add(self.input)
        self.add(self.brace)
        self.add(self.output)

    def _load_ibo(
        self,
        one_to_many: bool = True,
        p1: np.ndarray = UR,
        p2: np.ndarray = DR,
    ) -> tuple:
        """
        Load input, brace, output.

        Example
        -------
        marrow = MultiArrow()
        result = marrow._load_ibo()
        """
        bwidth = abs(float(p1[1] - p2[1]))
        input_width = bwidth * self.ratio_input
        brace_width = bwidth * self.ratio_brace
        output_width = bwidth * self.ratio_output
        if one_to_many:
            bend_x = min(float(p1[0]), float(p2[0])) - output_width
            bend_1 = np.array([bend_x, p1[1], 0])
            bend_2 = np.array([bend_x, p2[1], 0])
            bend_k = (bend_1 + bend_2) / 2
            iend = bend_k + LEFT * brace_width
            istart = iend + LEFT * input_width

            # create input line
            iput = Line(
                start=istart,
                end=iend,
                **LINE_CONFIG,
            )

            # create brace
            brace = BraceLike(
                one_to_many=True,
                key=bend_k,
                width=brace_width,
                height=bwidth,
            )

            # create output arrows
            output = VGroup(
                Arrow(
                    start=bend_1,
                    end=p1,
                    **ARROW_CONFIG,
                ),
                Arrow(
                    start=bend_2,
                    end=p2,
                    **ARROW_CONFIG,
                ),
            )

        else:
            bstart_x = max(float(p1[0]),float(p2[0])) + input_width
            bstart_1 = np.array([bstart_x, p1[1], 0])
            bstart_2 = np.array([bstart_x, p2[1], 0])
            bstart_k = (bstart_1 + bstart_2) / 2
            ostart = bstart_k + RIGHT * brace_width
            oend = ostart + RIGHT * output_width

            # create input lines
            iput = VGroup(
                Line(
                    start=p1,
                    end=bstart_1,
                    **LINE_CONFIG,
                ),
                Line(
                    start=p2,
                    end=bstart_2,
                    **LINE_CONFIG,
                ),
            )

            # create brace
            brace = BraceLike(
                one_to_many=False,
                key=bstart_k,
                width=brace_width,
                height=bwidth,
            )

            # create output arrow
            output = Arrow(
                start=ostart,
                end=oend,
                **ARROW_CONFIG,
            )
        return iput, brace, output

class Demo(Scene):
    def construct(self):
        p1 = UR
        p2 = DR + LEFT*2
        marrow = MultiArrow(
            one_to_many=True,
            p1=p1,
            p2=p2,
        )
        self.play(Write(marrow))
        self.wait()

        marrow.save_state()
        self.play(marrow.animate.fade(0.9))
        self.wait()
        self.play(marrow.animate.restore())
        self.wait()

from manim import *

import numpy as np
from utils.constants import *

# CORNER_OFFSETS = [
#     UP*0.85,
#     DOWN*0.85,
#     UP*0.85,
#     DOWN*0.85,
# ]

FRAME_WIDTH = 6.4
FRAME_COORD_WIDTH = 640
FRAME_COORD_HEIGHT = 360
FRAME_SCALE = FRAME_WIDTH / FRAME_COORD_WIDTH
FRAME_HEIGHT = FRAME_COORD_HEIGHT * FRAME_SCALE
HORIZONTAL_SHIFT = 0.5
FRAME_LEFT = -6.25 + HORIZONTAL_SHIFT
FRAME_TOP = 2.0

BOX_A_COLOR = ORANGE
BOX_B_COLOR = PURE_RED
INTERSECTION_COLOR = WHITE
UNION_COLOR = WHITE

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ####################################################################
        self.next_section('what IoU measures', skip_animations=False)
        # ####################################################################

        # title = Text(
        #     'Intersection over Union (IoU)',
        #     font='JetBrains Mono',
        #     font_size=30,
        # ).to_edge(UP, buff=0.25)
        # self.play(Write(title))

        frame = Rectangle(
            width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            stroke_color=WHITE,
            stroke_width=2,
        ).move_to(
            [
                FRAME_LEFT + FRAME_WIDTH / 2,
                FRAME_TOP - FRAME_HEIGHT / 2,
                0,
            ]
        )
        self.play(Create(frame))

        a_initial = (100, 80, 400, 280)
        b_initial = (280, 140, 540, 320)
        a_x1, a_y1, a_x2, a_y2 = (ValueTracker(value) for value in a_initial)
        b_x1, b_y1, b_x2, b_y2 = (ValueTracker(value) for value in b_initial)

        def point(x, y):
            return np.array([
                FRAME_LEFT + x * FRAME_SCALE,
                FRAME_TOP - y * FRAME_SCALE,
                0,
            ])

        def static_box_rect(coords):
            x1, y1, x2, y2 = coords
            return Rectangle(
                width=(x2 - x1) * FRAME_SCALE,
                height=(y2 - y1) * FRAME_SCALE,
                stroke_width=0,
            ).move_to(point((x1 + x2) / 2, (y1 + y2) / 2))

        def box_rect(x1, y1, x2, y2, color, fill_opacity):
            width = max(0.001, x2.get_value() - x1.get_value()) * FRAME_SCALE
            height = max(0.001, y2.get_value() - y1.get_value()) * FRAME_SCALE
            center = point(
                (x1.get_value() + x2.get_value()) / 2,
                (y1.get_value() + y2.get_value()) / 2,
            )
            return Rectangle(
                width=width,
                height=height,
                stroke_color=color,
                stroke_width=2.5,
                fill_color=color,
                fill_opacity=fill_opacity,
            ).move_to(center)

        box_a_fill = always_redraw(
            lambda: box_rect(a_x1, a_y1, a_x2, a_y2, BOX_A_COLOR, 0)
        )
        box_b_fill = always_redraw(
            lambda: box_rect(b_x1, b_y1, b_x2, b_y2, BOX_B_COLOR, 0)
        )

        initial_box_a = static_box_rect(a_initial)
        initial_box_b = static_box_rect(b_initial)
        overlap = Intersection(initial_box_a, initial_box_b)
        overlap.set_fill(INTERSECTION_COLOR, opacity=0.65).set_stroke(width=0)
        union = Union(initial_box_a, initial_box_b)
        union.set_fill(UNION_COLOR, opacity=0.65).set_stroke(width=0)

        def corner_label(x, y, text, color, direction):
            return Text(
                text,
                font='JetBrains Mono',
                font_size=10,
                color=color,
            ).next_to(point(x.get_value(), y.get_value()), direction, buff=0.12)

        corner_labels = [
            always_redraw(
                lambda x=x, y=y, label=label, color=color, direction=direction:
                    corner_label(x, y, label, color, direction)
            )
            for x, y, label, color, direction in (
                (a_x1, a_y1, '(x1a,y1a)', BOX_A_COLOR, UP),
                (a_x2, a_y2, '(x2a,y2a)', BOX_A_COLOR, DOWN),
                (b_x1, b_y1, '(x1b,y1b)', BOX_B_COLOR, UP),
                (b_x2, b_y2, '(x2b,y2b)', BOX_B_COLOR, DOWN),
            )
        ]
        self.play(AnimationGroup(
            Write(box_a_fill),
            Write(box_b_fill),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(Write(label) for label in corner_labels),
            lag_ratio=0.5,
            run_time=wt*2,
        ))
        self.wait(wt)

        self.play(
            FadeIn(overlap),
            run_time=wt,
        )
        self.wait(wt)
        self.play(FadeOut(overlap), run_time=wt)
        self.play(FadeIn(union), run_time=wt)
        self.wait(wt)
        self.play(FadeOut(union), run_time=wt)

        def geometry():
            ax1, ay1, ax2, ay2 = (
                round(v.get_value()) for v in (a_x1, a_y1, a_x2, a_y2)
            )
            bx1, by1, bx2, by2 = (
                round(v.get_value()) for v in (b_x1, b_y1, b_x2, b_y2)
            )
            x1I, y1I = max(ax1, bx1), max(ay1, by1)
            x2I, y2I = min(ax2, bx2), min(ay2, by2)
            SI = max(0, x2I - x1I) * max(0, y2I - y1I)
            Sa = (ax2 - ax1) * (ay2 - ay1)
            Sb = (bx2 - bx1) * (by2 - by1)
            SU = Sa + Sb - SI
            IoU = SI / SU if SU else 0
            return (ax1, ay1, ax2, ay2, bx1, by1, bx2, by2,
                    x1I, y1I, x2I, y2I, SI, Sa, Sb, SU, IoU)

        formula_x = 1.0 + HORIZONTAL_SHIFT
        formula_specs = [
            (
                'x1I = max(x1a,x1b)',
                lambda g: f'x1I = max({g[0]},{g[4]}) = {g[8]}',
                INTERSECTION_COLOR,
            ),
            (
                'y1I = max(y1a,y1b)',
                lambda g: f'y1I = max({g[1]},{g[5]}) = {g[9]}',
                INTERSECTION_COLOR,
            ),
            (
                'x2I = min(x2a,x2b)',
                lambda g: f'x2I = min({g[2]},{g[6]}) = {g[10]}',
                INTERSECTION_COLOR,
            ),
            (
                'y2I = min(y2a,y2b)',
                lambda g: f'y2I = min({g[3]},{g[7]}) = {g[11]}',
                INTERSECTION_COLOR,
            ),
            (
                'SI = max(0,x2I-x1I) x max(0,y2I-y1I)',
                lambda g: f'SI = max(0,{g[10]}-{g[8]}) * max(0,{g[11]}-{g[9]}) = {g[12]}',
                INTERSECTION_COLOR,
            ),
            (
                'Sa = (x2a-x1a) x (y2a-y1a)',
                lambda g: f'Sa = ({g[2]}-{g[0]}) * ({g[3]}-{g[1]}) = {g[13]}',
                BOX_A_COLOR,
            ),
            (
                'Sb = (x2b-x1b) x (y2b-y1b)',
                lambda g: f'Sb = ({g[6]}-{g[4]}) * ({g[7]}-{g[5]}) = {g[14]}',
                BOX_B_COLOR,
            ),
            (
                'SU = Sa + Sb - SI',
                lambda g: f'SU = {g[13]} + {g[14]} - {g[12]} = {g[15]}',
                UNION_COLOR,
            ),
            (
                'IoU = SI / SU',
                lambda g: f'IoU = {g[12]} / {g[15]} = {g[16]:.3f}',
                WHITE,
            ),
        ]
        formula_gap = FRAME_HEIGHT / len(formula_specs)
        formula_top = FRAME_TOP - formula_gap / 2

        def formula_prefix(text, row_idx, color):
            return Text(
                text,
                font='JetBrains Mono',
                font_size=10,
                color=color,
            ).move_to(
                [formula_x, formula_top - row_idx * formula_gap, 0],
                aligned_edge=LEFT,
            )

        formula_prefixes = []
        abstract_rhs_rows = []
        exact_rhs_rows = []
        for idx, (abstract, formatter, color) in enumerate(formula_specs):
            lhs, abstract_rhs = abstract.split('=', 1)
            prefix = formula_prefix(f'{lhs.strip()} =', idx, color)
            formula_prefixes.append(prefix)
            abstract_rhs_rows.append(
                Text(
                    abstract_rhs.strip(),
                    font='JetBrains Mono',
                    font_size=10,
                    color=color,
                ).next_to(prefix, RIGHT, buff=0.08)
            )
            exact_rhs_rows.append(
                always_redraw(
                    lambda formatter=formatter, color=color, prefix=prefix: Text(
                        formatter(geometry()).split('=', 1)[1].strip(),
                        font='JetBrains Mono',
                        font_size=10,
                        color=color,
                    ).next_to(prefix, RIGHT, buff=0.08)
                )
            )
        exact_corner_labels = [
            always_redraw(
                lambda x=x, y=y, color=color, direction=direction:
                    corner_label(
                        x,
                        y,
                        f'({round(x.get_value())}, {round(y.get_value())})',
                        color,
                        direction,
                    )
            )
            for x, y, color, direction in (
                (a_x1, a_y1, BOX_A_COLOR, UP),
                (a_x2, a_y2, BOX_A_COLOR, DOWN),
                (b_x1, b_y1, BOX_B_COLOR, UP),
                (b_x2, b_y2, BOX_B_COLOR, DOWN),
            )
        ]

        self.play(AnimationGroup(
            *(
                Write(mobject)
                for row in zip(formula_prefixes, abstract_rhs_rows)
                for mobject in row
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(ReplacementTransform(label, exact) for label, exact in zip(
                corner_labels, exact_corner_labels
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        # for abstract_rhs, exact_rhs in zip(abstract_rhs_rows, exact_rhs_rows):
        #     self.play(ReplacementTransform(abstract_rhs, exact_rhs), run_time=wt)
        self.play(AnimationGroup(
            *(ReplacementTransform(abstract_rhs, exact_rhs) for abstract_rhs, exact_rhs in zip(
                abstract_rhs_rows, exact_rhs_rows
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ####################################################################
        self.next_section('no overlap', skip_animations=False)
        # ####################################################################
        detached_x1 = a_initial[2] + 30
        detached_y1 = a_initial[1]
        self.play(
            b_x1.animate.set_value(detached_x1),
            b_y1.animate.set_value(detached_y1),
            b_x2.animate.set_value(detached_x1 + 150),
            b_y2.animate.set_value(detached_y1 + 150),
            run_time=wt*2,
        )
        self.wait(wt)

        # ####################################################################
        self.next_section('one box inside the other', skip_animations=False)
        # ####################################################################
        contained_x1 = a_initial[0] + (a_initial[2] - a_initial[0]) * 0.25
        contained_y1 = a_initial[1] + (a_initial[3] - a_initial[1]) * 0.25
        self.play(
            b_x1.animate.set_value(contained_x1),
            b_y1.animate.set_value(contained_y1),
            b_x2.animate.set_value(a_initial[0] + (a_initial[2] - a_initial[0]) * 0.75),
            b_y2.animate.set_value(a_initial[1] + (a_initial[3] - a_initial[1]) * 0.75),
            run_time=wt*2,
        )
        self.wait(wt)

        # ####################################################################
        self.next_section('near-perfect overlap', skip_animations=False)
        # ####################################################################
        self.play(
            b_x1.animate.set_value(a_initial[0] + 1),
            b_y1.animate.set_value(a_initial[1] + 1),
            b_x2.animate.set_value(a_initial[2] + 1),
            b_y2.animate.set_value(a_initial[3] + 1),
            run_time=wt*2,
        )
        self.wait(wt)

        # ####################################################################
        self.next_section('return to partial overlap', skip_animations=False)
        # ####################################################################
        self.play(
            b_x1.animate.set_value(b_initial[0]),
            b_y1.animate.set_value(b_initial[1]),
            b_x2.animate.set_value(b_initial[2]),
            b_y2.animate.set_value(b_initial[3]),
            run_time=wt*2,
        )
        self.wait(wt)

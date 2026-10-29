from manim import *
from utils.constants import *
from utils.general import *

DEFAULT_SQAURE_CONFIG = {
    'side_length': 0.4,
    'stroke_width': 2.0,
    'stroke_color': WHITE,
    'stroke_opacity': 1.0,
    'fill_opacity': 0.9,
    'fill_color': BLACK,
}

DEFAULT_DOT_CONFIG = {
    'radius': 0.02,
    'stroke_opacity': 0.0,
    'fill_color': WHITE,
    'fill_opacity': 1.0,
}

CHANNELS_OFFSET = UR * 0.2

SAMPLE_O_IDX = 8
SAMPLE_I_IDXS = [11, 12, 18, 19]

def create_cells(
    rows=6,
    cols=7,
):
    cells_rgb = VGroup(
        VGroup(
            Square(
                **DEFAULT_SQAURE_CONFIG,
            ) for _ in range(rows*cols)
        ).arrange_in_grid(
            rows=rows,
            cols=cols,
            buff=0.0,
        ) for _ in range(3)
    )
    cells_rgb[0].set_z_index(3)
    cells_rgb[1].set_z_index(2).shift(CHANNELS_OFFSET)
    cells_rgb[2].set_z_index(1).shift(CHANNELS_OFFSET*2)
    return cells_rgb

def create_dots(
    cells,
):
    dots = VGroup()
    for cell in cells:
        dot = Dot(**DEFAULT_DOT_CONFIG).move_to(cell)
        dots.add(dot)
    return dots

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'show inputs and outputs',
            skip_animations=False,
        )
        # ************************************************************
        cells_input_rgb = create_cells(6,7)
        cells_output_rgb = create_cells(4,5)
        VGroup(cells_input_rgb, cells_output_rgb).arrange(
            RIGHT, buff=2.0,
        )

        self.play(AnimationGroup(
            Write(cells_input_rgb),
            Write(cells_output_rgb),
            run_time=wt,
        ))
        self.wait(wt)

        # focus on mid channel
        self.play(AnimationGroup(
            FadeOut(cells_input_rgb[2], run_time=wt),
            FadeOut(cells_input_rgb[0], run_time=wt),
            FadeOut(cells_output_rgb[2], run_time=wt),
            FadeOut(cells_output_rgb[0], run_time=wt),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(
            cells_input_rgb[1].animate(
                run_time=wt,
            ).set_fill(opacity=0.0),
            cells_output_rgb[1].animate(
                run_time=wt,
            ).set_fill(opacity=0.0),
            lag_ratio=0.0,
        )
        self.wait(wt)
        cells_i = cells_input_rgb[1]
        cells_o = cells_output_rgb[1]

        # ************************************************************
        self.next_section(
            'same width/height and central points',
            skip_animations=False,
        )
        # ************************************************************
        self.play(cells_o.animate(
            run_time=wt,
        ).stretch_to_fit_width(
            cells_i.width,
        ))
        self.play(cells_o.animate(
            run_time=wt,
        ).stretch_to_fit_height(
            cells_i.height,
        ))
        self.wait(wt)

        # create dots for input and output
        dots_i = create_dots(cells_i)
        dots_o = create_dots(cells_o)
        self.play(AnimationGroup(
            cells_i.animate.set_stroke(opacity=0.05),
            cells_o.animate.set_stroke(opacity=0.05),
            FadeIn(dots_i),
            FadeIn(dots_o),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'output dots in input space',
            skip_animations=False,
        )
        # ************************************************************
        self.play(dots_o.animate(
            run_time=wt,
        ).set_fill(
            color=PURE_RED,
        ))
        self.wait(wt)

        dots_oi = dots_o.copy()
        offset = dots_oi.get_corner(UL) - cells_o.get_corner(UL)
        dots_oi.move_to(cells_i, aligned_edge=UL)
        dots_oi.shift(offset)
        self.play(FadeIn(dots_oi, run_time=wt))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on sample dots',
            skip_animations=False,
        )
        # ************************************************************
        sample_o_idx = SAMPLE_O_IDX
        sample_i_idxs = SAMPLE_I_IDXS

        other_o_idxs = [x for x in range(len(dots_o)) if x != sample_o_idx]
        other_i_idxs = [x for x in range(len(dots_i)) if x not in sample_i_idxs]

        # focus on sample output dot
        self.play(AnimationGroup(
            *(dots_o[idx].animate.set_fill(opacity=0.1)
             for idx in other_o_idxs),
            *(dots_oi[idx].animate.set_fill(opacity=0.1)
             for idx in other_o_idxs),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # focus on sample input dots
        self.play(AnimationGroup(
            *(dots_i[idx].animate.set_fill(opacity=0.1)
             for idx in other_i_idxs),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'export',
            skip_animations=False,
        )
        # ************************************************************
        mobs = VGroup(
            cells_i,
            cells_o,
            dots_i,
            dots_o,
            dots_oi,
        )
        export_mobs(__file__, mobs)
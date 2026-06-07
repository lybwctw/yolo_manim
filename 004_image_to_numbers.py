from manim import *
from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.color_cell import load_central_cells

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init from previous',
            skip_animations=False,
        )
        # ************************************************************
        (
            sin_raw, cells
        ) = import_mobs('001')

        # FIXME: to do with 360/2
        focus_cells = load_central_cells(
            PATH_IMAGE_640,
            rows=8,
            cols=8,
            target_height=config.frame_height/2,
        )

        # ************************************************************
        self.next_section(
            'focus on central cells',
            skip_animations=False,
        )
        # ************************************************************
        self.add(cells, focus_cells)
        self.wait(wt)
        self.play(FadeOut(
            cells,
            run_time=wt,
        ))
        self.wait(wt)

        # adjust perspective
        self.move_camera(
            phi=60*DEGREES,
            theta=-75*DEGREES,
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'split into color channels then numbers',
            skip_animations=False,
        )
        # ************************************************************
        cells_r = focus_cells.copy().set_z_index(5) # match with text's 6
        cells_g = focus_cells.copy().set_z_index(3) # match with text's 4
        cells_b = focus_cells.copy().set_z_index(1) # match with text's 2
        self.add(cells_r, cells_g, cells_b)
        self.remove(focus_cells)

        # split into 3 channels
        self.play(AnimationGroup(
            AnimationGroup(
                c.animate.\
                    set_fill(rgb_to_color((c.r, 0, 0))).\
                    set_opacity(0.5).\
                    set_stroke(opacity=0.5,color=BLACK).\
                    shift(OUT*0.5)\
                for c in cells_r
            ),
            AnimationGroup(
                c.animate.\
                    set_fill(rgb_to_color((0, c.g, 0))).\
                    set_opacity(0.5).\
                    set_stroke(opacity=0.5,color=BLACK)\
                for c in cells_g
            ),
            AnimationGroup(
                c.animate.\
                    set_fill(rgb_to_color((0, 0, c.b))).\
                    set_opacity(0.5).\
                    set_stroke(opacity=0.5,color=BLACK).\
                    shift(IN*0.5)\
                for c in cells_b
            ),
            run_time=wt,
        ))
        self.wait(wt)

        # show numbers for each channel
        self.play(AnimationGroup(
            AnimationGroup(
                c.write_digit('r') for c in cells_r
            ),
            AnimationGroup(
                c.write_digit('g') for c in cells_g
            ),
            AnimationGroup(
                c.write_digit('b') for c in cells_b
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # back to top perspective
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            added_anims=[
                cells_r.animate.shift(DL*0.3),
                cells_b.animate.shift(UR*0.3),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back into color channels into single channel',
            skip_animations=False,
        )
        # ************************************************************
        # from numbers into colors
        self.play(AnimationGroup(
            cells_r.animate.shift(UR * 0.3),
            cells_b.animate.shift(DL * 0.3),
            AnimationGroup(
                c.unwrite_digit('r') for c in cells_r
            ),
            AnimationGroup(
                c.unwrite_digit('g') for c in cells_g
            ),
            AnimationGroup(
                c.unwrite_digit('b') for c in cells_b
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # merge channels
        self.play(AnimationGroup(
            AnimationGroup(
                c.animate. \
                    set_fill(c._color,opacity=1.0). \
                    set_stroke(opacity=1.0, color=BLACK). \
                    shift(IN*0.5 + UR*0.3) \
                for c in cells_r
            ),
            AnimationGroup(
                c.animate. \
                    set_fill(c._color,opacity=1.0). \
                    set_stroke(opacity=1.0, color=BLACK) \
                for c in cells_g
            ),
            AnimationGroup(
                c.animate. \
                    set_fill(c._color,opacity=1.0). \
                    set_stroke(opacity=1.0, color=BLACK). \
                    shift(OUT*0.5 + DL*0.3) \
                for c in cells_b
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back into screen cell then raw image',
            skip_animations=False,
        )
        # ************************************************************
        self.play(FadeIn(
            cells,
            run_time=wt,
        ))
        self.play(FadeOut(
            cells_r,
            cells_g,
            cells_b,
            run_time=wt,
        ))
        self.wait(wt)

        self.bring_to_back(sin_raw)
        self.play(Unwrite(
            cells,
            run_time=wt,
        ))
        self.wait(wt)
        self.play(sin_raw.animate(
            run_time=wt,
        ).scale_to_fit_height(J000_IMAGE_HEIGHT))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'save mobs, used by 005',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # mobs = Group(
        #     sin_raw,
        # )
        # export_mobs(__file__, mobs)
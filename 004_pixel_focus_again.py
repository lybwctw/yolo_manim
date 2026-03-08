from manim import *
from utils.constants import *
from utils.general import load_everything, load_central_cells, save_everything

class MainScene(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES)

        (
            image_raw, cells
        ) = load_everything(S001_EVERYTHING)
        c_cells = load_central_cells(
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
        self.add(cells, c_cells)
        self.wait()
        self.play(FadeOut(cells))
        self.wait()

        # ************************************************************
        self.next_section(
            'adjust view point',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            phi=60*DEGREES,
            theta=-75*DEGREES,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'split into 3 channels',
            skip_animations=False,
        )
        # ************************************************************
        cells_r = c_cells.copy().set_z_index(5) # match with text's 6
        cells_g = c_cells.copy().set_z_index(3) # match with text's 4
        cells_b = c_cells.copy().set_z_index(1) # match with text's 2
        self.add(cells_r, cells_g, cells_b)
        self.remove(c_cells)

        self.play(AnimationGroup(
            AnimationGroup(
                c.animate.\
                    set_fill(rgb_to_color((c.r, 0, 0))).\
                    set_opacity(0.5).\
                    set_stroke(opacity=1.0,color=WHITE).\
                    shift(OUT*0.5)\
                for c in cells_r
            ),
            AnimationGroup(
                c.animate.\
                    set_fill(rgb_to_color((0, c.g, 0))).\
                    set_opacity(0.5).\
                    set_stroke(opacity=1.0,color=WHITE)\
                for c in cells_g
            ),
            AnimationGroup(
                c.animate.\
                    set_fill(rgb_to_color((0, 0, c.b))).\
                    set_opacity(0.5).\
                    set_stroke(opacity=1.0,color=WHITE).\
                    shift(IN*0.5)\
                for c in cells_b
            ),
        ))
        cells_g.set_stroke()

        # ************************************************************
        self.next_section(
            'show digits for each channel',
            skip_animations=False,
        )
        # ************************************************************
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
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'back to top view point, channels shift',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            added_anims=[
                cells_r.animate.shift(DL*0.3),
                cells_b.animate.shift(UR*0.3),
            ]
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'digit to color for each channels',
            skip_animations=False,
        )
        # ************************************************************
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
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'merge channels',
            skip_animations=False,
        )
        # ************************************************************
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
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'show edge cells',
            skip_animations=False,
        )
        # ************************************************************
        self.play(FadeIn(cells))
        self.play(FadeOut(cells_r, cells_g, cells_b),)
        self.wait()

        # ************************************************************
        self.next_section(
            'scale back to show image_raw',
            skip_animations=False,
        )
        # ************************************************************
        # add image_raw and remove cells
        self.bring_to_back(image_raw)
        self.play(Unwrite(cells))
        self.wait()
        self.play(image_raw.animate.scale_to_fit_height(6.4/2))   # FIXME, make height variable
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene, explain RGB color space',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(image_raw)
        save_everything(S004_EVERYTHING, everything)
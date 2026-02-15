from manim import *

class TimeWidthValues(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)
        cube = Cube(stroke_width=0, fill_opacity=0.6, fill_color=GREEN_E)
        path = VMobject()
        path.set_points_as_corners([
            cube.get_corner(LEFT+DOWN+IN),
            cube.get_corner(LEFT+DOWN+OUT),
            cube.get_corner(LEFT+UP+OUT),
            cube.get_corner(RIGHT+UP+OUT),
        ])
        # sq.set_points_as_corners([LEFT, LEFT])
        # sq.add_points_as_corners([RIGHT, UP])
        # self.add(sq)
        # self.play(ShowPassingFlash(sq, run_time=2, time_width=0.8))

        self.play(Write(cube))
        self.wait()
        self.play(ShowPassingFlash(path, run_time=2, time_width=1.8))
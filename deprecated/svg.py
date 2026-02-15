from manim import *

class Sample(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=60*DEGREES, theta=-100*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        svg = SVGMobject(r'C:\Users\lybwc\Desktop\svgs\hugging.svg')
        svg2 = SVGMobject(r'C:\Users\lybwc\Desktop\svgs\poker.svg')
        svg2.remove(svg2[0])
        svg2.rotate(90*DEGREES, RIGHT)
        svg.rotate(90*DEGREES, RIGHT)
        self.wait()
        self.play(Write(svg))
        self.wait(2)

        self.play(Transform(svg, svg2))
        self.wait(2)

        self.stop_ambient_camera_rotation()
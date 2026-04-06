import sys
sys.path.append('..')

from manim import *
import numpy as np

from utils.anchor_point import AnchorPoint
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import SingleAnnotation

class ExplainerBbox(VGroup):
    def __init__(
        self,
        background: ImageRaw | ImagePad | None = None,
        data: np.array = np.ones((4,4,4)),      # (h, w, 4)
    ):
        super().__init__()
        self.background = background
        self.data = data

        self.grid_shape = data.shape[:2]
        self.h, self.w = self.grid_shape

    def create_grid(
        self,
        **kwargs,
    ):
        grid = Rectangle(
            width=self.background.width,
            height=self.background.height,
            stroke_width=1,
            grid_xstep=self.background.width/self.w,
            grid_ystep=self.background.height/self.h,
        )
        grid.grid_lines.set_stroke(width=1)
        grid.move_to(
            self.background.get_corner(UL),
            aligned_edge=UL,
        )

        self.grid = grid
        self.add(self.grid)
        return Write(self.grid, **kwargs)

    def remove_grid(
        self,
        **kwargs,
    ):
        self.remove(self.grid)
        return Unwrite(self.grid, **kwargs)

    def create_anchor_points(
        self,
        **kwargs,
    ):
        base = self.background.get_corner(UL)
        anchor_points = VGroup(*[
            AnchorPoint(
                base+DOWN*self.sx*(i+0.5)+RIGHT*self.sy*(j+0.5),
                offset=self.data[i,j],
                s_xy=(self.sx, self.sy),
            )
            for i in range(self.h)
            for j in range(self.w)
        ])

        self.anchor_points = anchor_points
        self.add(self.anchor_points)
        return Write(self.anchor_points,**kwargs)

    def to_rects(
        self,
        **kwargs,
    ):
        anims = AnimationGroup(
            *(ap.to_rect() for ap in self.anchor_points),
            **kwargs,
        )
        return anims

    def to_dots(
        self,
        **kwargs,
    ):
        anims = AnimationGroup(
            *(ap.to_dot() for ap in self.anchor_points),
            **kwargs,
        )
        return anims

    def remove_anchor_points(
        self,
        **kwargs,
    ):
        self.remove(self.anchor_points)
        return Unwrite(self.anchor_points,**kwargs)

    def collect_in_out_aps(
        self,
        annotation: VGroup | None,      # VGroup of SingleAnnotation
    ):
        """FIXME, collect aps inside/outside a group of SingleAnnotation.
        """
        def _inside(point, anno):
            x, y, _ = point
            return (
                anno.bbox.get_left()[0] <= x <= anno.bbox.get_right()[0]
                and anno.bbox.get_bottom()[1] <= y <= anno.bbox.get_top()[1]
            )
        in_aps = VGroup()
        out_aps = VGroup()
        for ap in self.anchor_points:
            if any(_inside(ap.get_center(), anno) for anno in annotation):
                in_aps.add(ap)
            else:
                out_aps.add(ap)
        return in_aps, out_aps
        

    @property
    def sx(self):
        return self.background.width/self.w

    @property
    def sy(self):
        return self.background.height/self.h

class Demo(Scene):
    def construct(self):
        sq = Square(
            stroke_opacity=0,
            fill_opacity=0.3,
        ).scale(2.)
        explainer = ExplainerBbox(
            sq,
            data=np.random.uniform(1,2,(6,6,4)),
        )
        system = Group(sq, explainer)
        self.add(system)
        self.wait()

        self.play(system.animate.shift(LEFT).scale(0.8))

        self.play(explainer.create_grid())
        self.wait()

        self.play(explainer.create_anchor_points())
        self.wait()

        self.play(explainer.to_rects())
        self.wait()

        self.play(explainer.to_dots())
        self.wait()

        self.play(system.animate.scale(1.1).shift(RIGHT*2))
        self.wait()

        self.play(explainer.to_rects())
        self.wait()

        self.play(explainer.to_dots())
        self.wait()
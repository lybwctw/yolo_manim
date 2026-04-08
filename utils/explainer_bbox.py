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
        data: np.ndarray = np.ones((4,4,4)),      # (h, w, 4)
        sf_nominal: int = 32,                   # 8/16/32
    ):
        super().__init__()
        self.background = background
        self.data = data
        self.sf_nominal = sf_nominal

        self.shape = data.shape[:2]

    def create_grid(
        self,
    ) -> VMobject:
        grid = Rectangle(
            width=self.background.width,
            height=self.background.height,
            stroke_width=1,
            grid_xstep=self.step,
            grid_ystep=self.step,
        )
        grid.grid_lines.set_stroke(width=1)
        grid.move_to(
            self.background.get_corner(UL),
            aligned_edge=UL,
        )

        return grid
    
    def show_grid(
        self,
        **aargs,
    ) -> Animation:
        self.grid = self.create_grid()
        self.add(self.grid)

        return Write(self.grid, **aargs)

    def hide_grid(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.grid)
        return Unwrite(self.grid, **aargs)

    def create_anchor_points(
        self,
    ) -> VGroup:
        base = self.background.get_corner(UL)
        anchor_points = VGroup(*[
            AnchorPoint(
                base+DOWN*self.step*(i+0.5)+RIGHT*self.step*(j+0.5),
                offset=self.data[i,j],
                sf_screen=self.step,
                sf_nominal=self.sf_nominal,
            )
            for i in range(self.shape[0])
            for j in range(self.shape[1])
        ])

        return anchor_points

    def show_anchor_points(
        self,
        **aargs,
    ) -> Animation:
        self.anchor_points = self.create_anchor_points()
        self.add(self.anchor_points)
        return Write(self.anchor_points,**aargs)

    def to_rects(
        self,
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        anims = AnimationGroup(
            *(ap.to_rect(**aargs) for ap in self.anchor_points),
            **gargs,
        )
        return anims

    def to_dots(
        self,
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        anims = AnimationGroup(
            *(ap.to_dot(**aargs) for ap in self.anchor_points),
            **gargs,
        )
        return anims

    def hide_anchor_points(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.anchor_points)
        return Unwrite(self.anchor_points,**aargs)

    def collect_in_out_aps(
        self,
        annotation: VGroup | None,      # VGroup of SingleAnnotation
    ) -> tuple:
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
    
    def collect_focus_ap(
        self,
        idx: int = 0,                   # sample anchor point index
    ) -> tuple:
        """Collect sample ap and others as VGroup.
        """
        sample_ap = self.anchor_points[idx]
        others = VGroup(*(ap for i, ap in enumerate(self.anchor_points) if i!=idx))
        return sample_ap, others
    
    @property
    def step(self) -> float:
        # FIXME, assume that width and height hold same scale
        return self.background.width / self.shape[1]
        

class Demo(Scene):
    def construct(self):
        sq = Square(
            stroke_opacity=0,
            fill_opacity=0.3,
        ).scale(2.)
        explainer = ExplainerBbox(
            sq,
            data=np.random.uniform(1,2,(6,6,4)),
            sf_nominal=32,
        )
        system = Group(sq, explainer)
        self.add(system)
        self.wait()

        self.play(system.animate.shift(LEFT).scale(1.5))

        self.play(explainer.show_grid())
        self.wait()

        self.play(explainer.show_anchor_points())
        self.wait()

        self.play(explainer.hide_grid())
        self.wait()

        sample_ap = explainer.anchor_points[3]
        self.play(sample_ap.show_arrows())
        self.wait()
        self.play(sample_ap.show_distance_abs())
        self.wait()

        # self.play(explainer.hide_grid())
        # self.wait()

        # self.play(explainer.to_rects())
        # self.wait()

        # self.play(explainer.to_dots())
        # self.wait()

        # self.play(system.animate.scale(0.7).shift(RIGHT*2))
        # self.wait()

        # self.play(explainer.to_rects())
        # self.wait()

        # self.play(explainer.to_dots())
        # self.wait()
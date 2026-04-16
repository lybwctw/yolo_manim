import sys
sys.path.append('..')

from manim import *
import numpy as np

from utils.anchor_point import AnchorPoint
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import SingleAnnotation
from utils.line_matrix import LineMatrix
from utils.general import tensor_to_line_matrix
from utils.constants import MINI_32_DIST_PATH, MINI_32_PROB_PATH

TEXT_XY_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 15,
}

# TODO, renaming of ExplainerBbox -> Explainer
# TODO, renaming of self.data -> self.data_dist
# because class info is also stored
class ExplainerBbox(VGroup):
    def __init__(
        self,
        background: ImageRaw | ImagePad | None = None,
        data: np.ndarray = np.ones((4,4,4)),        # (h, w, 4)
        data_cls: np.ndarray = np.ones((4,4,3)),    # (h, w, 3)
        sf_nominal: int = 32,                       # 8/16/32
    ):
        super().__init__()
        self.background = background
        self.data = data
        self.data_cls = data_cls
        self.sf_nominal = sf_nominal,
        self.shape = data.shape[:2]             # (h, w)
        self.xyxy = self._compute_xyxy()

        # TODO, more elegant way?
        self.tmp_txts = None
    
    def _compute_xyxy(
        self,
    ) -> np.ndarray:
        """Compute decoded x1y1x2y2, (h, w, 4)
        """
        rows = np.arange(self.shape[0])[:, None]
        cols = np.arange(self.shape[1])[None, :]
        return np.stack([
            (cols + 0.5 - self.data[...,0]) * self.sf_nominal,  # x1
            (rows + 0.5 - self.data[...,1]) * self.sf_nominal,  # y1
            (cols + 0.5 + self.data[...,2]) * self.sf_nominal,  # x2
            (rows + 0.5 + self.data[...,3]) * self.sf_nominal,  # y2
        ], axis=-1).astype(np.int32)

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
                idx=(i, j),
                xyxy=self.xyxy[i, j],
                probs=self.data_cls[i, j],
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
    
    def show_arrows(
        self,
        arrow_config: dict={},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        anim = AnimationGroup(
            *(ap.show_arrows(arrow_config=arrow_config, **aargs)
              for ap in self.anchor_points),
            **gargs,
        )
        return anim
    
    def hide_arrows(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        anim = AnimationGroup(
            *(ap.hide_arrows(**aargs)
              for ap in self.anchor_points),
            **gargs,
        )
        return anim
    
    def show_pbars(
        self,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> Animation:
        anim = AnimationGroup(
            *(ap.show_pbars(aargs=aargs, gargs=gargs)
              for ap in self.anchor_points),
            **ggargs,
        )
        return anim
    
    def to_probs(
        self,
        probs: np.ndarray | None = None,        # (h, w, 3)
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Update probs and pbars in aps accordingly.
        """
        if probs is None:
            return Wait(1.0)

        self.probs = probs
        # FIXME, other than 3 classes
        anim = AnimationGroup(
            *(ap.to_probs(ps, **aargs)
              for ap,ps in zip(self.anchor_points, probs.reshape(-1,3))),
            **gargs,
        )
        return anim
    
    def hide_pbars(
        self,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> Animation:
        anim = AnimationGroup(
            *(ap.hide_pbars(aargs=aargs, gargs=gargs)
              for ap in self.anchor_points),
            **ggargs,
        )
        return anim
    
    def show_multi_labels(
        self,
        width_ratio: float = 0.6,            # width : baseline
        height_ratio: float = 0.4,           # height : baseline
        label_config: dict = {},             # rectangle config
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        anim = AnimationGroup(
            *(ap.show_multi_labels(
                width_ratio=width_ratio,
                height_ratio=height_ratio,
                label_config=label_config,
                **aargs,
            ) for ap in self.anchor_points),
            **gargs,
        )
        return anim
    
    def hide_multi_labels(
        self,
    ) -> Animation:
        pass

    def to_rects(
        self,
        rect_config: dict = {}, # rect config
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        anims = AnimationGroup(
            *(ap.to_rect(rect_config, **aargs) for ap in self.anchor_points),
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

    def collect_nth_result(
        self,
        idx: int = 0,                   # sample result index
    ) -> list:
        """Collect specific result as a list.
        TODO: rename, exposure problem
        """
        res = self.xyxy.reshape(-1, 4)[idx].tolist()
        res = [int(t) for t in res]
        return res
    
    def show_point_from_xy(
        self,
        idx: int = 0,                   # index of anchor point
        direction: np.ndarray = UL,     # corner direction of ap's rect, UL/DR
        pargs: dict = {},               # path animation args
        targs: dict = {},               # text animation args
        gargs: dict = {},               # group animation args
    ) -> Animation:
        """Animation illustrating x,y -> point
            TODO, config separation
        """
        # create two paths into (x,y)
        ap = self.anchor_points[idx]
        px = VMobject().set_points_as_corners([
            self.background.get_corner(UL),
            np.array([ap.get_corner(direction)[0], self.background.get_top()[1], 0]),
            ap.get_corner(direction),
        ]).set_stroke(color=PURE_YELLOW, width=3)
        py = VMobject().set_points_as_corners([
            self.background.get_corner(UL),
            np.array([self.background.get_left()[0], ap.get_corner(direction)[1], 0]),
            ap.get_corner(direction),
        ]).set_stroke(color=PURE_YELLOW, width=3)

        # create x y texts
        # TODO: only UL and DR are available now
        if np.array_equal(direction, UL):
            _tx = str(ap.xyxy[0])
            _ty = str(ap.xyxy[1])
        elif np.array_equal(direction, DR):
            _tx = str(ap.xyxy[2])
            _ty = str(ap.xyxy[3])
        tx = Text(
            _tx,
            color=WHITE,
            **TEXT_XY_CONFIG,
        ).next_to(px, UP, buff=0.2)
        ty = Text(
            _ty,
            color=WHITE,
            **TEXT_XY_CONFIG,
        ).next_to(px, LEFT, buff=0.2)

        # TODO, more elegant way of storing tmp text?
        if self.tmp_txts is None:
            self.tmp_txts = VGroup(tx, ty)
        else:
            self.tmp_txts.add(tx, ty)

        anim = AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(px, **pargs,),
                Write(tx, **targs),
                **gargs,
            ),
            AnimationGroup(
                ShowPassingFlash(py, **pargs,),
                Write(ty, **targs),
                **gargs,
            ),
        )
        return anim
    
    def hide_xy_txts(
        self,
        **aargs,
    ) -> Animation:
        mobs = self.tmp_txts
        self.tmp_txts = None
        return Unwrite(mobs, **aargs)
    
    def create_distance_tensor(
        self,
        font_size: int=8,               # small for tensor
    ) -> VGroup:
        dists = VGroup()
        for ap in self.anchor_points:
            dist = ap.create_ordered_distance(font_size=font_size)
            dists.add(dist)
        return dists

    def create_xyxy_tensor(
        self,
        font_size: int=8,               # small for tensor
    ) -> VGroup:
        xyxys = VGroup()
        for ap in self.anchor_points:
            xyxy = ap.create_ordered_xyxy(font_size=font_size)
            xyxys.add(xyxy)
        return xyxys
    
    def create_probs_tensor(
        self,
        font_size: int=8,
    ) -> VGroup:
        probs = VGroup()
        for ap in self.anchor_points:
            ps = ap.create_ordered_probs(font_size=font_size)
            probs.add(ps)
        return probs
    
    def create_line_matrix(
        self,
        n: int=4,              # n lines in a rows
    ):
        """Create 2d LineMatrix according to xyxy shape.
        """
        matrix = LineMatrix(
            (self.shape[0]*self.shape[1], n),
        )
        return matrix

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
            data=np.random.uniform(0.6,1.2,(6,6,4)),
            data_cls=np.random.uniform(0.1,0.9,(6,6,3)),
            sf_nominal=32,
        )
        explainer_system = Group(sq, explainer)
        self.add(explainer_system)
        self.wait(0.3)

        # self.play(explainer.show_grid())
        # self.wait()

        self.play(explainer.show_anchor_points(
            lag_ratio=0,
            run_time=0.5,
        ))
        self.wait(0.3)

        # self.play(explainer.hide_grid())
        # self.wait()
        
        self.play(explainer.to_rects())
        self.wait()

        self.play(explainer.show_multi_labels(
            label_config={
                'fill_opacity': 0.5,
                'stroke_opacity': 0.6,
            },
            aargs={
                'lag_ratio': 0.1,
            }
        ))
        self.wait()

        # self.play(explainer.to_dots())
        # self.wait()

        # self.play(explainer.hide_anchor_points())
        # self.wait()

        # self.play(explainer.hide_anchor_points(
        #     lag_ratio=0,
        #     run_time=0.5,
        # ))

        # self.play(AnimationGroup(
        #     *(ap.animate.set_pattern(color=GRAY,opacity=0.1)
        #       for ap in explainer.anchor_points),
        #       lag_ratio=0,
        #       run_time=1.0,
        # ))
        # self.wait()

        # self.play(explainer.show_pbars())
        # self.wait()

        # new_probs = np.random.uniform(0.1,0.3,(6,6,3))
        # self.play(explainer.to_probs(new_probs))
        # self.wait()

        # probs_tensor = explainer.create_probs_tensor().shift(RIGHT*2)
        # self.play(explainer_system.animate.shift(LEFT*2))
        # self.play(Write(probs_tensor, lag_ratio=0.1))
        # self.wait()

        # self.play(explainer.show_arrows())
        # self.wait()

        # self.play(explainer.hide_arrows())
        # self.wait()

        # self.play(explainer.hide_anchor_points())
        # self.wait()
        # self.remove(explainer)

        # explainer = ExplainerBbox(
        #     sq,
        #     data=np.load('../assets/numpy/mini_32.npy'),
        #     sf_nominal=32,
        # )
        # explainer_system = Group(sq, explainer)
        # self.add(explainer_system)
        # self.wait(0.3)

        # self.play(explainer.show_anchor_points())
        # self.wait()

        # self.play(explainer.to_rects())
        # self.wait()

        # self.play(explainer.show_pbars())
        # self.wait()

        # self.play(explainer.show_arrows())
        # self.wait()

        # self.play(explainer.hide_arrows())
        # self.wait()

        # self.play(explainer.to_rects())
        # self.wait()

        # self.play(explainer.to_rects(
        #     rect_config={'width': 2.0},
        #     gargs={'lag_ratio':0.2, 'run_time':0.5,},
        # ))
        # self.wait()

        # self.play(explainer_system.animate(run_time=0.5).shift(LEFT*3))
        # self.wait()

        # xyxy = explainer.create_xyxy_tensor()
        # xyxy.center()
        # self.play(Write(xyxy, lag_ratio=0, run_time=0.5))
        # self.wait(0.3)


        # line_matrix = explainer.create_line_matrix().scale(0.3).shift(RIGHT*4)
        # self.play(Write(line_matrix))
        # self.wait()

        # self.play(tensor_to_line_matrix(
        #     tensor=xyxy,
        #     lmatrix=line_matrix,
        #     targs={},
        #     gargs={'lag_ratio':0.02, 'run_time':0.1,},
        #     ggargs={'lag_ratio':0.05, 'run_time':1.0,},
        # ))
        # self.wait()

        # self.play(explainer.to_dots())
        # self.wait()

        # self.play(system.animate.scale(0.7).shift(RIGHT*2))
        # self.wait()

        # self.play(explainer.to_rects())
        # self.wait()

        # self.play(explainer.to_dots())
        # self.wait()
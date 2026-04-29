from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.anchor_point import AnchorPoint
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import SingleAnnotation
from utils.line_matrix import LineMatrix
from utils.general import tensor_to_line_matrix
from utils.constants import MINI_32_DIST_PATH, MINI_32_PROB_PATH
from utils.tensor_2d import Tensor2D

import numpy as np
import torch

# TODO, rename
PATH_DIST_BBOX = 'assets/tensors/_dist_box.pt'
PATH_NORM_CLS = 'assets/tensors/_norm_cls.pt'
PATH_DIST_BBOX_MINI = 'assets/numpy/mini_32_dist.npy'
PATH_NORM_CLS_MINI = 'assets/numpy/mini_32_prob.npy'

TEXT_XY_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 15,
}

class Explainer(VGroup):
    """Class for explaining YOLO output design.
    """
    def __init__(
        self,
        background: ImageRaw | ImagePad | None = None,
        dist_3d: np.ndarray = np.ones((4,4,4)),     # (h, w, 4)
        prob_3d: np.ndarray = np.ones((4,4,3)),     # (h, w, 3)
        sf_nominal: int = 32,                       # 8/16/32
    ):
        super().__init__()
        self.background = background
        self.sf_nominal = sf_nominal,

        assert dist_3d.shape[:2] == prob_3d.shape[:2]

        dist_2d = dist_3d.reshape(-1, 4)
        prob_2d = prob_3d.reshape(-1, 3)

        h, w = dist_3d.shape[:2]
        ys, xs = np.meshgrid(
            np.arange(h),
            np.arange(w),
            indexing='ij',
        )
        indices_3d = np.stack([ys, xs], axis=-1)
        indices_2d = indices_3d.reshape(-1, 2)

        # xs = (xs + 0.5) * self.sf_nominal
        # ys = (ys + 0.5) * self.sf_nominal
        xs = xs + 0.5
        ys = ys + 0.5

        center_3d = np.stack([ys, xs], axis=-1)
        center_2d = center_3d.reshape(-1, 2)

        xs_2d = xs.reshape(-1)
        ys_2d = ys.reshape(-1)

        dist_2d = dist_3d.reshape(-1, 4)
        prob_2d = prob_3d.reshape(-1, 3)

        x1 = xs_2d - dist_2d[:, 0]
        y1 = ys_2d - dist_2d[:, 1]
        x2 = xs_2d + dist_2d[:, 2]
        y2 = ys_2d + dist_2d[:, 3]

        xyxy_2d = np.stack([x1, y1, x2, y2], axis=-1)
        xyxy_3d = xyxy_2d.reshape(h, w, 4)

        xyxycls_2d = np.concat([xyxy_2d, prob_2d], axis=-1)
        xyxycls_3d = xyxycls_2d.reshape(h, w, 4+3)

        # common 2d/3d tensors
        self.shape = (h, w)
        self.indices_3d = indices_3d
        self.indices_2d = indices_2d
        self.center_3d = center_3d
        self.center_2d = center_2d
        self.dist_3d = dist_3d
        self.dist_2d = dist_2d
        self.xyxy_3d = xyxy_3d
        self.xyxy_2d = xyxy_2d
        self.prob_3d = prob_3d
        self.prob_2d = prob_2d
        self.xyxycls_3d = xyxycls_3d
        self.xyxycls_2d = xyxycls_2d

        # FIXME, more elegant way?
        self.tmp_txts = None
    
    def create_grid(
        self,
    ) -> VMobject:
        grid = Rectangle(
            width=self.background.width,
            height=self.background.height,
            stroke_width=1,
            grid_xstep=self.sf_screen,
            grid_ystep=self.sf_screen,
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
        anchor_points = VGroup(*[
            AnchorPoint(
                point=self.background.get_corner(UL)+
                    self.center_3d[i,j][0]*DOWN*self.sf_screen+
                    self.center_3d[i,j][1]*RIGHT*self.sf_screen,
                dist=self.dist_3d[i,j],
                xyxy=self.xyxy_3d[i,j],
                prob=self.prob_3d[i,j],
                index=self.indices_3d[i,j],
                sf_nominal=self.sf_nominal,
                sf_screen=self.sf_screen,
            ) for i in range(self.shape[0])
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
    
    # FIXME, sync_pbars
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

    def show_rect_mlabels(
        self,
        width_ratio: float = 0.6,            # width : baseline
        height_ratio: float = 0.4,           # height : baseline
        rect_config: dict = {},
        label_config: dict = {},
        rargs: dict = {},       # to_rect animation args
        largs: dict = {},       # show_multi_labels animation args
        gargs: dict = {},       # ap.show_rect_mlabels group args
        ggargs: dict = {},      # group of ap.show_rect_mlabels group args
    ) -> Animation:
        anim = AnimationGroup(
            *(ap.show_rect_mlabels(
                width_ratio=width_ratio,
                height_ratio=height_ratio,
                rect_config=rect_config,
                label_config=label_config,
                rargs=rargs,
                largs=largs,
                gargs=gargs,
            ) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def keep_max_label(
        self,
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
        ggargs: dict = {},      # group of group args
    ) -> Animation:
        """Keep only the label with maximum probability for each anchor point.
        Used to represent the take-max class step in YOLO postprocessing.
        """
        anim = AnimationGroup(
            *(ap.keep_max_label(aargs=aargs, gargs=gargs) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def keep_ratio(
        self,
        ratio: float = 0.5,    # ratio of anchor points to keep (0-1)
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        """Keep only a random subset of anchor points based on ratio.
        Can be called multiple times successively to further filter.
        """
        import random
        n_keep = max(1, int(len(self.anchor_points) * ratio))
        keep_indices = random.sample(range(len(self.anchor_points)), n_keep)

        # data_flat = self.data.reshape(-1, 4)       # (h*w, 4)
        # data_cls_flat = self.data_cls.reshape(-1, 3)  # (h*w, 3)
        # self.data = data_flat[keep_indices] # FIXME, 3d -> 2d
        # self.data_cls = data_cls_flat[keep_indices]
        
        # remember kept indices to be used later
        self.keep_indices = np.array(keep_indices, dtype=np.int64)

        aps_to_remove = [
            ap for i, ap in enumerate(self.anchor_points)
              if i not in keep_indices
        ]
        self.anchor_points.remove(*aps_to_remove)
        if aps_to_remove:
            anims = AnimationGroup(
                *(Unwrite(ap, **aargs) for ap in aps_to_remove),
                **gargs,
            )
        else:
            anims = Wait(0.1)
        return anims

    def to_rects(
        self,
        rect_config: dict = {}, # rect config
        aargs: dict = {},       # to_rect args
        gargs: dict = {},       # group args
    ) -> Animation:
        anims = AnimationGroup(
            *(ap.to_rect(
                rect_config,
                **aargs,
            ) for ap in self.anchor_points),
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
    
    def clip_to_background(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Clip aps cross border, remove if fully outside.
        """
        anims = []
        aps_to_remove = []
        for ap in self.anchor_points:
            anim = ap.clip_to_background(self.background, **aargs)
            if isinstance(anim.animations[0], Unwrite):   # TODO, better solution?
                aps_to_remove.append(ap)
            anims.append(anim)
        self.anchor_points.remove(*aps_to_remove)
        return AnimationGroup(*anims, **gargs)
    
    def xyxyccc(
        self,
    ) -> Tensor2D:
        """Combined xyxy and cls info, (h*w, 7)
        """
        data = [
            self._compute_xyxy_2d(),
            self._compute_cls_2d(),
        ]
        return Tensor2D(
            data=data,
            decimal_config={
                'font_size': 4.3,
                'color': WHITE,
            },
        )

    @property
    def sf_screen(self) -> float:
        """Screen distance / unit distance.
           Assume that width and height direction share the same factor.
        """
        return self.background.width / self.shape[1]
    
    @property
    def dots(self) -> VGroup:
        """Fast reference to all dots
        """
        vg = VGroup(*(ap.mob for ap in self.anchor_points))
        return vg

    @staticmethod
    def from_random(
        background,
        dist_range: tuple = (0, 5),
        prob_range: tuple = (0, 1),
        shape: tuple = (4, 4),
        sf_nominal: int = 32,
    ) -> Explainer:
        """Create random explainer.
        """
        dist_3d = np.random.uniform(dist_range[0], dist_range[1], shape+(4,))
        prob_3d = np.random.uniform(prob_range[0], prob_range[1], shape+(3,))

        return Explainer(
            background=background,
            dist_3d=dist_3d,
            prob_3d=prob_3d,
            sf_nominal=sf_nominal,
        )
    
    @staticmethod
    def from_file(
        background,
        version: str = 'mini',
        sf_nominal: int = 32,
    ) -> Explainer:
        if version == 'mini':
            dist_3d = np.load(PATH_DIST_BBOX_MINI)
            prob_3d = np.load(PATH_NORM_CLS_MINI)
        elif version == 'general':
            dist_3d = torch.load(
                PATH_DIST_BBOX,
                weights_only=True,
                map_location='cpu',
            )  # (1, 4, 8400)
            prob_3d = torch.load(
                PATH_NORM_CLS,
                weights_only=True,
                map_location='cpu',
            )  # (1, 3, 8400)
            if sf_nominal == 32:
                dist_3d = dist_3d[0,:,8000:].transpose(0,1).reshape(20,20,4).numpy()
                prob_3d = prob_3d[0,:,8000:].transpose(0,1).reshape(20,20,3).numpy()
            elif sf_nominal == 16:
                dist_3d = dist_3d[0,:,6400:8000].transpose(0,1).reshape(40,40,4).numpy()
                prob_3d = prob_3d[0,:,6400:8000].transpose(0,1).reshape(20,20,3).numpy()
            elif sf_nominal == 8:
                dist_3d = dist_3d[0,:,:6400].transpose(0,1).reshape(80,80,4).numpy()
                prob_3d = prob_3d[0,:,:6400].transpose(0,1).reshape(20,20,3).numpy()
        explainer = Explainer(
            background=background,
            dist_3d=dist_3d,
            prob_3d=prob_3d,
            sf_nominal=32,
        )
        return explainer
        
def load_explainer(
    background,
    version: str = 'mini',  # mini/general
    scale: int = 32,        # 32/16/8 for general
    random_probs: bool = False,   # random overriden probs for demo purpose
) -> Explainer:
    """User interface for explainer.
       TODO, make all data np/torch
       and make mini version customizable
    """
    if version == 'mini':
        data_dist = np.load(PATH_DIST_BBOX_MINI)
        data_cls = np.load(PATH_NORM_CLS_MINI)
    elif version == 'general':
        data_dist = torch.load(
            PATH_DIST_BBOX,
            weights_only=True,
            map_location='cpu',
        )  # (1, 4, 8400)
        data_cls = torch.load(
            PATH_NORM_CLS,
            weights_only=True,
            map_location='cpu',
        )  # (1, 3, 8400)
        if scale == 32:
            data_dist = data_dist[0,:,8000:].transpose(0,1).reshape(20,20,4).numpy()
            data_cls = data_cls[0,:,8000:].transpose(0,1).reshape(20,20,3).numpy()
        elif scale == 16:
            data_dist = data_dist[0,:,6400:8000].transpose(0,1).reshape(40,40,4).numpy()
            data_cls = data_cls[0,:,6400:8000].transpose(0,1).reshape(20,20,3).numpy()
        elif scale == 8:
            data_dist = data_dist[0,:,:6400].transpose(0,1).reshape(80,80,4).numpy()
            data_cls = data_cls[0,:,:6400].transpose(0,1).reshape(20,20,3).numpy()
        
        if random_probs:
            data_cls = np.random.uniform(0.0,0.98,(640//random_probs,640//random_probs,3))

    explainer = Explainer(
        background=background,
        data=data_dist,
        data_cls=data_cls,
        sf_nominal=scale,
    )
    return explainer

class Demo(Scene):
    def construct(self):
        sq = Square(
            stroke_opacity=0,
            fill_opacity=0.3,
        ).scale(2.)
        explainer = Explainer.from_random(
            background=sq,
            dist_range=(1,2.5),
            prob_range=(0,1),
            shape=(5,5),
            sf_nominal=32,
        )

        system = Group(explainer, sq)
        self.add(system)

        # self.play(explainer.show_grid())
        # self.wait()

        self.play(explainer.show_anchor_points(
            run_time=0.5,
        ))
        self.wait()

        # self.play(explainer.hide_grid())
        # self.wait()

        # self.play(explainer.show_arrows(
        #     aargs={'lag_ratio':0.1},
        #     gargs={'lag_ratio':0.1, 'run_time': 1.0},
        # ))
        # self.wait()

        # self.play(explainer.hide_arrows(
        #     aargs={'lag_ratio':0.1},
        #     gargs={'lag_ratio':0.1, 'run_time': 1.0},
        # ))
        # self.wait()

        dots = explainer.dots.save_state()
        self.play(dots.animate.set_stroke(opacity=0))
        self.wait()

        self.play(explainer.show_pbars())
        self.wait()

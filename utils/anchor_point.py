from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from typing import Self
from utils.computation import Computation
from utils.constants import KK_COLORS

DIRECTION_SERIES = [
    'left',
    'up',
    'right',
    'down',
]

DOT_CONFIG = {
    'fill_opacity': 0.0,
    'side_length': 0.01,
    'stroke_width': 3,
    'stroke_color': WHITE,
}

RECT_CONFIG = {
    'fill_opacity': 0.0,
    'stroke_width': 2,
    'stroke_color': WHITE,
}

ARROW_COLOR_MAP = {
    'left':  PURE_RED,
    'up':    PURE_GREEN,
    'right': PURE_BLUE,
    'down':  PURE_MAGENTA,
}

TEXT_COLOR_MAP = ARROW_COLOR_MAP

# next to arrow direction
TEXT_DIRECTION_MAP = {
    'left':  UP,
    'up':    RIGHT,
    'right': DOWN,
    'down':  LEFT,
}
TEXT_DIRECTION_BUFF = 0.1

# TODO, adjust the last two options
ARROW_CONFIG = {
    'stroke_width': 3,
    'tip_length': 0.15,
    'buff': 0.0,
    'max_stroke_width_to_length_ratio': 15,         # 5 by default
    'max_tip_length_to_length_ratio': 0.25,          # 0.25 by default
}

TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    # 'font_size': 15,
}

# pbars related
PBAR_SPACE_RATIO = 0.5          # pbar space : unit space
PBAR_GAP_RATIO = 0.1            # pbar gap : pbar space
PBAR_COLORS = KK_COLORS
PBAR_CONFIG = {
    'stroke_width': 0,
    'fill_opacity': 1.0,
}
CLASS_COLORS = PBAR_COLORS

# label related
LABEL_WIDTH_RATIO = 0.6             # label width / unit
LABEL_HEIGHT_RATIO = 0.4            # label height / width
LABEL_COLORS = PBAR_COLORS
LABEL_CONFIG = {
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'fill_opacity': 1.0,
}

class AnchorPoint(VMobject):
    def __init__(
        self,
        point: np.ndarray = ORIGIN,                         # starting position
        dist: np.ndarray | list | tuple = (1.,1.,1.,1.),    # left, up, right, down
        xyxy: np.ndarray | list | tuple = (10,20,30,40),    # x1, y1, x2, y2
        prob: np.ndarray | list | tuple = (.5,.5,.5),       # c1, c2, c3
        index: np.ndarray | list | tuple = (0, 0),          # index in explainer
        sf_nominal: int = 32,                               # nominal distance / unit distance
        sf_screen: int = 0.5,                               # screen distance / unit distance
    ):
        super().__init__()
        # user is responsible for providing matching tensors
        self.dist = np.array(dist)
        self.xyxy = np.array(xyxy)
        self.prob = np.array(prob)
        self.index = np.array(index)
        self.sf_nominal = sf_nominal

        dot = Square(
            stroke_opacity=0.0,
            **DOT_CONFIG,
        ).move_to(point)
        self.dot = dot

        ref = Line(
            LEFT/2,
            RIGHT/2,
        ).set_opacity(0.0).scale(sf_screen).move_to(self.dot)
        self.ref = ref              # reference line

        left, up, right, down = [x*sf_screen for x in self.dist]
        width, height = left+right, up+down
        center_offset = RIGHT*(right-left)/2 + UP*(up-down)/2
        rect = Rectangle(
            width=width,
            height=height,
            stroke_opacity=0.0,
            **RECT_CONFIG,
        ).move_to(point + center_offset)
        self.rect = rect

        self.mob = dot.copy().set_stroke(opacity=1.0)

        self.add(self.ref, self.dot, self.rect, self.mob)

    def to_rect(
        self,
        rect_config: dict = {}, # target rect config
        **aargs,
    ) -> Animation:
        """Apply config only once.
        """
        rect_config = {'stroke_opacity': 1.0, **rect_config}
        target = self.rect.copy().set_style(**rect_config)
        return Transform(
            self.mob,
            target,
            **aargs,
        )

    def to_dot(
        self,
        dot_config: dict = {}, # target dot config
        **aargs,
    ) -> Animation:
        """Apply config only once.
        """
        dot_config = {'stroke_opacity': 1.0, **dot_config}
        target = self.dot.copy().set_style(**dot_config)
        return Transform(
            self.mob,
            target,
            **aargs,
        )

    def create_arrows(
        self,
        arrow_config: dict={},
    ) -> VGroup:
        """Create arrows based on dot and rect.
        """
        cfg = {**ARROW_CONFIG, **arrow_config}
        arrows = VGroup(
            *(Arrow(
                start=self.dot.get_center(),
                end=self.node_map[direction],
                color=ARROW_COLOR_MAP[direction],
                **cfg,
            ) for direction in DIRECTION_SERIES),
        )
        return arrows
    
    def show_arrows(
        self,
        arrow_config: dict={},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """ NOTE: rate_func for arrow is inside aargs.
        """
        # rfunc = aargs.pop('rate_func', rate_functions.smooth)
        self.arrows = self.create_arrows(
            arrow_config=arrow_config,
        )
        self.add(self.arrows)
        return AnimationGroup(
            *(GrowArrow(
                arrow,
                **aargs,
            ) for arrow in self.arrows),
            **gargs,
        )
        # return Write(self.arrows, **aargs)
    
    def hide_arrows(
        self,
        **aargs,
    ) -> Animation:
        """TODO, shrink version?
        """
        self.remove(self.arrows)
        return Unwrite(self.arrows, **aargs)

    def create_dist(
        self,
        font_size: int = 15,            # specify font size manually
    ) -> VGroup :
        """Create distance Texts, not aligned.
        """
        ts = VGroup(
            *(Text(
                '{:.2f}'.format(self.dist[i]),
                color=TEXT_COLOR_MAP[direction],
                font_size=font_size,
                **TEXT_CONFIG,
            ) for i, direction in enumerate(DIRECTION_SERIES))
        )
        return ts

    def show_dist(
        self,
        font_size: int = 15,            # specifiy font manually
        **aargs,
    ) -> Animation:
        """Show distance Texts, aligned to arrows.
        """
        self.ts_dist = self.create_dist(
            font_size=font_size,
        )
        self._align_ts_to_arrows(self.ts_dist)
        self.add(self.ts_dist)
        return Write(self.ts_dist, **aargs)

    def hide_dist(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.ts_dist)
        return Unwrite(self.ts_dist, **aargs)

    def create_dist_nominal(
        self,
        font_size: int = 15,
    ) -> VGroup :
        """Create nominal distance Texts, not aligned.
        """
        ts = VGroup(
            *(Text(
                # str(int(self.dist[i]*self.sf_nominal)), # TODO, why the fuck this failed?
                '{:.0f}'.format(self.dist[i]*self.sf_nominal),
                color=TEXT_COLOR_MAP[direction],
                font_size=font_size,
                **TEXT_CONFIG,
            # ).next_to(
            #     self.arrows[i],
            #     TEXT_DIRECTION_MAP[direction],
            #     buff=TEXT_DIRECTION_BUFF,
            ) for i, direction in enumerate(DIRECTION_SERIES))
        )
        return ts

    def show_dist_nominal(
        self,
        font_size: int = 15,
        **aargs,
    ) -> Animation:
        """Show nominal distance Texts, aligned to arrows.
        """
        self.ts_dist_nominal = self.create_dist_nominal(
            font_size=font_size,
        )
        self._align_ts_to_arrows(self.ts_dist_nominal)
        self.add(self.ts_dist_nominal)
        return Write(self.ts_dist_nominal, **aargs)

    def hide_dist_nominal(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.ts_dist_nominal)
        return Unwrite(self.ts_dist_nominal, **aargs)

    def create_divide(
        self,
        font_size: int = 15,
    ) -> VGroup:
        """Create '/sf_nominal' for each dist_nominal.
        """
        divide = VGroup(*(
            Text(
                '/' + str(self.sf_nominal),
                color=TEXT_COLOR_MAP[direction],
                font_size=font_size,
                **TEXT_CONFIG,
            ).next_to(
                self.ts_dist_nominal[i],
                RIGHT,
                buff=0.05,
            ) for i, direction in enumerate(DIRECTION_SERIES)
        ))
        return divide
    
    def show_divide(
        self,
        **aargs,
    ) -> Animation:
        """Append '/sf_nominal' into each dist_nominal.
        """
        divide = self.create_divide()
        for dist, div in zip(self.ts_dist_nominal, divide):
            dist.add(div)
        return Write(divide, **aargs)
    
    def nominal_to_rela(
        self,
        aargs: dict = {},       # ReplacementTransform args
        gargs: dict = {},       # AnimationGroup args
    ) -> Animation:
        """ Convert ts_dist_nominal with divide into ts_dist.
        """
        self.remove(self.ts_dist_nominal)
        self.ts_dist = self.create_dist()
        self._align_ts_to_arrows(self.ts_dist)
        self.add(self.ts_dist)
        return AnimationGroup(
            *(ReplacementTransform(dist_nominal, dist_rela, **aargs)
            for dist_nominal, dist_rela in zip(self.ts_dist_nominal, self.ts_dist)),
            **gargs,
        )
    
    # def create_xyxy(
    #     self,
    #     font_size: int = 15,            # specify font size manually
    # ) -> VGroup:
    #     """Create xyxy not positioned.
    #     """
    #     xyxy = VGroup(
    #         *(Text(
    #             '{:>3d}'.format(self.xyxy[i]),
    #             color=WHITE,            # xyxy is all white
    #             font_size=font_size,
    #             **TEXT_CONFIG,
    #         ) for i in range(4))
    #     )
    #     return xyxy
    
    # def create_probs(
    #     self,
    #     font_size: int = 15,
    # ) -> VGroup:
    #     """Create cls not positioned.
    #     """
    #     probs = VGroup(
    #         *(Text(
    #             '{:.2f}'.format(self.probs[i]),
    #             color=CLASS_COLORS[i],
    #             font_size=font_size,
    #             **TEXT_CONFIG,
    #         ) for i in range(3))
    #     )
    #     return probs
    
    # def create_ordered_distance(
    #     self,
    #     font_size: int = 8,             # smaller for tensor
    # ) -> VGroup:
    #     """"Create distance ordered from DL to UR.
    #     """
    #     dists = self.create_distance(font_size=font_size)

    #     # manual arrange
    #     for i, dist in enumerate(dists):
    #         dist.move_to(self.dot)
    #         dist.set_z_index(4-i)
    #         dist.set_opacity(opacity=1-i*0.2)
    #         dist.shift((RIGHT*0.05 + UP*0.06)*i)

    #     dists.move_to(self.dot)
    #     return dists
    
    # def create_ordered_xyxy(
    #         self,
    #         font_size: int = 8,         # smaller for tensor
    # ) -> VGroup:
    #     """Create xyxy ordered from DL to UR.
    #     """
    #     xyxy = self.create_xyxy(font_size=font_size)

    #     # manual arrange
    #     for i, t in enumerate(xyxy):
    #         t.move_to(self.dot)
    #         t.set_z_index(4-i)
    #         t.set_opacity(opacity=1-i*0.2)
    #         t.shift((RIGHT*0.05 + UP*0.06)*i)
        
    #     xyxy.move_to(self.dot)
    #     return xyxy
    
    # def create_ordered_probs(
    #     self,
    #     font_size: int = 8,
    # ) -> VGroup:
    #     """Create xyxy ordered from DL to UR.
    #     """
    #     probs = self.create_probs(font_size=font_size)

    #     # manual arrange
    #     for i, t in enumerate(probs):
    #         t.move_to(self.dot)
    #         t.set_z_index(4-i)
    #         t.set_opacity(opacity=1-i*0.2)
    #         t.shift((RIGHT*0.05 + UP*0.06)*i)
        
    #     probs.move_to(self.dot)
    #     return probs
    

    # def get_center(
    #     self,
    # ) -> np.ndarray:
    #     """Override the default center with dot center.
    #     """
    #     return self.dot.get_center()

    def create_decode_computations(
        self,
        buff: float = 0.3,              # up-down buff between computations
        text_config: dict = {},         # for computation
    ) -> VGroup:
        """Create 4 Equations show computing from distance to position,
           not positioned, not arranged.
        """
        # f'({self.dir_to_idx[direction]:>2d}+0.5{self.dir_to_sign[direction]}'
        # f'<span foreground="{TEXT_COLOR_MAP[direction]}">{self.offset[i]:.2f}</span>'
        # f')*{self.sf_nominal} = '
        # f'<span foreground="white">{self.xyxy[i]:<3d}</span>'
        formatters = [
            (
                f'({{:>2d}}+0.5{self.dir_to_sign[direction]}'
                f'<span foreground="{TEXT_COLOR_MAP[direction]}">{{:.2f}}</span>)'
                f'*{self.sf_nominal} = <span foreground="white">{{:<3d}}</span>'
            ) for direction in DIRECTION_SERIES
        ]
        values = [
            [
                self.dir_to_idx[direction],
                self.dist[i],
                self.xyxy[i]
            ] for i, direction in enumerate(DIRECTION_SERIES)
        ]

        computations = VGroup(
            Computation(
                formatter=formatter,
                values=vs,
                **text_config,
            ) for formatter, vs in zip(formatters, values)
        ).arrange(
            DOWN,
            buff=buff,
            aligned_edge=LEFT,
        ).center()   # TODO, arrange args

        return computations
    
    def create_pbars(
        self,
        pbar_config: dict={},
    ) -> VGroup:
        """Realtime pbars based on given prob.
        """
        n_probs = len(self.prob)
        pbar_space = self.sf_screen * PBAR_SPACE_RATIO
        pbar_offset = self.sf_screen*(1-PBAR_SPACE_RATIO)/2
        pbar_gap = pbar_space * PBAR_GAP_RATIO
        pbar_width = pbar_space * (1-(n_probs-1)*PBAR_GAP_RATIO) / n_probs
        cfg = {**PBAR_CONFIG, **pbar_config}
        pbars = VGroup(
            Rectangle(
                width=pbar_width,
                height=pbar_space*p,
                fill_color=PBAR_COLORS[i],
                **cfg,
            ).align_to(self.ref, LEFT)\
             .shift((pbar_offset+pbar_width*i+pbar_gap*i)*RIGHT)\
             .set_y(self.ref.get_y())
            for i, p in enumerate(self.prob)
        )
        return pbars
    
    def show_pbars(
        self,
        pbar_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Grow pbars from baseline.
        """
        pbars_end = self.create_pbars(
            pbar_config=pbar_config,
        )
        pbars_start = pbars_end.copy()
        for bar in pbars_start:
            bar.stretch_to_fit_height(0)
        self.pbars = pbars_start
        self.add(self.pbars)
        return AnimationGroup(
            *(Transform(p0, p1, **aargs)
            for p0, p1 in zip(self.pbars, pbars_end)),
            **gargs,
        )
    
    def sync_pbars(
        self,
        pbar_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Sync pbars into current prob.
        """
        pbars_end = self.create_pbars(
            pbar_config=pbar_config,
        )     # current prob
        return AnimationGroup(
            *(Transform(p0, p1, **aargs)
            for p0, p1 in zip(self.pbars, pbars_end)),
            **gargs,
        )
    
    def hide_pbars(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Shrink pbars into baseline.
        """
        pbars_end = self.pbars.copy()
        for bar in pbars_end:
            bar.stretch_to_fit_height(0)
        self.remove(self.pbars)
        return AnimationGroup(
            *(Transform(p0, p1, **aargs)
            for p0, p1 in zip(self.pbars, pbars_end)),
            **gargs,
        )
    
    def create_multi_labels(
        self,
        **label_config,                      # rectangle config
    ) -> VGroup:
        """Create multi labels, not positioned.
        """
        label_width_ratio = label_config.pop('width_ratio', LABEL_WIDTH_RATIO)
        label_height_ratio = label_config.pop('height_ratio', LABEL_HEIGHT_RATIO)
        label_width = self.sf_screen * label_width_ratio
        label_height = self.sf_screen * label_height_ratio
        cfg = {**LABEL_CONFIG, **label_config}
        labels = VGroup(
            Rectangle(
                width=label_width,
                height=label_height,
                stroke_color=color,
                fill_color=color,
                **cfg,
            ) for color in LABEL_COLORS
        ).arrange(buff=0)
        return labels
    
    def show_multi_labels(
        self,
        label_config: dict = {},             # rectangle config
        **aargs,
    ) -> Animation:
        """Add labels as new member.
        """
        labels = self.create_multi_labels(
            **label_config,
        ).move_to(
            self.rect.get_corner(UL),
            aligned_edge=DL,
        )
        self.labels = labels
        self.add(self.labels)

        return Write(self.labels, **aargs)
        # return AnimationGroup(
        #     *(Write(label, **aargs) for label in labels),
        #     **gargs,
        # )
    
    def show_rect_mlabels(
        self,
        rect_config: dict = {},
        label_config: dict = {},
        rargs: dict = {},       # to_rect animation args
        largs: dict = {},       # show_multi_labels animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        """Show rect and multi labels at a time.
        """
        anims = AnimationGroup(
            self.to_rect(
                rect_config=rect_config,
                **rargs,
            ),
            self.show_multi_labels(
                label_config=label_config,
                **largs
            ),
            **gargs,
        )
        return anims

    def apply_max_select(
        self,
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        """Apply max conf filter.
           cls and conf created here.
        """
        max_idx = np.argmax(self.prob)
        max_label = self.labels[max_idx]

        self.cls = max_idx              # remember max class index
        self.conf = self.prob[max_idx]  # remember max class conf
        
        anims = [
            Transform(max_label, max_label.copy().move_to(self.labels[0], aligned_edge=DL), **aargs),
        ]
        labels_to_remove = []
        for i in range(len(self.labels)):
            if i != max_idx:
                anims.append(FadeOut(self.labels[i], **aargs))  # or Unwrite?
                labels_to_remove.append(self.labels[i])

        self.rect.set_stroke(color=PBAR_COLORS[max_idx])
        anims.append(self.mob.animate(**aargs).set_stroke(color=PBAR_COLORS[max_idx]))

        self.labels.remove(*labels_to_remove)
        
        return AnimationGroup(*anims, **gargs)
    
    def clip_to_background(
        self,
        background,
        **aargs,        # for both labels and rect
    ) -> Animation:
        anims = []
        inter_rect = self._intersect_bg(
            background,
        )
        if inter_rect is None:
            anims.append(Unwrite(self)) # TODO, or fade out???
        else:
            self.remove(self.rect)
            self.rect = inter_rect
            anims.append(AnimationGroup(
                self.to_rect(
                    rect_config={},
                    **aargs,
                ),
                self.labels.animate(**aargs).move_to(
                    self.rect.get_corner(UL),
                    aligned_edge=DL,
                ),
            ))
        return AnimationGroup(*anims)
    
    def _intersect_bg(
        self,
        background,
    ) -> Rectangle | None:
        """Compute the intersection between self.rect and background
        return a new Rectangle if intersected, otherwise return None.
        """
        r1, r2 = self.rect, background
        # compute edges of intersection
        x_min = max(r1.get_left()[0], r2.get_left()[0])
        x_max = min(r1.get_right()[0], r2.get_right()[0])
        y_min = max(r1.get_bottom()[1], r2.get_bottom()[1])
        y_max = min(r1.get_top()[1], r2.get_top()[1])

        # check if overlap exist or not
        if x_min < x_max and y_min < y_max:
            width = x_max - x_min
            height = y_max - y_min
            # The center is the average of the min and max coordinates
            center = [(x_min + x_max) / 2, (y_min + y_max) / 2, 0]
            
            rect = Rectangle(width=width, height=height).move_to(center)
            return rect.match_style(self.mob)
        
        return None # no intersection

    def _align_ts_to_arrows(
        self,
        ts,         # VGroup of 4 Texts
    ) -> Self:
        for i, direction in enumerate(DIRECTION_SERIES):
            ts[i].next_to(
                self.arrows[i],
                TEXT_DIRECTION_MAP[direction],
                buff=TEXT_DIRECTION_BUFF,
            )
        return self

    @property
    def dir_to_idx(self) -> dict:
        return {
            'left':  self.index[1],
            'up':    self.index[0],
            'right': self.index[1],
            'down':  self.index[0],
        }
    
    @property
    def dir_to_sign(self) -> dict:
        return {
            'left':  '-',
            'up':    '-',
            'right': '+',
            'down':  '+',
        }
    
    @property
    def sf_screen(self) -> float:
        return self.ref.width

    @property
    def node_left(self) -> np.ndarray:
        return np.array([self.rect.get_left()[0], self.dot.get_center()[1], 0])
    
    @property
    def node_up(self) -> np.ndarray:
        return np.array([self.dot.get_center()[0], self.rect.get_top()[1], 0])

    @property
    def node_right(self) -> np.ndarray:
        return np.array([self.rect.get_right()[0], self.dot.get_center()[1], 0])

    @property
    def node_down(self) -> np.ndarray:
        return np.array([self.dot.get_center()[0], self.rect.get_bottom()[1], 0])

    @property
    def node_map(self) -> dict:
        return {
            'left':  self.node_left,
            'up':    self.node_up,
            'right': self.node_right,
            'down':  self.node_down,
        }


class Demo(Scene):
    def construct(self):
        ap = AnchorPoint(
            point=ORIGIN,
            dist=(1.3,2.8,3.3,4.5),
            xyxy=(10,20,30,40),
            prob=(0.5,0.5,0.5),
            index=(0,1),
            sf_nominal=32,
            sf_screen=0.5,
        )
        self.play(Create(ap, run_time=0.3))
        self.wait()

        # self.play(ap.show_arrows(
        #     lag_ratio=0.2,
        #     rate_func=rate_functions.ease_out_back,
        # ))
        # self.wait()

        # self.play(ap.show_pbars())
        # self.wait()

        ap.prob = np.array([0.7, 0.8, 0.2])
        # self.play(ap.sync_pbars())
        # self.wait()

        # self.play(ap.hide_pbars())
        # self.wait()

        # self.play(ap.to_rect())
        # self.wait()

        # self.play(ap.show_multi_labels())
        # self.wait()

        self.play(ap.show_rect_mlabels(
            rect_config={},
            label_config={
                'width_ratio': 0.3,
                'height_ratio': 0.2,
                # 'fill_opacity': 0.8,
                # 'stroke_opacity': 0.8,
            },
            rargs={'rate_func': rate_functions.ease_out_back},
            largs={'lag_ratio': 0.1},
            gargs={'lag_ratio': 0.0},
        ))
        self.wait()

        self.play(ap.apply_max_select())
        self.wait()


        # rect = Rectangle()
        # self.play(Write(rect))
        # self.wait()

        # self.play(ap.clip_to_background(rect))
        # self.wait()

        # self.play(ap.keep_max_label())
        # self.wait()
from manim import *
from typing import Self

DIRECTION_SERIES = [
    'left',
    'up',
    'right',
    'down',
]

DOT_CONFIG = {
    'side_length': 0.01,
    'stroke_width': 3,
    'stroke_color': WHITE,
}

RECT_CONFIG = {
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

# FIXME, test the last two options
ARROW_CONFIG = {
    'stroke_width': 3,
    'tip_length': 0.15,
    'buff': 0.0,
    # 'max_stroke_width_to_length_ratio': 25,         # 5 by default
    # 'max_tip_length_to_length_ratio': 1.0,          # 0.25 by default
}

TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    # 'font_size': 15,
}

# pbars related
PBAR_SPACE_RATIO = 0.7          # pbar space : unit space
PBAR_GAP_RATIO = 0.1            # pbar gap : pbar space
PBAR_COLORS = [
    GREEN,
    RED,
    BLUE,
]
PBAR_CONFIG = {
    'stroke_width': 0,
    'fill_opacity': 1.0,
}
CLASS_COLORS = PBAR_COLORS

# fake labels related
FAKE_LABEL_COLORS = PBAR_COLORS
FAKE_LABEL_CONFIG = {
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'fill_opacity': 1.0,
}

class AnchorPoint(VMobject):
    def __init__(
        self,
        point: np.ndarray = ORIGIN,                         # starting position
        offset: np.ndarray | list | tuple = (1.,2.,3.,4.),  # left, up, right, down
        sf_screen: float = 0.5,                             # scale factor for screen
        sf_nominal: int = 32,                               # scale factor for nominal, 8/16/32
        idx: tuple = (0,0),                                 # indices of current anchor point
        xyxy: np.ndarray | list | tuple = (1.,2.,3.,4.),    # precomputed x1y1x2y2
        probs: np.ndarray | list | tuple = (0.3,0.8,0.5),   # probability for each class
    ):
        super().__init__()
        # make sure offset is list or tuple
        if isinstance(offset, np.ndarray):
            self.offset = offset.tolist()
        elif isinstance(offset, (list, tuple)):
            self.offset = offset
        self.sf_screen = sf_screen
        self.sf_nominal = sf_nominal
        self.idx = idx
        # make sure xyxy is a list
        if isinstance(xyxy, np.ndarray):
            self.xyxy = xyxy.tolist()
        elif isinstance(xyxy, tuple):
            self.xyxy = [t for t in xyxy]
        else:
            self.xyxy = xyxy
        # make sure probs is a list
        if isinstance(probs, np.ndarray):
            self.probs = probs.tolist()
        elif isinstance(probs, tuple):
            self.probs = [t for t in probs]
        else:
            self.probs = probs
        self.n_probs = len(self.probs)

        dot = Square(
            stroke_opacity=0.0,
            **DOT_CONFIG,
        ).move_to(point)
        self.dot = dot

        # setup baseline for pbars
        baseline = Line(
            start=ORIGIN,
            end=self.sf_screen*RIGHT*PBAR_SPACE_RATIO,
        ).move_to(self.dot)
        baseline.set_opacity(0)
        self.baseline = baseline
        self.add(baseline)      # used for reference

        self.dir_to_idx = {
            'left':  self.idx[1],
            'up':    self.idx[0],
            'right': self.idx[1],
            'down':  self.idx[0],
        }

        self.dir_to_sign = {
            'left':  '-',
            'up':    '-',
            'right': '+',
            'down':  '+',
        }

        left, up, right, down = [x*self.sf_screen for x in self.offset]
        width, height = left+right, up+down
        center_offset = RIGHT*(right-left)/2 + UP*(up-down)/2
        rect = Rectangle(
            width=width,
            height=height,
            stroke_opacity=0.0,
            **RECT_CONFIG,
        ).move_to(point + center_offset)
        self.rect = rect

        self.mob_opacity=1.0
        self.mob = dot.copy().set_stroke(
            opacity=self.mob_opacity,
        )
        self.add(self.dot, self.rect, self.mob)

    def to_rect(
        self,
        rect_config: dict = {}, # rect config
        **aargs,
    ) -> Animation:
        target = self.rect.copy().set_stroke(
            opacity=self.mob_opacity,
            **rect_config,
        )
        return Transform(self.mob, target, **aargs)

    def to_dot(
        self,
        **aargs,
    ) -> Animation:
        target = self.dot.copy().set_stroke(
            opacity=self.mob_opacity,
        )
        return Transform(self.mob, target, **aargs)

    def create_arrows(
        self,
        arrow_config: dict={},
    ) -> VGroup:
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
        **aargs,
    ) -> Animation:
        """ TODO, arrow growing effect.
        """
        self.arrows = self.create_arrows(
            arrow_config=arrow_config,
        )
        self.add(self.arrows)
        return Write(self.arrows, **aargs)
    
    def hide_arrows(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.arrows)
        return Unwrite(self.arrows, **aargs)

    def create_distance_abs(
        self,
        font_size: int = 15,
    ) -> VGroup :
        dists = VGroup(
            *(Text(
                # str(int(self.offset[i]*self.sf_nominal)), # TODO, why the fuck this failed?
                '{:.0f}'.format(self.offset[i]*self.sf_nominal),
                color=TEXT_COLOR_MAP[direction],
                font_size=font_size,
                **TEXT_CONFIG,
            ).next_to(
                self.arrows[i],
                TEXT_DIRECTION_MAP[direction],
                buff=TEXT_DIRECTION_BUFF,
            ) for i, direction in enumerate(DIRECTION_SERIES))
        )
        return dists

    def create_distance(
        self,
        font_size: int = 15,            # specify font size manually
    ) -> VGroup :
        """Create distance not positioned.
        """
        dists = VGroup(
            *(Text(
                '{:.2f}'.format(self.offset[i]),
                color=TEXT_COLOR_MAP[direction],
                font_size=font_size,
                **TEXT_CONFIG,
            ) for i, direction in enumerate(DIRECTION_SERIES))
        )
        return dists
    
    def create_xyxy(
        self,
        font_size: int = 15,            # specify font size manually
    ) -> VGroup:
        """Create xyxy not positioned.
        """
        xyxy = VGroup(
            *(Text(
                '{:>3d}'.format(self.xyxy[i]),
                color=WHITE,            # xyxy is all white
                font_size=font_size,
                **TEXT_CONFIG,
            ) for i in range(4))
        )
        return xyxy
    
    def create_probs(
        self,
        font_size: int = 15,
    ) -> VGroup:
        """Create cls not positioned.
        """
        probs = VGroup(
            *(Text(
                '{:.2f}'.format(self.probs[i]),
                color=CLASS_COLORS[i],
                font_size=font_size,
                **TEXT_CONFIG,
            ) for i in range(3))
        )
        return probs
    
    def create_ordered_distance(
        self,
        font_size: int = 8,             # smaller for tensor
    ) -> VGroup:
        """"Create distance ordered from DL to UR.
        """
        dists = self.create_distance(font_size=font_size)

        # manual arrange
        for i, dist in enumerate(dists):
            dist.move_to(self.dot)
            dist.set_z_index(4-i)
            dist.set_opacity(opacity=1-i*0.2)
            dist.shift((RIGHT*0.05 + UP*0.06)*i)

        dists.move_to(self.dot)
        return dists
    
    def create_ordered_xyxy(
            self,
            font_size: int = 8,         # smaller for tensor
    ) -> VGroup:
        """Create xyxy ordered from DL to UR.
        """
        xyxy = self.create_xyxy(font_size=font_size)

        # manual arrange
        for i, t in enumerate(xyxy):
            t.move_to(self.dot)
            t.set_z_index(4-i)
            t.set_opacity(opacity=1-i*0.2)
            t.shift((RIGHT*0.05 + UP*0.06)*i)
        
        xyxy.move_to(self.dot)
        return xyxy
    
    def create_ordered_probs(
        self,
        font_size: int = 8,
    ) -> VGroup:
        """Create xyxy ordered from DL to UR.
        """
        probs = self.create_probs(font_size=font_size)

        # manual arrange
        for i, t in enumerate(probs):
            t.move_to(self.dot)
            t.set_z_index(4-i)
            t.set_opacity(opacity=1-i*0.2)
            t.shift((RIGHT*0.05 + UP*0.06)*i)
        
        probs.move_to(self.dot)
        return probs
    
    def show_distance_abs(
        self,
        **aargs,
    ) -> Animation:
        self.distance_abs = self.create_distance_abs()
        self.add(self.distance_abs)
        return Write(self.distance_abs, **aargs)
    
    def hide_distance_abs(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.distance_abs)
        return Unwrite(self.distance_abs, **aargs)
    
    def align_distance_to_arrows(
        self,
    ) -> Self:
        for i, direction in enumerate(DIRECTION_SERIES):
            self.distance[i].next_to(
                self.arrows[i],
                TEXT_DIRECTION_MAP[direction],
                buff=TEXT_DIRECTION_BUFF,
            )
        return self
    
    def show_distance(
        self,
        font_size: int = 15,            # specifiy font manually
        **aargs,
    ) -> Animation:
        self.distance = self.create_distance()
        self.align_distance_to_arrows()
        self.add(self.distance)
        return Write(self.distance, **aargs)

    def hide_distance(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.distance)
        return Unwrite(self.distance, **aargs)
    
    def create_divide(
        self,
        font_size: int = 15,
    ) -> VGroup:
        divide = VGroup(*(
            Text(
                '/' + str(self.sf_nominal),
                color=TEXT_COLOR_MAP[direction],
                font_size=font_size,
                **TEXT_CONFIG,
            ).next_to(
                self.distance_abs[i],
                RIGHT,
                buff=0.05,
            ) for i, direction in enumerate(DIRECTION_SERIES)
        ))
        return divide
    
    def show_divide(
        self,
        **aargs,
    ) -> Animation:
        """ Create divide and add into distance.
        """
        divide = self.create_divide()
        for dis, div in zip(self.distance_abs, divide):
            dis.add(div)
        return Write(divide, **aargs)
    
    def abs_to_rela(
        self,
        aargs: dict = {},       # ReplacementTransform args
        gargs: dict = {},       # AnimationGroup args
    ) -> Animation:
        """ Convert distance_abs with divide into distance.
        """
        self.remove(self.distance_abs)
        self.distance = self.create_distance()
        self.align_distance_to_arrows()
        self.add(self.distance)
        return AnimationGroup(
            *(ReplacementTransform(dis_abs, dis_rela, **aargs)
            for dis_abs, dis_rela in zip(self.distance_abs, self.distance)),
            **gargs,
        )

    def get_center(
        self,
    ) -> np.ndarray:
        """Override the default center with dot center.
        """
        return self.dot.get_center()
    
    def set_pattern(
        self,
        opacity: float = 1.0,           # FIXME, the default opacity?
        color: ManimColor = WHITE,      # FIXME, the default color?
    ) -> Self:
        """FIXME, Set pattern, only care about opacity and color.
        """
        self.mob_opacity = opacity
        self.mob.set_stroke(opacity=opacity, color=color)
        self.dot.set_stroke(color=color)
        self.rect.set_stroke(color=color)
        return self

    def create_decode_equations(
        self,
        font_size: int = 15,
        buff: float = 0.3,              # up-down buff between equatinos
    ) -> VGroup:
        """Create 4 Equations show computing from distance to position,
           not positioned, not arranged.
        """
        equations = VGroup()
        for i, direction in enumerate(DIRECTION_SERIES):
            text = (
                f'({self.dir_to_idx[direction]:>2d}+0.5{self.dir_to_sign[direction]}'
                f'<span foreground="{TEXT_COLOR_MAP[direction]}">{self.offset[i]:.2f}</span>'
                f')*{self.sf_nominal} = '
                f'<span foreground="white">{self.xyxy[i]:<3d}</span>'
            )
            equation = MarkupText(
                text,
                color=GRAY,
                font_size=font_size,
                **TEXT_CONFIG,
            )
            equations.add(equation)

        equations.arrange(
            DOWN,
            buff=buff,
            aligned_edge=LEFT,
        ).center()

        return equations
    
    def create_pbars(
        self,
        probs: list | None = None,        # (n_probs,)
    ) -> VGroup:
        """Realtime pbars based on baseline.
        """
        if probs is None:
            probs = self.probs

        space_size = self.baseline.width
        pbar_gap = space_size * PBAR_GAP_RATIO
        pbar_width = space_size * (1-(self.n_probs-1)*PBAR_GAP_RATIO) / self.n_probs
        pbars = VGroup(
            Rectangle(
                width=pbar_width,
                height=space_size*p,
                fill_color=PBAR_COLORS[i],
                **PBAR_CONFIG,
            ).align_to(self.baseline, LEFT)\
             .shift((pbar_width+pbar_gap)*i*RIGHT)\
             .set_y(self.baseline.get_y())
            for i, p in enumerate(probs)
        )
        return pbars
    
    def show_pbars(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Grow pbars from baseline.
        """
        pbars_end = self.create_pbars()
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
    
    def to_probs(
        self,
        probs: np.ndarray | list | None,         # (n_probs, )
        **aargs,
    ) -> Animation:
        """Update pbars with new one.
        """
        if probs is None:
            return Wait(1.0)
        if isinstance(probs, np.ndarray):
            probs = probs.tolist()

        self.probs = probs
        new_pbars = self.create_pbars(probs)
        return Transform(self.pbars, new_pbars, **aargs)
    
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
        width_ratio: float = 0.6,            # width : baseline
        height_ratio: float = 0.4,           # height : baseline
        **label_config,                      # rectangle config
    ) -> VGroup:
        """Create multi labels, not positioned.
        """
        cfg = {**FAKE_LABEL_CONFIG, **label_config}
        label_width = self.baseline.width * width_ratio
        label_height = self.baseline.width * height_ratio
        labels = VGroup(
            Rectangle(
                width=label_width,
                height=label_height,
                stroke_color=color,
                fill_color=color,
                **cfg,
            ) for color in FAKE_LABEL_COLORS
        ).arrange(buff=0)
        return labels
    
    def show_multi_labels(
        self,
        width_ratio: float = 0.6,            # width : baseline
        height_ratio: float = 0.4,           # height : baseline
        label_config: dict = {},             # rectangle config
        **aargs,
    ) -> Animation:
        self.labels = self.create_multi_labels(
            width_ratio=width_ratio,
            height_ratio=height_ratio,
            **label_config,
        ).move_to(
            self.rect.get_corner(UL),
            aligned_edge=DL,
        )

        self.add(self.labels)
        return Write(self.labels, **aargs)

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
            offset=(1,2,3,4),
            sf_screen=0.5,
            idx=(5,6),
            xyxy=(120,230,312,23),
        ).scale(1.5)
        self.play(Create(ap, run_time=0.3))
        self.wait()

        # self.play(ap.show_arrows(
        #     lag_ratio=0.3,
        #     run_time=0.3,
        # ))
        # self.wait(0.3)

        self.play(ap.to_rect(
            rect_config={'width': 1},
        ))
        self.wait()

        self.play(ap.show_pbars())
        self.wait()

        self.play(ap.show_multi_labels(
            label_config={'fill_opacity': 0.3},
        ))
        self.wait()

        # self.play(ap.to_probs([0.5,0.5,0.5]))
        # self.wait()

from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from typing import Self
from utils.comment import Comment
from utils.constants import KK_COLORS


# ------------- general --------------
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

TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    # 'font_size': 15,
}

DIRECTION_SERIES = [
    'left',
    'up',
    'right',
    'down',
]

DIRECTION_MAP = {
    'left': LEFT,
    'up': UP,
    'right': RIGHT,
    'down': DOWN,
}

COLOR_MAP = {
    'left':  PURE_RED,
    'up':    PURE_GREEN,
    'right': PURE_BLUE,
    'down':  PURE_MAGENTA,
}

# ------------- arrow related --------------
ARROW_COLOR_MAP = COLOR_MAP

TEXT_COLOR_MAP = COLOR_MAP

TEXT_DIRECTION_MAP = {
    'left':  UP,
    'up':    RIGHT,
    'right': DOWN,
    'down':  LEFT,
}
TEXT_DIRECTION_BUFF = 0.1

ARROW_CONFIG = {
    'stroke_width': 3,
    'tip_length': 0.15,
    'buff': 0.0,
    'max_stroke_width_to_length_ratio': 15,         # FIXME: 5 by default
    'max_tip_length_to_length_ratio': 0.25,          # FIXME: 0.25 by default
}


# ------------- pbar related --------------
PBAR_SPACE_RATIO = 0.5          # pbar space : unit space
PBAR_GAP_RATIO = 0.1            # pbar gap : pbar space
PBAR_COLORS = KK_COLORS
PBAR_CONFIG = {
    'stroke_width': 0,
    'fill_opacity': 1.0,
}
CLASS_COLORS = PBAR_COLORS

# ------------- label related --------------
LABEL_COLORS = PBAR_COLORS
LABEL_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 9,
    'color': WHITE,
}

# box for label with text
BOX_BG_CONFIG = {
    'stroke_width': 0,
    'stroke_opacity': 0.0,
    'opacity': 1.0,         # background rectangle interface
}
# box for label without text
BOX_RAW_CONFIG = {
    'stroke_width': 0,
    'stroke_opacity': 0.0,
    'fill_opacity': 1.0,    # native rectangle interface
}

# ------------- pcell related --------------
PCELL_TEXT_CONFIG = {
    'num_decimal_places': 2,
    'font_size': 54,
    'color': WHITE,
}
PCELL_BOX_CONFIG = {
    'stroke_width': 1,
    'stroke_opacity': 1.0,
}
PCELL_STROKE_OPACITY_E = 0.5
PCELL_FILL_OPACITY_E = 0.7

class PCell(VMobject):
    def __init__(
        self,
        prob: float = 0.00,
        box_config: dict = {},
    ):
        """
        Square cell contains prob of specific distance.
        """
        super().__init__()
        self.prob = prob

        box_config = {
            **PCELL_BOX_CONFIG,
            **box_config,
        }
        mob_box = Square(
            **box_config,
        )

        self.mob_box = mob_box
        self.add(self.mob_box)
    
    def show_text(
        self,
        text_config: dict = {},
        **aargs,
    ) -> Animation:
        text_config = {
            **PCELL_TEXT_CONFIG,
            **text_config,
        }
        mob_text = DecimalNumber(
            self.prob,
            **text_config,
        )

        self.mob_text = mob_text
        self.add(self.mob_text)
        return Create(
            self.mob_text,
            **aargs,
        )
    
    def hide_text(
        self,
        **aargs,
    ) -> Animation:
        assert hasattr(self, 'mob_text'), 'mob_text not exist yet'

        self.remove(self.mob_text)
        return Uncreate(
            self.mob_text,
            **aargs,
        )

class AnchorLabel(VMobject):
    def __init__(
        self,
        include_text: bool = True,      # include conf text or not
        text: str = 'None',             # conf text content
        label_config: dict | None = None,        # text config
        box_config: dict | None = None,          # background config
    ):
        """
        Use the same interface as native Label class.

        Example
        -------
        label = AnchorLabel(text="0.95")
        """
        super().__init__()
        self.include_text = include_text
        self.text = text if include_text else None
        self.label_config = {**LABEL_CONFIG, **(label_config or {})} if include_text else {}
        self.box_config = {**(
            BOX_BG_CONFIG if include_text else BOX_RAW_CONFIG
            ), **(box_config or {})}

        if include_text:
            mob_text = Text(
                text=self.text,
                **self.label_config,
            ).add_background_rectangle(
                **self.box_config,
            )

            # fix background rectangle
            mob_box = Rectangle(
                width=mob_text.background_rectangle.width,
                height=mob_text.background_rectangle.height,
            ).set_style(
                **mob_text.background_rectangle.get_style(simple=True),
            ).move_to(mob_text.background_rectangle)
            mob_text.remove(mob_text.background_rectangle)

            self.mob_text = mob_text
            self.mob_box = mob_box
            self.add(self.mob_box, self.mob_text)
        else:
            mob_box = Rectangle(
                **self.box_config,
            )
            self.mob_box = mob_box
            self.add(self.mob_box)

class AnchorPoint(VMobject):
    def __init__(
        self,
        point: np.ndarray = ORIGIN,                         # starting position
        distrib: np.ndarray | list | None = None,           # box distance distribution, (4, 16), (left, up, right down)
        offsets: np.ndarray | list | tuple = (1.,1.,1.,1.), # box distance offsets, (4,), (left, up, right, down)
        xyxy: np.ndarray | list | tuple = (10,20,30,40),    # box position, (4,), (x1, y1, x2, y2)
        prob: np.ndarray | list | tuple = (.5,.5,.5),       # prob, (3,), (c1, c2, c3)
        index: np.ndarray | list | tuple = (0, 0),          # index in explainer, (2,), (h, w)
        shape: tuple = (5, 5),                              # shape of explainer, (2,), (H, W)
        sf_nominal: int = 32,                               # nominal length / unit length
        sf_screen: int = 0.5,                               # screen length / unit length
        dot_config: dict = {},                              # default dot config
        rect_config: dict = {},                             # default rect config
    ):
        """ User is responsible for providing matching tensors.
            mob works as a copy of dot or rect.
            pcells, arrows, pbars, comments created in real time.
        """
        super().__init__()
        # user is responsible for providing matching tensors
        self.distrib = np.array(distrib)
        self.n_distrib = self.distrib.shape[1]
        self.offsets = np.array(offsets)
        self.xyxy = np.array(xyxy)
        self.prob = np.array(prob)
        self.index = np.array(index)
        self.shape = shape
        self.sf_nominal = sf_nominal
        # self.sf_screen = sf_screen  # NOTE: as a property in real time

        dot_config = {**DOT_CONFIG, **dot_config}
        rect_config = {**RECT_CONFIG, **rect_config}

        dot = Square(
            stroke_opacity=0.0,
            **dot_config,
        ).move_to(point)

        left, up, right, down = [x*sf_screen for x in self.offsets]
        rect = Rectangle(
            width=left+right,
            height=up+down,
            stroke_opacity=0.0,
            **rect_config,
        ).move_to(
            point + left*LEFT + up*UP,
            aligned_edge=UL,
        )

        self.dot = dot
        self.rect = rect

        self.mob = dot.copy().set_stroke(opacity=1.0)

        self.add(self.dot, self.rect, self.mob)

    def to_rect(
        self,
        rect_config: dict = {}, # override default
        **aargs,
    ) -> Animation:
        rect_config = {'stroke_opacity': 1.0, **rect_config}
        target = self.rect.copy().set_style(
            **rect_config,
        )
        return Transform(
            self.mob,
            target,
            **aargs,
        )

    def to_dot(
        self,
        dot_config: dict = {}, # override default
        **aargs,
    ) -> Animation:
        dot_config = {'stroke_opacity': 1.0, **dot_config}
        target = self.dot.copy().set_style(
            **dot_config,
        )
        return Transform(
            self.mob,
            target,
            **aargs,
        )

    # ---------------- pcells related -------------------
    def create_pcells(
        self,
        direction: str | None = None,   # all or specific direction
        sf_pcell: float = 1.0,      # pcell size ratio, <1.0 for mini explainer
        box_config: dict = {},      # config for pcells
        arranged: bool = False,     # arrange in IN direction or not
        buff: float = 0.1,          # arrange buff
    ) -> VGroup:
        pcells = {}
        directions = [direction] if direction else DIRECTION_SERIES
        for idx, direction in enumerate(directions):
            dist = self.distrib[idx]
            series = VGroup()
            for i, p in enumerate(dist):
                pcell = PCell(
                    prob=float(p),
                    box_config={
                        'side_length': self.sf_screen*sf_pcell,
                        'stroke_color': COLOR_MAP[direction],
                        'stroke_opacity': float(p)**PCELL_STROKE_OPACITY_E,
                        'fill_color': COLOR_MAP[direction],
                        'fill_opacity': float(p)**PCELL_FILL_OPACITY_E,
                        **box_config,
                    },
                ).move_to(self.dot).shift(
                    DIRECTION_MAP[direction] * i * self.sf_screen * sf_pcell
                )
                series.add(pcell)
            pcells[direction] = series
        
        if (direction is None) and arranged:
            pcells.arrange(
                direction=IN,
                buff=buff,
            ).move_to(self.dot)

        return pcells

    def show_pcells(
        self,
        direction: str | None = None,   # all or specific direction
        sf_pcell: float = 1.0,
        box_config: dict = {},
        arranged: bool = False,     # arrange in IN direction or not
        buff: float = 0.1,          # arrange buff
        **aargs,
    ) -> Animation:
        pcells = self.create_pcells(
            direction=direction,
            sf_pcell=sf_pcell,
            box_config=box_config,
            arranged=arranged,
            buff=buff,
        )
        if hasattr(self, 'pcells'):
            self.pcells.update(pcells)
        else:
            self.pcells = pcells

        mobs = VGroup(pc for pcs in pcells.values() for pc in pcs)

        self.add(*mobs)

        return Create(
            mobs,
            **aargs,
        )

        # NOTE: HERE TO GO....

    def show_pcells_text(
        self,
        text_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        assert hasattr(self, 'pcells'), 'pcells not exist yet'

        return AnimationGroup(
            *(pc.show_text(
                text_config=text_config,
                **aargs,
            ) for pc in self.pcells),
            **gargs,
        )

    def hide_pcells_text(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        assert hasattr(self, 'pcells'), 'pcells not exist yet'

        return AnimationGroup(
            *(pc.hide_text(
                **aargs,
            ) for pc in self.pcells),
            **gargs,
        )

    def hide_pcells(
        self,
        **aargs,
    ) -> Animation:
        self.remove(self.pcells)
        return Unwrite(self.pcells, **aargs)

    def arrange_pcells(
        self,
        **aargs,
    ) -> Animation:
        """
        Stack existing pcells along the depth axis.


        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_pcells())
        self.play(ap.arrange_pcells())
        """
        self.pcells.generate_target()

        # TODO
        self.pcells.target.arrange(
            direction=IN,
            buff=0.1,
        ).move_to(self.dot)
        return MoveToTarget(
            self.pcells,
            **aargs,
        )

    def create_arrow_direction(
        self,
        direction: str = 'left',
        arrow_config: dict | None = None,
    ) -> Arrow:
        """
        Create arrow in specific direction.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap.create_arrow_direction()
        """
        cfg = {**ARROW_CONFIG, **(arrow_config or {})}
        arrow = Arrow(
            start=self.dot.get_center(),
            end=self.node_map[direction],
            color=ARROW_COLOR_MAP[direction],
            **cfg,
        )
        return arrow

    def show_arrow_direction(
        self,
        direction: str = 'left',
        arrow_config: dict | None = None,
        **aargs,
    ) -> Animation:
        """
        Show arrow in specific direction.


        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrow_direction())
        """
        arrow = self.create_arrow_direction(
            direction=direction,
            arrow_config=arrow_config,
        )
        if hasattr(self, 'arrows'):
            self.arrows.add(arrow)
        else:
            self.arrows = VGroup(arrow)
            self.add(self.arrows)
        return GrowArrow(
            arrow,
            **aargs,
        )

    def create_arrows(
        self,
        arrow_config: dict | None = None,
    ) -> VGroup:
        """
        Create arrows based on dot and rect.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap.create_arrows()
        """
        cfg = {**ARROW_CONFIG, **(arrow_config or {})}
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
        arrow_config: dict | None = None,
        aargs: dict | None = None,
        gargs: dict | None = None,
    ) -> Animation:
        """
        Show arrows in all four directions.

                NOTE: rate_func for arrow is inside aargs.


        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
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
        # return Write(self.arrows, **(aargs or {}))

    def hide_arrows(
        self,
        **aargs,
    ) -> Animation:
        """
        TODO, shrink version?

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.hide_arrows())
        """
        self.remove(self.arrows)
        return Unwrite(self.arrows, **(aargs or {}))

    def create_dist(
        self,
        font_size: int = 15,            # specify font size manually
    ) -> VGroup :
        """
        Create distance Texts, not aligned.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        result = ap.create_dist()
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
        """
        Show distance Texts, aligned to arrows.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        self.play(ap.show_dist())
        """
        self.ts_dist = self.create_dist(
            font_size=font_size,
        )
        self._align_ts_to_arrows(self.ts_dist)
        self.add(self.ts_dist)
        return Write(self.ts_dist, **(aargs or {}))

    def hide_dist(
        self,
        **aargs,
    ) -> Animation:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        self.play(ap.hide_dist())
        """
        self.remove(self.ts_dist)
        return Unwrite(self.ts_dist, **(aargs or {}))

    def create_dist_nominal(
        self,
        font_size: int = 15,
    ) -> VGroup :
        """
        Create nominal distance Texts, not aligned.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        result = ap.create_dist_nominal()
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
        """
        Show nominal distance Texts, aligned to arrows.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        self.play(ap.show_dist_nominal())
        """
        self.ts_dist_nominal = self.create_dist_nominal(
            font_size=font_size,
        )
        self._align_ts_to_arrows(self.ts_dist_nominal)
        self.add(self.ts_dist_nominal)
        return Write(self.ts_dist_nominal, **(aargs or {}))

    def hide_dist_nominal(
        self,
        **aargs,
    ) -> Animation:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        self.play(ap.hide_dist_nominal())
        """
        self.remove(self.ts_dist_nominal)
        return Unwrite(self.ts_dist_nominal, **(aargs or {}))

    def create_divide(
        self,
        font_size: int = 15,
    ) -> VGroup:
        """
        Create '/sf_nominal' for each dist_nominal.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        result = ap.create_divide()
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
        """
        Append '/sf_nominal' into each dist_nominal.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        self.play(ap.show_divide())
        """
        divide = self.create_divide()
        for dist, div in zip(self.ts_dist_nominal, divide):
            dist.add(div)
        return Write(divide, **(aargs or {}))

    def nominal_to_rela(
        self,
        aargs: dict | None = None,       # ReplacementTransform args
        gargs: dict | None = None,       # AnimationGroup args
    ) -> Animation:
        """
        Convert ts_dist_nominal with divide into ts_dist.


        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_arrows())
        self.play(ap.nominal_to_rela())
        """
        self.remove(self.ts_dist_nominal)
        self.ts_dist = self.create_dist()
        self._align_ts_to_arrows(self.ts_dist)
        self.add(self.ts_dist)
        return AnimationGroup(
            *(ReplacementTransform(dist_nominal, dist_rela, **(aargs or {}))
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

    def create_DFL_computations(
        self,
        buff: float = 0.3,
        text_config: dict | None = None,
    ) -> VGroup:
        """
        Create 4 computations from distribution to distance.
                   not positioned.
                   FIXME: use 16 reg by default.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap.create_DFL_computations()
        """
        cws = [ # color wrappers
            f'<span foreground="{TEXT_COLOR_MAP[d]}">{{:.2f}}</span>'
              for d in DIRECTION_SERIES
            ]
        formatters = [
            (
                f'  {cw}x 0 + {cw}x 1 + {cw}x 2 + {cw}x 3\n'
                f'+ {cw}x 4 + {cw}x 5 + {cw}x 6 + {cw}x 7\n'
                f'+ {cw}x 8 + {cw}x 9 + {cw}x10 + {cw}x11\n'
                f'+ {cw}x12 + {cw}x13 + {cw}x14 + {cw}x15\n'
                f'= <span foreground="white">{{:.2f}}</span>'
            ) for cw in cws
        ]
        values = [
            [float(v) for v in row] + [float(d)]
             for row, d in zip(self.reg, self.dist)
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


    def create_decode_computations(
        self,
        buff: float = 0.3,              # up-down buff between computations
        text_config: dict | None = None,         # for computation
    ) -> VGroup:
        """
        Create 4 computations from distance to position,
                   not positioned.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap.create_decode_computations()
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
        pbar_config: dict | None = None,
    ) -> VGroup:
        """
        Realtime pbars based on given prob.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap.create_pbars()
        """
        n_probs = len(self.prob)
        pbar_space = self.sf_screen * PBAR_SPACE_RATIO
        pbar_offset = self.sf_screen*(1-PBAR_SPACE_RATIO)/2
        pbar_gap = pbar_space * PBAR_GAP_RATIO
        pbar_width = pbar_space * (1-(n_probs-1)*PBAR_GAP_RATIO) / n_probs
        cfg = {**PBAR_CONFIG, **(pbar_config or {})}
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
        pbar_config: dict | None = None,
        aargs: dict | None = None,
        gargs: dict | None = None,
    ) -> Animation:
        """
        Grow pbars from baseline.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_pbars())
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
            *(Transform(p0, p1, **(aargs or {}))
            for p0, p1 in zip(self.pbars, pbars_end)),
            **gargs,
        )

    def sync_pbars(
        self,
        pbar_config: dict | None = None,
        aargs: dict | None = None,
        gargs: dict | None = None,
    ) -> Animation:
        """
        Sync pbars into current prob.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.sync_pbars())
        """
        pbars_end = self.create_pbars(
            pbar_config=pbar_config,
        )     # current prob
        return AnimationGroup(
            *(Transform(p0, p1, **(aargs or {}))
            for p0, p1 in zip(self.pbars, pbars_end)),
            **gargs,
        )

    def hide_pbars(
        self,
        aargs: dict | None = None,
        gargs: dict | None = None,
    ) -> Animation:
        """
        Shrink pbars into baseline.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.hide_pbars())
        """
        pbars_end = self.pbars.copy()
        for bar in pbars_end:
            bar.stretch_to_fit_height(0)
        self.remove(self.pbars)
        return AnimationGroup(
            *(Transform(p0, p1, **(aargs or {}))
            for p0, p1 in zip(self.pbars, pbars_end)),
            **gargs,
        )

    def create_multi_labels(
        self,
        include_text: bool = True,      # include conf text or not
        label_config: dict | None = None,        # font size 12 by default
        box_config: dict | None = None,
    ) -> VGroup:
        """
        Create multi labels, not positioned.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        result = ap.create_multi_labels()
        """
        labels = VGroup(
            AnchorLabel(
                include_text=include_text,
                text='{:.2f}'.format(prob),
                label_config=label_config,
                box_config={**(box_config or {}), 'color': color},  # TODO: Label's interface
            ) for prob, color in zip(self.prob, LABEL_COLORS)
        ).arrange(RIGHT, buff=0.0)
        return labels

    def show_multi_labels(
        self,
        include_text: bool = True,      # show conf text or not
        label_config: dict | None = None,        # font size 12 by default
        box_config: dict | None = None,
        **aargs,
    ) -> Animation:
        """
        Add labels as new member.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        self.play(ap.show_multi_labels())
        """
        labels = self.create_multi_labels(
            include_text=include_text,
            label_config=label_config,
            box_config=box_config,
        ).move_to(
            self.rect.get_corner(UL),
            aligned_edge=DL,
        )
        self.labels = labels
        self.add(self.labels)

        return Write(self.labels, **(aargs or {}))

    def show_rect_mlabels(
        self,
        rect_config: dict | None = None,
        include_text: bool = True,      # show conf score or not
        label_config: dict | None = None,        # font size 12 by default
        box_config: dict | None = None,
        rargs: dict | None = None,       # to_rect animation args
        largs: dict | None = None,       # show_multi_labels animation args
        gargs: dict | None = None,       # group args
    ) -> Animation:
        """
        Show rect and multi labels at a time.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        self.play(ap.show_rect_mlabels())
        """
        anims = AnimationGroup(
            self.to_rect(
                rect_config=rect_config,
                **rargs,
            ),
            self.show_multi_labels(
                include_text=include_text,
                label_config=label_config,
                box_config=box_config,
                **largs
            ),
            **gargs,
        )
        return anims

    def apply_max_select(
        self,
        max_idx: int = 0,       # the max index to keep
        aargs: dict | None = None,       # animation args
        gargs: dict | None = None,       # group args
    ) -> Animation:
        """
        Select max conf label and append cls label.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        result = ap.apply_max_select()
        """
        # max_idx = np.argmax(self.prob)
        max_label = self.labels[max_idx]

        self.cls = max_idx              # remember max class index
        self.conf = self.prob[max_idx]  # remember max class conf

        max_target = max_label.copy().move_to(self.labels[0], aligned_edge=DL)
        max_target.mob_box.set_stroke(
            color=max_target.mob_box.fill_color,
            opacity=1.0,
            width=2,
        )   # NOTE, visual adjustment for max label
        anims = [
            Transform(max_label, max_target, **(aargs or {})),
        ]
        labels_to_remove = []
        for i in range(len(self.labels)):
            if i != max_idx:
                anims.append(FadeOut(self.labels[i], **(aargs or {})))  # or Unwrite?
                labels_to_remove.append(self.labels[i])

        self.rect.set_stroke(color=PBAR_COLORS[max_idx])
        anims.append(self.mob.animate(**(aargs or {})).set_stroke(color=PBAR_COLORS[max_idx]))

        self.labels.remove(*labels_to_remove)

        return AnimationGroup(*anims, **(gargs or {}))

    def use_color(
        self,
        color: ManimColor = PURE_YELLOW,
        font_color: ManimColor = None,
    ) -> Self:
        """
        TODO: better naming?
                   Setup fill color of labels[0].mob_box and stroke color of mob.
                   Usually used after save_state, to be restored soon.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        ap.use_color()
        """
        # self.labels[0].mob_box.set_fill(color=color, opacity=1.0)
        # self.labels[0].mob_box.set_stroke(color=color, opacity=1.0)
        self.labels[0].mob_box.set_color(color=color)
        self.mob.set_stroke(color=color)
        if font_color is not None:
            self.labels[0].mob_text.set_color(color=font_color)
        return self

    def use_fade(
        self,
        darkness: float = 0.5,
    ) -> Self:
        """
        NOTE: better naming?
                   Fade all, hide label_box's stroke for better visual effect.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        ap.use_fade()
        """
        self.labels[0].mob_box.fade(darkness=darkness)
        self.labels[0].mob_box.set_stroke(opacity=0.0)
        self.labels[0].mob_text.fade(darkness=darkness)
        self.mob.fade(darkness=darkness)
        return self

    def check_clip(
        self,
        background,
    ) -> bool:
        """
        Check if current ap remains after clipping.
                   Save target intersection by the way.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap.check_clip(background=Square())
        """
        self.clip_target = self._intersect_background(background)
        return self.clip_target is not None

    def do_clip(
        self,
        **aargs,
    ) -> Animation:
        """
        Make rect clipping.
                   clip_target should be properly setup.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        self.play(ap.show_multi_labels())
        self.play(ap.do_clip())
        """
        self.remove(self.rect)
        self.rect = self.clip_target    # NOTE: use's responsibility
        anims = AnimationGroup(
            self.to_rect(
                rect_config={},
            ),
            self.labels.animate.move_to(
                self.rect.get_corner(UL),
                aligned_edge=DL,
            ),
            **aargs,
        )
        return anims
        #     anims.append(Unwrite(self)) # TODO, or fade out???
        # else:
        #     self.remove(self.rect)
        #     self.rect = inter_rect
        #     anims.append(AnimationGroup(
        #         self.to_rect(
        #             rect_config={},
        #             **(aargs or {}),
        #         ),
        #         self.labels.animate(**(aargs or {})).move_to(
        #             self.rect.get_corner(UL),
        #             aligned_edge=DL,
        #         ),
        #     ))
        # return AnimationGroup(*anims)

    def _intersect_background(
        self,
        background,
    ) -> Rectangle | None:
        """
        Compute the intersection between self.rect and background
                   return a new Rectangle if intersected, None otherwise.

        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap._intersect_background(background=Square())
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
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        result = ap._align_ts_to_arrows(ts=VGroup(Text("1"), Text("2"), Text("3"), Text("4")))
        """
        for i, direction in enumerate(DIRECTION_SERIES):
            ts[i].next_to(
                self.arrows[i],
                TEXT_DIRECTION_MAP[direction],
                buff=TEXT_DIRECTION_BUFF,
            )
        return self
    
    def inside_box(
        self,
        box: Rectangle,
    ) -> bool:
        """Check if anchor point (dot) is inside rectangle.
        """
        point = self.dot.get_center()
        left   = box.get_left()[0]
        right  = box.get_right()[0]
        bottom = box.get_bottom()[1]
        top    = box.get_top()[1]
        inside = (
            left <= point[0] <= right and
            bottom <= point[1] <= top
        )
        return inside
    
    @property
    def sf_screen(
        self,
    ) -> float:
        width_screen = self.rect.width
        width_offset = self.offsets[0] + self.offsets[2]
        return width_screen / width_offset
    
    @property
    def index_flatten(
        self,
    ) -> int:
        return self.index[0]*self.shape[1] + self.index[1]
    
    @property
    def dir_to_idx(self) -> dict:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.dir_to_idx
        """
        return {
            'left':  self.index[1],
            'up':    self.index[0],
            'right': self.index[1],
            'down':  self.index[0],
        }

    @property
    def dir_to_sign(self) -> dict:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.dir_to_sign
        """
        return {
            'left':  '-',
            'up':    '-',
            'right': '+',
            'down':  '+',
        }

    @property
    def node_left(self) -> np.ndarray:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.node_left
        """
        return np.array([self.rect.get_left()[0], self.dot.get_center()[1], 0])

    @property
    def node_up(self) -> np.ndarray:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.node_up
        """
        return np.array([self.dot.get_center()[0], self.rect.get_top()[1], 0])

    @property
    def node_right(self) -> np.ndarray:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.node_right
        """
        return np.array([self.rect.get_right()[0], self.dot.get_center()[1], 0])

    @property
    def node_down(self) -> np.ndarray:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.node_down
        """
        return np.array([self.dot.get_center()[0], self.rect.get_bottom()[1], 0])

    @property
    def node_map(self) -> dict:
        """
        Example
        -------
        ap = AnchorPoint(reg=np.random.rand(4, 16))
        value = ap.node_map
        """
        return {
            'left':  self.node_left,
            'up':    self.node_up,
            'right': self.node_right,
            'down':  self.node_down,
        }


class Demo(ThreeDScene):
    def construct(self):
        distrib = np.random.rand(4, 4)
        distrib /= distrib.sum(axis=1, keepdims=True)
        ap = AnchorPoint(
            point=ORIGIN,
            distrib=distrib,
            offsets=(1.3,2.8,3.3,2.5),
            xyxy=(10,20,30,40),
            prob=(0.5,0.5,0.5),
            index=(0,1),
            shape=(4,4),
            sf_nominal=32,
            sf_screen=0.5,
            dot_config={},
            rect_config={},
        )
        self.play(Create(ap, run_time=0.3))
        self.wait()

        self.play(ap.to_rect())
        self.wait()

        # self.play(ap.show_pcells())
        # self.wait()

        for direction in DIRECTION_SERIES:
            self.play(ap.show_pcells(direction=direction))
            self.wait()
        self.wait()


        # self.play(ap.to_dot())
        # self.wait()

        # self.play(ap.show_pcells(
        #     label_config={
        #         'font_size': 5,
        #     },
        #     box_config={},
        #     run_time=0.5,
        # ))
        # self.wait(0.5)

        # self.play(ap.show_pcells_text(
        #     run_time=0.5,
        # ))
        # self.wait(0.5)

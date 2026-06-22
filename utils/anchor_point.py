from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.comment import Comment
from utils.ylabel import YLabel
from utils.constants import *

from typing import Self
from random import uniform

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
    'font_size': 24,
    'font': 'JetBrains Mono',
    # 'font_size': 15,
}

# ------------- arrow related --------------
TEXT_DIRECTION_MAP = {
    'left':  UP,
    'up':    RIGHT,
    'right': DOWN,
    'down':  LEFT,
}
TEXT_DIRECTION_BUFF = 0.1

ARROW_CONFIG = {
    'stroke_width': 3,
    'tip_length': 0.10,
    'buff': 0.0,
    'max_stroke_width_to_length_ratio': 15,         # FIXME: 5 by default
    'max_tip_length_to_length_ratio': 0.85,          # FIXME: 0.25 by default
}

ARROW_TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 12,
}

ARROW_DIVIDE_COLOR = GRAY
ARROW_DIVIDE_BUFF = 0.03

# ------------- pbar related --------------
PBAR_SPACE_RATIO = 0.6          # pbar space : unit space
PBAR_GAP_RATIO = 0.1            # pbar gap : pbar space
PBAR_COLORS = KK_COLORS
PBAR_CONFIG = {
    'stroke_width': 0,
    'fill_opacity': 1.0,
}
PBAR_NEG_RANGE = (0, 0.3)
PBAR_POS_RANGE = (0.7, 1.0)

# ------------- label related --------------
LABEL_COLORS = KK_COLORS
LABEL_TXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 9,
    'color': WHITE,
}
LABEL_BG_CONFIG = {
    'stroke_width': 0,
    'stroke_opacity': 0.0,
    'fill_opacity': 1.0,         # background rectangle interface
}
# LABEL_CONFIG = {
#     'font': 'JetBrains Mono',
#     'font_size': 9,
#     'color': WHITE,
# }

# # box for label with text
# BOX_BG_CONFIG = {
#     'stroke_width': 0,
#     'stroke_opacity': 0.0,
#     'opacity': 1.0,         # background rectangle interface
# }
# # box for label without text
# BOX_RAW_CONFIG = {
#     'stroke_width': 0,
#     'stroke_opacity': 0.0,
#     'fill_opacity': 1.0,    # native rectangle interface
# }

# ------------- coords related --------------
COORDS_PATH_CONFIG = {
    'color': PURE_YELLOW,
    'width': 3,
    'opacity': 1.0,
}
COORDS_TEXT_CONFIG = {
    'font_size': 15,
    'font': 'JetBrains Mono',
    'color': WHITE,
}
COORDS_TEXT_BUFF = 0.2

# ------------- computation related --------------
COMPUTATION_TEXT_CONFIG = {
    "font": "JetBrains Mono",
    "font_size": 32,
    'color': GRAY,
}

# ------------- pcell related --------------
PCELL_TEXT_CONFIG = {
    'num_decimal_places': 2,
    'font_size': 24,
    'color': WHITE,
}
PCELL_BOX_CONFIG = {
    'stroke_width': 1,
    'stroke_opacity': 1.0,
}
PCELL_STROKE_OPACITY_E = 0.5
PCELL_FILL_OPACITY_E = 0.7

PCELL_DEPTH_BUFF_RATIO = 1.0

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
        ).move_to(self.mob_box)

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

# class AnchorLabel(VMobject):
#     def __init__(
#         self,
#         include_text: bool = True,      # include conf text or not
#         text: str = 'None',             # conf text content
#         label_config: dict | None = None,        # text config
#         box_config: dict | None = None,          # background config
#     ):
#         """
#         Use the same interface as native Label class.

#         Example
#         -------
#         label = AnchorLabel(text="0.95")
#         """
#         super().__init__()
#         self.include_text = include_text
#         self.text = text if include_text else None
#         self.label_config = {**LABEL_CONFIG, **(label_config or {})} if include_text else {}
#         self.box_config = {**(
#             BOX_BG_CONFIG if include_text else BOX_RAW_CONFIG
#             ), **(box_config or {})}

#         if include_text:
#             mob_text = Text(
#                 text=self.text,
#                 **self.label_config,
#             ).add_background_rectangle(
#                 **self.box_config,
#             )

#             # fix background rectangle
#             mob_box = Rectangle(
#                 width=mob_text.background_rectangle.width,
#                 height=mob_text.background_rectangle.height,
#             ).set_style(
#                 **mob_text.background_rectangle.get_style(simple=True),
#             ).move_to(mob_text.background_rectangle)
#             mob_text.remove(mob_text.background_rectangle)

#             self.mob_text = mob_text
#             self.mob_box = mob_box
#             self.add(self.mob_box, self.mob_text)
#         else:
#             mob_box = Rectangle(
#                 **self.box_config,
#             )
#             self.mob_box = mob_box
#             self.add(self.mob_box)

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
        """Can be used as restore animation.
        """
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
    ) -> dict:
        """Create pcells based on direction specified.
        """
        pcells = {}
        directions = [direction] if direction else DIRECTION_SERIES
        box_config = {**PCELL_BOX_CONFIG, **box_config}

        for direction in directions:
            idx = DIRECTION_SERIES.index(direction)
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
        
        if arranged:
            mobs = VGroup(pc for pcs in pcells.values() for pc in pcs)
            mobs.arrange(
                direction=IN,
                buff=self.sf_screen * PCELL_DEPTH_BUFF_RATIO,
            ).move_to(self.dot)

        return pcells

    def show_pcells(
        self,
        direction: str | None = None,   # all or specific direction
        sf_pcell: float = 1.0,
        box_config: dict = {},
        arranged: bool = False,     # arrange in IN direction or not
        **aargs,
    ) -> Animation:
        """Show pcells based on direction specified.
           Append to dict member named pcells.
        """
        pcells = self.create_pcells(
            direction=direction,
            sf_pcell=sf_pcell,
            box_config=box_config,
            arranged=arranged,
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

    def show_pcells_text(
        self,
        text_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Show text in all pcells currently available.
        """
        assert hasattr(self, 'pcells'), 'pcells not exist yet'
        pcells = VGroup(pc for pcs in self.pcells.values() for pc in pcs)
        text_config = {**TEXT_CONFIG, **text_config}

        return AnimationGroup(
            *(pc.show_text(
                text_config=text_config,
                **aargs,
            ) for pc in pcells),
            **gargs,
        )

    def hide_pcells_text(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Hide text in all pcells currently available.
        """
        assert hasattr(self, 'pcells'), 'pcells not exist yet'
        pcells = VGroup(pc for pcs in self.pcells.values() for pc in pcs)

        return AnimationGroup(
            *(pc.hide_text(
                **aargs,
            ) for pc in pcells),
            **gargs,
        )

    def hide_pcells(
        self,
        **aargs,
    ) -> Animation:
        """Hide all pcells currently available.
        """
        assert hasattr(self, 'pcells'), 'pcells not exist yet'
        pcells = VGroup(pc for pcs in self.pcells.values() for pc in pcs)

        self.remove(*pcells)
        del self.pcells
        return Unwrite(pcells, **aargs)

    def arrange_pcells(
        self,
        **aargs,
    ) -> Animation:
        """
        Stack existing pcells along the depth axis.
        """
        assert hasattr(self, 'pcells'), 'pcells not exist yet'
        pcells = VGroup(pc for pcs in self.pcells.values() for pc in pcs)

        pcells.generate_target()

        pcells.target.arrange(
            direction=IN,
            buff=self.sf_screen * PCELL_DEPTH_BUFF_RATIO,
        ).move_to(self.dot)
        return MoveToTarget(
            pcells,
            **aargs,
        )

    # ---------------- arrows related -------------------
    def create_arrows(
        self,
        direction: str | None = None,       # all or specific direction
        arrow_config: dict = {},
    ) -> dict:
        """Create arrows based on direction specified.
        """
        arrows = {}
        directions = [direction] if direction else DIRECTION_SERIES
        arrow_config = {**ARROW_CONFIG, **arrow_config}

        for direction in directions:
            idx = DIRECTION_SERIES.index(direction)
            offset = self.offsets[idx] * DIRECTION_MAP[direction]
            arrow = Arrow(
                start=self.dot.get_center(),
                end=self.dot.get_center() + offset * self.sf_screen,
                color=COLOR_MAP[direction],
                **arrow_config,
            )

            # store useful info in arrow
            arrow.offset_rela = '{:.2f}'.format(
                self.offsets[idx]
            )
            arrow.offset_abs = '{:d}'.format(
                int(self.offsets[idx] * self.sf_nominal)
            )
            arrow.color = COLOR_MAP[direction]

            arrows[direction] = arrow
        
        return arrows

    def show_arrows(
        self,
        direction: str | None = None,   # all or specific direction
        arrow_config: dict = {},
        **aargs,
    ) -> Animation:
        """Show arrows based on direction specified.
        """
        arrows = self.create_arrows(
            direction=direction,
            arrow_config=arrow_config,
        )
        if hasattr(self, 'arrows'):
            self.arrows.update(arrows)
        else:
            self.arrows = arrows
        
        mobs = VGroup(arrow for arrow in arrows.values())

        self.add(*mobs)

        return AnimationGroup(
            *(GrowArrow(
                arrow,
            ) for arrow in mobs),
            **aargs,
        )

    def hide_arrows(
        self,
        **aargs,
    ) -> Animation:
        """Hide all arrows currently available.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        arrows = VGroup(arrow for arrow in self.arrows.values())

        self.remove(*arrows)
        del self.arrows
        return Unwrite(arrows, **aargs)

    def create_arrows_offset_rela(
        self,
        text_config: dict = {},
    ) -> VGroup:
        """Create relative offsets next to current arrows.
        """
        text_config = {**ARROW_TEXT_CONFIG, **text_config}

        mobs = VGroup(
            Text(
                text=arrow.offset_rela,
                **{'color': arrow.color, **text_config},    # use member color by default
            ).next_to(
                arrow,
                TEXT_DIRECTION_MAP[direction],
                buff= TEXT_DIRECTION_BUFF,
            ) for direction, arrow in self.arrows.items()
        )
        return mobs

    def show_arrows_offset_rela(
        self,
        text_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Show relative offset in all arrows currently avaiable.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        texts = self.create_arrows_offset_rela(
            text_config=text_config,
        )

        for arrow, text in zip(self.arrows.values(), texts):
            arrow.mob_rela = text
            self.add(arrow.mob_rela)    # NOTE: child of anchor point instead of arrow
        
        return AnimationGroup(
            *(Write(text, **aargs) for text in texts),
            **gargs,
        )
    
    def hide_arrows_offset_rela(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Hide relative offset in all arrows currently avaiable.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        texts = VGroup(arrow.mob_rela for arrow in self.arrows.values())
        for arrow in self.arrows.values():
            self.remove(arrow.mob_rela)
            del arrow.mob_rela

        return AnimationGroup(
            *(Unwrite(text, **aargs) for text in texts),
            **gargs,
        )
    
    def create_arrows_offset_abs(
        self,
        text_config: dict = {},
    ) -> VGroup:
        """Create absolute offsets next to current arrows.
        """
        text_config = {**ARROW_TEXT_CONFIG, **text_config}

        mobs = VGroup(
            Text(
                text=arrow.offset_abs,
                **{'color': arrow.color, **text_config},    # use member color by default
            ).next_to(
                arrow,
                TEXT_DIRECTION_MAP[direction],
                buff=TEXT_DIRECTION_BUFF,
            ) for direction, arrow in self.arrows.items()
        )
        return mobs
    
    def show_arrows_offset_abs(
        self,
        text_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Show absolute offset in all arrows currently avaiable.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        texts = self.create_arrows_offset_abs(
            text_config=text_config,
        )

        for arrow, text in zip(self.arrows.values(), texts):
            arrow.mob_abs = text
            self.add(arrow.mob_abs) # child of ap instead of arrow
        
        return AnimationGroup(
            *(Write(text, **aargs) for text in texts),
            **gargs,
        )

    def hide_arrows_offset_abs(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Hide absolute offset in all arrows currently avaiable.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        texts = VGroup(arrow.mob_abs for arrow in self.arrows.values())
        for arrow in self.arrows.values():
            self.remove(arrow.mob_abs) # remove mob from children
            del arrow.mob_abs
        return AnimationGroup(
            *(Unwrite(text, **aargs) for text in texts),
            **gargs,
        )

    def create_arrows_divide(
        self,
        text_config: dict = {},
    ) -> VGroup:
        """Create '/sf_nominal' next to mob_abs for current arrows.
        """
        text_config = {**ARROW_TEXT_CONFIG, **text_config}

        mobs = VGroup(
            Text(
                text= '/' + '{:d}'.format(self.sf_nominal),
                **{'color': ARROW_DIVIDE_COLOR, **text_config}
            ).next_to(
                arrow.mob_abs,
                RIGHT,
                buff=ARROW_DIVIDE_BUFF,
            # ).align_to(
            #     arrow.mob_abs,
            #     DOWN,
            ) for arrow in self.arrows.values()
        )
        return mobs

    def show_arrows_divide(
        self,
        text_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Show '/sf_nominal' next to mob_abs for current arrows.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        divs = self.create_arrows_divide(
            text_config=text_config,
        )

        for arrow, div in zip(self.arrows.values(), divs):
            arrow.mob_abs.add(div)
        
        return AnimationGroup(
            *(Write(div, **aargs) for div in divs),
            **gargs,
        )
    
    def arrows_abs_to_rela(
        self,
        text_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """Convert mob_abs in each arrow into mob_rela.
        """
        assert hasattr(self, 'arrows'), 'arrows not exist yet'
        mobs_rela = self.create_arrows_offset_rela(
            text_config=text_config,
        )

        anims = []
        for arrow, mob_rela in zip(self.arrows.values(), mobs_rela):
            arrow.mob_rela = mob_rela
            anims.append(ReplacementTransform(
                arrow.mob_abs,
                mob_rela,
                **aargs,
            ))
            self.remove(arrow.mob_abs)
            del arrow.mob_abs
        return AnimationGroup(
            *anims,
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

    # ---------------- computations related -------------------
    def create_computation_abs_to_position(
        self,
        buff=1.0,
        text_config: dict = {},
    ) -> Comment:
        text_config = {**COMPUTATION_TEXT_CONFIG, **text_config}

        comments = VGroup()
        for idx, direction in enumerate(DIRECTION_SERIES):
            formatter = (
                f'{self.index[1-idx%2]+0.5:>4.1f} * {self.sf_nominal:>2d} '
                f'{self.dir_to_sign[direction]} {{:>3d}} '
                f'= {{:>3d}}'
            )
            values = [
                int(self.offsets[idx].item() * self.sf_nominal),
                int(self.xyxy[idx].item() * self.sf_nominal),
            ]
            comment = Comment(
                formatter=formatter,
                values=values,
                colors=[COLOR_MAP[direction], WHITE],
                **text_config,
            )
            comments.add(comment)
        comments.arrange(
            DOWN,
            buff=buff,
            aligned_edge=RIGHT,     # FIXME: or LFET?
        ).center()      # always centered at creation
        return comments

    def create_computation_rela_to_position(
        self,
        buff=1.0,
        text_config: dict = {},
    ) -> Comment:
        text_config = {**COMPUTATION_TEXT_CONFIG, **text_config}

        comments = VGroup()
        for idx, direction in enumerate(DIRECTION_SERIES):
            formatter = (
                f'{self.index[1-idx%2]+0.5:>4.1f} * {self.sf_nominal:>2d} '
                f'{self.dir_to_sign[direction]} {{:>5.2f}} * {self.sf_nominal:>2d} '
                f'= {{:>3d}}'
            )
            values = [
                float(self.offsets[idx].item()),
                int(self.xyxy[idx].item() * self.sf_nominal),
            ]
            comment = Comment(
                formatter=formatter,
                values=values,
                colors=[COLOR_MAP[direction], WHITE],
                **text_config,
            )
            comments.add(comment)
        comments.arrange(
            DOWN,
            buff=buff,
            aligned_edge=RIGHT,     # FIXME: or LFET?
        ).center()      # always centered at creation
        return comments

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
            f'<span foreground="{COLOR_MAP[d]}">{{:.2f}}</span>'
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
                f'<span foreground="{COLOR_MAP[direction]}">{{:.2f}}</span>)'
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

    # ---------------- pbars related -------------------
    def create_pbars(
        self,
        random: bool = False,       # use random prob instead of internal
        target: int | None = None,  # target class index
        pbar_config: dict = {},
    ) -> VGroup:
        """Create pbars.
        """
        n_probs = len(self.prob)
        pbar_space = self.sf_screen * PBAR_SPACE_RATIO
        pbar_gap = pbar_space * PBAR_GAP_RATIO
        pbar_width = pbar_space * (1-(n_probs-1)*PBAR_GAP_RATIO) / n_probs
        cfg = {**PBAR_CONFIG, **pbar_config}

        # prob = self.prob if not random else np.random.random(size=n_probs)
        if not random:
            prob = self.prob
        else:
            if target is not None:
                prob = [uniform(*PBAR_NEG_RANGE) for _ in range(n_probs)]
                prob[target] = uniform(*PBAR_POS_RANGE)
            else:
                prob = np.random.random(size=n_probs)

        pbars = VGroup(
            Rectangle(
                width=pbar_width,
                height=pbar_space*p,
                fill_color=PBAR_COLORS[i],
                **cfg,
            ) for i, p in enumerate(prob)
        )
        # NOTE: arrange then move
        pbars.arrange(
            RIGHT,
            buff=pbar_gap,
        ).move_to(self.dot)
        return pbars

    def show_pbars(
        self,
        random: bool = False,
        target: int | None = None,  # target class index
        pbar_config: dict = {},
        **aargs,
    ) -> Animation:
        """Show pbars.
        """
        pbars_end = self.create_pbars(
            random=random,
            target=target,
            pbar_config=pbar_config,
        )
        pbars_start = pbars_end.copy()
        for bar in pbars_start:
            bar.stretch_to_fit_height(0)
        self.pbars = pbars_start
        self.add(self.pbars)
        return AnimationGroup(
            *(Transform(p0, p1)
              for p0, p1 in zip(self.pbars, pbars_end)),
            **aargs,
        )

    def sync_pbars(
        self,
        random: bool = False,
        pbar_config: dict = {},
        **aargs,
    ) -> Animation:
        """Sync pbars into current prob or random.
        """
        pbars_end = self.create_pbars(
            random=random,
            pbar_config=pbar_config,
        )
        return AnimationGroup(
            *(Transform(p0, p1)
            for p0, p1 in zip(self.pbars, pbars_end)),
            **aargs,
        )

    def hide_pbars(
        self,
        **aargs,
    ) -> Animation:
        """Hide pbars.
        """
        pbars_start = self.pbars
        pbars_end = self.pbars.copy()
        for bar in pbars_end:
            bar.stretch_to_fit_height(0)
        self.remove(self.pbars)
        del self.pbars
        return AnimationGroup(
            *(Transform(p0, p1)
            for p0, p1 in zip(pbars_start, pbars_end)),
            **aargs,
        )

    # ---------------- labels related -------------------
    def create_labels(
        self,
        include_text: bool = True,      # include conf text or not
        label_txt_config: dict = {},    # font size 9 by default
        label_bg_config: dict = {},
    ) -> VGroup:
        """Create multiple labels, not positioned.
        """
        labels = VGroup(
            YLabel(
                include_text=include_text,
                text='{:.2f}'.format(prob),
                label_txt_config={
                    **LABEL_TXT_CONFIG,
                    **label_txt_config,
                },
                label_bg_config={
                    **LABEL_BG_CONFIG,
                    'color': color,
                    **label_bg_config,
                },
            ) for prob, color in zip(self.prob, LABEL_COLORS)
        ).arrange(RIGHT, buff=0.0)
        return labels

    def show_labels(
        self,
        include_text: bool = True,      # show conf text or not
        label_txt_config: dict = {},    # font size 9 by default
        label_bg_config: dict = {},
        **aargs,
    ) -> Animation:
        """Show multiple labels, aligned to box.
        """
        labels = self.create_labels(
            include_text=include_text,
            label_txt_config=label_txt_config,
            label_bg_config=label_bg_config,
        ).move_to(
            self.rect.get_corner(UL),
            aligned_edge=DL,
        )
        self.labels = labels
        self.add(self.labels)

        return Write(
            self.labels,
            **aargs,
        )

    def show_rect_labels(
        self,
        rect_config: dict = {},         # box config
        include_text: bool = True,      # show conf score or not
        label_txt_config: dict = {},    # font size 9 by default
        label_bg_config: dict = {},
        **aargs,
    ) -> Animation:
        """Show box and multiple labels together.
        """
        anims = AnimationGroup(
            self.to_rect(
                rect_config=rect_config,
            ),
            self.show_labels(
                include_text=include_text,
                label_txt_config=label_txt_config,
                label_bg_config=label_bg_config,
            ),
            **aargs,
        )
        return anims
    
    # ---------------- postprocess related -------------------
    def apply_max_select(
        self,
        max_idx: int = 0,       # max index to keep
        aargs: dict = {},       # animation args
    ) -> Animation:
        """Select max conf label (class info implied).
        """
        max_label = self.labels[max_idx]

        # self.cls = max_idx              # remember max class index
        # self.conf = self.prob[max_idx]  # remember max class conf

        max_target = max_label.copy().move_to(
            # self.labels[0],
            self.rect.get_corner(UL),
            aligned_edge=DL,
        )
        max_target.label_bg.set_stroke(
            color=max_target.label_bg.fill_color,
            # opacity=max_target.label_bg.fill_opacity,
            opacity=0.5,            # FIXME, use reference instead of hardcode
            width=self.mob.stroke_width,
        )
        anims = [Transform(max_label, max_target)]
        # labels_to_remove = []
        for i in range(len(self.labels)):
            if i != max_idx:
                anims.append(FadeOut(self.labels[i]))
                # labels_to_remove.append(self.labels[i])

        # self.rect.set_stroke(color=PBAR_COLORS[max_idx])
        anims.append(self.mob.animate.set_stroke(color=LABEL_COLORS[max_idx]))

        self.label = max_label
        self.add(self.label)
        self.labels.remove(*self.labels)
        del self.labels

        return AnimationGroup(*anims, **aargs)

    # ---------------- general related -------------------
    def use_color(
        self,
        color: ManimColor = PURE_YELLOW,
        font_color: ManimColor = None,
    ) -> Self:
        """Set color of label and box helper.
        """
        self.label.label_bg.set_color(color=color)
        self.mob.set_stroke(color=color)
        if font_color is not None:
            self.label.label_txt.set_color(color=font_color)
        return self

    def use_fade(
        self,
        darkness: float = 0.5,
    ) -> Self:
        """Fade label and box helper.
        """
        self.label.label_bg.fade(darkness=darkness)
        self.label.label_bg.set_stroke(opacity=0.0)
        self.label.label_txt.fade(darkness=darkness)
        self.mob.fade(darkness=darkness)
        return self
    
    def use_opacity(
        self,
        opacity: float = 1.0,
    ) -> Self:
        """Set opacity of label and box helper.
        """
        self.label.label_bg.set_stroke(opacity=opacity)
        self.label.label_bg.set_fill(opacity=opacity)
        self.mob.set_stroke(opacity=opacity)
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
    
    # ---------------- coords related -------------------
    def show_coords(
        self,
        position: np.ndarray,       # position to show coords
        origin: np.ndarray,         # reference origin point
        v1: float,                  # value for first path
        v2: float,                  # value for second path
        num_decimal_places: int = 0,# number of decimal places
        reversed=False,             # reverse path points or not
        path_config: dict = {},     # path config
        text_config: dict = {},     # text config
        **aargs,                    # animation args
    ) -> Animation:
        """Show coords from specific point to reference origin.
        """
        if np.array_equal(position, ORIGIN):
            point = self.dot.get_center()
        else:
            point = self.rect.get_corner(position)
        point_x, point_y, _ = point
        origin_x, origin_y, _ = origin
        path_config = {**COORDS_PATH_CONFIG, **path_config}
        text_config = {**COORDS_TEXT_CONFIG, **text_config}

        # init two paths
        path1 = VMobject().set_points_as_corners([
            point,
            np.array([point_x, origin_y, 0]),
            origin,
        ]).set_stroke(**path_config)
        path2 = VMobject().set_points_as_corners([
            point,
            np.array([origin_x, point_y, 0]),
            origin,
        ]).set_stroke(**path_config)

        if reversed:
            path1.reverse_direction()
            path2.reverse_direction()

        # init two texts
        text1 = Text(
            text=f'{{:.{num_decimal_places}f}}'.format(float(v1)),
            **text_config,
        ).next_to(
            path1,
            UP,
            buff=COORDS_TEXT_BUFF,
        ).align_to(
            path1,
            RIGHT,
        )
        text2 = Text(
            text=f'{{:.{num_decimal_places}f}}'.format(float(v2)),
            **text_config,
        ).next_to(
            path2,
            LEFT,
            buff=COORDS_TEXT_BUFF,
        ).align_to(
            path2,
            DOWN,
        )

        # coord texts can be accumulated
        if hasattr(self, 'coords'):
            self.coords.add(text1, text2)
        else:
            self.coords = VGroup(text1, text2)
            self.add(self.coords)       # make coords child of anchor point

        return AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(path1, time_width=3.0),
                Write(text1),
            ),
            AnimationGroup(
                ShowPassingFlash(path2, time_width=3.0),
                Write(text2),
            ),
            **aargs,
        )
    
    def hide_coords(
        self,
        **aargs,
    ) -> Animation:
        """Hide all existing coord texts.
        """
        assert hasattr(self, 'coords'), 'coords not exist yet'

        coords = self.coords
        del self.coords
        return AnimationGroup(
            *(Unwrite(coord) for coord in coords),
            **aargs,
        )

    # ---------------- utils related -------------------
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

class Demo(Scene):
    def construct(self):
        # self.set_camera_orientation(
        #     phi=60*DEGREES,
        #     theta=-75*DEGREES,
        # )

        distrib = np.random.rand(8, 8)
        distrib /= distrib.sum(axis=1, keepdims=True)
        ap = AnchorPoint(
            point=ORIGIN,
            distrib=distrib,
            offsets=(1.3,2.8,3.3,2.5),
            xyxy=(10,20,30,40),
            prob=(0.1,0.5,0.9),
            index=(0,1),
            shape=(8,8),
            sf_nominal=32,
            sf_screen=0.5,
            dot_config={},
            rect_config={},
        )
        self.play(Create(ap, run_time=0.3))
        self.wait()

        self.play(ap.to_rect())
        self.wait()

        self.play(ap.show_pbars())
        self.wait()

        self.play(ap.hide_pbars())
        self.wait()

        # self.play(ap.animate.scale(2.0))
        # self.wait()

        # self.play(ap.show_pcells(
        #     arranged=False,
        # ))
        # self.wait(0.5)

        # self.play(ap.show_arrows())
        # self.wait()

        # self.play(ap.show_arrows_offset_abs())
        # self.wait()

        # self.play(ap.show_arrows_divide())
        # self.wait()

        # # self.play(ap.hide_arrows_offset_abs())
        # # self.wait()

        # self.play(ap.arrows_abs_to_rela())
        # self.wait()

        # self.play(ap.hide_arrows_offset_rela())
        # self.wait(0.5)

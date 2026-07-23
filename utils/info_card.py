from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.aligned_text import AlignedText
from utils.loop import Loop

UNKNOWN = '?'

# arrange constants
CARD_EDGE_BUFF = 0.3
CARD_VGAP = 0.1
CARD_FOCUS_Y = 0.0
CARD_FADE_VALUE = 0.8
CARD_HIDE_Y = config['frame_height']/2 + 2
CARD_EXIT_X = -config['frame_width']/2 - 2

# default configs
BUFF_HEIGHT_RATIO = 0.8         # padding height / colon height

DEFAULT_HEAD_CONFIG = {
    'color': WHITE,
    'font': 'JetBrains Mono',
    'font_size': 12,
}
DEFAULT_LINE_CONFIG = {
    'color': GRAY,
    'font': 'JetBrains Mono',
    'font_size': 12,
}
DEFAULT_FRAME_CONFIG = {
    'fill_color': GRAY,
    'fill_opacity': 1.0,
    'stroke_color': WHITE,
    'stroke_width': 2,
    'stroke_opacity': 0.0,
}

class InfoCard(VMobject):
    def __init__(
        self,
        head: str,
        params: dict | None = None,
        summary: str | None = None,
        head_config: dict = {},
        frame_config: dict = {},
        common_config: dict = {},
    ):
        super().__init__()

        self.head = head
        self.params = {} if params is None else params
        self.summary = '' if summary is None else summary

        # config members
        self.head_config = {**DEFAULT_HEAD_CONFIG, **head_config}
        self.line_config = {**DEFAULT_LINE_CONFIG, **common_config}
        self.frame_config = {**DEFAULT_FRAME_CONFIG, **frame_config}    # hight infered

        # mob members
        self.head_mob = AlignedText(self.head, **self.head_config).set_z_index(999)
        self.frame_mob = Rectangle(
            width=self.head_mob.width,
            height=self.line_height + self.buff_height*2,
            **self.frame_config,
        )
        self.attach_to_frame_index(self.head_mob, 0)

        self.add(self.frame_mob, self.head_mob)
        self.center()
    
    def expand_params(
        self,
        params: dict | None = None,
        **aargs,
    ) -> Animation:
        """Introduce name_objs, value_objs, line_mobs.
           name_objs, value_objs, param_idxs for reference.
        """
        self.params = params or self.params

        name_objs = {}
        value_objs = {}
        param_idxs = {}

        # create line mobs
        text_config = {**self.line_config, 'font_size': self.head_mob.get_font_size()}
        for idx, (name, value) in enumerate(self.params.items()):
            param_idxs[name] = idx + 1

            name_mob = AlignedText(str(name)+':', **text_config)

            self.attach_to_frame_index(name_mob, param_idxs[name])

            value_mob = AlignedText(str(value), **text_config)
            self.attach_to_frame_index(value_mob, param_idxs[name])
            value_mob.shift(RIGHT*(name_mob.get_width()-value_mob.colon_width()))

            name_objs[name] = name_mob
            value_objs[name] = value_mob

        self.name_objs = name_objs
        self.value_objs = value_objs
        self.param_idxs = param_idxs

        self.line_mobs = VGroup(
            VGroup(self.name_objs[name], self.value_objs[name])
            for name in self.params
        )

        target_width = max(self.line_mobs.width, self.head_width)
        target_height = (1+len(self.params))*(self.buff_height+self.line_height) + self.buff_height

        rect1 = self.frame_mob.copy().stretch_to_fit_width(target_width)
        rect1.align_to(self.frame_mob, LEFT)
        rect1.set_fill(opacity=0.0).set_stroke(
            color=rect1.fill_color,
            opacity=1.0,
        )
        rect2 = rect1.copy().stretch_to_fit_height(target_height)

        head_mob_new = self.head_mob.copy()
        self.attach_to_frame_index(
            head_mob_new, 0, rect2,
        )
        lines_offset = self.line_mobs[0][0].attach_offset(
            rect2.get_corner(UL) + (2*self.buff_height+1.5*self.line_height)*DOWN
        )
        self.line_mobs.shift(lines_offset)

        return Succession(
            Transform(self.frame_mob, rect1),
            AnimationGroup(
                Transform(self.frame_mob, rect2),
                Transform(self.head_mob, head_mob_new),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(Create(line, fixed=True) for line in self.line_mobs),
                lag_ratio=0.3,
            ),
            **aargs,
        )
    
    def update_params(
        self,
        params: dict,
        **aargs,
    ) -> Animation:
        anims = []

        text_config = {**self.line_config, 'font_size': self.head_mob.get_font_size()}
        for name, value in params.items():
            value_mob = AlignedText(str(value), **text_config)
            self.attach_to_frame_index(value_mob, self.param_idxs[name])
            value_mob.shift(RIGHT*(self.name_objs[name].get_width()-value_mob.colon_width()))

            value_mob_old = self.value_objs[name]
            self.remove(value_mob_old)
            self.value_objs[name] = value_mob

            anims.append(AnimationGroup(
                Uncreate(value_mob_old),
                Create(value_mob, fixed=True),
                lag_ratio=0.0,
            ))
        
        self.line_mobs = VGroup(
            VGroup(self.name_objs[name], self.value_objs[name])
            for name in self.params
        )

        target_width = max(self.line_mobs.width, self.head_width)

        rect1 = self.frame_mob.copy().stretch_to_fit_width(target_width)
        rect1.align_to(self.frame_mob, LEFT)
        return Succession(
            AnimationGroup(*anims, lag_ratio=0.0),
            Transform(self.frame_mob, rect1),
            **aargs,
        )
    
    def shrink_params(
        self,
        **aargs,
    ) -> Animation:
        """Remove name_objs, value_objs, line_mobs.
        """
        target_width = self.head_mob.width
        target_height = self.line_height + self.buff_height*2
        
        rect1 = self.frame_mob.copy().stretch_to_fit_height(target_height)
        rect2 = rect1.copy().stretch_to_fit_width(target_width)
        rect2.align_to(self.frame_mob, LEFT)
        rect2.set_fill(
            color=rect2.stroke_color,
            opacity=1.0,
        ).set_stroke(
            opacity=0.0,
        )

        head_mob_new = self.head_mob.copy()
        self.attach_to_frame_index(
            head_mob_new, 0, rect2,
        )
        
        ManimBanner
        line_mobs = self.line_mobs
        self.remove(line_mobs)
        del self.line_mobs
        del self.name_objs
        del self.value_objs

        return Succession(
            AnimationGroup(
                *(Uncreate(line) for line in line_mobs),
                lag_ratio=0.3,
            ),
            AnimationGroup(
                Transform(self.frame_mob, rect1),
                Transform(self.head_mob, head_mob_new),
                lag_ratio=0.0,
            ),
            Transform(self.frame_mob, rect2),
            **aargs,
        )
    
    def expand_summary(
        self,
        summary: str | None = None,
        **aargs,
    ) -> Animation:
        """Introduce smob.
        """
        self.summary = summary or self.summary

        smob = AlignedText(self.summary, **self.head_config).set_z_index(999)
        self.attach_to_frame_index(smob, 0)
        smob.shift(RIGHT*(self.head_width-smob.colon_width()))

        target_width = self.head_width + smob.get_width() - smob.colon_width()
        rect1 = self.frame_mob.copy().stretch_to_fit_width(target_width)
        rect1.align_to(self.frame_mob, LEFT)

        self.smob = smob
        return Succession(
            Transform(self.frame_mob, rect1),
            Create(self.smob, fixed=True),
            **aargs,
        )

    def update_summary(
        self,
        summary: str = UNKNOWN,
        **aargs,
    ) -> Animation:
        """Update summary text.
        """
        smob_old = self.smob

        smob = AlignedText(summary, **self.head_config).set_z_index(999)
        self.attach_to_frame_index(smob, 0)
        smob.shift(RIGHT*(self.head_width-smob.colon_width()))

        target_width = self.head_width + smob.get_width() - smob.colon_width()
        rect1 = self.frame_mob.copy().stretch_to_fit_width(target_width)
        rect1.align_to(self.frame_mob, LEFT)

        self.smob = smob
        return Succession(
            Transform(self.frame_mob, rect1),
            AnimationGroup(
                Uncreate(smob_old),
                Create(self.smob, fixed=True),
                lag_ratio=0.0,
            ),
            **aargs,
        )
    
    def shrink_summary(
        self,
        **aargs,
    ) -> Animation:
        """Remove summary and shrink frame.
        """
        smob = self.smob
        del self.smob

        target_width = self.head_width
        rect1 = self.frame_mob.copy().stretch_to_fit_width(target_width)
        rect1.align_to(self.frame_mob, LEFT)

        return Succession(
            Uncreate(smob),
            Transform(self.frame_mob, rect1),
            **aargs,
        )
    
    def suggest_failure(
        self,
        **aargs,
    ) -> Animation:
        return self.frame_mob.animate(
            rate_func=rate_functions.there_and_back,
            **aargs,
        ).set_fill(color=PURE_RED)
    
    def attach_to_frame_index(
        self,
        mob,
        idx: int = 0,   # 0 for head, 1 for 1st line ...
        frame: Rectangle | None = None,
    ):
        """Helper function for positioning text mobs.
        """
        if frame is None:
            frame = self.frame_mob
        ref = frame.get_corner(UL)
        ref += ((idx+1)*self.buff_height + (idx+0.5)*self.line_height) * DOWN
        mob.attach_to_point(ref)
    
    def hide_to_corner(
        self,
        direction: np.ndarray = UP,
    ):
        self.to_edge(LEFT, buff=CARD_EDGE_BUFF)
        # self.set_y(direction[1]*(config['frame_height']/2)+2)
        self.set_y(direction[1]*CARD_HIDE_Y)
        return self
    
    @property
    def head_width(
        self,
    ) -> float:
        return self.head_mob.get_width()
    
    @property
    def line_height(
        self,
    ) -> float:
        return self.head_mob.get_height()
    
    @property
    def buff_height(
        self,
    ) -> float:
        return self.line_height * BUFF_HEIGHT_RATIO

def collect_idx_card(
    cards,
    idx,
) -> tuple:
    card = cards[idx]
    others = VGroup(c for c in cards if c is not card)
    return card, others

def attach_to_ref(
    mobs,
    ref,
    direction: np.ndarray = UP,
    **aargs,
) -> Animation:
    """Attach card(s) to ref card.
    """
    mobs.generate_target()
    if isinstance(mobs, VGroup):
        mobs.target.arrange(
            DOWN,
            buff=CARD_VGAP,
            aligned_edge=LEFT,
        )
    mobs.target.next_to(
        ref,
        direction,
        buff=CARD_VGAP,
        aligned_edge=LEFT,
    )
    return MoveToTarget(mobs, **aargs)

def detach_to_ref(
    mobs,
    direction: np.ndarray = UP,
    **aargs,
) -> Animation:
    """Detach card(s) to ref card.
    """
    if not isinstance(mobs, VGroup):
        mobs = VGroup(mobs)
    return AnimationGroup(
        *(mob.animate.set_y(CARD_HIDE_Y*direction[1])
          for mob in mobs),
        **aargs,
    )
    
class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=60*DEGREES,
            theta=-75*DEGREES,
        )

        card = InfoCard(
            'module',
            params={
                'first': 1,
                'second': 2,
                'third': 3,
            },
        )
        self.add_fixed_in_frame_mobjects(card)

        self.play(card.expand_summary(
            'for test here',
            run_time=1.0,
        ))
        self.wait()

        self.play(card.update_summary(
            'test short',
            run_time=1.0,
        ))
        self.wait()

        self.play(card.shrink_summary(
            run_time=1.0,
        ))
        self.wait()

        # self.play(card.expand_params(
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(card.update_params(
        #     {'first': 'test', 'second': 'again'},
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(card.update_params(
        #     {'first': 'tt', 'second': 5, 'third': 0},
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(card.shrink_params(
        #     run_time=1.0,
        # ))
        # self.wait()
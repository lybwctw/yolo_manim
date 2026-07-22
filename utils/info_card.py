from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.aligned_text import AlignedText
from utils.loop import Loop

UNKNOWN = '???'

# three modes
MINIMAL = 'minimal'
SUMMARY = 'summary'
DETAILED = 'detailed'

# default configs
BUFF_HEIGHT_RATIO = 0.8         # padding height / colon height
BUFF_HEIGHT_RATIO_MINI = 0.4    # padding height / colon height
BUFF_WIDTH_RATIO = 0.0          # padding width / colon height

DEFAULT_HEAD_CONFIG = {
    'color': WHITE,
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
COMMON_LINES_CONFIG = {
    'color': GRAY,
    'font': 'JetBrains Mono',
    'font_size': 12,
}
IGNORE_LINES_CONFIG = {
    'color': DARK_GRAY,
    'font': 'JetBrains Mono',
    'font_size': 12,
}

class InfoCard(VMobject):
    def __init__(
        self,
        head: str,
        params: dict | None = None,
        ignores: list | None = None,
        head_config: dict = {},
        frame_config: dict = {},
        common_config: dict = {},
        ignore_config: dict = {},
    ):
        super().__init__()

        self.mode = MINIMAL

        self.head = head
        self.params = {} if params is None else params
        self.ignores = [] if ignores is None else ignores

        # store config
        self.head_config = {**DEFAULT_HEAD_CONFIG, **head_config}
        self.frame_config = {**DEFAULT_FRAME_CONFIG, **frame_config}
        self.common_config = {**COMMON_LINES_CONFIG, **common_config}   # font_size infered
        self.ignore_config = {**IGNORE_LINES_CONFIG, **ignore_config}   # font_size infered

        # create mobs and helper members
        self.head_mob = AlignedText(self.head, **self.head_config).set_z_index(999)
        self.line_height = self.head_mob.get_height()
        self.buff_height = self.head_mob.get_height() * BUFF_HEIGHT_RATIO
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
        **aargs,
    ) -> Animation:
        """Introduce name_objs, value_objs, line_mobs.
        """
        if not self.params:
            return None

        name_objs = {}
        value_objs = {}

        # create line mobs
        for idx, (name, value) in enumerate(self.params.items()):
            text_config = self.common_config if name not in self.ignores else self.ignore_config
            text_config = {**text_config, 'font_size': self.head_mob.get_font_size()}

            name_mob = AlignedText(str(name)+':', **text_config)

            self.attach_to_frame_index(name_mob, idx+1)

            value_mob = AlignedText(str(value), **text_config)
            self.attach_to_frame_index(value_mob, idx+1)
            value_mob.shift(RIGHT*(name_mob.get_width()-value_mob.colon_width()))

            name_objs[name] = name_mob
            value_objs[name] = value_mob

        self.name_objs = name_objs
        self.value_objs = value_objs

        self.line_mobs = VGroup(
            VGroup(self.name_objs[name], self.value_objs[name])
            for name in self.params
        )

        target_width = max(self.line_mobs.width, self.frame_mob.width)
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
                *(Write(line, fixed=True) for line in self.line_mobs),
                lag_ratio=0.3,
            ),
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
        
        line_mobs = self.line_mobs
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
    
    def update_params(
        self,
        params: dict,
        **aargs,
    ) -> Animation:
        pass
    
    def expand_summary(
        self,
        summary: str = UNKNOWN,
        **aargs,
    ) -> Animation:
        """Expand frame to show summary text.
        """
        smob = AlignedText(summary, **self.head_config).set_z_index(1)
        smob.concat_to_atext(self.head_mob)

        target_width = self.head_mob.get_width() + smob.get_width() + smob.get_height()*BUFF_WIDTH_RATIO*2
        target_rect = self.frame_mob.copy().stretch_to_fit_width(target_width)
        target_rect.align_to(self.frame_mob, LEFT)

        self.smob = smob
        return Succession(
            Transform(self.frame_mob, target_rect),
            Write(self.smob, fixed=True),
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

        target_width = self.head_mob.get_width() + self.head_mob.get_height()*BUFF_WIDTH_RATIO*2
        target_rect = self.frame_mob.copy().stretch_to_fit_width(target_width)
        target_rect.align_to(self.frame_mob, LEFT)

        return Succession(
            Unwrite(smob),
            Transform(self.frame_mob, target_rect),
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

        smob = AlignedText(summary, **self.head_config).set_z_index(1)
        smob.concat_to_atext(self.head_mob)

        target_width = self.head_mob.get_width() + smob.get_width() + smob.get_height()*BUFF_WIDTH_RATIO*2
        target_rect = self.frame_mob.copy().stretch_to_fit_width(target_width)
        target_rect.align_to(self.frame_mob, LEFT)

        self.smob = smob

        return Succession(
            Transform(
                self.frame_mob,
                target_rect,
            ),
            AnimationGroup(
                Unwrite(smob_old),
                Write(self.smob, fixed=True),
                lag_ratio=0.0,
            ),
            **aargs,
        )
    
    # def update_values(
    #     self,
    #     values: dict,       # kv pairs
    #     **aargs,
    # ) -> Animation:
    #     nmob = self.name_objs[name]
    #     vmob_old = self.value_objs[name]

    #     text_config = self.common_config if name not in self.ignores else self.ignore_config
    #     text_config = {**text_config, 'font_size': self.head_mob.mob.font_size}
    #     vmob_new = AlignedText(str(value), **text_config)
    #     vmob_new.concat_to_atext(nmob, closer=True)

    #     # update data and mob
    #     self.params[name] = value
    #     self.value_objs[name] = vmob_new
        
    #     return AnimationGroup(
    #         Unwrite(vmob_old),
    #         Write(vmob_new, fixed=True),
    #         lag_ratio=0.0,
    #         **aargs,
    #     )
    
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
    
class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=60*DEGREES,
            theta=-75*DEGREES,
        )

        card = InfoCard(
            'test',
            params={
                'first': 1,
                'second': 2,
                'third': 3,
            },
        )
        self.add_fixed_in_frame_mobjects(card)

        # self.play(Write(card, fixed=True))
        # self.wait()

        self.play(card.expand_params(
            run_time=1.0,
        ))
        self.wait()

        self.play(card.shrink_params(
            run_time=1.0,
        ))
        self.wait()
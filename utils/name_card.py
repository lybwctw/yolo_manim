from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.loop import Loop

DEFAULT_HEAD_CONFIG = {
    'color': WHITE,
    'font': 'JetBrains Mono',
    'font_size': 12,
}
COMMON_LINES_CONFIG = {
    'color': GRAY,
    'font': 'JetBrains Mono',
    'font_size': 12,
    'line_spacing': 1.0,
}
IGNORE_LINES_CONFIG = {
    'color': DARK_GRAY,
    'font': 'JetBrains Mono',
    'font_size': 12,
    'line_spacing': 1.0,
}
DEFAULT_SECTION_BUFF = 0.2
DEFAULT_VALUE_BUFF = 0.15

class NameCard(VMobject):
    def __init__(
        self,
        name: str,
        params: dict,
        levels: dict = {},
        head_config: dict = {},
        common_config: dict = {},
        ignore_config: dict = {},
    ):
        super().__init__()
        self.name = name
        self.params = params
        self.levels = levels

        # store config
        self.head_config = {**DEFAULT_HEAD_CONFIG, **head_config}
        self.common_config = {**COMMON_LINES_CONFIG, **common_config}
        self.ignore_config = {**IGNORE_LINES_CONFIG, **ignore_config}

        # create head mob
        self.head_mob = self.create_head_mob()

        # create common lines
        self.mobs_common, self.anchors_common = self.create_pk_mobs(level=0)
        self.mobs_common.next_to(
            self.head_mob,
            DOWN,
            buff=DEFAULT_SECTION_BUFF,
        ).align_to(
            self.head_mob,
            LEFT,
        )

        # create ignore lines
        self.mobs_ignore, self.anchors_ignore = self.create_pk_mobs(level=1)
        self.mobs_ignore.next_to(
            self.mobs_common,
            DOWN,
            buff=DEFAULT_SECTION_BUFF,
        ).align_to(
            self.mobs_common,
            LEFT,
        )

        # create value mob
        self.mobs_value, self.objs_value = self.create_pv_mobs()

        self.add(
            self.head_mob,
            self.mobs_common,
            self.mobs_ignore,
            self.mobs_value,
        )
        self.center()
    
    def create_head_mob(
        self,
    ) -> VMobject:
        """Depends on nothing, starting point.
        """
        return Text(
            self.name,
            **self.head_config,
        )
    
    def create_pk_mobs(
        self,
        level: int = 0,
    ) -> tuple:
        """create lines mob, not positioned.
        """
        lines = []
        anchors = {}
        counter = -1
        for p in self.params:
            if self.levels[p] == level:
                lines.append(p + ':')
                counter = counter + len(p) + 1
                anchors[p] = counter
        text = '\n'.join(lines)
        mobs = Text(
            text,
            **self.level_config(level),
        )
        return mobs, anchors
    
    def new_value_mob(
        self,
        key,
        value = None,
    ) -> VMobject:
        level = self.levels[key]
        ref_mobs = self.mobs_common if level==0 else self.mobs_ignore
        ref_anchors = self.anchors_common if level==0 else self.anchors_ignore
        config = self.param_config(key)
        value = value if value is not None else self.params[key]
        mob = Text(
            str(value),
            **config,
        ).next_to(
            ref_mobs[ref_anchors[key]],
            RIGHT,
            buff=DEFAULT_VALUE_BUFF,
        ).align_to(
            ref_mobs[ref_anchors[key]],
            DOWN,
        )
        return mob
    
    def update_value_mob(
        self,
        key,
        value,
        **aargs,
    ) -> Animation:
        self.params[key] = value
        new_mob = self.new_value_mob(key, value)
        return Transform(
            self.value_mob(key),
            new_mob,
            **aargs,
        )
    
    def value_mob(
        self,
        key,
    ) -> VMobject:
        return self.objs_value[key]
    
    def create_pv_mobs(
        self,
    ) -> VMobject:
        mobs = VGroup()
        objs = {}
        params = list(self.params.keys())
        for p in params:
            mob = self.new_value_mob(
                key=p,
                value=self.params[p],
            )
            mobs.add(mob)
            objs[p] = mob

        return mobs, objs
        
    def level_config(
        self,
        level,
    ) -> dict:
        """Collect text config according to level.
        """
        text_config = self.common_config if level==0 else self.ignore_config
        return text_config

    def param_config(
        self,
        key,
    ) -> dict:
        """Collect text config according to param name.
        """
        text_config = self.level_config(self.levels[key])
        return text_config

    
class Demo(Scene):
    def construct(self):
        card = NameCard(
            name='conv2d',
            params={
                'in_channels': 3,
                'out_channels': 4,
                'kernel_size': 3,
                'stride': 1,
                'padding': 0,
                'bias': False,
                'dilation': 1,
                'groups': 1,
                'padding_mode': 'zeros',
            },
            levels={
                'in_channels': 0,
                'out_channels': 0,
                'kernel_size': 0,
                'stride': 0,
                'padding': 0,
                'bias': 0,
                'dilation': 1,
                'groups': 1,
                'padding_mode': 1,
            },
        ).to_edge(LEFT).shift(UP*.5)
        self.play(Create(card))
        self.wait()

        # series = [
        #     card.new_value_mob('in_channels', x)
        #      for x in range(4, 100)
        # ]

        # self.play(Loop(
        #     card.value_mob('in_channels'),
        #     series,
        #     run_time=3.0,
        #     rate_func=rate_functions.ease_in_out_expo,
        # ))
        # self.wait()
        self.play(card.update_value_mob(
            'bias',
            True,
            run_time=0.5,
        ))
        self.wait()
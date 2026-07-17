from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.aligned_text import AlignedText
from utils.loop import Loop

DEFAULT_HEAD_CONFIG = {
    'color': WHITE,
    'font': 'JetBrains Mono',
    'font_size': 12,
}
DEFAULT_FRAME_CONFIG = {
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
        self.head = head
        self.params = params
        self.ignores = ignores

        # store config
        self.head_config = {**DEFAULT_HEAD_CONFIG, **head_config}
        self.frame_config = {**DEFAULT_FRAME_CONFIG, **frame_config}
        self.common_config = {**COMMON_LINES_CONFIG, **common_config}
        self.ignore_config = {**IGNORE_LINES_CONFIG, **ignore_config}

        # create head text and frame
        self.head_mob = self.create_head_mob()
        self.frame_mob = self.create_frame_mob(self.head_mob.)
        self.add(self.frame_mob, self.head_mob)

        # start positioning
        self.center()
    
    def create_head_mob(
        self,
    ) -> VMobject:
        return AlignedText(
            self.name,
            **self.head_config,
        )

    def create_frame_mob(
        self,
    ) -> VMobject:
        pass
    
class Demo(Scene):
    def construct(self):
        card = InfoCard(
            head='Conv2d',
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
            ignores=[
                'dilation',
                'groups',
                'padding_mode',
            ],
        )
        self.play(Write(card))
        self.wait()

        # self.play(card.extend())
        # self.wait()

        # self.play(card.update_value(
        #     name='in_channels',
        #     value=123,
        # ))
        # self.wait()
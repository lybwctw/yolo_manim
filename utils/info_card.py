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

        # create head text and frame
        head_mob = self.create_head_mob().set_z_index(1)
        frame_mob = self.create_frame_mob(head_mob).set_z_index(0)
        head_mob.align_to_corner(
            frame_mob.get_corner(UL),
            buff_w = head_mob.get_height() * BUFF_WIDTH_RATIO,
            buff_h = head_mob.get_height() * BUFF_HEIGHT_RATIO,
        )

        self.head_mob = head_mob
        self.frame_mob = frame_mob
        self.add(self.frame_mob, self.head_mob)

        self.head_mob_updater = lambda m: m.align_to_corner(
                self.frame_mob.get_corner(UL),
                buff_w = self.head_mob.get_height() * BUFF_WIDTH_RATIO,
                buff_h = self.head_mob.get_height() * BUFF_HEIGHT_RATIO,
            )

        # start positioning
        self.center()
    
    def create_head_mob(
        self,
    ) -> VMobject:
        return AlignedText(
            self.head,
            **self.head_config,
        )

    def create_frame_mob(
        self,
        ref: AlignedText,
    ) -> VMobject:
        return Rectangle(
            width=ref.get_width() + ref.get_height()*BUFF_WIDTH_RATIO*2,
            height=ref.get_height() + ref.get_height()*BUFF_HEIGHT_RATIO*2,
            **self.frame_config,
        )
    
    def start_updater(
        self,
    ):
        self.head_mob.add_updater(self.head_mob_updater)
    
    def stop_updater(
        self,
    ):
        self.head_mob.remove_updater(self.head_mob_updater)
    
    def expand_frame_detailed(
        self,
        aligned_edge: np.ndarray = LEFT,
        **aargs,
    ) -> Animation:
        name_objs = {}
        value_objs = {}
        line_objs = {}

        # create new mobs only when params is not empty
        if self.params:
            for idx, (name, value) in enumerate(self.params.items()):
                text_config = self.common_config if name not in self.ignores else self.ignore_config
                text_config = {**text_config, 'font_size': self.head_mob.mob.font_size}

                name_mob = AlignedText(str(name)+':', **text_config)
                prop_height = name_mob.get_height() * (1 + BUFF_HEIGHT_RATIO_MINI * 2)

                name_mob.align_to_corner(
                    self.frame_mob.get_corner(UL),
                    buff_w = name_mob.get_height() * BUFF_WIDTH_RATIO,
                    # buff_h = name_mob.get_height() * (idx + (idx*2+1)*BUFF_HEIGHT_RATIO),
                    buff_h = self.head_height + idx*prop_height + name_mob.get_height()*BUFF_HEIGHT_RATIO_MINI,
                )

                value_mob = AlignedText(str(value), **text_config)
                value_mob.concat_to_atext(name_mob)

                name_objs[name] = name_mob
                value_objs[name] = value_mob
                line_objs[name] = VGroup(name_mob, value_mob)
            
            line_mobs = VGroup(line for line in line_objs.values())

        self.name_objs = name_objs
        self.value_objs = value_objs
        self.line_objs = line_objs

        if self.params:
            self.line_mobs = line_mobs
            # compute target frame width and height
            target_width = self.line_mobs.width + self.line_mobs[0][0].get_height()*BUFF_WIDTH_RATIO*2
            target_height = self.head_height + prop_height * len(self.line_mobs)
            target_height += self.head_mob.get_height()*BUFF_HEIGHT_RATIO - self.line_mobs[0][0].get_height()*BUFF_HEIGHT_RATIO_MINI
        else:
            self.line_mobs = None   # empty line mobs
            target_width = self.frame_mob.width
            target_height = self.frame_mob.height

        rect1 = self.frame_mob.copy().stretch_to_fit_width(target_width)
        rect1.align_to(self.frame_mob, aligned_edge)
        rect1.set_fill(opacity=0.0).set_stroke(opacity=1.0)
        rect2 = rect1.copy().stretch_to_fit_height(target_height)

        return Succession(
            Transform(self.frame_mob, rect1),
            Transform(self.frame_mob, rect2),
            **aargs,
        )
    
    def write_properties_detailed(
        self,
        **aargs,
    ) -> Animation:
        # wait if empty params
        if self.line_mobs is None:
            return Wait(**aargs)

        # positioning lines
        ref = self.line_mobs[0][0]
        offset = ref.offset_to_corner(
            self.frame_mob.get_corner(UL),
            buff_w = ref.get_height() * BUFF_WIDTH_RATIO,
            buff_h = self.head_height + ref.get_height() * BUFF_WIDTH_RATIO
        )
        self.line_mobs.shift(offset)

        self.add(self.line_mobs)
        return Create(self.line_mobs, **aargs)
    
    @property
    def head_height(
        self,
    ) -> float:
        height = self.head_mob.get_height() * (1 + BUFF_HEIGHT_RATIO * 2)
        return height
    
class Demo(Scene):
    def construct(self):
        names_t = [
            'add', 'split', 'concat',
            'Conv2d', 'MaxPool2d', 'Upsample', 'SiLU', 'Sigmoid', 'Sofmax', 'Linear', 'BatchNorm2d',
        ]
        names_u = [
            'Conv', 'BottleNeck', 'C2f', 'SPPF', 'Detect',
        ]

        cards = VGroup()
        for name in names_t:
            card = InfoCard(name, frame_config={'fill_color': ORANGE})
            cards.add(card)
        for name in names_u:
            card = InfoCard(name, frame_config={'fill_color': PURE_BLUE})
            cards.add(card)
        cards.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        cards.move_to(LEFT*10)

        self.play(AnimationGroup(
            *(card.animate.to_edge(LEFT, buff=0.5)
              for card in cards),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()

        # focus on specific card
        focus_card = cards[3]
        other_cards = VGroup(cards[i] for i in range(len(cards)) if i != 3)

        other_cards.save_state()
        self.play(other_cards.animate(
            run_time=1.0,
        ).fade(0.8))

        # self.play(other_cards.animate(
        #     run_time=1.0,
        # ).restore())
        # self.wait()

        self.play(AnimationGroup(
            other_cards.animate.shift(LEFT*2),
            focus_card.animate.set_y(0.0),
            lag_ratio=0.5,
            run_time=1.0,
        ))
        self.wait()

        # self.play(focus_card.expand_frame_detailed(
        #     aligned_edge=LEFT,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(focus_card.write_properties_detailed(
        #     run_time=1.0,
        # ))
        # self.wait()

        # card = InfoCard(
        #     head='Conv2d',
        #     params={
        #         'in_channels': 3,
        #         'out_channels': 4,
        #         'kernel_size': 3,
        #         'stride': 1,
        #         'padding': 0,
        #         'bias': False,
        #         'dilation': 1,
        #         'groups': 1,
        #         'padding_mode': 'zeros',
        #     },
        # ).shift(LEFT*8)
        # self.add(card)

        # self.wait()
        # self.play(card.animate(
        #     run_time=0.5,
        #     # rate_func=rate_functions.ease_out_back,
        # ).center())
        # # self.wait()

        # self.play(card.expand_frame_detailed(
        #     run_time=0.6,
        # ))
        # self.play(card.write_properties_detailed(
        #     run_time=0.5,
        # ))
        # self.wait()
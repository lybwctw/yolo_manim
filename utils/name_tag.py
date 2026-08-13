from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
import numpy as np

DEFAULT_LEADER_CONFIG = {
    'stroke_color': WHITE,
    'stroke_width': 2,
    'stroke_opacity': 1.0,
}
DEFAULT_LABEL_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 12,
    'color': WHITE,
}

class NameTag(VMobject):
    def __init__(
        self,
        ref: np.ndarray = ORIGIN,
        text: str = 'None',
        leader_angle: float = 45 * DEGREES,
        leader_length: str = 0.8,
        leader_buff: str = 0.05,
        label_buff: str = 0.05,
        leader_config: dict = {},
        label_config: dict = {},
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.ref = ref
        self.text = text
        self.leader_angle = leader_angle            # first segment
        self.leader_length = leader_length          # first segment
        self.leader_buff = leader_buff              # first segment
        self.label_buff = label_buff                # label buff to second segment
        self.leader_config = {**DEFAULT_LEADER_CONFIG, **leader_config}
        self.label_config = {**DEFAULT_LABEL_CONFIG, **label_config}

        # init label mob
        mob_label = Text(text, **self.label_config)

        # init leader mob
        leader_direction = np.array([
            np.cos(leader_angle),
            np.sin(leader_angle),
            0,
        ])
        start_point = self.ref + leader_direction*self.leader_buff
        mid_point = start_point + leader_direction*self.leader_length
        end_point = mid_point + RIGHT*(mob_label.width+0.1)
        mob_leader = VMobject(**self.leader_config)
        mob_leader.set_points_as_corners([
            start_point,
            mid_point,
            end_point,
        ])

        # reposition label mob
        mob_label.next_to(
            mid_point,
            DOWN,
            label_buff,
        ).align_to(
            mid_point,
            LEFT,
        ).shift(RIGHT*0.05)

        mob_label.align_to

        self.mob_leader = mob_leader
        self.mob_label = mob_label
        self.add(self.mob_leader, self.mob_label)

    def create(
        self,
        **aargs,
    ) -> AnimationGroup:
        return Succession(
            Write(self.mob_leader),
            Write(self.mob_label),
            **aargs,
            _on_finish=lambda s: s.add(self),
        )

    def uncreate(
        self,
        **aargs,
    ) -> AnimationGroup:
        return Succession(
            Unwrite(self.mob_label),
            Unwrite(self.mob_leader),
            **aargs,
            _on_finish=lambda s: s.remove(self),
        )

class Demo(Scene):
    def construct(self):
        rect = Rectangle()

        tag = NameTag(
            ref=rect.get_corner(UR),
            text="weight",
            leader_angle=45*DEGREES,
        )

        self.play(Write(rect))
        self.wait()

        self.play(tag.create(run_time=1.0))
        self.wait()

        self.play(tag.uncreate(run_time=1.0))
        self.wait()
from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.constants_3d import *

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

# FIXME: ugly hash on np.array
# leader direction to angle
MAP_DIR_2_ANGLE = {
    tuple(UR): 45*DEGREES,
    tuple(DR): -45*DEGREES,
    tuple(UL): 135*DEGREES,
    tuple(DL): -135*DEGREES,
}

# leader direction to label next direction
MAP_DIR_2_LABEL_NEXT_DIR = {
    tuple(UR): DOWN,
    tuple(DR): UP,
    tuple(UL): DOWN,
    tuple(DL): UP,
}

# leader direction to label align direction
MAP_DIR_2_LABEL_ALIGN_DIR = {
    tuple(UR): LEFT,
    tuple(DR): LEFT,
    tuple(UL): RIGHT,
    tuple(DL): RIGHT,
}

# leader direction to label shift direction
MAP_DIR_2_LABEL_SHIFT_DIR = {
    tuple(UR): RIGHT,
    tuple(DR): RIGHT,
    tuple(UL): LEFT,
    tuple(DL): LEFT,
}

class NameTag(VMobject):
    def __init__(
        self,
        ref: np.ndarray = ORIGIN,
        text: str = 'None',
        leader_direction: np.ndarray = UR,
        leader_length: float = 0.8,
        leader_buff: float = 0.05,
        label_buff: float = 0.05,
        leader_config: dict = {},
        label_config: dict = {},
        fixed_in_3d: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.ref = ref
        self.text = text
        self.leader_direction = leader_direction    # first segment
        self.leader_length = leader_length          # first segment
        self.leader_buff = leader_buff              # first segment
        self.label_buff = label_buff                # label buff to second segment
        self.leader_config = {**DEFAULT_LEADER_CONFIG, **leader_config}
        self.label_config = {**DEFAULT_LABEL_CONFIG, **label_config}
        self.fixed_in_3d = fixed_in_3d

        # init label mob
        mob_label = Text(text, **self.label_config)

        # init leader mob
        leader_angle = MAP_DIR_2_ANGLE[tuple(self.leader_direction)]
        leader_offset = np.array([
            np.cos(leader_angle),
            np.sin(leader_angle),
            0,
        ])
        start_point = self.ref + leader_offset*self.leader_buff
        mid_point = start_point + leader_offset*self.leader_length
        end_point = (
            mid_point
            + MAP_DIR_2_LABEL_SHIFT_DIR[tuple(self.leader_direction)]
            * (mob_label.width+0.1)
        )
        mob_leader = VMobject(**self.leader_config)
        mob_leader.set_points_as_corners([
            start_point,
            mid_point,
            end_point,
        ])

        # reposition label mob
        mob_label.next_to(
            mid_point,
            MAP_DIR_2_LABEL_NEXT_DIR[tuple(self.leader_direction)],
            label_buff,
        ).align_to(
            mid_point,
            MAP_DIR_2_LABEL_ALIGN_DIR[tuple(self.leader_direction)],
        ).shift(
            MAP_DIR_2_LABEL_SHIFT_DIR[tuple(self.leader_direction)] * 0.05,
        )

        self.mob_leader = mob_leader
        self.mob_label = mob_label
        self.add(self.mob_leader, self.mob_label)

    def create(
        self,
        **aargs,
    ) -> AnimationGroup:
        return Succession(
            Write(self.mob_leader, fixed=self.fixed_in_3d),
            Write(self.mob_label, fixed=self.fixed_in_3d),
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

def p2f(
    scene,
    point,
) -> np.ndarray:
    """Helper function for projecting 3D point into 2D frame.
    """
    return scene.camera.project_point(point)

class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        cube = Cube(
            stroke_width=3,
            stroke_color=WHITE,
            stroke_opacity=1.0,
            fill_color=GRAY,
            fill_opacity=0.8,
        )
        self.play(Write(cube))
        self.wait()

        tag1 = NameTag(
            ref=p2f(self, cube.get_corner(DR+IN)),
            text="weight",
            leader_direction=DR,
            fixed_in_3d=True,
        )
        tag2 = NameTag(
            ref=p2f(self, cube.get_corner(DR+OUT)),
            text="bias",
            leader_direction=UR,
            fixed_in_3d=True,
        )

        self.play(AnimationGroup(
            tag1.create(run_time=1.0),
            tag2.create(run_time=1.0),
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait()

        self.play(AnimationGroup(
            tag1.uncreate(run_time=1.0),
            tag2.uncreate(run_time=1.0),
            lag_ratio=0.0,
            run_time=1.0,
        ))
        self.wait()
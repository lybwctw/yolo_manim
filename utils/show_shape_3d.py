from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *

DEFAULT_SHAPE_PATH_CONFIG = {
    'color': GOLD,
    'width': 3,
    'opacity': 1.0,
}

DEFAULT_SHAPE_TEXT_CONFIG = {
    'buff': 0.15,
    'font_size': 15,
    'font': 'JetBrains Mono',
    'color': GOLD,
}

DEFAULT_SHOW_AARGS = {
    'lag_ratio': 0.0,
    'run_time': 1.0,
}

DEFAULT_HIDE_AARGS = {
    'lag_ratio': 0.0,
    'run_time': 1.0,
}

class ShowShape3D(AnimationGroup):
    def __init__(
        self,
        scene,
        mob: MTensorGeneral,
        facing: str = 'left',
        path_config: dict = {},
        text_config: dict = {},
        aargs: dict = {},
    ):
        path_config = {**DEFAULT_SHAPE_PATH_CONFIG, **path_config}
        text_config = {**DEFAULT_SHAPE_TEXT_CONFIG, **text_config}
        text_buff = text_config.pop('buff')
        aargs = {**DEFAULT_SHOW_AARGS, **aargs}

        if isinstance(mob, MTensor_1D):
            s0 = str(mob.shape[0])
            if facing == 'horizontal':
                p0 = Line(
                    start=mob[0].get_corner(UL+OUT),
                    end=mob[-1].get_corner(UR+OUT),
                ).shift(
                    (OUT+UP)*0.01,
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, UP, buff=text_buff*2.0)      # tweak
            elif facing == 'vertical':
                p0 = Line(
                    start=mob[0].get_corner(UR+OUT),
                    end=mob[-1].get_corner(DR+OUT),
                ).shift(
                    (OUT+RIGHT)*0.01,
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, RIGHT, buff=text_buff*2.0)      # tweak
            elif facing == 'horizontal reverse':
                p0 = Line(
                    start=mob[0].get_corner(UR+OUT),
                    end=mob[-1].get_corner(UL+OUT),
                ).shift(
                    (OUT+UP)*0.01,
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, UP, buff=text_buff*2.0)      # tweak
            elif facing == 'vertical reverse':
                p0 = Line(
                    start=mob[0].get_corner(DR+OUT),
                    end=mob[-1].get_corner(UR+OUT),
                ).shift(
                    (OUT+RIGHT)*0.01,
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, RIGHT, buff=text_buff*2.0)      # tweak
            elif facing == 'left':
                p0 = Line(
                    start=mob[0].get_corner(DL+IN),
                    end=mob[-1].get_corner(DR+IN),
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, DOWN, buff=text_buff*2.0)      # tweak
            elif facing == 'right':
                p0 = Line(
                    start=mob[0].get_corner(DL+IN),
                    end=mob[-1].get_corner(DR+IN),
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, DOWN, buff=text_buff*2.0)      # tweak
            elif facing == 'right erect':
                p0 = Line(
                    start=mob[0].get_corner(DR+OUT),
                    end=mob[-1].get_corner(DR+IN),
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, DR, buff=text_buff*1.5)      # tweak
            ps = VGroup(p0)
            ts = VGroup(t0).set_z_index(999)
        elif isinstance(mob, MTensor_2D):
            # Not verified yet; please validate visually later.
            s1, s2 = [str(s) for s in mob.shape]
            if facing == 'left':
                p1 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(DL+OUT),
                ).set_stroke(**path_config)
                p2 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(UR+OUT),
                ).set_stroke(**path_config)
                t1 = Text(
                    text=s1,
                    **text_config,
                ).next_to(p1, LEFT, buff=text_buff)     # tweak
                t2 = Text(
                    text=s2,
                    **text_config,
                ).next_to(p2, UP, buff=text_buff*1.2)     # tweak
            elif facing == 'right':
                p1 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(DL+OUT),
                ).set_stroke(**path_config)
                p2 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(UR+OUT),
                ).set_stroke(**path_config)
                t1 = Text(
                    text=s1,
                    **text_config,
                ).next_to(p1, RIGHT, buff=text_buff)    # tweak
                t2 = Text(
                    text=s2,
                    **text_config,
                ).next_to(p2, UP, buff=text_buff*1.2)     # tweak
            ps = VGroup(p1, p2)
            ts = VGroup(t1, t2).set_z_index(999)
        elif isinstance(mob, MTensor_3D):
            s1, s2, s3 = [str(s) for s in mob.shape]
            if facing == 'left':
                p1 = Line(
                    start=mob.get_corner(DL+OUT),
                    end=mob.get_corner(DL+IN),
                ).set_stroke(**path_config)
                p2 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(DL+OUT),
                ).set_stroke(**path_config)
                p3 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(UR+OUT),
                ).set_stroke(**path_config)
                t1 = Text(
                    text=s1,
                    **text_config,
                ).next_to(p1, LEFT, buff=text_buff)     # tweak
                t2 = Text(
                    text=s2,
                    **text_config,
                ).next_to(p2, LEFT, buff=text_buff*1.2)     # tweak
                t3 = Text(
                    text=s3,
                    **text_config,
                ).next_to(p3, UP, buff=text_buff*1.8)   # tweak
            elif facing == 'right':
                p1 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(UL+IN),
                ).set_stroke(**path_config)
                p2 = Line(
                    start=mob.get_corner(UR+OUT),
                    end=mob.get_corner(DR+OUT),
                ).set_stroke(**path_config)
                p3 = Line(
                    start=mob.get_corner(UL+OUT),
                    end=mob.get_corner(UR+OUT),
                ).set_stroke(**path_config)
                t1 = Text(
                    text=s1,
                    **text_config,
                ).next_to(p1, UP, buff=text_buff*1.0)     # tweak
                t2 = Text(
                    text=s2,
                    **text_config,
                ).next_to(p2, RIGHT, buff=text_buff*2.0)     # tweak
                t3 = Text(
                    text=s3,
                    **text_config,
                ).next_to(p3, UP, buff=text_buff*1.1)   # tweak
            ps = VGroup(p1, p2, p3)
            ts = VGroup(t1, t2, t3).set_z_index(999)
        elif isinstance(mob, MTensor_4D):
            s0, s1, s2, s3 = [str(s) for s in mob.shape]
            if facing == 'left':
                p0 = Line(
                    start=mob[0].get_corner(DL+IN),
                    end=mob[-1].get_corner(DR+IN),
                ).set_stroke(**path_config)
                p1 = Line(
                    start=mob[0].get_corner(DL+OUT),
                    end=mob[0].get_corner(DL+IN),
                ).set_stroke(**path_config)
                p2 = Line(
                    start=mob[0].get_corner(UL+OUT),
                    end=mob[0].get_corner(DL+OUT),
                ).set_stroke(**path_config)
                p3 = Line(
                    start=mob[0].get_corner(UL+OUT),
                    end=mob[0].get_corner(UR+OUT),
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, DOWN, buff=text_buff*2.0)      # tweak
                t1 = Text(
                    text=s1,
                    **text_config,
                ).next_to(p1, LEFT, buff=text_buff)     # tweak
                t2 = Text(
                    text=s2,
                    **text_config,
                ).next_to(p2, LEFT, buff=text_buff*1.2)     # tweak
                t3 = Text(
                    text=s3,
                    **text_config,
                ).next_to(p3, UP, buff=text_buff*1.8)   # tweak
            elif facing == 'right':
                p0 = Line(
                    start=mob[0].get_corner(DL+IN),
                    end=mob[-1].get_corner(DR+IN),
                ).set_stroke(**path_config)
                p1 = Line(
                    start=mob[0].get_corner(UL+OUT),
                    end=mob[0].get_corner(UL+IN),
                ).set_stroke(**path_config)
                p2 = Line(
                    start=mob[-1].get_corner(UR+OUT),
                    end=mob[-1].get_corner(DR+OUT),
                ).set_stroke(**path_config)
                p3 = Line(
                    start=mob[0].get_corner(UL+OUT),
                    end=mob[0].get_corner(UR+OUT),
                ).set_stroke(**path_config)
                t0 = Text(
                    text=s0,
                    **text_config,
                ).next_to(p0, DOWN, buff=text_buff*2.0)      # tweak
                t1 = Text(
                    text=s1,
                    **text_config,
                ).next_to(p1, UP, buff=text_buff*1.0)     # tweak
                t2 = Text(
                    text=s2,
                    **text_config,
                ).next_to(p2, RIGHT, buff=text_buff*1.6)     # tweak
                t3 = Text(
                    text=s3,
                    **text_config,
                ).next_to(p3, UP, buff=text_buff*1.1)   # tweak
            ps = VGroup(p0, p1, p2, p3)
            ts = VGroup(t0, t1, t2, t3).set_z_index(999)

        mob.shape_texts = ts
        # make text always face audience in 3d scene
        scene.camera.add_fixed_orientation_mobjects(*ts)
        
        super().__init__(
            AnimationGroup(
                *(AnimationGroup(
                    ShowPassingFlash(p, time_width=10.0),
                    Write(t),
                ) for p, t in zip(ps, ts)),
                **aargs,
            )
        )

class HideShape3D(AnimationGroup):
    def __init__(
        self,
        mob: MTensorGeneral,
        aargs: dict = {},
    ):
        ts = getattr(mob, "shape_texts", VGroup())
        mob.remove(ts)

        aargs = {**DEFAULT_HIDE_AARGS, **aargs}
        super().__init__(
            AnimationGroup(
                *(Unwrite(t) for t in ts),
                **aargs,
            )
        )
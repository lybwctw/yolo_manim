from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.layers_fake import LayersFake
from utils.ftensor import *

DEFAULT_SHAPE_PATH_CONFIG = {
    'stroke_color': ORANGE,
    'stroke_width': 3,
    'stroke_opacity': 1.0,
}

DEFAULT_SHAPE_TEXT_CONFIG = {
    'font_size': 15,
    'font': 'JetBrains Mono',
    'color': ORANGE,
}

DEFAULT_TEXT_BUFF = 0.2

SHAPE_MAPPING = {
    (MTensor1D, 'top', 'horizontal'): {
        'path_info': [
            [[(0,), UL+OUT], [(-1,), UR+OUT]],
        ],
        'text_info': [
            [0, UP],
        ],
    },
    (MTensor1D, 'top', 'vertical'): {
        'path_info': [
            [[(0,), UR+OUT], [(-1,), DR+OUT]],
        ],
        'text_info': [
            [0, RIGHT],
        ],
    },
    (MTensor1D, 'intro', 'horizontal'): {
        'path_info': [
            [[(0,), UL+OUT], [(-1,), UR+OUT]],
        ],
        'text_info': [
            [0, UP+OUT],
        ],
    },
    (MTensor1D, 'intro', 'vertical'): {},
    (MTensor1D, 'intro', 'erect'): {
        'path_info': [
            [[(0,), UR+OUT], [(-1,), UR+IN]],
        ],
        'text_info': [
            [0, UR],
        ],
    },
    (MTensor1D, 'compute', 'horizontal'): {
        'path_info': [
            [[(0,), UL+OUT], [(-1,), UR+OUT]],
        ],
        'text_info': [
            [0, UP+OUT],
        ],
    },
    (MTensor1D, 'compute', 'vertical'): {},
    (MTensor1D, 'compute', 'erect'): {
        'path_info': [
            [[(0,), DR+OUT], [(-1,), DR+IN]],
        ],
        'text_info': [
            [0, DR],
        ],
    },
    (MTensor2D, 'top', 'horizontal'): {
        'path_info': [
            [[(0,0), UL], [(-1,0), DL]],
            [[(0,0), UL], [(0,-1), UR]],
        ],
        'text_info': [
            [0, LEFT+OUT],
            [1, UP+OUT],
        ],
    },
    (MTensor2D, 'intro', 'horizontal'): {
        'path_info': [
            [[(0,0), UL+OUT], [(-1,0), DL+OUT]],
            [[(0,0), UL+OUT], [(0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, LEFT+OUT],
            [1, UP+OUT],
        ],
    },
    (MTensor2D, 'intro', 'erect'): {
        'path_info': [
            [[(0,0), DL+OUT], [(-1,0), DL+IN]],
            [[(0,0), UL+OUT], [(0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, DL],
            [1, UP+OUT],
        ],
    },
    (MTensor2D, 'compute', 'horizontal'): {
        'path_info': [
            [[(0,-1), UR+OUT], [(-1,-1), DR+OUT]],
            [[(0,0), UL+OUT], [(0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, RIGHT+OUT],
            [1, UP+OUT],
        ],
    },
    (MTensor2D, 'compute', 'erect'): {
        'path_info': [
            [[(0,0), UL+OUT], [(-1,0), UL+IN]],
            [[(0,0), UL+OUT], [(0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, UL],
            [1, UP+OUT],
        ],
    },
    (MTensor3D, 'intro', None): {
        'path_info': [
            [[(0,-1,0), DL+OUT], [(-1,-1,0), DL+IN]],
            [[(0,0,0), UL+OUT], [(0,-1,0), DL+OUT]],
            [[(0,0,0), UL+OUT], [(0,0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, DL],
            [1, LEFT+OUT],
            [2, UP+OUT],
        ],
    },
    (MTensor3D, 'compute', None): {
        'path_info': [
            [[(0,0,0), UL+OUT], [(-1,0,0), UL+IN]],
            [[(0,0,-1), UR+OUT], [(0,-1,-1), DR+OUT]],
            [[(0,0,0), UL+OUT], [(0,0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, UL],
            [1, RIGHT+OUT],
            [2, UP+OUT],
        ],
    },
    (MTensor4D, 'intro', 'horizontal'): {
        'path_info': [
            [[(0,-1,-1,0), DL+IN], [(-1,-1,-1,-1), DR+IN]],
            [[(0,0,-1,0), DL+OUT], [(0,-1,-1,0), DL+IN]],
            [[(0,0,0,0), UL+OUT], [(0,0,-1,0), DL+OUT]],
            [[(0,0,0,0), UL+OUT], [(0,0,0,-1), UR+OUT]],
        ],
        'text_info': [
            [0, DOWN+IN],
            [1, DL],
            [2, LEFT+OUT],
            [3, UP+OUT],
        ],
    },
    (MTensor4D, 'compute', 'horizontal'): {
        'path_info': [
            [[(0,0,0,0), UL+OUT], [(-1,0,0,-1), UR+OUT]],
            [[(0,0,0,0), UL+OUT], [(0,-1,0,0), UL+IN]],
            [[(0,-1,0,0), UL+IN], [(0,-1,-1,0), DL+IN]],
            [[(0,-1,-1,0), DL+IN], [(0,-1,-1,-1), DR+IN]],
        ],
        'text_info': [
            [0, UP+OUT],
            [1, UL],
            [2, LEFT+IN],
            [3, DOWN+IN],
        ],
    },
    (FTensor3D, 'compute', None): {
        'path_info': [
            [[None, UL+OUT], [None, UL+IN]],
            [[None, UR+OUT], [None, DR+OUT]],
            [[None, UL+OUT], [None, UR+OUT]],
        ],
        'text_info': [
            [0, UL],
            [1, RIGHT+OUT],
            [2, UP+OUT],
        ],
    },   # TODO
    (FTensor4D, 'compute', None): {
        'path_info': [
            [[(0,), UL+OUT], [(-1,), UR+OUT]],
            [[(0,), UL+OUT], [(0,), UL+IN]],
            [[(0,), UL+IN], [(0,), DL+IN]],
            [[(0,), DL+IN], [(0,), DR+IN]],
        ],
        'text_info': [
            [0, UP+OUT],
            [1, UL],
            [2, LEFT+IN],
            [3, DOWN+IN],
        ],
    },
    (LayersFake, 'intro', None): {
        'path_info': [
            [[0, DL], [-1, DL]],        # VGroup indexing
            [[0, UL], [0, DL]],
            [[0, UL], [0, UR]],
        ],
        'text_info': [
            [0, DL],
            [1, LEFT+OUT],
            [2, UP+OUT],
        ],
    },
}

# TODO: use fixed in frame instead of fixed in orientation?
class ShowShape3D(AnimationGroup):
    def __init__(
        self,
        scene,
        mob: MTensorGeneral,
        view: str = 'compute',
        path_config: dict = {},
        text_config: dict = {},
        text_buff: float = DEFAULT_TEXT_BUFF,
        **aargs,
    ):
        path_config = {**DEFAULT_SHAPE_PATH_CONFIG, **path_config}
        text_config = {**DEFAULT_SHAPE_TEXT_CONFIG, **text_config}

        pmobs = VGroup()
        tmobs = VGroup()
        for pinfo, tinfo in zip(
            SHAPE_MAPPING[type(mob), view, mob.style if hasattr(mob,'style') else None]['path_info'],
            SHAPE_MAPPING[type(mob), view, mob.style if hasattr(mob,'style') else None]['text_info'],
        ):
            (p1_idx, p1_corner), (p2_idx, p2_corner) = pinfo
            t_idx, t_dir = tinfo
            if p1_idx is None and p2_idx is None:
                # for FTensor3D
                pmob = Line(
                    start=mob.get_corner(p1_corner),
                    end=mob.get_corner(p2_corner),
                    **path_config,
                )
                tmob = Text(
                    text=str(mob.shape[t_idx]),
                    **text_config,
                ).next_to(
                    pmob,
                    t_dir,
                    buff=text_buff,
                )
            else:
                # for MTensor(1/2/3/4)D, LayersFake(FIXME), FTensor4D
                pmob = Line(
                    start=mob[p1_idx].get_corner(p1_corner),
                    end=mob[p2_idx].get_corner(p2_corner),
                    **path_config,
                )
                tmob = Text(
                    text=str(mob.shape[t_idx]),
                    **text_config,
                ).next_to(
                    pmob,
                    t_dir,
                    buff=text_buff,
                )

            pmobs.add(pmob)
            tmobs.add(tmob)

        # make path and text always in front of others
        pmobs.set_z_index(998)
        tmobs.set_z_index(999)

        mob.shape_texts = tmobs
        # make text always face audience in 3d scene
        scene.camera.add_fixed_orientation_mobjects(*tmobs)
        
        super().__init__(
            *(AnimationGroup(
                ShowPassingFlash(pmob, time_width=10.0),
                Write(tmob),
                lag_ratio=0.3,
            ) for pmob, tmob in zip(pmobs, tmobs)),
            **aargs,
        )

class HideShape3D(AnimationGroup):
    def __init__(
        self,
        mob: MTensorGeneral,
        **aargs,
    ):
        tmobs = getattr(mob, "shape_texts", VGroup())

        super().__init__(
            *(Unwrite(tmob) for tmob in tmobs),
            **aargs,
        )
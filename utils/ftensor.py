from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
import itertools
import random
import numpy as np
import torch

from utils.mcube import MCube
from utils.mtensor import *
from utils.constants_3d import *

DEFAULT_CUBE_CONFIG = {
    'fill_color': GRAY,
    'fill_opacity': 0.8,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_SIZE_CONFIG = {
    'width': 0.1,
    'height': 0.1,
    'depth': 0.4,
}

class FTensor3D(VMobject):
    def __init__(
        self,
        ref_3d: MTensor3D | None = None,    # override shape, size_config
        shape: tuple | None = None,         # nominal shape like (3, 640, 640)
        z_index: float = 0.0,
        cube_config: dict = {},
        size_config: dict = {},
    ):
        super().__init__()

        self.z_index = z_index
        self.cube_config = {**DEFAULT_CUBE_CONFIG, **cube_config}
        if ref_3d is not None:
            shape = ref_3d.shape
            size_config = {
                'width': ref_3d.width,
                'height': ref_3d.height,
                'depth': ref_3d.depth,
            }
        self.shape = shape
        self.size_config = {**DEFAULT_SIZE_CONFIG, **size_config}

        mob = Cube(**self.cube_config)
        mob.stretch_to_fit_width(self.size_config['width'])
        mob.stretch_to_fit_height(self.size_config['height'])
        mob.stretch_to_fit_depth(self.size_config['depth'])
        mob.set_z_index(self.z_index)

        self.mob = mob
        self.add(self.mob)

        if ref_3d is not None:
            self.align_to(ref_3d, UL+OUT)
        else:
            self.center()

    def create(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        mob_init = Cube(**self.mob.get_style(simple=True))
        mob_init.width = self.mob.width
        mob_init.height = self.mob.height
        mob_init.stretch_to_fit_depth(0.0)
        if direction == 'top':
            mob_init.next_to(self.mob, OUT, buff=0.0)
        elif direction == 'center':
            mob_init.move_to(self.mob)
        elif direction == 'bottom':
            mob_init.next_to(self.mob, IN, buff=0.0)
        return Succession(
            Write(mob_init),
            ReplacementTransform(mob_init, self.mob),
            _on_finish=lambda s: s.add(self),
            **aargs,
        )

    def breath(
        self,
        **aargs,
    ):
        target = self.mob.copy()
        target.stretch_to_fit_width(self.mob.width*0.8)
        target.stretch_to_fit_height(self.mob.height*0.8)
        return Transform(
            self.mob,
            target,
            rate_func=rate_functions.there_and_back,
            **aargs,
        )

    def uncreate(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        target = self.mob.copy()
        target.stretch_to_fit_depth(0.0)
        if direction == 'top':
            target.next_to(self.mob, OUT, buff=0.0)
        elif direction == 'center':
            target.move_to(self.mob)
        elif direction == 'bottom':
            target.next_to(self.mob, IN, buff=0.0)
        return Succession(
            Transform(self.mob, target),
            Unwrite(self.mob),
            _on_finish=lambda s: s.remove(self),
            **aargs,
        )


class FTensor4D(VMobject):
    def __init__(
        self,
        shape: tuple | None = None,         # nominal shape like (64, 128, 320, 320)
        ref_4d: MTensor4D | None = None,    # override size_config, n, block_gap
        z_index: float = 0.0,
        cube_config: dict = {},
        size_config: dict = {},
        n: int = 8,
        block_gap: float = 0.3,
    ):
        super().__init__()
        self.z_index = z_index  # (z, z+n-1)
        self.cube_config = cube_config
        if ref_4d is not None:
            shape = ref_4d.shape
            size_config = {
                'width': ref_4d[0].width,
                'height': ref_4d[0].height,
                'depth': ref_4d[0].depth,
            }
            n = ref_4d.shape[0]
            # NOTE: assume that ref's style is horizontal
            block_gap = float(ref_4d[1].get_left()[0] - ref_4d[0].get_right()[0])
        self.shape = shape
        self.size_config = size_config
        self.n = n
        self.block_gap = block_gap

        objs = np.empty(self.n, dtype=object)
        for idx in range(self.n):
            ft = FTensor3D(
                shape=self.shape[1:],
                z_index=self.z_index + self.n - idx + 1,   # z+n-1, ... z
                cube_config=self.cube_config,
                size_config=self.size_config,
            )
            objs[idx] = ft
        mobs = VGroup(*objs.flat).center()
        mobs.arrange(
            RIGHT,
            buff=self.block_gap,
        )
        self.objs = objs
        self.mobs = mobs
        self.add(self.mobs)

        if ref_4d is not None:
            self.align_to(ref_4d, UL+OUT)
        else:
            self.center()

    def create(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        return AnimationGroup(
            *(mob.create(
                direction=direction
            ) for mob in self.mobs),
            _on_finish=lambda s: s.add(self),
            **aargs,
        )

    def breath(
        self,
        **aargs,
    ):
        return AnimationGroup(
            *(mob.breath() for mob in self.mobs),
            **aargs,
        )

    def uncreate(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        return AnimationGroup(
            *(mob.uncreate(
                direction=direction
            ) for mob in self.mobs),
            _on_finish=lambda s: s.remove(self),
            **aargs,
        )

    def __getitem__(
        self,
        idx,
    ) -> VMobject:
        res = self.objs[idx]
        if isinstance(res, FTensor3D):
            return res
        return VGroup(*res.flat)

    @property
    def z_index_start(self):
        return self.z_index

    @property
    def z_index_end(self):
        return self.z_index + self.n

wt = 1.0
class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        # cubes = FTensor4D(
        #     n=16,
        # )

        # self.wait(wt)
        # self.play(cubes.create(
        #     direction='bottom',
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # # self.play(Write(cubes, run_time=wt))
        # self.wait(wt)

        # self.play(cubes.breath(
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # self.play(cubes.uncreate(
        #     direction='bottom',
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        mt = MTensor4D(
            array=np.random.randn(6, 9, 3, 3),
            mode='cube',
            style='horizontal',
            side_length=0.3,
        )
        ft = FTensor4D(
            ref_4d=mt,
        )
        self.play(mt.create(
            style='beam',
            direction=OUT,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            mt.uncreate(
                style='beam',
                direction=OUT,
                anim=Unwrite,
                run_time=wt,
            ),
            ft.create(
                direction='bottom',
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)
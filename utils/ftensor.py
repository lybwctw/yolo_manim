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

def stretch_inplace_3d(
    mob,
    direction: str = 'erect',               # horizontal/erect
    size_scale: float | None = None,        # overrides size_target
    size_target: float | None = 2.0,
):
    """Assume that width==height and both scaled when horizontal.
    """
    if size_scale is not None:
        if direction == 'horizontal':
            size_target = mob.width * size_scale
        elif direction == 'erect':
            size_target = mob.depth * size_scale

    if direction == 'horizontal':
        mob.stretch_to_fit_width(
            size_target
        ).stretch_to_fit_height(
            size_target
        )
    elif direction == 'erect':
        mob.stretch_to_fit_depth(
            size_target
        )

def stretch_target_4d(
    mobs: VGroup,                           # a group of FTensor3D
    direction: str = 'erect',               # horizontal/erect
    size_scale: float | None = None,        # overrides size_target
    size_target: float | None = 2.0,
    keep_gap: bool = False,                 # use original gap?
):
    """Create target for each mob and stretch accordingly.
       Assume that width==height and both scaled when horizontal.
    """
    if len(mobs) > 1:
        orig_gap = mobs[1].get_left()[0] - mobs[0].get_right()[0]
    else:
        orig_gap = 0.0
    orig_center = mobs.get_center()

    # create targets
    for mob in mobs:
        mob.generate_target()
        stretch_inplace_3d(
            mob=mob.target,
            direction=direction,
            size_scale=size_scale,
            size_target=size_target,
        )

    # arrange targets
    vg = VGroup(mob.target for mob in mobs)
    if keep_gap:
        vg.arrange(RIGHT, buff=orig_gap)
    vg.move_to(
        orig_center
    )

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

        # self.z_index = z_index
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
        # mob.set_z_index(z_index)
        self.set_z_index(z_index)

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


    def stretch_direction(
        self,
        direction: str = 'erect',               # horizontal/erect
        size_scale: float | None = None,        # overrides size_target
        size_target: float | None = 2.0,
        shape: tuple | None = None,             # manual new shape
        **aargs,
    ) -> Animation:
        target = self.mob.copy()
        stretch_inplace_3d(
            mob=target,
            direction=direction,
            size_scale=size_scale,
            size_target=size_target,
        )

        # manual setup shape
        self.shape = shape

        return Transform(
            self.mob,
            target,
            rate_func=rate_functions.ease_out_back,
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
        z_index: float = 0.0,               # starting z_index for 3ds
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

    def stretch_direction(
        self,
        direction: str = 'erect',           # horizontal/erect
        size_scale: float | None = None,    # overrides size_target
        size_target: float | None = 2.0,
        keep_gap: bool = False,
        shape: tuple | None = None,         # manual new shape
        **aargs,
    ) -> AnimationGroup:
        stretch_target_4d(
            self.mobs,
            direction=direction,
            size_scale=size_scale,
            size_target=size_target,
            keep_gap=keep_gap,
        )

        # manual setup shape and child shapes
        self.shape = shape
        for mob in self.mobs:
            mob.shape = shape[1:]

        return AnimationGroup(
            *(MoveToTarget(
                mob,
                rate_func=rate_functions.ease_out_back,
            ) for mob in self.mobs),
            **aargs,
        )

    def stretch_blocks(
        self,
        diff: int = 1,                  # -n / n
        direction: str = 'center',      # top/center/bottom
        shape: tuple | None = None,     # manual new shape
        **aargs,
    ) -> AnimationGroup:
        if diff > 0:
            orig_center = self.get_center()
            orig_gap = self.mobs[1].get_left()[0] - self.mobs[0].get_right()[0]
            orig_n = self.n
            new_n = orig_n + diff * 2

            objs_new = np.empty(new_n, dtype=object)
            for idx in range(len(objs_new)):
                if idx < diff or idx >= self.n+diff:
                    objs_new[idx] = self.objs[0].copy()
                else:
                    objs_new[idx] = self.objs[idx-diff]
            mobs_new = VGroup(*objs_new.flat).arrange(
                RIGHT,
                buff=orig_gap,
            )
            mobs_new.move_to(orig_center)

            # reset z_index
            for idx, mob in enumerate(mobs_new):
                mob.z_index = self.z_index + new_n - idx + 1
                
            self.objs = objs_new
            self.mobs = mobs_new
            self.n = new_n
            self.shape = shape      # manual setup shape
            # self.add(self.mobs_new)

            vgs_left = self.mobs[:diff][::-1]
            vgs_right = self.mobs[-diff:]
            return AnimationGroup(
                AnimationGroup(
                    *(mob.create(direction=direction)
                    for mob in vgs_left),
                    **aargs,
                ),
                AnimationGroup(
                    *(mob.create(direction=direction)
                    for mob in vgs_right),
                    **aargs,
                ),
                lag_ratio=0.0,
                _on_finish=lambda _: self.add(self.mobs),
            )

        elif diff < 0:
            diff = -diff
            orig_n = self.n
            new_n = orig_n - diff * 2

            objs_new = self.objs[diff:diff+new_n]
            mobs_new = VGroup(*objs_new.flat)

            # skip z_index reset?

            objs_old = self.objs
            mobs_old = self.mobs

            self.objs = objs_new
            self.mobs = mobs_new
            self.n = new_n
            self.shape = shape

            vgs_left = mobs_old[:diff]
            vgs_right = mobs_old[-diff:][::-1]

            return AnimationGroup(
                AnimationGroup(
                    *(mob.uncreate(direction=direction)
                    for mob in vgs_left),
                    **aargs,
                ),
                AnimationGroup(
                    *(mob.uncreate(direction=direction)
                    for mob in vgs_right),
                    **aargs,
                ),
                lag_ratio=0.0,
                _on_finish=lambda _: mobs_old.remove(*vgs_left, *vgs_right),
            )

        else:
            raise NotImplementedError('diff should not be zero')

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

wt = 0.5
class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        # cube = FTensor3D(
        #     shape=(3, 4, 5),
        #     size_config={
        #         'width': 0.3,
        #         'height': 0.3,
        #         'depth': 1.0,
        #     },
        # )
        # self.wait(wt)

        # self.play(cube.create(
        #     direction='bottom',
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # self.play(cube.stretch_direction(
        #     direction='horizontal',
        #     size_scale=1.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # self.play(cube.breath(
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # self.play(cube.uncreate(
        #     direction='bottom',
        #     run_time=wt,
        # ))
        # self.wait(wt)

        ft4 = FTensor4D(
            shape=(3,4,5),
            size_config={
                'width': 0.2,
                'height': 0.2,
                'depth': 1.0,
            },
            n=6,
            block_gap=0.3,
        )
        self.play(ft4.create(
            direction='bottom',
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(ft4.stretch_direction(
            direction='horizontal',
            size_scale=2.0,
            shape=(3,5,5),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(ft4.stretch_blocks(
            diff=3,
            direction='bottom',
            shape=(2,3,5,5),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # self.play(ft4.stretch_direction(
        #     direction='horizontal',
        #     size_scale=2.0,
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        self.play(ft4.breath(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # self.play(ft4.animate(
        #     run_time=wt,
        # ).shift(DOWN*3))
        # self.wait(wt)

        self.play(ft4.uncreate(
            direction='bottom',
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
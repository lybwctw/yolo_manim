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

UNIT_FTENSOR_SIZE = 0.15

DEFAULT_CUBE_CONFIG = {
    'fill_color': GRAY,
    'fill_opacity': 0.8,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_SIZE_CONFIG = {
    'width': UNIT_FTENSOR_SIZE,
    'height': UNIT_FTENSOR_SIZE,
    'depth': UNIT_FTENSOR_SIZE*4,
}

TARNISH_CUBE_CONFIG = {
    'fill_opacity': 0.0,
    'stroke_opacity': 0.1,
}

# def stretch_inplace_3d(
#     mob,
#     direction: str = 'erect',               # horizontal/erect
#     size_scale: float | None = None,        # overrides size_target
#     size_target: float | None = 2.0,
# ):
#     """Assume that width==height and both scaled when horizontal.
#     """
#     if size_scale is not None:
#         if direction == 'horizontal':
#             target_width = mob.width * size_scale
#             target_height = mob.height * size_scale
#             # size_target = mob.width * size_scale
#         elif direction == 'erect':
#             target_depth = mob.depth * size_scale
#             # size_target = mob.depth * size_scale
#     else:
#         if direction == 'horizontal':
#             target_width = size_target[0] if isinstance(size_target, (list, tuple)) else size_target
#             target_height = size_target[1] if isinstance(size_target, (list, tuple)) else size_target
#         elif direction == 'erect':
#             target_depth = size_target  # assume that size_target is a float

#     if direction == 'horizontal':
#         mob.stretch_to_fit_width(
#             target_width
#         ).stretch_to_fit_height(
#             target_height
#         )
#     elif direction == 'erect':
#         mob.stretch_to_fit_depth(
#             target_depth
#         )

# def stretch_target_4d(
#     mobs: VGroup,                           # a group of FTensor3D
#     direction: str = 'erect',               # horizontal/erect
#     size_scale: float | None = None,        # overrides size_target
#     size_target: float | None = 2.0,
# ):
#     """Create target for each mob and stretch accordingly.
#     """
#     # create targets
#     for mob in mobs:
#         mob.generate_target()
#         stretch_inplace_3d(
#             mob=mob.target,
#             direction=direction,
#             size_scale=size_scale,
#             size_target=size_target,
#         )

class FTensor3D(VMobject):
    def __init__(
        self,
        ref_3d: MTensor3D | None = None,    # override shape, size_config
        shape: tuple | None = None,         # nominal shape like (3, 640, 640)
        z_index: float = 0.0,
        cube_config: dict = {},
        size_config: dict = {},             # override that from shape
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

        # default -> shape-based -> user-provided
        size_config_shape = {
            'width': shape[2] * UNIT_FTENSOR_SIZE,
            'height': shape[1] * UNIT_FTENSOR_SIZE,
            'depth': shape[0] * UNIT_FTENSOR_SIZE,
        }
        size_config = {
            **DEFAULT_SIZE_CONFIG,
            **size_config_shape,
            **size_config,
        }
        self.size_config = size_config

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
        ref: str = 'center',      # top/center/bottom
        **aargs,
    ):
        mob_init = self.mob.copy()
        mob_init.stretch_to_fit_depth(0.0)
        if ref == 'top':
            mob_init.next_to(self.mob, OUT, buff=0.0)
        elif ref == 'center':
            mob_init.move_to(self.mob)
        elif ref == 'bottom':
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

    def tarnish(
        self,
        **aargs,
    ) -> Animation:
        return self.mob.animate(
            **aargs,
        ).set_style(**TARNISH_CUBE_CONFIG)

    def lightup(
        self,
        **aargs,
    ) -> Animation:
        return self.mob.animate(
            **aargs,
        ).set_style(**self.cube_config)

    def stretch_3d(
        self,
        new_shape: tuple,                       # (c, h, w)
        scale_factor: tuple | None = None,      # (c, h, w)
        target_size: tuple | None = None,       # (c, h, w)
        **aargs,
    ) -> Animation:
        target = self.mob.copy()
        if scale_factor is not None:
            target.stretch_to_fit_depth(self.mob.depth*scale_factor[0])
            target.stretch_to_fit_height(self.mob.height*scale_factor[1])
            target.stretch_to_fit_width(self.mob.width*scale_factor[2])
        elif target_size is not None:
            target.stretch_to_fit_depth(target_size[0])
            target.stretch_to_fit_height(target_size[1])
            target.stretch_to_fit_width(target_size[2])
        else:
            target.stretch_to_fit_depth(new_shape[0]*UNIT_FTENSOR_SIZE)
            target.stretch_to_fit_height(new_shape[1]*UNIT_FTENSOR_SIZE)
            target.stretch_to_fit_width(new_shape[2]*UNIT_FTENSOR_SIZE)
        self.shape = new_shape
        return Transform(
            self.mob,
            target,
            rate_func=rate_functions.ease_out_back,
            **aargs,
        )

    def uncreate(
        self,
        ref: str = 'center',      # top/center/bottom
        **aargs,
    ):
        target = self.mob.copy()
        target.stretch_to_fit_depth(0.0)
        if ref == 'top':
            target.next_to(self.mob, OUT, buff=0.0)
        elif ref == 'center':
            target.move_to(self.mob)
        elif ref == 'bottom':
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
        ref_4d: MTensor4D | None = None,    # override size_config, n, block_gap
        shape: tuple | None = None,         # nominal shape like (64, 128, 320, 320)
        z_index: float = 0.0,               # starting z_index for 3ds
        cube_config: dict = {},
        size_config: dict = {},             # override that from shape[1:]
        n: int | None = None,               # override that from shape[0]
        block_gap: float = UNIT_FTENSOR_SIZE,
    ):
        super().__init__()
        self.zidx = z_index  # (z, z+n-1)
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

        self.shape = shape      # (b,c,h,w)

        # default -> shape-based -> user-provided
        size_config_shape = {
            'width': shape[3] * UNIT_FTENSOR_SIZE,
            'height': shape[2] * UNIT_FTENSOR_SIZE,
            'depth': shape[1] * UNIT_FTENSOR_SIZE,
        }
        size_config = {
            **DEFAULT_SIZE_CONFIG,
            **size_config_shape,
            **size_config,
        }
        self.size_config = size_config

        self.n = n if n is not None else shape[0]   # number of 3D blocks
        self.block_gap = block_gap

        objs = np.empty(self.n, dtype=object)
        for idx in range(self.n):
            ft = FTensor3D(
                shape=self.shape[1:],
                z_index=self.zidx + self.n - idx + 1,   # z+n-1, ... z
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
        ref: str = 'center',      # top/center/bottom
        **aargs,
    ):
        return AnimationGroup(
            *(mob.create(
                ref=ref,
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

    def tarnish(
        self,
        **aargs,
    ) -> Animation:
        return AnimationGroup(
            *(mob.tarnish() for mob in self.mobs),
            **aargs,
        )

    def lightup(
        self,
        **aargs,
    ) -> Animation:
        return AnimationGroup(
            *(mob.lightup() for mob in self.mobs),
            **aargs,
        )

    def stretch_3d(
        self,
        new_shape: tuple,                       # (c, h, w)
        scale_factor: tuple | None = None,      # (c, h, w)
        target_size: tuple | None = None,       # (c, h, w)
        **aargs,
    ) -> AnimationGroup:
        self.shape = self.shape[:1] + new_shape
        return AnimationGroup(
            *(mob.stretch_3d(
                new_shape=new_shape,
                scale_factor=scale_factor,
                target_size=target_size,
            ) for mob in self.mobs),
            **aargs,
        )

    def stretch_blocks(
        self,
        direction: str = 'out',             # out/in
        diff: int = 1,                      # number of blocks to stretch
        ref: str = 'center',                # top/center/bottom
        new_shape: tuple | None = None,     # overriding new shape
        **aargs,
    ) -> AnimationGroup:
        if direction == 'out':
            orig_center = self.get_center()
            new_n = self.n + diff * 2
            if new_shape is None:
                new_shape = (self.shape[0]+diff*2, *self.shape[1:])

            objs_new = np.empty(new_n, dtype=object)
            for idx in range(new_n):
                if idx < diff or idx >= self.n+diff:
                    objs_new[idx] = self.objs[0].copy()
                else:
                    objs_new[idx] = self.objs[idx-diff]
            mobs_new = VGroup(*objs_new.flat).arrange(
                RIGHT,
                buff=self.current_gap,
            )
            mobs_new.move_to(orig_center)

            # reset z_index
            for idx, mob in enumerate(mobs_new):
                mob.set_z_index(self.zidx + new_n - idx + 1)
                # mob.z_index = self.zidx + new_n - idx + 1
                
            self.objs = objs_new
            self.mobs = mobs_new
            self.n = new_n
            self.shape = new_shape

            vgs_left = self.mobs[:diff][::-1]
            vgs_right = self.mobs[-diff:]
            return AnimationGroup(
                AnimationGroup(
                    *(mob.create(ref=ref)
                    for mob in vgs_left),
                    **aargs,
                ),
                AnimationGroup(
                    *(mob.create(ref=ref)
                    for mob in vgs_right),
                    **aargs,
                ),
                lag_ratio=0.0,
                _on_finish=lambda _: self.add(self.mobs),
            )

        elif direction == 'in':
            new_n = self.n - diff * 2
            if new_shape is None:
                new_shape = (self.shape[0]-diff*2, *self.shape[1:])

            objs_new = self.objs[diff:diff+new_n]
            mobs_new = VGroup(*objs_new.flat)

            # skip z_index reset

            mobs_old = self.mobs

            self.objs = objs_new
            self.mobs = mobs_new
            self.n = new_n
            self.shape = new_shape

            vgs_left = mobs_old[:diff]
            vgs_right = mobs_old[-diff:][::-1]

            return AnimationGroup(
                AnimationGroup(
                    *(mob.uncreate(ref=ref)
                    for mob in vgs_left),
                    **aargs,
                ),
                AnimationGroup(
                    *(mob.uncreate(ref=ref)
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
        ref: str = 'center',      # top/center/bottom
        **aargs,
    ):
        return AnimationGroup(
            *(mob.uncreate(
                ref=ref,
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
    def current_gap(self):
        if self.n > 1:
            return self.mobs[1].get_left()[0] - self.mobs[0].get_right()[0]
        else:
            return 0.0

    @property
    def z_index_start(self):
        return self.zidx

    @property
    def z_index_end(self):
        return self.zidx + self.n

wt = 0.5
class Demo(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        # cube = FTensor3D(
        #     shape=(3, 4, 5),
        #     # size_config={
        #     #     'width': 0.3,
        #     #     'height': 0.3,
        #     #     'depth': 1.0,
        #     # },
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
            shape=(8,8,3,3),
            size_config={
                # 'width': UNIT_FTENSOR_SIZE*2.0,
                # 'height': UNIT_FTENSOR_SIZE*2.0,
            },
        )
        self.play(ft4.create(
            ref='bottom',
            lag_ratio=0.5,
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait(wt)

        self.play(ft4.stretch_3d(
            new_shape=(8,1,1),
            scale_factor=(1.0, 0.5, 0.5),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(ft4.stretch_blocks(
            direction='out',
            diff=3,
            ref='bottom',
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(ft4.stretch_blocks(
            direction='in',
            diff=5,
            ref='bottom',
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

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
            ref='bottom',
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
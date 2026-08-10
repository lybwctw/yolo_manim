from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
import itertools
import random
import numpy as np
import torch

from utils.mcube import MCube
from utils.constants_3d import *

class MTensorGeneral(VMobject):
    def __init__(
        self,
        objs: list | None = None,
        mobs: VGroup | None = None,
        array: torch.Tensor | np.ndarray | None = None,
        mode: str = 'cube',
        style: str | None = None,
        side_length: float = 0.5,
        font_size: float = 18,
        padding: float = 0.0,
        cube_config: dict = {},
        square_config: dict = {},
        decimal_config: dict = {},
    ):
        super().__init__()
        if isinstance(array, torch.Tensor):
            self.tensor = array
            self.array = array.numpy()
        else:
            self.array = array
        self.mode = mode
        self.style = style

        self.side_length = side_length
        self.font_size = font_size
        self.padding = padding
        self.cube_config = cube_config
        self.square_config = square_config
        self.decimal_config = decimal_config

        self.hl_state = np.ones(self.shape, dtype=bool)

        if objs is None and mobs is None:
            objs, mobs = self._create_mobs()
        self.objs = objs
        self.mobs = mobs
        self.add(self.mobs)

    def _make_cube(
        self,
        value,
        z_index: float = 0.0,
        cube_config: dict = {},     # override internal
        square_config: dict = {},   # override internal
        decimal_config: dict = {},  # override internal
    ):
        return MCube(
            value=float(value),
            mode=self.mode,
            z_index=z_index,
            side_length=self.side_length,
            font_size=self.font_size,
            cube_config={**self.cube_config, **cube_config},
            square_config={**self.square_config, **square_config},
            decimal_config={**self.decimal_config, **decimal_config},
        )
    
    def __getitem__(
        self,
        idx,
    ) -> VMobject:
        res = self.objs[idx]
        if isinstance(res, MCube):
            return res
        return VGroup(*res.flat)

    def get_vgs(
        self,
        masks: list | np.ndarray,
        reverse: bool = False,      # reverse internal mobs in each vg
    ) -> VGroup:
        step = -1 if reverse else 1
        vmobs = VGroup(
            self[mask][::step] for mask in masks
        )
        return vmobs
    
    def highlight(
        self,
        mask: np.ndarray | None = None,
        **aargs,
    ) -> Animation:
        if mask is None:
            mask = np.ones(self.shape, dtype=bool)
        
        mask_start = self.hl_state
        mask_end = mask

        mask_hl = ~mask_start & mask_end
        mask_dm = ~mask_end & mask_start

        anims_hl = [mob.lightup() for mob in self[mask_hl]]
        anims_dm = [mob.tarnish() for mob in self[mask_dm]]

        self.hl_state = mask
        return AnimationGroup(
            *anims_hl,
            *anims_dm,
            **aargs,
        )
    
    def highlight_loop(
        self,
        masks: list | np.ndarray,
        back: bool = False,              # back to initial state or not
        **aargs,
    ) -> AnimationGroup:
        # convert 1st dim into list
        if isinstance(masks, np.ndarray):
            masks = list(masks)

        if back:
            masks_start = [self.hl_state] + masks
            masks_end = masks + [self.hl_state]
        else:
            masks_start = [self.hl_state] + masks[:-1]
            masks_end = masks

        anims_loop = []
        for start, end in zip(masks_start, masks_end):
            mask_hl = ~start & end
            mask_dm = ~end & start
            anims_hl = [mob.lightup() for mob in self[mask_hl]]
            anims_dm = [mob.tarnish() for mob in self[mask_dm]]
            anims_loop.append(AnimationGroup(
                *anims_hl,
                *anims_dm,
                lag_ratio=0.0,  # highlight/fade at the same time
            ))
        
        if not back:
            self.hl_state = masks_end[-1]

        return Succession(
            *anims_loop,
            rate_func=smooth,
            **aargs,
        )

    def _loop_anims(self):
        raise NotImplementedError

    def update_values(
        self,
        values: torch.Tensor | np.ndarray | None = None,
        **aargs,
    ) -> Animation:
        """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        NOTE update manim ChangeDecimalToValue source to sync z_index. NOTE
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        assert self.mode == 'card', "update_value only works in 'card' mode"
        if isinstance(values, torch.Tensor):
            self.tensor = values
            self.array = values.numpy()
        elif isinstance(values, np.ndarray):
            self.array = values
        elif values is None:
            self.array = np.random.randn(*self.shape)

        anims = AnimationGroup(
            *(mob.update_value(value)
            for mob, value in zip(self.mobs, self.array.flat)),
            **aargs,
        )
        return anims

    def create(
        self,
        style: str = 'whole',
        direction: np.ndarray = DOWN,
        anim: Animation = GrowFromCenter,
        **aargs,
    ) -> AnimationGroup:
        anims = self._loop_anims(
            style=style,
            direction=direction,
            anim=anim,
            aargs_unit={
                'rate_func': rate_functions.ease_out_back
                    if anim is GrowFromCenter else smooth,
            },
            aargs_series={'lag_ratio': 0.5},
            aargs_layer={'lag_ratio': 0.5},
            aargs_beam={'lag_ratio': 0.8},
            aargs=aargs,
            _on_finish=lambda s: s.add(self),
        )
        return anims

    def translate(
        self,
        style: str = 'whole',
        direction: np.ndarray = DOWN,
        **aargs,
    ) -> AnimationGroup:
        anims = self._loop_anims(
            style=style,
            direction=direction,
            anim=lambda mob, **args: mob.translate(**args),
            aargs_unit={},
            aargs_series={'lag_ratio': 0.1},
            aargs_layer={'lag_ratio': 0.1},
            aargs_beam={'lag_ratio': 0.1},
            aargs=aargs,
        )
        return anims
    
    def breath(
        self,
        style: str = 'whole',
        direction: np.ndarray = DOWN,
        **aargs,
    ) -> AnimationGroup:
        anims = self._loop_anims(
            style=style,
            direction=direction,
            anim=lambda mob, **args: mob.breath(**args),
            aargs_unit={},
            aargs_series={'lag_ratio': 0.1},
            aargs_layer={'lag_ratio': 0.1},
            aargs_beam={'lag_ratio': 0.1},
            aargs=aargs,
        )
        return anims

    def switch(
        self,
        style: str = 'whole',
        direction: np.ndarray = DOWN,
        **aargs,
    ) -> AnimationGroup:
        self.mode = 'cube' if self.mode == 'card' else 'card'

        anims = self._loop_anims(
            style=style,
            direction=direction,
            anim=lambda mob, **args: mob.switch(**args),
            aargs_unit={},
            aargs_series={'lag_ratio': 0.5},
            aargs_layer={'lag_ratio': 0.5},
            aargs_beam={'lag_ratio': 0.8},
            aargs=aargs,
        )
        return anims

    def uncreate(
        self,
        style: str = 'whole',
        direction: np.ndarray = DOWN,
        anim: Animation = ShrinkToCenter,
        **aargs,
    ) -> AnimationGroup:
        anims = self._loop_anims(
            style=style,
            direction=direction,
            anim=anim,
            aargs_unit={},
            aargs_series={'lag_ratio': 0.5},
            aargs_layer={'lag_ratio': 0.5},
            aargs_beam={'lag_ratio': 0.8},
            aargs=aargs,
            _on_finish=lambda s: s.remove(self),
        )
        return anims

    @property
    def shape(self):
        return self.array.shape

    @property
    def ndim(self):
        return self.array.ndim

    @property
    def step(self):
        return self.side_length + self.padding

class MTensor1D(MTensorGeneral):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _create_mobs(
        self,
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        w = self.shape[0]

        if self.style == 'horizontal':
            xs = [RIGHT * i * self.step for i in range(w)]
        elif self.style == 'vertical':
            xs = [DOWN * i * self.step for i in range(w)]
        elif self.style == 'erect':
            xs = [IN * i * self.step for i in range(w)]

        for i in range(w):
            if self.style == 'horizontal':
                z_index = w - i
            elif self.style == 'vertical':
                z_index = i
            elif self.style == 'erect':
                z_index = w - i

            cube = self._make_cube(
                value=self.array[i],
                z_index=z_index,
            )
            cube.shift(xs[i])
            objs[i] = cube

        mobs = VGroup(*objs.flat).center()
        return objs, mobs

    def _loop_anims(
        self,
        style: str,
        direction: np.ndarray,
        anim: Animation,
        aargs_unit: dict = {},
        aargs_series: dict = {},
        aargs_layer: dict = {},
        aargs_beam: dict = {},
        aargs: dict = {},   # run_time
        **kwargs,           # _on_finish
    ) -> Animation:
        if style == 'series':
            if np.array_equal(direction, RIGHT):
                mobs = self.mobs
            elif np.array_equal(direction, LEFT):
                mobs = self.mobs[::-1]
            anims = AnimationGroup(
                *(anim(mob, **aargs_unit) for mob in mobs),
                rate_func=smooth,
                **aargs_series, # lag_ratio
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'whole':
            anims = AnimationGroup(
                *(anim(mob, **aargs_unit) for mob in self.mobs),
                lag_ratio=0.0,
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        return anims

class MTensor2D(MTensorGeneral):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _create_mobs(
        self,
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        h, w = self.shape

        xs = [RIGHT * j * self.step for j in range(w)]
        if self.style == 'horizontal':
            ys = [DOWN * i * self.step for i in range(h)]
        elif self.style == 'erect':
            ys = [IN * i * self.step for i in range(h)]

        for i, j in np.ndindex(self.shape):
            if self.style == 'horizontal':
                z_index = i * w - j
            elif self.style == 'erect':
                z_index = (h-i) * w - j

            cube = self._make_cube(
                value=self.array[i, j],
                z_index=z_index,
            )
            cube.shift(xs[j] + ys[i])
            objs[i, j] = cube

        mobs = VGroup(*objs.flat).center()
        return objs, mobs

    def get_layers(
        self,
        direction: np.ndarray = RIGHT,
        reverse: bool = False,
    ) -> VGroup:
        h, w = self.shape
        if np.array_equal(direction, RIGHT):
            masks = np.eye(w, dtype=bool)[:, None, :].repeat(h, axis=1)
        elif np.array_equal(direction, LEFT):
            masks = np.eye(w, dtype=bool)[:, None, :].repeat(h, axis=1)[::-1]
        elif np.array_equal(direction, DOWN):
            masks = np.eye(h, dtype=bool)[:, :, None].repeat(w, axis=2)
        elif np.array_equal(direction, UP):
            masks = np.eye(h, dtype=bool)[:, :, None].repeat(w, axis=2)[::-1]
        vgs = self.get_vgs(masks, reverse=reverse)
        return vgs

    def _loop_anims(
        self,
        style: str | None,
        direction: np.ndarray,
        anim: Animation,
        aargs_unit: dict = {},
        aargs_series: dict = {},
        aargs_layer: dict = {},
        aargs_beam: dict = {},
        aargs: dict = {},   # run_time
        **kwargs,           # _on_finish
    ) -> Animation:
        if style == 'series':
            if np.array_equal(direction, RIGHT):
                mobs = self.mobs
            elif np.array_equal(direction, LEFT):
                mobs = self.mobs[::-1]
            anims = AnimationGroup(
                *(anim(mob, **aargs) for mob in mobs),
                rate_func=smooth,
                **aargs_series, # lag_ratio
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'layer':
            layers = self.get_layers(direction=direction)
            anims = AnimationGroup(
                *(AnimationGroup(
                    *(anim(mob, **aargs_unit) for mob in layer),
                    lag_ratio=0.0,
                ) for layer in layers),
                rate_func=smooth,
                **aargs_layer,  # lag_ratio
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'beam':
            if np.array_equal(direction, RIGHT):
                beams = self.get_layers(DOWN, reverse=False)
            elif np.array_equal(direction, LEFT):
                beams = self.get_layers(DOWN, reverse=True)
            elif np.array_equal(direction, DOWN):
                beams = self.get_layers(RIGHT, reverse=False)
            elif np.array_equal(direction, UP):
                beams = self.get_layers(RIGHT, reverse=True)
            anims = AnimationGroup(
                *(Succession(
                    *(anim(mob, **aargs_unit) for mob in beam),
                    run_time=random.random()+1,
                    rate_func=smooth,
                    **aargs_beam,
                ) for beam in beams),
                lag_ratio=0.0,
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'whole':
            anims = AnimationGroup(
                *(anim(mob, **aargs_unit) for mob in self.mobs),
                lag_ratio=0.0,
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        return anims

class MTensor3D(MTensorGeneral):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _create_mobs(
        self,
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        c, h, w = self.shape

        xs = [RIGHT * k * self.step for k in range(w)]
        ys = [DOWN * j * self.step for j in range(h)]
        zs = [IN * i * self.step for i in range(c)]

        for i, j, k in np.ndindex(self.shape):
            cube = self._make_cube(
                value=self.array[i, j, k],
                z_index=(c-i)*h+j,          # z_index
            )
            cube.shift(xs[k] + ys[j] + zs[i])
            objs[i, j, k] = cube
        
        mobs = VGroup(*objs.flat).center()
        return objs, mobs

    def get_layers(
        self,
        direction: np.ndarray = OUT,
    ) -> VGroup:
        c, h, w = self.shape
        if np.array_equal(direction, RIGHT):
            masks = np.tile(np.eye(w, dtype=bool)[:,None,None,:], (1,c,h,1))
        elif np.array_equal(direction, LEFT):
            masks = np.tile(np.eye(w, dtype=bool)[:,None,None,:], (1,c,h,1))[::-1]
        elif np.array_equal(direction, DOWN):
            masks = np.tile(np.eye(h, dtype=bool)[:,None,:,None], (1,c,1,w))
        elif np.array_equal(direction, UP):
            masks = np.tile(np.eye(h, dtype=bool)[:,None,:,None], (1,c,1,w))[::-1]
        elif np.array_equal(direction, IN):
            masks = np.tile(np.eye(c, dtype=bool)[:,:,None,None], (1,1,h,w))
        elif np.array_equal(direction, OUT):
            masks = np.tile(np.eye(c, dtype=bool)[:,:,None,None], (1,1,h,w))[::-1]
        vgs = self.get_vgs(masks)
        return vgs

    def get_beams(
        self,
        direction: np.ndarray = OUT,
    ) -> VGroup:
        c, h, w = self.shape
        if np.array_equal(direction, RIGHT):
            masks = np.eye(c*h, dtype=bool).reshape(-1,c,h)[:,:,:,None].repeat(w, axis=3)
            vgs = self.get_vgs(masks, reverse=False)
        elif np.array_equal(direction, LEFT):
            masks = np.eye(c*h, dtype=bool).reshape(-1,c,h)[:,:,:,None].repeat(w, axis=3)
            vgs = self.get_vgs(masks, reverse=True)
        elif np.array_equal(direction, DOWN):
            masks = np.eye(c*w, dtype=bool).reshape(-1,c,w)[:,:,None,:].repeat(w, axis=2)
            vgs = self.get_vgs(masks, reverse=False)
        elif np.array_equal(direction, UP):
            masks = np.eye(c*w, dtype=bool).reshape(-1,c,w)[:,:,None,:].repeat(w, axis=2)
            vgs = self.get_vgs(masks, reverse=True)
        elif np.array_equal(direction, IN):
            masks = np.eye(h*w, dtype=bool).reshape(-1,h,w)[:,None,:,:].repeat(c, axis=1)
            vgs = self.get_vgs(masks, reverse=False)
        elif np.array_equal(direction, OUT):
            masks = np.eye(h*w, dtype=bool).reshape(-1,h,w)[:,None,:,:].repeat(c, axis=1)
            vgs = self.get_vgs(masks, reverse=True)
        return vgs

    def _loop_anims(
        self,
        style: str,
        direction: np.ndarray,
        anim: Animation,
        aargs_unit: dict = {},
        aargs_series: dict = {},
        aargs_layer: dict = {},
        aargs_beam: dict = {},
        aargs: dict = {},   # run_time
        **kwargs,           # _on_finish
    ) -> Animation:
        if style == 'series':
            if np.array_equal(direction, RIGHT):
                mobs = self.mobs
            elif np.array_equal(direction, LEFT):
                mobs = self.mobs[::-1]
            anims = AnimationGroup(
                *(anim(mob, **aargs_unit) for mob in mobs),
                rate_func=smooth,
                **aargs_series, # lag_ratio
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'layer':
            layers = self.get_layers(direction=direction)
            anims = AnimationGroup(
                *(AnimationGroup(
                    *(anim(mob, **aargs_unit) for mob in layer),
                    lag_ratio=0.0,
                ) for layer in layers),
                rate_func=smooth,
                **aargs_layer,  # lag_ratio
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'beam':
            beams = self.get_beams(direction=direction)
            anims = AnimationGroup(
                *(AnimationGroup(
                    *(anim(mob, **aargs_unit) for mob in beam),
                    run_time=random.random()+1,
                    rate_func=smooth,
                    **aargs_beam,
                ) for beam in beams),
                lag_ratio=0.0,
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'whole':
            anims = AnimationGroup(
                *(anim(mob, **aargs_unit) for mob in self.mobs),
                lag_ratio=0.0,
                **aargs,        # run_time
                **kwargs,       # _on_finish
            )
        return anims
    
    def pad(
        self,
        pad_width: list | tuple,    # (c, h, w)
        pad_value: float = 0.0,
        **aargs,
    ) -> AnimationGroup:
        pad_c, pad_h, pad_w = pad_width

        mask_pad = ~np.pad(
            np.ones(self.shape, dtype=bool),
            ((pad_c, pad_c), (pad_h, pad_h), (pad_w, pad_w)),
        )
        mask_orig = (
            slice(pad_c, pad_c+self.shape[0]),
            slice(pad_h, pad_h+self.shape[1]),
            slice(pad_w, pad_w+self.shape[2]),
        )

        array_new = np.pad(
            self.array,
            ((pad_c, pad_c), (pad_h, pad_h), (pad_w, pad_w)),
            mode='constant',
            constant_values=pad_value,
        )
        c_new, h_new, w_new = array_new.shape
        objs_new = np.empty(array_new.shape, dtype=object)

        orig_center = self.objs[0,0,0].get_center()

        xs = [RIGHT * k * self.step for k in range(w_new)]
        ys = [DOWN * j * self.step for j in range(h_new)]
        zs = [IN * i * self.step for i in range(c_new)]
        for i, j, k in np.ndindex(array_new.shape):
            if not mask_pad[i,j,k]:
                mob = self.objs[i-pad_c, j-pad_h, k-pad_w]
                mob.set_z_index((c_new-i)*h_new+j)
                mob.center()
            else:
                mob = self._make_cube(
                    array_new[i,j,k],
                    (c_new-i)*h_new+j,      # z_index
                    cube_config={**self.cube_config, 'stroke_color': TEAL},
                    square_config={**self.square_config},
                    decimal_config={**self.decimal_config},
                ).center()
            mob.shift(xs[k] + ys[j] + zs[i])
            objs_new[i,j,k] = mob

        mobs_new = VGroup(*objs_new.flat)
        offset = orig_center - objs_new[pad_c,pad_h,pad_w].get_center()
        mobs_new.shift(offset)

        self.mask_pad = mask_pad
        self.mask_orig = mask_orig
        self.array = array_new
        self.objs = objs_new
        self.mobs = mobs_new
        self.hl_state = np.ones(self.shape, dtype=bool)
        self.add(self.mobs)

        return AnimationGroup(
            *(GrowFromCenter(
                mob,
                rate_func=rate_functions.ease_out_back,
            ) for mob in VGroup(*self.objs[self.mask_pad])),
            **aargs,
        )

    def unpad(
        self,
        **aargs,
    ) -> AnimationGroup:
        assert hasattr(self, 'mask_pad')
        assert hasattr(self, 'mask_orig')

        self.remove(self.mobs)

        pmobs = VGroup(*self.objs[self.mask_pad])
        self.array = self.array[self.mask_orig]     # use slice
        self.objs = self.objs[self.mask_orig]
        self.mobs = VGroup(*self.objs.flat)
        self.hl_state = np.ones(self.shape, dtype=bool)

        self.add(self.mobs)

        del self.mask_pad
        del self.mask_orig

        return AnimationGroup(
            *(ShrinkToCenter(
                cube,
            ) for cube in pmobs),
            **aargs,
        )

    def conv2d_masks(
        self,
        kh: int = 3,
        kw: int = 3,
        sh: int = 1,
        sw: int = 1,
    ) -> np.ndarray:
        c, h, w = self.shape

        out_h = (h - kh) // sh + 1
        out_w = (w - kw) // sw + 1

        # top-left corner of each kernel window
        y0 = np.arange(out_h) * sh
        x0 = np.arange(out_w) * sw

        # kernel offsets
        ky = np.arange(kh)
        kx = np.arange(kw)

        # absolute coordinates of kernel elements
        yy = y0[:, None, None, None] + ky[None, None, :, None]
        xx = x0[None, :, None, None] + kx[None, None, None, :]

        # create spatial masks
        spatial = np.zeros((out_h, out_w, h, w), dtype=bool)

        spatial[
            np.arange(out_h)[:, None, None, None],
            np.arange(out_w)[None, :, None, None],
            yy,
            xx,
        ] = True

        # duplicate for channels
        masks = spatial[:, :, None].repeat(c, axis=2)
        masks = masks.reshape(-1, c, h, w)

        return masks

class MTensor4D(MTensorGeneral):
    def __init__(
        self,
        block_gap: float = 0.5,
        **kwargs,
    ):
        self.block_gap = block_gap
        super().__init__(**kwargs)
    
    def _create_mobs(
        self,
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        b, c, h, w = self.shape

        xs = [RIGHT * l * self.step for l in range(w)]
        ys = [DOWN * k * self.step for k in range(h)]
        zs = [IN * j * self.step for j in range(c)]

        for i in range(b):
            for j, k, l in np.ndindex((c, h, w)):
                cube = self._make_cube(
                    value=self.array[i, j, k, l],
                    z_index=(c-j) * h + k,        # z_index
                )
                cube.shift(xs[l] + ys[k] + zs[j])
                objs[i, j, k, l] = cube
        
        blocks = VGroup(VGroup(*objs[i].flat) for i in range(b))
        if self.style == 'horizontal':
            blocks.arrange(RIGHT, buff=self.block_gap)
        elif self.style == 'vertical':
            blocks.arrange(DOWN, buff=self.block_gap)
        mobs = VGroup(*objs.flat).center()
        return objs, mobs
    
    def to_3ds(
        self,
    ) -> list:
        vgs = [
            MTensor3D(
                objs=self.objs[i],
                mobs=self[i],
                array=self.array[i],
                mode=self.mode,
                style=self.style,
                side_length=self.side_length,
                font_size=self.font_size,
                padding=self.padding,
                cube_config=self.cube_config,
                square_config=self.square_config,
                decimal_config=self.decimal_config,
            ) for i in range(self.shape[0])
        ]
        return vgs

    def create(
        self,
        style: str | None = None,
        direction: np.ndarray = OUT,
        anim: Animation = GrowFromCenter,
        **gargs,
    ) -> AnimationGroup:
        """based on implementation of 3d.
        """
        blocks = self.to_3ds()
        anims = AnimationGroup(
            *(block.create(
                style=style,
                direction=direction,
                anim=anim,
            ) for block in blocks),
            **gargs,
        )
        return anims

    def translate(
        self,
        style: str | None = None,
        direction: np.ndarray = DOWN,
        **gargs,
    ) -> AnimationGroup:
        """based on implementation of 3d.
        """
        blocks = self.to_3ds()
        anims = AnimationGroup(
            *(block.translate(
                style=style,
                direction=direction,
            ) for block in blocks),
            **gargs,
        )
        return anims

    def breath(
        self,
        style: str | None = None,
        direction: np.ndarray = DOWN,
        **gargs,
    ) -> AnimationGroup:
        """based on implementation of 3d.
        """
        blocks = self.to_3ds()
        anims = AnimationGroup(
            *(block.breath(
                style=style,
                direction=direction,
            ) for block in blocks),
            **gargs,
        )
        return anims
    
    def switch(
        self,
        style: str | None = None,
        direction: np.ndarray = OUT,
        **gargs,
    ) -> Animation:
        """based on implementation of 3d.
        """
        self.mode = 'cube' if self.mode == 'card' else 'card'

        blocks = self.to_3ds()
        anims = AnimationGroup(
            *(block.switch(
                style=style,
                direction=direction,
            ) for block in blocks),
            **gargs,
        )
        return anims

    def uncreate(
        self,
        style: str | None = None,
        direction: np.ndarray = DOWN,
        anim: Animation = ShrinkToCenter,
        **gargs,
    ) -> AnimationGroup:
        """based on implementation of 3d.
        """
        blocks = self.to_3ds()
        anims = AnimationGroup(
            *(block.create(
                style=style,
                direction=direction,
                anim=anim,
            ) for block in blocks),
            **gargs,
        )
        return anims

class Demo1D(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        tensor = MTensor1D(
            array=np.random.randn(15),
            mode='cube',
            style='erect',
            side_length=0.5,
            font_size=18,
            padding=0.0,
        )

        self.play(tensor.create(
            direction=RIGHT,
            run_time=1.0,
        ))
        self.wait()

        m1 = np.eye(15, dtype=bool)
        m2 = np.triu(np.ones((15, 15), dtype=bool))[::-1][1:]
        masks = np.concatenate([m1, m2], axis=0)
        self.play(tensor.highlight_loop(
            masks=masks,
            back=False,
            run_time=3.0,
        ))
        self.wait()

        self.play(tensor.switch(
            direction=RIGHT,
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.update_values(
            values=np.random.randn(15),
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.switch(
            direction=LEFT,
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.uncreate(
            direction=RIGHT,
            run_time=1.0,
        ))
        self.wait()

class Demo2D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        tensor = MTensor2D(
            array=np.random.randn(7,9),
            mode='cube',
            style='horizontal',
            side_length=0.5,
            font_size=18,
            padding=0.0,
        )

        self.play(tensor.create(
            style='beam',
            direction=RIGHT,
            run_time=1.0,
        ))
        self.wait()

        masks=np.eye(9,dtype=bool)[:,None,:].repeat(7,axis=1)
        masks = np.concat([masks, masks[::-1][1:]], axis=0)
        self.play(tensor.highlight_loop(
            masks=masks,
            back=False,
            run_time=3.0,
        ))
        self.wait()

        self.play(tensor.highlight(
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.switch(
            style='beam',
            direction=DOWN,
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.update_values(
            values=np.random.randn(7,9),
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.uncreate(
            style='beam',
            direction=LEFT,
            run_time=1.0,
        ))
        self.wait()


class Demo3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        tensor = MTensor3D(
            array=np.random.randn(6,4,4),
            mode='cube',
            side_length=0.5,
            font_size=18,
            padding=0.0,
        )

        self.play(tensor.create(
            style='beam',
            direction=RIGHT,
            run_time=1.0,
        ))
        self.wait()

        masks = np.tile(
            np.eye(6,dtype=bool)[:,:,None,None],
            (1,1,4,4),
        )
        self.play(tensor.highlight_loop(
            masks=masks,
            back=True,
            run_time=3.0,
        ))
        self.wait()

        # self.play(tensor.switch(
        #     style='beam',
        #     direction=DOWN,
        #     run_time=1.0,
        # ))
        # self.wait()

        # self.play(tensor.update_values(
        #     values=np.random.randn(6,4,4),
        #     run_time=1.0,
        # ))
        # self.wait()

        self.play(tensor.uncreate(
            style='beam',
            direction=LEFT,
            run_time=1.0,
        ))
        self.wait()

class Demo4D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )

        tensor = MTensor4D(
            block_gap=0.3,
            array=np.random.randn(10,7,2,2),
            mode='cube',
            style='horizontal',
            side_length=0.3,
            font_size=12,
            padding=0.0,
        )

        self.play(tensor.create(
            style='beam',
            direction=OUT,
            run_time=1.0,
            lag_ratio=0.5,
        ))
        self.wait()

        masks = np.tile(
            np.eye(10,dtype=bool)[:,:,None,None,None],
            (1,1,7,2,2),
        )
        self.play(tensor.highlight_loop(
            masks=masks,
            back=True,
            run_time=3.0,
        ))
        self.wait()

        # self.play(tensor.switch(
        #     style='beam',
        #     direction=IN,
        #     run_time=1.0,
        #     lag_ratio=0.5,
        # ))
        # self.wait()

        # self.play(tensor.update_values(
        #     values=np.random.randn(5,4,3,3),
        #     run_time=1.0,
        # ))
        # self.wait()

        self.play(tensor.uncreate(
            style='beam',
            direction=IN,
            run_time=1.0,
        ))
        self.wait()
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
            objs, mobs = self.create_mobs(style)
        self.objs = objs
        self.mobs = mobs
        self.add(self.mobs)

    def make_cube(
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
    
    def update_values(
        self,
        values: torch.Tensor | np.ndarray,
        **aargs,
    ) -> Animation:
        """!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        NOTE: update manim ChangeDecimalToValue source to sync z_index.
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        assert self.mode == 'card', "update_value only works in 'card' mode"
        if isinstance(values, torch.Tensor):
            self.tensor = values
            self.array = values.numpy()
        else:
            self.array = values

        anims = AnimationGroup(
            *(mob.update_value(value)
            for mob, value in zip(self.mobs, self.array.flat)),
            **aargs,
        )
        return anims

    def loop_anims(self):
        raise NotImplementedError

    def create(
        self,
        style: str | None = None,
        direction: np.ndarray = DOWN,
        anim: Animation = GrowFromCenter,
        **gargs,
    ) -> AnimationGroup:
        if anim is GrowFromCenter:
            aargs = {'rate_func': rate_functions.ease_out_back}
        else:
            aargs = {}
        anims = self.loop_anims(
            style=style,
            direction=direction,
            anim=anim,
            aargs=aargs,
            gargs=gargs,
            _on_finish=lambda s: s.add(self),
        )
        return anims

    def switch(
        self,
        style: str | None = None,
        direction: np.ndarray = DOWN,
        **gargs,
    ) -> AnimationGroup:
        self.mode = 'cube' if self.mode == 'card' else 'card'

        anims = self.loop_anims(
            style=style,
            direction=direction,
            anim=lambda mob, **aargs: mob.switch(**aargs),
            gargs=gargs,
        )
        return anims

    def uncreate(
        self,
        style: str | None = None,
        direction: np.ndarray = DOWN,
        anim: Animation = ShrinkToCenter,
        **gargs,
    ) -> AnimationGroup:
        aargs = {}
        anims = self.loop_anims(
            style=style,
            direction=direction,
            anim=anim,
            aargs=aargs,
            gargs=gargs,
            _on_finish=lambda s: s.remove(self),
        )
        return anims

    @property
    def shape(self):
        return self.array.shape

    @property
    def ndim(self):
        return self.array.ndim

class MTensor1D(MTensorGeneral):
    def __init__(
        self,
        style: str = 'horizontal',
        **kwargs,
    ):
        super().__init__(
            style=style,
            **kwargs,
        )

    def create_mobs(
        self,
        style: str = 'horizontal',
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        w = self.shape[0]
        step = self.side_length + self.padding

        if style == 'horizontal':
            xs = [RIGHT * i * step for i in range(w)]
        elif style == 'vertical':
            xs = [DOWN * i * step for i in range(w)]
        elif style == 'erect':
            xs = [IN * i * step for i in range(w)]

        for i in range(w):
            if style == 'horizontal':
                z_index = w - i
            elif style == 'vertical':
                z_index = i
            elif style == 'erect':
                z_index = w - i

            cube = self.make_cube(
                value=self.array[i],
                z_index=z_index,
            )
            cube.shift(xs[i])
            objs[i] = cube

        mobs = VGroup(*objs.flat).center()
        return objs, mobs

    def loop_anims(
        self,
        style: str | None,  # not used
        direction: np.ndarray,
        anim: Animation,
        aargs: dict = {},   # unit anim args
        gargs: dict = {},   # run_time
        **kwargs,           # _on_finish
    ) -> Animation:
        if np.array_equal(direction, RIGHT):
            anims = AnimationGroup(
                *(anim(mob, **aargs) for mob in self.mobs),
                rate_func=smooth,
                lag_ratio=0.5,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif np.array_equal(direction, LEFT):
            anims = AnimationGroup(
                *(anim(mob, **aargs) for mob in self.mobs[::-1]),
                rate_func=smooth,
                lag_ratio=0.5,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        return anims

class MTensor2D(MTensorGeneral):
    def __init__(
        self,
        style: str = 'horizontal',
        **kwargs,
    ):
        super().__init__(
            style=style,
            **kwargs,
        )

    def create_mobs(
        self,
        style: str = 'horizontal',
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        h, w = self.shape
        step = self.side_length + self.padding

        xs = [RIGHT * j * step for j in range(w)]
        if style == 'horizontal':
            ys = [DOWN * i * step for i in range(h)]
        elif style == 'erect':
            ys = [IN * i * step for i in range(h)]

        for i, j in np.ndindex(self.shape):
            if style == 'horizontal':
                z_index = i * w - j
            elif style == 'erect':
                z_index = (h-i) * w - j

            cube = self.make_cube(
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

    def loop_anims(
        self,
        style: str | None,
        direction: np.ndarray,
        anim: Animation,
        aargs: dict = {},   # unit anim args
        gargs: dict = {},   # run_time
        **kwargs,           # _on_finish
    ) -> Animation:
        if style is None:
            if np.array_equal(direction, RIGHT):
                mobs = self.mobs
            elif np.array_equal(direction, LEFT):
                mobs = self.mobs[::-1]
            anims = AnimationGroup(
                *(anim(mob, **aargs) for mob in mobs),
                rate_func=smooth,
                lag_ratio=0.5,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'layer':
            vgs = self.get_layers(direction=direction)
            anims = Succession(
                *(AnimationGroup(
                    *(anim(mob, **aargs) for mob in vg),
                    lag_ratio=0.0,
                ) for vg in vgs),
                rate_func=smooth,
                lag_ratio=0.5,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'beam':
            if np.array_equal(direction, RIGHT):
                vgs = self.get_layers(DOWN, reverse=False)
            elif np.array_equal(direction, LEFT):
                vgs = self.get_layers(DOWN, reverse=True)
            elif np.array_equal(direction, DOWN):
                vgs = self.get_layers(RIGHT, reverse=False)
            elif np.array_equal(direction, UP):
                vgs = self.get_layers(RIGHT, reverse=True)
            anims = AnimationGroup(
                *(Succession(
                    *(anim(mob, **aargs) for mob in vg),
                    run_time=random.random()+1,
                    lag_ratio=0.8,
                    rate_func=smooth,
                ) for vg in vgs),
                lag_ratio=0.0,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        return anims

class MTensor3D(MTensorGeneral):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    def create_mobs(
        self,
        style: str | None = None,   # not used
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        c, h, w = self.shape
        step = self.side_length + self.padding

        xs = [RIGHT * k * step for k in range(w)]
        ys = [DOWN * j * step for j in range(h)]
        zs = [IN * i * step for i in range(c)]

        for i, j, k in np.ndindex(self.shape):
            cube = self.make_cube(
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

    # def create_mobs_padded(
    #     self,
    #     array: np.ndarray | None = None,
    #     reuse_objs: np.ndarray | None = None,
    #     offset: tuple = (0, 0, 0),
    #     z_style: str | None = None,
    #     pad_cube_config: dict = {},
    #     pad_square_config: dict = {},
    #     pad_decimal_config: dict = {},
    # ) -> tuple:
    #     if array is None:
    #         array = self.array
    #     if offset is None:
    #         offset = (0, 0, 0)

    #     do_pad = reuse_objs is not None

    #     objs = np.empty(array.shape, dtype=object)
    #     c, h, w = array.shape
    #     step = self.side_length + self.padding

    #     offset = tuple(int(v) for v in offset)
    #     xs = [RIGHT * k * step for k in range(w)]
    #     ys = [DOWN * j * step for j in range(h)]
    #     zs = [IN * i * step for i in range(c)]

    #     if do_pad:
    #         orig_ul = reuse_objs[0,0,0].get_corner(UL)

    #     for i, j, k in np.ndindex(array.shape):
    #         src_idx = (i - offset[0], j - offset[1], k - offset[2])
    #         reuse_cube = None
    #         if (
    #             do_pad and len(reuse_objs.shape) == 3
    #             and all(0 <= src_idx[d] < reuse_objs.shape[d] for d in range(3))
    #         ):
    #             reuse_cube = reuse_objs[src_idx]

    #         if reuse_cube is not None:
    #             cube = reuse_cube.center()
    #         else:
    #             cube = self.make_cube(
    #                 array[i, j, k],
    #                 (c-i)*h+j,          # z_index
    #                 pad_cube_config if do_pad else {},
    #                 pad_square_config if do_pad else {},
    #                 pad_decimal_config if do_pad else {},
    #             ).center()

    #         cube.shift(xs[k] + ys[j] + zs[i])
    #         # cube.set_z_index((c - i) * h + j)
    #         objs[i, j, k] = cube
        
    #     mobs = VGroup(*objs.flat)

    #     # align to old or center
    #     if reuse_objs is not None:
    #         shift_mobs = orig_ul - objs[*offset].get_corner(UL)
    #         mobs.shift(shift_mobs)
    #     else:
    #         mobs.center()

    #     return objs, mobs
    
    # def create_conv2d_masks(
    #     self,
    #     conv2d_config: dict,
    # ) -> list:
    #     """Return a list of boolean masks for Conv2d-style sliding windows.

    #     The masks are ordered row-major over output positions (top-to-bottom,
    #     left-to-right), and each mask marks the input cubes that participate in
    #     the corresponding kernel application.
    #     """
    #     if self.ndim != 3:
    #         raise ValueError("create_conv2d_masks only supports 3D tensors")

    #     def _normalize_pair(value, default=(1, 1)):
    #         if isinstance(value, (tuple, list)):
    #             if len(value) != 2:
    #                 raise ValueError("expected a 2-tuple/list for spatial parameter")
    #             return int(value[0]), int(value[1])
    #         return int(value), int(value)

    #     kernel_size = conv2d_config.get('kernel_size', 3)
    #     stride = conv2d_config.get('stride', 1)

    #     kernel_h, kernel_w = _normalize_pair(kernel_size)
    #     stride_h, stride_w = _normalize_pair(stride)

    #     c, h, w = self.shape
    #     out_h = (h - kernel_h) // stride_h + 1
    #     out_w = (w - kernel_w) // stride_w + 1

    #     masks = []
    #     for out_i in range(out_h):
    #         for out_j in range(out_w):
    #             mask = np.zeros(self.shape, dtype=bool)
    #             in_i_start = out_i * stride_h
    #             in_i_end = in_i_start + kernel_h
    #             in_j_start = out_j * stride_w
    #             in_j_end = in_j_start + kernel_w

    #             for i in range(in_i_start, min(h, in_i_end)):
    #                 for j in range(in_j_start, min(w, in_j_end)):
    #                     mask[:, i, j] = True

    #             masks.append(mask)

    #     return masks
    
    # def get_beams(
    #     self,
    #     direction=OUT,
    # ) -> VGroup:
    #     direction = direction.astype(np.int32)
    #     c, h, w = self.shape
    #     if direction[0] != 0:
    #         vgs = VGroup(
    #             self[i,j,:][::direction[0]]
    #             for i, j in itertools.product(range(c), range(h))
    #         )
    #     elif direction[1] != 0:
    #         vgs = VGroup(
    #             self[i,:,k][::-direction[1]]
    #             for i, k in itertools.product(range(c), range(w))
    #         )
    #     elif direction[2] != 0:
    #         vgs = VGroup(
    #             self[:,j,k][::-direction[2]]
    #             for j, k in itertools.product(range(h), range(w))
    #         )
    #     return vgs

    # def get_layers(
    #     self,
    #     direction=OUT,
    # ) -> VGroup:
    #     direction = direction.astype(np.int32)
    #     c, h, w = self.shape
    #     if direction[0] != 0:
    #         vgs = VGroup(self[:,:,k] for k in range(w))
    #         vgs = vgs[::direction[0]]
    #     elif direction[1] != 0:
    #         vgs = VGroup(self[:,j,:] for j in range(h))
    #         vgs = vgs[::-direction[1]]
    #     elif direction[2] != 0:
    #         vgs = VGroup(self[i,:,:] for i in range(c))
    #         vgs = vgs[::-direction[2]]
    #     return vgs

    def loop_anims(
        self,
        style: str,
        direction: np.ndarray,
        anim: Animation,
        aargs: dict = {},   # unit anim args
        gargs: dict = {},   # run_time
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
                lag_ratio=0.5,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'layer':
            layers = self.get_layers(direction=direction)
            anims = Succession(
                *(AnimationGroup(
                    *(anim(mob, **aargs) for mob in layer),
                    lag_ratio=0.0,
                ) for layer in layers),
                rate_func=smooth,
                lag_ratio=0.5,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        elif style == 'beam':
            vgs = self.get_beams(direction=direction)
            anims = AnimationGroup(
                *(Succession(
                    *(anim(mob, **aargs) for mob in beam),
                    run_time=random.random()+1,
                    lag_ratio=0.8,
                    rate_func=smooth,
                ) for beam in vgs),
                lag_ratio=0.0,
                **gargs,        # run_time
                **kwargs,       # _on_finish
            )
        return anims

    # def switch_mode(
    #     self,
    #     style: str = 'layer',
    #     direction: np.ndarray = OUT,
    #     aargs: dict = {},
    # ) -> Animation:
    #     if self.mode == 'card':
    #         self.mode = 'cube'
    #     elif self.mode == 'cube':
    #         self.mode = 'card'

    #     if style == 'layer':
    #         layers = self.get_layers(direction=direction)
    #         anims = AnimationGroup(
    #             *(AnimationGroup(
    #                 *(cube.switch_mode() for cube in layer),
    #                 lag_ratio=0.0,
    #             ) for layer in layers),
    #             rate_func=smooth,
    #             **aargs,
    #         )
    #         return anims
    #     elif style == 'beam':
    #         beams = self.get_beams(direction=direction)
    #         anims = AnimationGroup(
    #             *(AnimationGroup(
    #                 *(cube.switch_mode() for cube in beam),
    #                 run_time=random.random()+1,
    #                 lag_ratio=0.8,
    #                 rate_func=smooth,
    #             ) for beam in beams),
    #             lag_ratio=0.0,
    #             **aargs,
    #         )
    #         return anims

    # def create(
    #     self,
    #     style='layer',
    #     direction=OUT,
    #     anim=Create,
    #     aargs: dict = {},
    #     gargs: dict = {},
    # ) -> AnimationGroup:
    #     if style == 'layer':
    #         layers = self.get_layers(direction=direction)
    #         anims = Succession(
    #             *(AnimationGroup(
    #                 *(anim(cube, **aargs) for cube in layer),
    #                 lag_ratio=0.0,
    #             ) for layer in layers),
    #             rate_func=smooth,
    #             **gargs,
    #         )
    #         return anims
    #     elif style == 'beam':
    #         beams = self.get_beams(direction=direction)
    #         anims = AnimationGroup(
    #             *(Succession(
    #                 *(anim(cube, **aargs) for cube in beam),
    #                 run_time=random.random()+1,
    #                 rate_func=smooth,
    #             ) for beam in beams),
    #             lag_ratio=0.0,
    #             **gargs,
    #         )
    #         return anims
    
    # def create_index(
    #     self,
    #     index,
    #     anim=Create,
    #     aargs: dict = {},
    # ) -> Animation:
    #     mob = self[index]
    #     return anim(mob, **aargs)

    # def uncreate(
    #     self,
    #     style='layer',
    #     direction=OUT,
    #     anim=Uncreate,
    #     aargs: dict = {},
    #     gargs: dict = {},
    # ) -> AnimationGroup:
    #     anims = self.create(
    #         style=style,
    #         direction=direction,
    #         anim=anim,
    #         aargs=aargs,
    #         gargs=gargs,
    #     )
    #     return anims

    # def highlight_layer(
    #     self,
    #     direction = IN,
    #     n: int = 0,
    #     **aargs,
    # ) -> Animation:
    #     if direction[0] != 0:
    #         d = int(direction[0])
    #         mask = np.full_like(self.hl_state, False, dtype=bool)
    #         mask[:,:,d*n+(d-1)//2] = True
    #     elif direction[1] != 0:
    #         d = int(direction[1])
    #         mask = np.full_like(self.hl_state, False, dtype=bool)
    #         mask[:,-d*n-(d+1)//2,:] = True
    #     elif direction[2] != 0:
    #         d = int(direction[2])
    #         mask = np.full_like(self.hl_state, False, dtype=bool)
    #         mask[-d*n-(d+1)//2,:,:] = True
    #     anims = self.highlight(mask=mask, **aargs)
    #     return anims
    
    # def highlight_beam(
    #     self,
    #     direction = IN,
    #     ij: tuple = (0, 0),
    #     **aargs,
    # ) -> Animation:
    #     if direction[0] != 0:
    #         mask = np.full_like(self.hl_state, False, dtype=bool)
    #         mask[ij[0], ij[1], :] = True
    #     elif direction[1] != 0:
    #         mask = np.full_like(self.hl_state, False, dtype=bool)
    #         mask[ij[0], :, ij[1]] = True
    #     elif direction[2] != 0:
    #         mask = np.full_like(self.hl_state, False, dtype=bool)
    #         mask[:, ij[0], ij[1]] = True
    #     anims = self.highlight(mask=mask, **aargs)
    #     return anims

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
        step = self.side_length + self.padding

        orig_center = self.objs[0,0,0].get_center()

        xs = [RIGHT * k * step for k in range(w_new)]
        ys = [DOWN * j * step for j in range(h_new)]
        zs = [IN * i * step for i in range(c_new)]
        for i, j, k in np.ndindex(array_new.shape):
            if not mask_pad[i,j,k]:
                mob = self.objs[i-pad_c, j-pad_h, k-pad_w]
                mob.set_z_index((c_new-i)*h_new+j)
                mob.center()
            else:
                mob = self.make_cube(
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
        self.shape = self.array.shape
        self.ndim = self.array.ndim
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
        self.shape = self.array.shape
        self.ndim = self.array.ndim
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

    def highlight_loop_conv2d_mask(
        self,
        kernel_size,
        stride,
    ) -> list:
        c, h, w = self.shape
        out_h = (h - kernel_size) // stride + 1
        out_w = (w - kernel_size) // stride + 1
        masks = []
        for out_i in range(out_h):
            for out_j in range(out_w):
                mask = np.zeros(self.shape, dtype=bool)
                in_i_start = out_i * stride
                in_i_end = in_i_start + kernel_size
                in_j_start = out_j * stride
                in_j_end = in_j_start + kernel_size

                mask[:, in_i_start:in_i_end, in_j_start:in_j_end] = True
                masks.append(mask)
        return masks
    
    def highlight_loop_conv2d(
        self,
        kernel_size: int = 3,
        stride: int = 1,
        back: bool = True,
        **aargs,
    ) -> AnimationGroup:
        masks = self.highlight_loop_conv2d_mask(
            kernel_size=kernel_size,
            stride=stride,
        )
        return self.highlight_loop(
            masks=masks,
            back=back,
            **aargs,
        )
    
class MTensor4D(MTensorGeneral):
    def __init__(
        self,
        block_gap: float = 0.5,
        **kwargs,
    ):
        self.block_gap = block_gap
        super().__init__(**kwargs)
    
    def create_mobs(
        self,
        style: str = 'horizontal',
    ):
        objs = np.empty(self.shape, dtype=object)
        b, c, h, w = self.shape
        step = self.side_length + self.padding
        # blocks = VGroup()

        xs = [RIGHT * l * step for l in range(w)]
        ys = [DOWN * k * step for k in range(h)]
        zs = [IN * j * step for j in range(c)]

        for i in range(b):
            # block_objs = np.empty((c, h, w), dtype=object)
            for j, k, l in np.ndindex((c, h, w)):
                cube = self.make_cube(
                    value=self.array[i, j, k, l],
                    z_index=(c-j) * h + k,        # z_index
                )
                cube.shift(xs[l] + ys[k] + zs[j])
                # block_objs[j, k, l] = cube
                objs[i, j, k, l] = cube

            # block_mobs = VGroup(*block_objs.flat).center()
            # blocks.add(block_mobs)
        
        blocks = VGroup(VGroup(*objs[i].flat) for i in range(b))
        if style == 'horizontal':
            blocks.arrange(RIGHT, buff=self.block_gap)
        elif style == 'vertical':
            blocks.arrange(DOWN, buff=self.block_gap)
        mobs = VGroup(*objs.flat).center()
        return objs, mobs

        # blocks.arrange(self.block_direction, self.block_gap)
        # mobs = VGroup(*(mob for block in blocks for mob in block))
        # return objs, mobs
    
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
    
    # def highlight_block(
    #     self,
    #     direction = RIGHT,
    #     n: int = 0,
    #     **aargs,
    # ) -> Animation:
    #     d = int(direction[0])
    #     mask = np.full_like(self.hl_state, False, dtype=bool)
    #     mask[d*n+(d-1)//2] = True
    #     anims = self.highlight(mask=mask, **aargs)
    #     return anims

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

        self.play(tensor.switch(
            style='beam',
            direction=DOWN,
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.update_values(
            values=np.random.randn(6,4,4),
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.uncreate(
            style='beam',
            direction=LEFT,
            run_time=1.0,
        ))
        self.wait()

class Demo4D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)

        tensor = MTensor4D(
            block_direction=RIGHT,
            block_gap=0.3,
            array=np.random.randn(5,4,3,3),
            mode='cube',
            size=0.3,
            padding=0.0,
        )

        self.play(tensor.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={'lag_ratio': 0.3, 'run_time': 1.0},
        ))
        self.wait()

        self.move_camera(
            phi=60*DEGREES,
            theta=-135*DEGREES,
            run_time=1.0,
        )
        self.wait()

        self.play(tensor.switch_mode(
            style='beam',
            direction=IN,
            aargs={},
            gargs={'run_time': 1.0},
        ))
        self.wait()

        self.play(tensor.uncreate(
            style='beam',
            direction=IN,
            anim=ShrinkToCenter,
            aargs={},
            gargs={},
            ggargs={'lag_ratio': 0.3, 'run_time': 1.0},
        ))
        self.wait()
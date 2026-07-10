from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
import itertools
import random
from enum import Enum
import numpy as np

from manim.utils.rate_functions import ease_in_quart

DEFAULT_CUBE_CONFIG = {
    'side_length': 0.3,
    'fill_color': BLACK,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}

DEFAULT_SQUARE_CONFIG = {
    'side_length': 0.3,
    'fill_color': BLACK,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}

DEFAULT_DECIMAL_CONFIG = {
    'num_decimal_places': 2,
    'mob_class': MathTex,
    'include_sign': True,
    'font_size': 10,
    'fill_opacity': 1.0,
}

class MCube(VMobject):
    def __init__(
        self,
        value: float = 0.0,
        size: float = 0.5,
        mode: str ='card',
        cube_config: dict = {},
        square_config: dict = {},
        decimal_config: dict = {},
    ):
        super().__init__()
        self.value = value
        self.cube_config = { **DEFAULT_CUBE_CONFIG, **cube_config }
        self.square_config = { **DEFAULT_SQUARE_CONFIG, **square_config }
        self.decimal_config = { **DEFAULT_DECIMAL_CONFIG, **decimal_config }

        self.mode = mode
        if mode == 'card':
            square_config = {**self.square_config, 'side_length': size}
            self.mob = VGroup(
                Square(**square_config),
                DecimalNumber(self.value, **self.decimal_config),
            )
        elif mode == 'cube':
            cube_config = {**self.cube_config, 'side_length': size}
            self.mob = Cube(**cube_config)

        self.add(self.mob)
    
    def switch_mode(
        self,
        **aargs,
    ) -> Animation:
        # new mob according to current mode
        if self.mode == 'card':
            self.cube_config = {**self.cube_config, 'side_length': self.mob.width}
            new_mob = Cube(**self.cube_config)
            self.mode = 'cube'
        elif self.mode == 'cube':
            self.square_config = {**self.square_config, 'side_length': self.mob.width}
            new_mob = VGroup(
                Square(**self.square_config),
                DecimalNumber(self.value, **self.decimal_config),
            )
            self.mode = 'card'
        new_mob.move_to(self.mob)

        # remove current mob
        anims = []
        anims.append(Unwrite(self.mob))
        self.remove(self.mob)

        # add new mob
        self.mob = new_mob
        self.add(self.mob)
        anims.append(Write(self.mob))
        return AnimationGroup(
            *anims,
            **aargs,
        )
    
    def update_value(
        self,
        value: float = 0.0,
        **aargs,
    ) -> Animation:
        assert self.mode == 'card', "update_value only works in 'card' mode"
        self.value = value

        return ChangeDecimalToValue(
            self.mob[1],
            self.value,
            **aargs,
        )

class MTensorGeneral(VMobject):
    def __init__(
        self,
        objs: list | None = None,
        mobs: VGroup | None = None,
        array: np.ndarray | None = None,
        mode: str = 'cube',
        size: float = 0.5,
        padding: float = 0.1,
        cube_config: dict = {},
        square_config: dict = {},
        decimal_config: dict = {},
    ):
        super().__init__()
        self.array = array
        self.shape = array.shape
        self.ndim = array.ndim
        self.size = size
        self.mode = mode
        self.padding = padding
        self.cube_config = {**DEFAULT_CUBE_CONFIG, **cube_config}
        self.square_config = {**DEFAULT_SQUARE_CONFIG, **square_config}
        self.decimal_config = {**DEFAULT_DECIMAL_CONFIG, **decimal_config}

        self.hl_state = np.full(self.shape, True, dtype=bool)

        if objs is None and mobs is None:
            objs, mobs = self.create_mobs()
        self.objs = objs
        self.mobs = mobs
        self.add(self.mobs)
    
    def __getitem__(
        self,
        idx,
    ) -> VMobject:
        res = self.objs[idx]
        if isinstance(res, MCube):
            return res
        return VGroup(*res.flat)

    def make_cube(
        self,
        value,
        cube_config: dict = {},     # override internal
        square_config: dict = {},   # override internal
        decimal_config: dict = {},  # override internal
    ):
        return MCube(
            value=float(value),
            size=self.size,
            mode=self.mode,
            cube_config={**self.cube_config, **cube_config},
            square_config={**self.square_config, **square_config},
            decimal_config={**self.decimal_config, **decimal_config},
        )
    
    def create_mobs(self) -> tuple:
        raise NotImplementedError("not implement")
    
    def switch_mode(self) -> Animation:
        raise NotImplementedError("not implement")
    
    def create(self) -> Animation:
        raise NotImplementedError("not implement")

    def uncreate(self) -> Animation:
        raise NotImplementedError("not implement")

    def highlight(
        self,
        mask,
        **aargs,
    ) -> Animation:
        if mask is None:
            mask = np.full(self.shape, True, dtype=bool)
        mask_hl = ~self.hl_state & mask
        mask_dim = ~mask & self.hl_state

        anims = []
        for idx_list in np.argwhere(mask_dim):
            idx_tuple = tuple(idx_list.tolist())
            self[*idx_tuple].save_state()
            anims.append(self[*idx_tuple].animate.fade(0.995))
        for idx_list in np.argwhere(mask_hl):
            idx_tuple = tuple(idx_list.tolist())
            anims.append(self[*idx_tuple].animate.restore())
        self.hl_state = mask

        return AnimationGroup(
            *anims,
            **aargs,
        )

class MTensor_1D(MTensorGeneral):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
    
    def create_mobs(
        self,
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        step = self.size + self.padding

        for i in range(self.shape[0]):
            cube = self.make_cube(self.array[i])
            cube.shift(RIGHT * i * step)
            cube.set_z_index(self.shape[0] - i)
            objs[i] = cube

        mobs = VGroup(*objs.flat).center()
        return objs, mobs
    
    def get_mobs(
        self,
        direction=RIGHT,
    ) -> VGroup:
        direction = direction.astype(np.int32)
        vgs = self.mobs
        if direction[0] < 0:        # LEFT
            vgs = vgs[::-1]
        return vgs
    
    def switch_mode(
        self,
        direction: np.ndarray = RIGHT,
        aargs: dict = {},
    ) -> Animation:
        mobs = self.get_mobs(direction=direction)
        anims = AnimationGroup(
            *(cube.switch_mode() for cube in mobs),
            lag_ratio=0.8,
            rate_func=smooth,
            **aargs,
        )
        return anims
    
    def create(
        self,
        direction: np.ndarray = RIGHT,
        anim=Create,
        aargs: dict = {},
        gargs: dict = {},
    ) -> AnimationGroup:
        mobs = self.get_mobs(direction=direction)
        anims = AnimationGroup(
            *(anim(cube, **aargs) for cube in mobs),
            rate_func=smooth,
            **gargs,
        )
        return anims
    
    def uncreate(
        self,
        direction: np.ndarray = DOWN,
        anim = Uncreate,
        aargs: dict = {},
        gargs: dict = {},
    ) -> AnimationGroup:
        anims = self.create(
            direction=direction,
            anim=anim,
            aargs=aargs,
            gargs=gargs,
        )
        return anims
    
    def highlight_mob(
        self,
        direction = RIGHT,
        n: int = 0,
        **aargs,
    ) -> Animation:
        d = int(direction[0])
        mask = np.full_like(self.hl_state, False, dtype=bool)
        mask[d*n+(d-1)//2] = True
        anims = self.highlight(mask=mask, **aargs)
        return anims
    
    def highlight_mob_loop(
        self,
        direction = RIGHT,
        **aargs,
    ):
        """FIXME
        Example usage:
            for mob in tensor.get_mobs():
                mob.save_state()
            self.play(tensor.highlight_mob(
                direction=RIGHT,
                n=0,
                run_time=1.0,
            ))
            self.wait()
            self.play(tensor.highlight_mob_loop(
                direction=RIGHT,
                run_time=1.0,
            ))
            self.play(tensor.highlight_mob_loop(
                direction=LEFT,
                run_time=1.0,
            ))
            self.wait()
        """
        vg1 = self.get_mobs(direction=direction)[:-1]
        vg2 = self.get_mobs(direction=direction)[1:]
        return Succession(
            *(AnimationGroup(
                ApplyMethod(hide_mob.fade, 0.8),
                ApplyMethod(show_mob.restore),
                lag_ratio=0.0,
            ) for hide_mob, show_mob in zip(vg1, vg2)),
            rate_func=rate_functions.smooth,
            **aargs,
        )

class MTensor_2D(MTensorGeneral):
    """Only layer animations are implemented.
    """
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def create_mobs(
        self,
    ) -> tuple:
        objs = np.empty(self.shape, dtype=object)
        step = self.size + self.padding

        xs = [RIGHT * j * step for j in range(self.shape[1])]
        ys = [DOWN * i * step for i in range(self.shape[0])]

        for i, j in np.ndindex(self.shape):
            cube = self.make_cube(self.array[i, j])
            cube.shift(xs[j] + ys[i])
            cube.set_z_index((self.shape[0] - i) * self.shape[1] + (self.shape[1] - j))
            objs[i, j] = cube

        mobs = VGroup(*objs.flat).center()
        return objs, mobs
    
    def get_rows(
        self,
        direction=DOWN,
    ) -> VGroup:
        direction = direction.astype(np.int32)
        h, w = self.shape
        vgs = VGroup(self[i,:] for i in range(h))
        if direction[1] > 0:        # UP
            vgs = vgs[::-1]
        return vgs
    
    def get_cols(
        self,
        direction=RIGHT,
    ) -> VGroup:
        direction = direction.astype(np.int32)
        h, w = self.shape
        vgs = VGroup(self[:,j] for j in range(w))
        if direction[0] < 0:        # LEFT
            vgs = vgs[::-1]
        return vgs

    def switch_mode(
        self,
        direction: np.ndarray = DOWN,
        aargs: dict = {},
    ) -> Animation:
        get_lines = self.get_cols if direction[0]!=0 else self.get_rows
        lines = get_lines(direction=direction)
        anims = AnimationGroup(
            *(AnimationGroup(
                *(cube.switch_mode() for cube in line),
                lag_ratio=0.0,
            ) for line in lines),
            lag_ratio=0.8,
            rate_func=smooth,
            **aargs
        )
        return anims
    
    def create(
        self,
        direction: np.ndarray = DOWN,
        anim=Create,
        aargs: dict = {},
        gargs: dict = {},
    ) -> AnimationGroup:
        get_lines = self.get_cols if direction[0]!=0 else self.get_rows
        lines = get_lines(direction=direction)
        anims = Succession(
            *(AnimationGroup(
                *(anim(cube, **aargs) for cube in line),
                lag_ratio=0.0,
            ) for line in lines),
            rate_func=smooth,
            **gargs
        )
        return anims

    def uncreate(
        self,
        direction: np.ndarray = DOWN,
        anim = Uncreate,
        aargs: dict = {},
        gargs: dict = {},
    ) -> AnimationGroup:
        anims = self.create(
            direction=direction,
            anim=anim,
            aargs=aargs,
            gargs=gargs,
        )
        return anims
    
    def highlight_row(
        self,
        direction = DOWN,
        n: int = 0,
        **aargs,
    ) -> Animation:
        d = int(direction[1])
        mask = np.full_like(self.hl_state, False, dtype=bool)
        mask[-d*n-(d+1)//2,:] = True
        anims = self.highlight(mask=mask, **aargs)
        return anims
    
    def highlight_col(
        self,
        direction = RIGHT,
        n: int = 0,
        **aargs,
    ) -> Animation:
        d = int(direction[0])
        mask = np.full_like(self.hl_state, False, dtype=bool)
        mask[:,d*n+(d-1)//2] = True
        anims = self.highlight(mask=mask, **aargs)
        return anims

class MTensor_3D(MTensorGeneral):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    # TODO: update 1d.. version like this, and make_cube into general
    def create_mobs(
        self,
        array: np.ndarray | None = None,
        reuse_objs: np.ndarray | None = None,
        offset: tuple = (0, 0, 0),
        pad_cube_config: dict = {},
        pad_square_config: dict = {},
        pad_decimal_config: dict = {},
    ) -> tuple:
        if array is None:
            array = self.array
        if offset is None:
            offset = (0, 0, 0)

        do_pad = reuse_objs is not None

        objs = np.empty(array.shape, dtype=object)
        c, h, w = array.shape
        step = self.size + self.padding

        offset = tuple(int(v) for v in offset)
        xs = [RIGHT * k * step for k in range(w)]
        ys = [DOWN * j * step for j in range(h)]
        zs = [IN * i * step for i in range(c)]

        if do_pad:
            orig_ul = reuse_objs[0,0,0].get_corner(UL)

        for i, j, k in np.ndindex(array.shape):
            src_idx = (i - offset[0], j - offset[1], k - offset[2])
            reuse_cube = None
            if (
                do_pad and len(reuse_objs.shape) == 3
                and all(0 <= src_idx[d] < reuse_objs.shape[d] for d in range(3))
            ):
                reuse_cube = reuse_objs[src_idx]

            if reuse_cube is not None:
                cube = reuse_cube.center()
            else:
                cube = self.make_cube(
                    array[i, j, k],
                    pad_cube_config if do_pad else {},
                    pad_square_config if do_pad else {},
                    pad_decimal_config if do_pad else {},
                ).center()

            cube.shift(xs[k] + ys[j] + zs[i])
            cube.set_z_index((c - i) * h + j)
            objs[i, j, k] = cube
        
        mobs = VGroup(*objs.flat)

        # align to old or center
        if reuse_objs is not None:
            shift_mobs = orig_ul - objs[*offset].get_corner(UL)
            mobs.shift(shift_mobs)
        else:
            mobs.center()

        return objs, mobs
    
    def create_conv2d_masks(
        self,
        conv2d_config: dict,
    ) -> list:
        """Return a list of boolean masks for Conv2d-style sliding windows.

        The masks are ordered row-major over output positions (top-to-bottom,
        left-to-right), and each mask marks the input cubes that participate in
        the corresponding kernel application.
        """
        if self.ndim != 3:
            raise ValueError("create_conv2d_masks only supports 3D tensors")

        def _normalize_pair(value, default=(1, 1)):
            if isinstance(value, (tuple, list)):
                if len(value) != 2:
                    raise ValueError("expected a 2-tuple/list for spatial parameter")
                return int(value[0]), int(value[1])
            return int(value), int(value)

        kernel_size = conv2d_config.get('kernel_size', 3)
        stride = conv2d_config.get('stride', 1)

        kernel_h, kernel_w = _normalize_pair(kernel_size)
        stride_h, stride_w = _normalize_pair(stride)

        c, h, w = self.shape
        out_h = (h - kernel_h) // stride_h + 1
        out_w = (w - kernel_w) // stride_w + 1

        masks = []
        for out_i in range(out_h):
            for out_j in range(out_w):
                mask = np.zeros(self.shape, dtype=bool)
                in_i_start = out_i * stride_h
                in_i_end = in_i_start + kernel_h
                in_j_start = out_j * stride_w
                in_j_end = in_j_start + kernel_w

                for i in range(in_i_start, min(h, in_i_end)):
                    for j in range(in_j_start, min(w, in_j_end)):
                        mask[:, i, j] = True

                masks.append(mask)

        return masks
    
    def get_beams(
        self,
        direction=OUT,
    ) -> VGroup:
        direction = direction.astype(np.int32)
        c, h, w = self.shape
        if direction[0] != 0:
            vgs = VGroup(
                self[i,j,:][::direction[0]]
                for i, j in itertools.product(range(c), range(h))
            )
        elif direction[1] != 0:
            vgs = VGroup(
                self[i,:,k][::-direction[1]]
                for i, k in itertools.product(range(c), range(w))
            )
        elif direction[2] != 0:
            vgs = VGroup(
                self[:,j,k][::-direction[2]]
                for j, k in itertools.product(range(h), range(w))
            )
        return vgs

    def get_layers(
        self,
        direction=OUT,
    ) -> VGroup:
        direction = direction.astype(np.int32)
        c, h, w = self.shape
        if direction[0] != 0:
            vgs = VGroup(self[:,:,k] for k in range(w))
            vgs = vgs[::direction[0]]
        elif direction[1] != 0:
            vgs = VGroup(self[:,j,:] for j in range(h))
            vgs = vgs[::-direction[1]]
        elif direction[2] != 0:
            vgs = VGroup(self[i,:,:] for i in range(c))
            vgs = vgs[::-direction[2]]
        return vgs

    def switch_mode(
        self,
        style: str = 'layer',
        direction: np.ndarray = OUT,
        aargs: dict = {},
    ) -> Animation:
        if style == 'layer':
            layers = self.get_layers(direction=direction)
            anims = Succession(
                *(AnimationGroup(
                    *(cube.switch_mode() for cube in layer),
                    lag_ratio=0.0,
                ) for layer in layers),
                rate_func=smooth,
                **aargs,
            )
            return anims
        elif style == 'beam':
            beams = self.get_beams(direction=direction)
            anims = AnimationGroup(
                *(AnimationGroup(
                    *(cube.switch_mode() for cube in beam),
                    run_time=random.random()+1,
                    lag_ratio=0.8,
                    rate_func=smooth,
                ) for beam in beams),
                lag_ratio=0.0,
                **aargs,
            )
            return anims

    def create(
        self,
        style='layer',
        direction=OUT,
        anim=Create,
        aargs: dict = {},
        gargs: dict = {},
    ) -> AnimationGroup:
        if style == 'layer':
            layers = self.get_layers(direction=direction)
            anims = Succession(
                *(AnimationGroup(
                    *(anim(cube, **aargs) for cube in layer),
                    lag_ratio=0.0,
                ) for layer in layers),
                rate_func=smooth,
                **gargs,
            )
            return anims
        elif style == 'beam':
            beams = self.get_beams(direction=direction)
            anims = AnimationGroup(
                *(Succession(
                    *(anim(cube, **aargs) for cube in beam),
                    run_time=random.random()+1,
                    rate_func=smooth,
                ) for beam in beams),
                lag_ratio=0.0,
                **gargs,
            )
            return anims
    
    def create_index(
        self,
        index,
        anim=Create,
        aargs: dict = {},
    ) -> Animation:
        mob = self[index]
        return anim(mob, **aargs)

    def uncreate(
        self,
        style='layer',
        direction=OUT,
        anim=Uncreate,
        aargs: dict = {},
        gargs: dict = {},
    ) -> AnimationGroup:
        anims = self.create(
            style=style,
            direction=direction,
            anim=anim,
            aargs=aargs,
            gargs=gargs,
        )
        return anims

    def highlight_layer(
        self,
        direction = IN,
        n: int = 0,
        **aargs,
    ) -> Animation:
        if direction[0] != 0:
            d = int(direction[0])
            mask = np.full_like(self.hl_state, False, dtype=bool)
            mask[:,:,d*n+(d-1)//2] = True
        elif direction[1] != 0:
            d = int(direction[1])
            mask = np.full_like(self.hl_state, False, dtype=bool)
            mask[:,-d*n-(d+1)//2,:] = True
        elif direction[2] != 0:
            d = int(direction[2])
            mask = np.full_like(self.hl_state, False, dtype=bool)
            mask[-d*n-(d+1)//2,:,:] = True
        anims = self.highlight(mask=mask, **aargs)
        return anims
    
    def highlight_beam(
        self,
        direction = IN,
        ij: tuple = (0, 0),
        **aargs,
    ) -> Animation:
        if direction[0] != 0:
            mask = np.full_like(self.hl_state, False, dtype=bool)
            mask[ij[0], ij[1], :] = True
        elif direction[1] != 0:
            mask = np.full_like(self.hl_state, False, dtype=bool)
            mask[ij[0], :, ij[1]] = True
        elif direction[2] != 0:
            mask = np.full_like(self.hl_state, False, dtype=bool)
            mask[:, ij[0], ij[1]] = True
        anims = self.highlight(mask=mask, **aargs)
        return anims

    def _normalize_padding(self, padding) -> tuple:
        if isinstance(padding, (int, np.integer)):
            pad = int(padding)
            return pad, pad, pad, pad
        padding = tuple(int(p) for p in padding)
        if len(padding) == 2:
            return padding[0], padding[0], padding[1], padding[1]
        if len(padding) == 4:
            return padding
        raise ValueError("padding must be int, 2-tuple, or 4-tuple")

    def pad(
        self,
        padding: int = 1,
        pad_value: float = 0.0,
        aargs: dict = {},
    ) -> AnimationGroup:
        top, bottom, left, right = self._normalize_padding(padding)

        self.pad_state = {
            'array': self.array.copy(),
            'shape': self.shape,
            'ndim': self.ndim,
            'objs': self.objs.copy(),
            'mobs': self.mobs,
            'hl_state': self.hl_state.copy(),
        }

        padded_array = np.pad(
            self.array,
            ((0, 0), (top, bottom), (left, right)),
            mode='constant',
            constant_values=pad_value,
        )
        objs, mobs = self.create_mobs(
            array=padded_array,
            reuse_objs=self.objs,
            offset=(0, top, left),
            pad_cube_config={
                'stroke_color': GRAY,
                'stroke_width': 0.6,
                'fill_opacity': 0.5,
            },
            pad_square_config={
                'stroke_color': GRAY,
                'stroke_width': 1.0,
                'fill_opacity': 0.5,
            },
            pad_decimal_config={},
        )

        old_mobs = self.mobs
        self.remove(old_mobs)
        self.array = padded_array
        self.shape = padded_array.shape
        self.ndim = padded_array.ndim
        self.objs = objs
        self.mobs = mobs
        self.hl_state = np.full(self.shape, True, dtype=bool)
        self.add(self.mobs)

        new_cubes = [cube for cube in objs.flat if cube is not None and cube not in old_mobs]
        self.pad_state['mobs_pad'] = new_cubes

        return AnimationGroup(
            *(GrowFromCenter(
                cube,
                rate_func=rate_functions.ease_out_back,
            ) for cube in new_cubes),
            **aargs,
        )

    def unpad(
        self,
        aargs: dict = {},
    ) -> AnimationGroup:
        assert hasattr(self, 'pad_state'), 'not padded yet'

        old_mobs = self.mobs
        self.remove(old_mobs)

        self.array = self.pad_state['array']
        self.shape = self.pad_state['shape']
        self.ndim = self.pad_state['ndim']
        self.objs = self.pad_state['objs']
        self.mobs = self.pad_state['mobs']
        self.hl_state = self.pad_state['hl_state']
        self.add(self.mobs)

        mobs_pad = self.pad_state['mobs_pad']
        del self.pad_state

        return AnimationGroup(
            *(ShrinkToCenter(
                cube,
            ) for cube in mobs_pad),
            **aargs,
        )

    
class MTensor_4D(MTensorGeneral):
    def __init__(
        self,
        block_direction: np.ndarray = RIGHT,
        block_gap: float = 0.5,
        **kwargs,
    ):
        self.block_direction = block_direction
        self.block_gap = block_gap
        super().__init__(**kwargs)
    
    def create_mobs(
        self,
    ):
        objs = np.empty(self.shape, dtype=object)
        blocks = VGroup()

        nb, nc, nh, nw = self.shape
        step = self.size + self.padding

        xs = [RIGHT * l * step for l in range(nw)]
        ys = [DOWN * k * step for k in range(nh)]
        zs = [IN * j * step for j in range(nc)]

        for i in range(nb):
            block_objs = np.empty((nc, nh, nw), dtype=object)
            for j, k, l in np.ndindex((nc, nh, nw)):
                cube = self.make_cube(self.array[i, j, k, l])
                cube.shift(xs[l] + ys[k] + zs[j])
                cube.set_z_index((nc - j) * nh + k)
                block_objs[j, k, l] = cube
                objs[i, j, k, l] = cube

            block_mobs = VGroup(*block_objs.flat).center()
            blocks.add(block_mobs)

        blocks.arrange(self.block_direction, self.block_gap)
        mobs = VGroup(*(mob for block in blocks for mob in block))
        return objs, mobs
    
    def switch_mode(
        self,
        style: str = 'layer',
        direction: np.ndarray = OUT,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """based on implementation of 3d.
        """
        vgs = [
            MTensor_3D(
                objs=self.objs[i],
                mobs=self[i],
                array=self.array[i],
                mode=self.mode,
                size=self.size,
                padding=self.padding,
                cube_config=self.cube_config,
                square_config=self.square_config,
                decimal_config=self.decimal_config,
            ) for i in range(self.shape[0])
        ]
        anims = AnimationGroup(
            *(vg.switch_mode(
                style=style,
                direction=direction,
                aargs=aargs,
            ) for vg in vgs),
            **gargs,
        )
        return anims

    def create(
        self,
        style='layer',
        direction=OUT,
        anim=Create,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> AnimationGroup:
        """based on implementation of 3d.
        """
        vgs = [
            MTensor_3D(
                objs=self.objs[i],
                mobs=self[i],
                array=self.array[i],
                mode=self.mode,
                size=self.size,
                padding=self.padding,
                cube_config=self.cube_config,
                square_config=self.square_config,
                decimal_config=self.decimal_config,
            ) for i in range(self.shape[0])
        ]

        anims = AnimationGroup(
            *(vg.create(
                style=style,
                direction=direction,
                anim=anim,
                aargs=aargs,
                gargs=gargs,
            ) for vg in vgs),
            **ggargs,
        )
        return anims

    def uncreate(
        self,
        style='layer',
        direction=OUT,
        anim=Uncreate,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> AnimationGroup:
        """based on implementation of 3d.
        """
        vgs = [
            MTensor_3D(
                objs=self.objs[i],
                mobs=self[i],
                array=self.array[i],
                mode=self.mode,
                size=self.size,
                padding=self.padding,
                cube_config=self.cube_config,
                square_config=self.square_config,
                decimal_config=self.decimal_config,
            ) for i in range(self.shape[0])
        ]

        anims = AnimationGroup(
            *(vg.uncreate(
                style=style,
                direction=direction,
                anim=anim,
                aargs=aargs,
                gargs=gargs,
            ) for vg in vgs),
            **ggargs,
        )
        return anims

class Demo1D(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)
        tensor = MTensor_1D(
            array=np.random.randn(25),
            mode='cube',
            size=0.3,
            padding=0.0,
        )

        # self.add(tensor)
        # self.wait()

        self.play(tensor.create(
            direction=RIGHT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': 1.0},
        ))
        self.wait()

        self.play(tensor.switch_mode(
            direction=RIGHT,
            aargs={'run_time': 1.0},
        ))
        self.wait()

        # for mob in tensor.get_mobs():
        #     mob.save_state()
        # self.play(tensor.highlight_mob(
        #     direction=RIGHT,
        #     n=0,
        #     run_time=1.0,
        # ))
        # self.wait()
        # self.play(tensor.highlight_mob_loop(
        #     direction=RIGHT,
        #     run_time=1.0,
        # ))
        # self.play(tensor.highlight_mob_loop(
        #     direction=LEFT,
        #     run_time=1.0,
        # ))
        # self.wait()

        self.move_camera(
            phi=60*DEGREES,
            theta=-135*DEGREES,
            run_time=1.0,
        )
        self.wait()

        self.play(tensor.uncreate(
            direction=RIGHT,
            anim=ShrinkToCenter,
            aargs={},
            gargs={'run_time': 1.0},
        ))
        self.wait()

class Demo2D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)

        tensor = MTensor_2D(
            array=np.random.randn(4,5),
            mode='cube',
            size=0.3,
            padding=0.0,
        )

        # self.add(tensor)
        # self.wait()

        self.play(tensor.create(
            direction=RIGHT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': 1.0},
        ))
        self.wait()

        self.play(tensor.switch_mode(
            direction=DOWN,
            aargs={'run_time': 1.0},
        ))
        self.wait()
        
        self.play(tensor.highlight_row(
            direction=DOWN,
            n=1,
            run_time=1.0,
        ))
        self.wait()

        self.move_camera(
            phi=60*DEGREES,
            theta=-135*DEGREES,
            run_time=1.0,
        )
        self.wait()

        self.play(tensor.uncreate(
            direction=RIGHT,
            anim=ShrinkToCenter,
            aargs={},
            gargs={'run_time': 1.0},
        ))
        self.wait()

class Demo3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)

        tensor = MTensor_3D(
            array=np.random.randn(5,3,3),
            mode='cube',
            size=0.3,
            padding=0.00,
        )

        self.play(tensor.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': 1.0},
        ))
        self.wait()

        self.play(tensor.switch_mode(
            style='beam',
            direction=IN,
            aargs={'run_time': 1.0},
        ))
        self.wait()

        self.play(tensor.highlight_layer(
            direction=IN,
            n=1,
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.highlight(
            mask=None,
            run_time=1.0,
        ))
        self.wait()

        self.play(tensor.uncreate(
            style='beam',
            direction=IN,
            anim=ShrinkToCenter,
            aargs={},
            gargs={'run_time': 1.0},
        ))
        self.wait()

class Demo4D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)

        tensor = MTensor_4D(
            block_direction=RIGHT,
            block_gap=0.3,
            array=np.random.randn(5,8,3,3),
            mode='cube',
            size=0.3,
            padding=0.0,
        )

        # self.add(tensor)
        # self.wait()

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
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
        """ Indexing utils.
            Prerequisites: ndim, shape, objs
        """
        # normalize idx
        if not isinstance(idx, tuple):
            idx = (idx,)

        # expand ellipsis
        if Ellipsis in idx:
            pos = idx.index(Ellipsis)
            missing = self.ndim - (len(idx) - 1)
            idx = (
                idx[:pos]
                + (slice(None),) * missing
                + idx[pos + 1 :]
            )

        # fill missing dims
        idx = idx + (slice(None),) * (self.ndim - len(idx))

        if len(idx) != self.ndim:
            raise IndexError("Invalid index dimension")

        resolved = []
        for part, size in zip(idx, self.shape):
            if isinstance(part, (int, np.integer)):
                data = [part]
            elif isinstance(part, slice):
                start, stop, step = part.indices(size)
                data = list(range(start, stop, step))
            else:
                raise TypeError(f"Invalid index: {part}")
            resolved.append(data)

        keys = list(itertools.product(*resolved))

        if not keys:
            return VGroup()

        # FIXME, ugly design for list of list
        def nested_get(obj, idx_tuple):
            for i in idx_tuple:
                obj = obj[i]
            return obj

        if len(keys) == 1:
            return nested_get(self.objs, keys[0])
        return VGroup(*(nested_get(self.objs, k) for k in keys))

    
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
            anims.append(self[*idx_tuple].animate.fade(0.9))
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
        objs = [
            MCube(
                value=float(self.array[i]),
                size=self.size,
                mode=self.mode,
                cube_config=self.cube_config,
                square_config=self.square_config,
                decimal_config=self.decimal_config,
            ).shift(RIGHT * i * (self.size + self.padding))
            for i in range(self.array.shape[0])
        ]
        n_mobs = self.shape[0]
        for i, cube in enumerate(objs):
            cube.set_z_index(n_mobs - i)
        mobs = VGroup(*objs).center()
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
        objs = [
            [ MCube(
                    value=float(self.array[i, j]),
                    size=self.size,
                    mode=self.mode,
                    cube_config=self.cube_config,
                    square_config=self.square_config,
                    decimal_config=self.decimal_config,
                ).shift(RIGHT * j * (self.size + self.padding) +\
                        DOWN * i * (self.size + self.padding))
                for j in range(self.array.shape[1])
            ] for i in range(self.array.shape[0])
        ]
        n_rows, n_cols = self.shape
        for i, row in enumerate(objs):
            for j, cube in enumerate(row):
                cube.set_z_index((n_rows-i)*n_cols + (n_cols-j))
        flat_mobs = [mob for plane in objs for row in plane for mob in row]
        mobs = VGroup(*flat_mobs).center()
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
    
    def create_mobs(
        self,
    ) -> tuple:
        objs = [
            [
                [ MCube(
                        value=float(self.array[i, j, k]),
                        size=self.size,
                        mode=self.mode,
                        cube_config=self.cube_config,
                        square_config=self.square_config,
                        decimal_config=self.decimal_config,
                    ).shift(RIGHT * k * (self.size + self.padding) +\
                             DOWN * j * (self.size + self.padding) +\
                                IN * i * (self.size + self.padding))
                    for k in range(self.array.shape[2])
                ] for j in range(self.array.shape[1])
            ] for i in range(self.array.shape[0])
        ]
        n_layers, n_rows, n_cols = self.shape
        for i, layer in enumerate(objs):
            for j, row in enumerate(layer):
                for cube in row:
                    cube.set_z_index((n_layers-i)*n_rows + j)
        flat_mobs = [mob for plane in objs for row in plane for mob in row]
        mobs = VGroup(*flat_mobs).center()
        return objs, mobs
    
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
        objs_4d = []
        blocks = VGroup()
        nb, nc, nh, nw = self.array.shape
        for i, block in enumerate(self.array):
            objs = [
                [
                    [ MCube(
                            value=float(block[j, k, l]),
                            size=self.size,
                            mode=self.mode,
                            cube_config=self.cube_config,
                            square_config=self.square_config,
                            decimal_config=self.decimal_config,
                        ).shift(RIGHT * l * (self.size + self.padding) +\
                                DOWN * k * (self.size + self.padding) +\
                                    IN * j * (self.size + self.padding))
                        for l in range(nw)
                    ] for k in range(nh)
                ] for j in range(nc)
            ]
            for j, ch in enumerate(objs):
                for k, row in enumerate(ch):
                    for l, cube in enumerate(row):
                        cube.set_z_index((nc-j)*nh+k)
            flat_mobs = [mob for ch in objs for row in ch for mob in row]
            mobs = VGroup(*flat_mobs).center()
            objs_4d.append(objs)
            blocks.add(mobs)
        blocks.arrange(self.block_direction, self.block_gap)
        mobs_4d = VGroup(mob for block in blocks for mob in block)
        return objs_4d, mobs_4d
    
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
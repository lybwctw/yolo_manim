from manim import *
import itertools
import random
from enum import Enum

from manim.utils.rate_functions import ease_in_quart
from typing_extensions import runtime

DEFAULT_CUBE_CONFIG = {
    'side_length': 0.5,
    'fill_color': ORANGE,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_SQUARE_CONFIG = {
    'side_length': 0.5,
    'fill_color': ORANGE,
    'fill_opacity': 0.8,
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
DEFAULT_DECIMAL_CONFIG = {
    'num_decimal_places': 2,
    'mob_class': MathTex,
    'include_sign': True,
    'font_size': 18,
    'fill_opacity': 1.0,
}

class CCMode(Enum):
    CUBE = 1
    CARD = 2

def _normalize_idx(idx):
    if not isinstance(idx, tuple):
        idx = (idx,)
    return idx
def _expand_ellipsis(idx, ndim):
    if Ellipsis not in idx:
        return idx

    pos = idx.index(Ellipsis)
    missing = ndim - (len(idx) - 1)
    return (
        idx[:pos]
        + (slice(None),) * missing
        + idx[pos + 1 :]
    )
def _fill_missing_dims(idx, ndim):
    return idx + (slice(None),) * (ndim - len(idx))
def _indices_from_part(part, size):
    # np.int64 for ijk from np.argwhere(...)
    if isinstance(part, (int, np.int64)):
        return [part]
    if isinstance(part, slice):
        start, stop, step = part.indices(size)
        return list(range(start, stop, step))
    raise TypeError(f"Invalid index: {part}")

def shift_layers(direction=UR, scale=0.5):
    """
        # shift layers in xy directions
        self.move_camera(phi=0*DEGREES, theta=-90*DEGREES, focal_distance=80)
        self.play(ApplyFunction(shift_layers(UR), cubes))
        self.play(ApplyFunction(shift_layers(2*LEFT), cubes))
        self.play(ApplyFunction(shift_layers(DR), cubes))
    """
    def _shift_layers(cubes):
        for i, layer in enumerate(cubes.get_layers()):
            layer.shift(direction*i*scale*cubes.size)
        cubes.center()
        return cubes
    return _shift_layers

class Card(VMobject):
    def __init__(
        self,
        value=0.0,
        square_config=None,
        decimal_config=None,
    ):
        super().__init__()
        self.value = value
        self.square_config = square_config if square_config else {}
        self.decimal_config = decimal_config if decimal_config else {}
        self.square = Square(**self.square_config)
        self.decimal = DecimalNumber(
            self.value, **self.decimal_config
        )
        self.add(self.square, self.decimal)

class MCube(VMobject):
    def __init__(
        self,
        array,
        size=0.5,
        mode=CCMode.CUBE,
        padding=0.1,
        center=ORIGIN,
        cube_config=None,
        square_config=None,
        decimal_config=None,
    ):
        super().__init__()
        self.array = array
        self.shape = array.shape
        self.ndim = array.ndim
        self.indices = self._build_indices()
        self.current_hl = np.full(self.shape, True, dtype=bool)
        self.size = size
        self.mode = mode
        self.padding=padding
        self.card_uopacity = 0.1
        self.cube_uopacity = 0.03
        self._center=center  # FIXME: redundant?

        # setup config
        self.cube_config = {
            **DEFAULT_CUBE_CONFIG,
            **cube_config,
            **{'side_length': self.size},
        } if cube_config else {**DEFAULT_CUBE_CONFIG}
        self.square_config = {
            **DEFAULT_SQUARE_CONFIG,
            **square_config,
            **{'side_length': self.size},
        } if square_config else {**DEFAULT_SQUARE_CONFIG}
        self.decimal_config = {
            **DEFAULT_DECIMAL_CONFIG,
            **{'font_size': DEFAULT_DECIMAL_CONFIG['font_size']*self.size},
            **decimal_config,
        } if decimal_config else {**DEFAULT_DECIMAL_CONFIG}

        # init indices->cubes, indices->cards
        self.cubes = {
            idx: Cube(**self.cube_config)
            for idx in itertools.product(
                range(self.shape[0]),
                range(self.shape[1]),
                range(self.shape[2]),
            )
        }
        self.cards = {
            idx: Card(
                float(self.array[idx]),
                self.square_config,
                self.decimal_config
            ) for idx in self.cubes.keys()
        }

        # arrange cubes and cards in manim view
        shift_m = self._compute_shift_m()
        z_index_m = self._compute_z_index_m()
        for idx in self.cubes:
            self.cubes[idx].move_to(shift_m[idx])
            self.cards[idx].move_to(shift_m[idx])
            self.cubes[idx].set_z_index(z_index_m[idx])
            self.cards[idx].set_z_index(z_index_m[idx])

        # collect cubes and cards for manim
        self.mobs_cube = VGroup(*self.cubes.values())
        self.mobs_card = VGroup(*self.cards.values())
        if self.mode == CCMode.CUBE:
            self.obs = self.cubes
            self.mobs = self.mobs_cube
        else:
            self.obs = self.cards
            self.mobs = self.mobs_card
        self.add(self.mobs)
        self.mobs_cube.move_to(self._center)
        self.mobs_card.move_to(self._center)

    def _build_indices(self, shape=None):
        if shape is None:
            shape = self.shape
        i, j, k = shape
        z_range = np.arange(i)
        y_range = np.arange(j)
        x_range = np.arange(k)
        zz, yy, xx = np.meshgrid(
            z_range, y_range, x_range,
            indexing='ij',
        )
        indices = np.stack([xx, yy, zz], axis=-1)
        return indices

    def _compute_shift_m(self, indices=None):
        if indices is None:
            indices = self.indices
        shift_m = indices \
                * np.array([1,-1,-1])[None,None,None,:] \
                * (self.size*(1+self.padding))
        return shift_m

    def _compute_z_index_m(self, shape=None):
        if shape is None:
            shape = self.shape
        i, j, k = shape
        z_index = np.arange(i)[::-1]
        z_index_m = z_index[:,None,None] * \
            np.ones((1,j,k),dtype=np.int32)
        return z_index_m

    def _switch_mode(self):
        for mob in self.mobs:
            mob.save_state()

        if self.mode == CCMode.CUBE:
            self.mobs_card.move_to(self.mobs)
            self.remove(self.mobs)
            self.mobs = self.mobs_card
            self.obs = self.cards
            self.mode = CCMode.CARD
        elif self.mode == CCMode.CARD:
            self.mobs_cube.move_to(self.mobs)
            self.remove(self.mobs)
            self.mobs = self.mobs_cube
            self.obs = self.cubes
            self.mode = CCMode.CUBE
        self.add(self.mobs)

        return self

    def switch_mode(
            self,
            type='layer',
            direction=IN,
            in_anim=Create,
            out_anim=Uncreate,
    ):
        """
            self.play(mcubes.switch_mode(type='beam', direction=IN))
            mcubes.restore_states()
            self.play(mcubes.switch_mode(type='beam', direction=OUT))
            mcubes.restore_states()
        """
        # FIXME: when using Uncreate/Unwrite
        #  restore_states() should be called immediately
        if type == 'layer':
            layers1 = self.get_layers(direction=direction)
            self._switch_mode()
            layers2 = self.get_layers(direction=direction)

            anims = AnimationGroup(
                *(AnimationGroup(
                    AnimationGroup(
                        out_anim(m) for m in layer1
                    ),
                    AnimationGroup(
                        in_anim(m) for m in layer2
                    ),
                    lag_ratio=0.1,
                ) for layer1, layer2 in zip(layers1, layers2)),
                lag_ratio=0.2,
            )
        elif type == 'beam':
            beams1 = self.get_beams(direction=direction)
            self._switch_mode()
            beams2 = self.get_beams(direction=direction)

            anims = AnimationGroup(
                *(AnimationGroup(
                    *(AnimationGroup(
                        out_anim(b1),
                        in_anim(b2),
                        lag_ratio=0.1,
                    ) for b1, b2 in zip(beam1, beam2)),
                    lag_ratio=random.random()*0.5,
                ) for beam1, beam2 in zip(beams1, beams2))
            )
        return anims

    def __getitem__(self, idx):
        idx = _normalize_idx(idx)
        idx = _expand_ellipsis(idx, self.ndim)
        idx = _fill_missing_dims(idx, self.ndim)
        if len(idx) != self.ndim:
            raise IndexError("Invalid index dimension")
        resolved = [
            _indices_from_part(part, size)
            for part, size in zip(idx, self.shape)
        ]
        keys = list(itertools.product(*resolved))
        if not keys:
            return VGroup()
        if len(keys) == 1:
            return self.obs[keys[0]]
        return VGroup(*(self.obs[k] for k in keys))

    def get_beams(self, direction=OUT):
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

    def get_layers(self, direction=OUT):
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

    def restore_states(self):
        '''
        used after switch_mode to restore states of those uncreated
        '''
        _mobs = self.mobs_card if self.mode==CCMode.CUBE else self.mobs_cube
        for mob in _mobs:
            mob.restore()

    def _get_mask(self, start, end, mask):
        """
            get boolean mask
            filled with True by default
        """
        if mask is not None:
            return mask
        if start is None or end is None:
            mask = np.full_like(self.current_hl, True, dtype=bool)
        else:
            i1, j1, k1 = start
            i2, j2, k2 = end
            mask = np.full_like(self.current_hl, False, dtype=bool)
            mask[i1:i2, j1:j2, k1:k2] = True
        return mask

    def _highlight(self, start=None, end=None, mask=None):
        start_mask = self.current_hl
        target_mask = self._get_mask(start, end, mask)
        _unhighlight_mask = start_mask & ~target_mask
        _highlight_mask = target_mask & ~start_mask

        if self.mode == CCMode.CUBE:
            uopacity = self.cube_uopacity
        else:
            uopacity = self.card_uopacity

        for i, j, k in np.argwhere(_unhighlight_mask):
            self[i, j, k].save_state()
            self[i, j, k].set_opacity(opacity=uopacity)
        for i, j, k in np.argwhere(_highlight_mask):
            self[i, j, k].restore()
        self.current_hl = target_mask

        return self

    def highlight(self, start=None, end=None, mask=None):
        """
            # highlight from last channel back to all
            self.play(Succession(
                *(mcubes.highlight((n,0,0),mcubes.shape) for n in range(mcubes.shape[0]-2,-1,-1)),
                run_time=1,
                rate_func=ease_in_quart,
            ))
        """
        start_mask = self.current_hl
        target_mask = self._get_mask(start, end, mask)
        _unhighlight_mask = start_mask & ~target_mask
        _highlight_mask = target_mask & ~start_mask

        if self.mode == CCMode.CUBE:
            uopacity = self.cube_uopacity
        else:
            uopacity = self.card_uopacity

        anims = []
        for i, j, k in np.argwhere(_unhighlight_mask):
            self[i, j, k].save_state()
            anims.append(self[i, j, k].animate.set_opacity(opacity=uopacity))
        for i, j, k in np.argwhere(_highlight_mask):
            anims.append(self[i, j, k].animate.restore())
        self.current_hl = target_mask
        return AnimationGroup(
            *anims
        )

    def _highlight_layer(self, direction, n):
        pass

    def _highlight_channel(self, n):
        c, h, w = self.shape
        self._highlight((n, 0, 0), (n+1, h, w))
        return self

    def highlight_channel(self, n):
        """
            self.play(Succession(
                *(mcubes.highlight_channel(n) for n in range(mcubes.shape[0])),
                run_time=3,
                rate_func=ease_in_quart,
            ))
        """
        c, h, w = self.shape
        anims = self.highlight((n, 0, 0), (n+1, h, w))
        return anims

    def _extend(self, value=0.0, n=1, direction=OUT):
        direction = direction.astype(np.int32)
        oc, oh, ow = self.shape

        # create numpy array
        if direction[0] != 0:
            n_shape = (oc, oh, n)
        elif direction[1] != 0:
            n_shape = (oc, n, ow)
        elif direction[2] != 0:
            n_shape = (n, oh, ow)

        n_indices = self._build_indices(n_shape)

        if isinstance(value, (int, float)):
            n_array = np.ones(n_shape) * value
        else:
            n_array = np.random.randn(*n_shape)

        # create new indices->cubes, indices->cards
        n_cubes = {
            idx: Cube(**self.cube_config)
            for idx in itertools.product(
                range(n_shape[0]),
                range(n_shape[1]),
                range(n_shape[2]),
            )
        }
        n_cards = {
            idx: Card(**self.card_config)
            for idx in itertools.product(
                range(n_shape[0]),
                range(n_shape[1]),
                range(n_shape[2]),
            )
        }

        n_shift_m = self._compute_shift_m(n_indices)
        n_z_index_m = self._compute_z_index_m()
        for idx in n_cubes:
            n_cubes[idx].move_to(n_shift_m[idx])
            n_cards[idx].move_to(n_shift_m[idx])
            n_cubes[idx].set_z_index(n_z_index_m[idx])
            n_cards[idx].set_z_index(n_z_index_m[idx])

        # normally, time for build
        # mobs_cube, mobs_card
        # mobs, obs
        # add mobs, move_to..

        # TODO ...
        # directed concat into array

        # directed concat into cubes, cards
        # refresh z_index
        # obs auto updated

        # undirected concat into mobs_cube, mobs_card
        # mobs auto update
        # readd mobs

    # FIXME, add after create()???
    def create(
            self,
            type='layer',
            direction=OUT,
            anim=Create,
            run_time=2,
    ):
        if type == 'layer':
            layers = self.get_layers(direction=direction)
            anims = Succession(
                *(AnimationGroup(
                    *(anim(cube) for cube in layer),
                ) for layer in layers),
                run_time=run_time,
                rate_func=smooth,
            )
            return anims
        elif type == 'beam':
            beams = self.get_beams(direction=direction)
            anims = AnimationGroup(
                Succession(
                    *(anim(cube) for cube in beam),
                    run_time=random.random()+1,
                    rate_func=smooth,
                ) for beam in beams
            )
            return anims

    def uncreate(
            self,
            type='layer',
            direction=OUT,
            anim=Uncreate,
            run_time=2,
    ):
        anims = self.create(
            type=type,
            direction=direction,
            anim=anim,
            run_time=run_time,
        )
        return anims

class SampleScene(ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        cube_config = {'fill_color': BLACK}
        square_config = {'fill_color': BLACK}
        mcubes = MCube(
            np.random.randn(5,5,5),
            size=0.5,
            padding=0.01,
            mode=CCMode.CUBE,
            cube_config=cube_config,
            square_config=square_config,
        )

        self.wait()

        # self.add(mcubes)
        self.play(mcubes.create(type='beam', direction=OUT))
        self.wait()

        # self.play(mcubes.switch_mode(type='beam'))
        # mcubes.restore_states()
        # self.wait()
        #
        # self.play(mcubes.uncreate(type='beam', direction=IN))
        # self.wait()

        self.stop_ambient_camera_rotation()
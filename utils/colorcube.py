from manim import *
import itertools
import random

DEFAULT_CUBE_CONFIG = {
    'side_length': 0.3,
    'fill_opacity': 0.6,
    # 'stroke_opacity': 0.0,
}

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

class ColorCube(VMobject):
    def __init__(
        self,
        axis,
        shape=5,
        size=0.5,
        cube_config=None,
    ):
        super().__init__()
        self.axis = axis
        self.shape = (shape,shape,shape)
        self.ndim = 3
        step = 256//(shape-1)
        values = [n*step for n in range(shape)]
        values[-1] = 255
        self.values = values
        self.indices = self._build_indices()
        self.current_hl = np.full(self.shape, True, dtype=bool)
        self.size = size
        self.cube_uopacity = 0.03

        # setup config
        self.cube_config = {
            **DEFAULT_CUBE_CONFIG,
            **cube_config,
            **{'side_length': self.size},
        } if cube_config else {**DEFAULT_CUBE_CONFIG}

        # init indices->cubes, indices->cards
        self.cubes = {
            idx: Cube(**self.cube_config)
            for idx in itertools.product(
                range(self.shape[0]),
                range(self.shape[1]),
                range(self.shape[2]),
            )
        }

        z_index_m = self._compute_z_index_m()
        for idx in self.cubes:
            self.cubes[idx].set_z_index(z_index_m[idx])
        for idx in self.cubes:
            i, j, k = idx
            r, g, b = self.values[i], self.values[j], self.values[k]
            color = rgb_to_color([r/255,g/255,b/255])
            self.cubes[idx].set_fill(color=color)
            self.cubes[idx].move_to(
                self.axis.c2p(r/255,g/255,b/255)
            )

        self.mobs_cube = VGroup(*self.cubes.values())
        self.obs = self.cubes
        self.mobs = self.mobs_cube

        self.add(self.mobs)

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

    def _compute_z_index_m(self, shape=None):
        if shape is None:
            shape = self.shape
        i, j, k = shape
        z_index = np.arange(i)[::-1]
        z_index_m = z_index[:,None,None] * \
            np.ones((1,j,k),dtype=np.int32)
        return z_index_m

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
        n = self.shape[0]   # colorcube always use the same c,h,w
        if direction[0] != 0:
            vgs = VGroup(
                self[:,i,j][::direction[0]]
                for i, j in itertools.product(range(n),range(n))
            )
        elif direction[1] != 0:
            vgs = VGroup(
                self[i,j,:][::direction[1]]
                for i, j in itertools.product(range(n),range(n))
            )
        elif direction[2] != 0:
            vgs = VGroup(
                self[i,:,j][::-direction[2]]
                for i, j in itertools.product(range(n),range(n))
            )
        return vgs

    def get_layers(self, direction=OUT):
        direction = direction.astype(np.int32)
        n = self.shape[0]
        if direction[0] != 0:
            vgs = VGroup(self[i,:,:] for i in range(n))
            vgs = vgs[::direction[0]]
        elif direction[1] != 0:
            vgs = VGroup(self[:,:,i] for i in range(n))
            vgs = vgs[::direction[1]]
        elif direction[2] != 0:
            vgs = VGroup(self[:,i,:] for i in range(n))
            vgs = vgs[::-direction[2]]
        return vgs

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

        uopacity = self.cube_uopacity

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

        uopacity = self.cube_uopacity

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

    # FIXME, add after create()???
    def create(
            self,
            type='layer',
            direction=OUT,
            anim=Write,
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
            anim=Unwrite,
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
        axes = ThreeDAxes(
            x_range=[0, 1.2],
            y_range=[0, 1.2],
            z_range=[0, 1.2],
            x_length=4,
            y_length=4,
            z_length=4,
        ).shift(IN * 1)
        axes_labels = axes.get_axis_labels(
            x_label='R',
            y_label='G',
            z_label='B',
        )
        self.play(Create(axes))
        self.play(Write(axes_labels))

        cubes = ColorCube(axis=axes)
        cubes[0,0,0].set_fill(opacity=0.9)

        self.play(cubes.create(type='beam', direction=UP))

        self.play(cubes.highlight_channel(2))
        self.wait()
        self.play(cubes.highlight())
        self.wait()

        self.play(cubes.uncreate(type='beam', direction=DOWN))
        self.play(Unwrite(axes), Unwrite(axes_labels))

        self.stop_ambient_camera_rotation()
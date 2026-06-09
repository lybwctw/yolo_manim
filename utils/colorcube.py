"""Usage
-----
Example inside a scene outside ``utils/``::

    from utils.colorcube import ColorCube

    self.set_camera_orientation(phi=60*DEGREES, theta=-75*DEGREES)
    axes = ThreeDAxes(x_range=[0, 1.2], y_range=[0, 1.2], z_range=[0, 1.2])
    cubes = ColorCube(axis=axes)
    self.play(cubes.create(type='beam', direction=UP))
    self.play(cubes.highlight_channel(2))
"""

from manim import *
import itertools
import random

DEFAULT_CUBE_CONFIG = {
    'side_length': 0.3,
    'fill_opacity': 0.6,
    # 'stroke_opacity': 0.0,
}

SHOW_OPACITY = 0.6
HIDE_OPACITY = 0.0

class ColorCube(VMobject):
    def __init__(
        self,
        axis,                   # reference 3d axes
        shape: int = 5,         # number of cubes each direction
        cube_config: dict | None = None, # mainly side_length
    ):
        super().__init__()
        self.axis = axis
        self.shape = (shape,shape,shape)
        self.ndim = 3
        step = 256//(shape-1)
        values = [n*step for n in range(shape)]
        values[-1] = 255
        self.values = [v/255 for v in values]

        # track current highlight cubes
        self.hl_state = np.full(self.shape, True, dtype=bool)

        cube_config = {
            **DEFAULT_CUBE_CONFIG,
            **cube_config,
        }

        objs = []
        for i in range(shape):
            r_ch = []
            for j in range(shape):
                g_ch = []
                for k in range(shape):
                    color = rgb_to_color([
                        self.values[i],
                        self.values[j],
                        self.values[k],
                    ])
                    cfg = {**(cube_config or {}), 'fill_color': color}
                    cube = Cube(**cfg)
                    pos = self.axis.c2p(
                        self.values[i],
                        self.values[j],
                        self.values[k],
                    )
                    z_idx = k+1       # base on blue channel index
                    cube.move_to(pos).set_z_index(z_idx)
                    g_ch.append(cube)
                r_ch.append(g_ch)
            objs.append(r_ch)
        self.objs = objs
        self.mobs = VGroup(
            *[cube for r_ch in self.objs for g_ch in r_ch for cube in g_ch]
        )
        self.add(self.mobs)

    def __getitem__(
        self,
        idx,
    ) -> VMobject:
        """
        Indexing utils.
        Prerequisites:
            ndim, dimensions of data
            shape, shape of data
            objs, list of list of vmobject
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
            if isinstance(part, (int, np.int64)):
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
            vgs = VGroup(self[:,i,:] for i in range(n))
            vgs = vgs[::direction[1]]
        elif direction[2] != 0:
            vgs = VGroup(self[:,:,i] for i in range(n))
            vgs = vgs[::direction[2]]
        return vgs

    # def _get_mask(self, start, end, mask):
    #     """
    #         get boolean mask
    #         filled with True by default

    #     Example
    #     -------
    #     cubes = ColorCube(axis=ThreeDAxes())
    #     result = cubes._get_mask(start=0, end=0, mask=0)
    #     """
    #     if mask is not None:
    #         return mask
    #     if start is None or end is None:
    #         mask = np.full_like(self.current_hl, True, dtype=bool)
    #     else:
    #         i1, j1, k1 = start
    #         i2, j2, k2 = end
    #         mask = np.full_like(self.current_hl, False, dtype=bool)
    #         mask[i1:i2, j1:j2, k1:k2] = True
    #     return mask

    # def _highlight(self, start=None, end=None, mask=None):
    #     """
    #     Example
    #     -------
    #     cubes = ColorCube(axis=ThreeDAxes())
    #     result = cubes._highlight()
    #     """
    #     start_mask = self.current_hl
    #     target_mask = self._get_mask(start, end, mask)
    #     _unhighlight_mask = start_mask & ~target_mask
    #     _highlight_mask = target_mask & ~start_mask

    #     uopacity = self.cube_uopacity

    #     for i, j, k in np.argwhere(_unhighlight_mask):
    #         self[i, j, k].save_state()
    #         self[i, j, k].set_opacity(opacity=uopacity)
    #     for i, j, k in np.argwhere(_highlight_mask):
    #         self[i, j, k].restore()
    #     self.current_hl = target_mask

    #     return self

    def highlight(
        self,
        mask=None,
        **aargs,
    ) -> AnimationGroup:
        """
        Highlight cubes according to mask.
        All by default.
        """
        start_mask = self.hl_state
        if mask is None:
            target_mask = np.full(self.shape, True, dtype=np.bool)
        else:
            target_mask = mask
        show_mask = target_mask & ~start_mask
        hide_mask = ~target_mask & start_mask

        show_anims = [
            ApplyMethod(self[i,j,k].set_opacity, SHOW_OPACITY)
                for i,j,k in np.argwhere(show_mask)
        ]
        hide_anims = [
            ApplyMethod(self[i,j,k].set_opacity, HIDE_OPACITY)
                for i,j,k in np.argwhere(hide_mask)
        ]
        anims = [*show_anims, *hide_anims]
        if anims:
            return AnimationGroup(
                *anims,
                **aargs,
            )
        else:
            return Wait(0.5)

    # def _highlight_channel(self, n):
    #     """
    #     Example
    #     -------
    #     cubes = ColorCube(axis=ThreeDAxes())
    #     result = cubes._highlight_channel(n=0)
    #     """
    #     c, h, w = self.shape
    #     self._highlight((n, 0, 0), (n+1, h, w))
    #     return self

    # def highlight_channel(self, n):
    #     """
    #         self.play(Succession(
    #             *(mcubes.highlight_channel(n) for n in range(mcubes.shape[0])),
    #             run_time=3,
    #             rate_func=ease_in_quart,
    #         ))

    #     Example
    #     -------
    #     cubes = ColorCube(axis=ThreeDAxes())
    #     self.play(cubes.highlight_channel(n=0))
    #     """
    #     c, h, w = self.shape
    #     anims = self.highlight((n, 0, 0), (n+1, h, w))
    #     return anims

    def create(
        self,
        type: str = 'layer',
        direction: np.ndarray = OUT,
        **aargs,
    ):
        if type == 'layer':
            layers = self.get_layers(direction=direction)
            anims = Succession(
                *(AnimationGroup(
                    *(Write(cube) for cube in layer),
                ) for layer in layers),
                **aargs,
            )
            return anims
        elif type == 'beam':
            beams = self.get_beams(direction=direction)
            anims = AnimationGroup(
                *(Succession(
                    *(Write(cube) for cube in beam),
                    run_time=random.random()+1,
                    rate_func=smooth,
                ) for beam in beams),
                **aargs,
            )
            return anims

    def uncreate(
            self,
            type='layer',
            direction=OUT,
            anim=Unwrite,
            run_time=2,
    ):
        """
        Example
        -------
        cubes = ColorCube(axis=ThreeDAxes())
        self.play(cubes.uncreate())
        """
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

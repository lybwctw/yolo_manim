import sys
sys.path.append('..')

from manim import *

import itertools
import numpy as np
from typing import Self

DECIMAL_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 22,
    'color': WHITE,
}

ARRANGE_CONFIG = {
    'cell_width': 0.8,
    'cell_height': 0.4,
}

# also used by mcubes
# TODO, make these functions general
def _indices_from_part(part, size):
    # np.int64 for ijk from np.argwhere(...)
    if isinstance(part, (int, np.int64)):
        return [part]
    if isinstance(part, slice):
        start, stop, step = part.indices(size)
        return list(range(start, stop, step))
    raise TypeError(f"Invalid index: {part}")

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

class Tensor2D(VMobject):
    def __init__(
        self,
        data: list | None = None,   # [(a, n), (b, n), (c, n), ...]
        decimal_config: dict = {},
        arrange_config: dict = {},
    ):
        super().__init__()
        # TODO, make sure all dim is the same except the last
        self.formatters, self.col_ratios = self._create_formatters(data)
        self.data = np.concat(data, axis=-1)
        self.shape = self.data.shape
        self.ndim = self.data.ndim
        self.decimal_config = {**DECIMAL_CONFIG, **decimal_config}
        auto_arrange_config = {
            'cell_width': self.decimal_config['font_size']*0.052,
            'cell_height': self.decimal_config['font_size']*0.026,
        }
        self.arrange_config = {**auto_arrange_config, **arrange_config}

        self.decimals = self._create_decimals()
        self.mobs = self._create_mobs()
        self._arrange_mobs()

        self.add(self.mobs)
    
    def _create_formatters(
        self,
        group,
    ):
        """Compute formatter for each col.
           Compute col ratio for each col.
        """
        fs = []
        cs = []
        for data in group:
            if np.issubdtype(data.dtype, np.integer):
                formatter = ['{:>3.0f}'] * data.shape[1]
                col_ratio = [0.8] * data.shape[1]
                col_ratio[-1] += 0.23     # a little bit more on first of next
            elif np.issubdtype(data.dtype, np.floating):
                formatter = ['{:.2f}'] * data.shape[1]
                col_ratio = [1.0] * data.shape[1]
            fs = fs + formatter
            cs = cs + col_ratio
        return fs, cs

    def _create_decimals(
        self,
    ) -> list:
        """Create a list of list of decimal vmobject.
        """
        data = self.data.tolist()   # start with list of list

        mobs = []
        for row in data:
            row_mobs = []
            for i,d in enumerate(row):
                mob = Text(
                    self.formatters[i].format(d),
                    # f'{d:.2f}',
                    **self.decimal_config,
                )
                row_mobs.append(mob)
            mobs.append(row_mobs)
        return mobs
    
    def _create_mobs(
        self,
    ) -> VGroup:
        """Create a vgroup of vgroup of Text based on decimals.
        """
        return VGroup( *(VGroup(*row) for row in self.decimals))
    
    def _arrange_mobs(
        self,
    ) -> Self:
        """Arrange rows and cols separately
        """
        cfg = self.arrange_config

        for i, row in enumerate(self.mobs):
            for j, mob in enumerate(row):
                dy = i * cfg['cell_height'] * DOWN
                dx = sum(self.col_ratios[:j]) * cfg['cell_width'] * RIGHT
                mob.align_to(dy, DOWN)
                mob.align_to(dx, RIGHT)
            
        self.mobs.center()  # to origin after arrange
        return self

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
            i, j = keys[0]
            return self.decimals[i][j]

        return VGroup(*(self.decimals[i][j] for i, j in keys))
    
class Demo(Scene):
    def construct(self):
        t1 = Tensor2D(
            data=[
                np.random.randint(0,999,(60,4)),
                np.random.uniform(0,1,(60,3))
            ],
            decimal_config={
                'font_size': 5.5,
                'color': WHITE,
            },
            # arrange_config={
            #     'buff_row': 0.03,
            #     'buff_col': 0.10,
            # },
        )
        # t1 = Tensor2D(
        #     data=[
        #         np.random.randint(0,999, (10,4)),
        #         np.random.uniform(0,1, (10,3)),
        #     ],
        #     decimal_config={
        #         'font_size': 15.5,
        #         'color': WHITE,
        #     },
        #     # arrange_config={
        #     #     'cell_width': 1.8,
        #     #     'cell_height': 1.4,
        #     # },
        # )

        self.add(t1)
        # self.play(Write(
        #     t1,
        #     lag_ratio=0.1,
        #     run_time=0.5,
        # ))
        self.wait()

        partial = t1[:,-3:]
        self.play(partial.animate.set_color(RED))
        self.wait()
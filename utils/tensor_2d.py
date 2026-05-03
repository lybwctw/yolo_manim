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

# empirically determined, for monospaced font
FONT_SIZE_WIDTH_RATIO = 0.06
FONT_SIZE_HEIGHT_RATIO = 0.02

# helper functions


class Tensor2D(VMobject):
    def __init__(
        self,
        data: list | None = None,   # [(n, a), (n, b), (n, c), ...]
        decimal_config: dict = {},
        arrange_config: dict = {},
    ):
        super().__init__()
        # TODO, make sure all dim is the same except the last
        self.formatters, self.col_ratios = self._create_formatters(data)
        self.data = np.concat(data, axis=-1)    # (n,7)
        self.shape = self.data.shape
        self.ndim = self.data.ndim
        self.decimal_config = {**DECIMAL_CONFIG, **decimal_config}
        auto_arrange_config = {
            'cell_width': self.decimal_config['font_size']*FONT_SIZE_WIDTH_RATIO,
            'cell_height': self.decimal_config['font_size']*FONT_SIZE_HEIGHT_RATIO,
        }
        self.arrange_config = {**auto_arrange_config, **arrange_config}

        self.objs = self._create_objs()
        self.mobs = self._create_mobs()
        self._arrange_mobs()

        self.add(self.mobs)
    
    def _create_formatters(
        self,
        group: list,
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
            elif np.issubdtype(data.dtype, np.floating):
                formatter = ['{:.2f}'] * data.shape[1]
                col_ratio = [1.0] * data.shape[1]
            fs = fs + formatter
            cs = cs + col_ratio
        return fs, cs

    def _create_objs(
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
                    **self.decimal_config,
                )
                row_mobs.append(mob)
            mobs.append(row_mobs)
        return mobs
    
    def _create_mobs(
        self,
    ) -> VGroup:
        """Create a vgroup of vgroup of Text based on objs.
        """
        return VGroup( *(VGroup(*row) for row in self.objs))
    
    def _arrange_mobs(
        self,
    ) -> Self:
        """Arrange rows and cols separately
        """
        cfg = self.arrange_config

        for i, row in enumerate(self.mobs):
            for j, mob in enumerate(row):
                dy = i * cfg['cell_height'] * DOWN
                dx = sum(self.col_ratios[:j+1]) * cfg['cell_width'] * RIGHT
                mob.align_to(dy, DOWN)
                mob.align_to(dx, RIGHT)
            
        self.mobs.center()  # to origin after arrange
        return self

    def __getitem__(
        self,
        idx,
    ) -> VMobject:
        """Indexing utils.
           Prerequisites:
                ndims, dimensions of data
                shape, shape of data
                mobs, ???
           NOTE, general naming as self.objs
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

    def apply_whole_take_max(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """For all rows.
           xyxyccc -> xyxyc
        """
        anims = AnimationGroup(
            *(self.apply_row_take_max(
                i,
                **aargs
            ) for i in range(self.shape[0])),
            **gargs,
        )

        # FIXME: update data and shape manually, including cls
        self.data = self.data[:, :6]
        self.shape = self.data.shape

        # FIXME: update formatters and col_ratios, including cls
        self.formatters = self.formatters[:5] + [self.formatters[0]]
        self.col_ratios = self.col_ratios[:5] + [0.6]

        return anims
    
    def apply_row_take_max(
        self,
        n: int,
        **aargs,
    ) -> Animation:
        """For a single row.
           xyxyccc -> xyxyc
        """
        # preserve max conf and cls only, with garbage tail
        row = self.data[n]
        row_tail = row[4:]
        local_idx = row_tail.argmax()
        global_idx = local_idx + 4
        max_val = row_tail[local_idx]
        row[4] = max_val        # save max conf
        row[5] = local_idx      # save cls index
        
        # update objs and mobs
        row_objs = self.objs[n]
        keep_obj = row_objs[global_idx]
        keep_indices = set(list(range(4)) + [global_idx])
        self.objs[n] = row_objs[:4] + [row_objs[global_idx]]
        rm_objs = [
            obj for j, obj in enumerate(row_objs)
            if j not in keep_indices
        ]
        self.mobs.remove(
            *rm_objs
        )

        # shift and unwrite animations
        anims = [
            keep_obj.animate.move_to(
                row_objs[4],
                aligned_edge=(UL),
            )
        ]
        for obj in rm_objs:
            anim = Uncreate(obj)
            anims.append(anim)
        return AnimationGroup(
            *anims,
            **aargs,
        )

    def apply_whole_append_cls(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """For all rows.
        xyxyc -> xyxycC
        """
        anims = AnimationGroup(
            *(self.apply_row_append_cls(
                i,
                **aargs,
            ) for i in range(self.shape[0])),
            **gargs,
        )

        # data and shape already updated
        # formatters and col_ratios already updated

        return anims
    
    def apply_row_append_cls(
        self,
        n: int,
        **aargs,
    ) -> Animation:
        """For a single row.
           Append cls text.
           data is already updated.
        """
        # FIXME, use realtime font size
        mob = Text(
            self.formatters[5].format(self.data[n,5]),
            **self.decimal_config,
        )
        mob.move_to(self[n,-1], aligned_edge=RIGHT)
        mob.shift(RIGHT * self.col_ratios[5] * self.arrange_config['cell_width'])

        # update objs and mobs
        self.objs[n].append(mob)
        self.mobs.add(mob)      # TODO: rearrange??

        anim = Create(
            mob,
            **aargs,
        )
        return anim
    
    def apply_whole_filter_conf(
        self,
        conf: float = 0.5,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """For all rows.
           Keep or remove.
        """
        anims = AnimationGroup(
            *(self.apply_row_filter_conf(
                i, conf=conf, **aargs,
            ) for i in range(self.shape[0])),
            **gargs,
        )

        # update objs and mobs
        objs_to_keep = [row for row, k in zip(self.objs, self.keep) if k]
        objs_to_remove = [row for row, k in zip(self.objs, self.keep) if not k]
        self.objs = objs_to_keep
        for row in objs_to_remove:
            self.mobs.remove(*row)

        # update data and shape
        self.data = self.data[self.keep]
        del self.keep
        self.shape = self.data.shape

        return anims

    def apply_row_filter_conf(
        self,
        n: int,
        conf: float = 0.5,  # conf threshold
        **aargs,
    ) -> Animation:
        """For a single row.
           keep or remove.
        """
        gap = aargs.pop('gap', 1.0)

        row = self[n]
        keep = self.data[n,4] > conf

        # maintian a keep member for later clean job
        if not hasattr(self, 'keep'):
            self.keep = np.zeros(self.shape[0], dtype=bool)
            # FIXME: remember current y and left
            self.orig_y = self.get_y()
            self.orig_left = self.get_corner(LEFT)
        self.keep[n] = keep

        if keep:
            run_time = aargs.get('run_time', 1.0)
            aargs['run_time'] = 2*run_time
            anim = ApplyFunction(
                    lambda mob: mob.scale(1.5).set_color(PURE_GREEN),
                    row,
                    rate_func=rate_functions.there_and_back,
                    **aargs,
                )
        else:
            anim = Succession(
                ApplyFunction(
                    lambda mob: mob.scale(1.5).set_color(PURE_RED),
                    row,
                    **aargs,
                ),
                Wait(gap),
                Uncreate(row, **aargs),
            )
        return anim
    
    def rearrange_after_filter(
        self,
        buff: float | None = None,
        **aargs,
    ) -> Animation:
        """Rearrange current rows.
           Used after filter function.
        """
        buff = buff or self.arrange_config['cell_height']

        rows = VGroup()
        for i in range(self.shape[0]):
            rows.add(self[i])
        rows.generate_target()

        for i, row in enumerate(rows.target):
            # FIXME, use adapted cell height
            dy = i * self.arrange_config['cell_height'] * DOWN
            row.align_to(dy, DOWN)
        rows.target.set_y(self.orig_y)
        rows.target.align_to(self.orig_left, LEFT)

        # clean members?
        del self.orig_y
        del self.orig_left

        anim = MoveToTarget(
            rows, **aargs,
        )

        return anim
    
    def sort(
        self,
        reversed: bool = True, # 1->0 by default
    ) -> Animation:
        """Animation to sort rows according to conf.
           Used before NMS.
        """
        pass
    
    def split_into_classes(
        self,
        direction: np.ndarray = DOWN,
    ) -> list:      # -> (n,6)*[3|2|1]
        pass

    def apply_whole_filter_nms(
        self,
    ) -> Animation:
        pass
    
class Demo(Scene):
    def construct(self):
        tensor = Tensor2D(
            data=[
                np.random.randint(0,999,(20,4)),
                np.random.uniform(0,1,(20,3))
            ],
            decimal_config={
                'font_size': 14.3,
                'color': WHITE,
            },
            arrange_config={
                'cell_width': 0.55,
                'cell_height': 0.3,
            },
        )

        self.play(Create(
            tensor,
            lag_ratio=0.1,
            run_time=0.5,
        ))
        self.wait()

        self.play(AnimationGroup(
            tensor[:,4].animate.set_color(RED),
            tensor[:,5].animate.set_color(GREEN),
            tensor[:,6].animate.set_color(BLUE),
        ))
        self.wait()

        self.play(tensor.apply_whole_take_max(
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': 0.5}
        ))
        # self.play(AnimationGroup(
        #     *(tensor.apply_row_take_max(i) for i in range(tensor.shape[0])),
        #     lag_ratio=0.5,
        #     run_time=2.0,
        # ))
        self.wait()

        self.play(tensor.apply_whole_append_cls(
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': 0.5,},
        ))
        self.wait()

        self.play(tensor[:,4].animate(
            lag_ratio=0.5,
            run_time=0.5,
        ).set_color(WHITE))
        self.wait()

        # self.play(AnimationGroup(
        #     *(tensor.apply_row_filter_conf(
        #         i, conf=0.5, run_time=0.5, gap=0.5,
        #     ) for i in range(tensor.shape[0])),
        #     lag_ratio=0.5,
        #     run_time=2.0,
        # ))
        self.play(tensor.apply_whole_filter_conf(
            conf=0.7,
            aargs={},
            gargs={'lag_ratio':0.5, 'run_time':1.0},
        ))
        self.wait()

        self.play(tensor.rearrange_after_filter(
            run_time=1.0,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait()
import sys
sys.path.append('..')

from manim import *

import itertools
import numpy as np
from typing import Self

from utils.constants import KK_COLORS
from utils.general import compute_iou, random_boxes

DECIMAL_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 22,
    'color': WHITE,
}

# empirically determined, for monospaced font
FONT_SIZE_WIDTH_RATIO = 0.06
FONT_SIZE_HEIGHT_RATIO = 0.02

# helper functions here...

# TODO, store color_map as member
class Tensor2D(VMobject):
    def __init__(
        self,
        data: list | np.ndarray | None = None,   # [(n, a), (n, b), (n, c), ...]
        objs: list | None = None,       # create anew or out-of-the-box
        mobs: list | None = None,       # create anew or out-of-the-box
        formatters: list | None = None, # create anew or out-of-the-box
        col_ratios: list | None = None, # create anew or out-of-the-box
        decimal_config: dict | None = None,
        arrange_config: dict | None = None,
    ):
        """Most complicated and general way of init.
        """
        super().__init__()
        # TODO, make sure all dim is the same except the last
        if isinstance(data, np.ndarray):
            # init from existing
            self.data = data                        # given array
            self.formatters = formatters
            self.col_ratios = col_ratios
        else:
            # init anew
            self.data = np.concat(data, axis=-1)    # a list -> (n,7)
            self.formatters, self.col_ratios = self._create_formatters(data)
        self.shape = self.data.shape
        self.ndim = self.data.ndim
        self.decimal_config = {**DECIMAL_CONFIG, **decimal_config}
        auto_arrange_config = {
            'cell_width': self.decimal_config['font_size']*FONT_SIZE_WIDTH_RATIO,
            'cell_height': self.decimal_config['font_size']*FONT_SIZE_HEIGHT_RATIO,
        }
        self.arrange_config = {**auto_arrange_config, **arrange_config}

        if objs and mobs:
            # init from existing
            self.objs = objs
            self.mobs = mobs
        else:
            # init anew
            self.objs = self._create_objs()
            self.mobs = self._create_mobs()
            self._arrange_mobs()
            self.mobs.center()      # invalid center after arrange
        
        self.nms_done = False       # FIXME, used while start nms loop

        self.add(self.mobs)
    
    def _create_formatters(
        self,
        group: list,
    ) -> tuple:
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
        data: list | None = None,
    ) -> list:
        """Create a list of list of decimal vmobject.
        """
        if data is None:
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
        """Create a vgroup of vgroup of Text.
        """
        # if objs is None:
        #     objs = self.objs
        # return VGroup(*(mob for row in self.objs for mob in row))
        return VGroup( *(VGroup(*row) for row in self.objs))
    
    def arrange_as_matrix(
        self,
        center_x: float | None = None,      # target cx
        center_y: float | None = None,      # target cy
    ) -> Self:
        """Arrange internal mobs into matrix.
           Assume that self.mobs is a vg of vg.
        """
        center_x = center_x or self.get_x()
        center_y = center_y or self.get_y()
        cfg = self.arrange_config
        for i, row in enumerate(self.mobs):
            for j, mob in enumerate(row):
                mob.move_to(ORIGIN, aligned_edge=RIGHT)
                mob.shift(
                    cfg['cell_height']*DOWN*i +
                    sum(self.col_ratios[:j+1]) * cfg['cell_width'] * RIGHT
                )
        self.mobs.move_to(np.array([center_x, center_y, 0]))
        return Self
    
    def _arrange_mobs(
        self,
        objs: list | VGroup | None = None,
    ) -> Self:
        """Arrange mobs by rows and cols.
           Current objs by default.
           Keep original cx/cy or use given cx/cy as center.
        """
        if objs is None:
            objs = self.objs

        cfg = self.arrange_config

        for i, row in enumerate(objs):
            for j, mob in enumerate(row):
                dy = i * cfg['cell_height'] * DOWN
                dx = sum(self.col_ratios[:j+1]) * cfg['cell_width'] * RIGHT
                mob.align_to(dy, DOWN)
                mob.align_to(dx, RIGHT)
            
        # self.mobs.center()  # to origin after arrange
        return self     # FIXME: or what else?

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
        aargs: dict | None = None,
        gargs: dict | None = None,
    ) -> Animation:
        """For all rows.
           xyxyccc -> xyxyc
        """
        anims = AnimationGroup(
            *(self.apply_row_take_max(
                i,
                **(aargs or {})
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
                aligned_edge=RIGHT,
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
        aargs: dict | None = None,
        gargs: dict | None = None,
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

        # update mobs according to objs
        self.mobs = self._create_mobs()
        self.add(self.mobs)
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
        ).set_color(KK_COLORS[int(self.data[n,5])])  # from color map
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
        aargs: dict | None = None,
        gargs: dict | None = None,
    ) -> Animation:
        """For all rows.
           Keep or remove.
        """
        anims = AnimationGroup(
            *(self.apply_row_filter_conf(
                i, conf=conf, **(aargs or {}),
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
                Uncreate(row, **(aargs or {})),
            )
        return anim
    
    def rearrange_after_filter(
        self,
        buff: float | None = None,
        **aargs,
    ) -> Animation:
        """Rearrange current rows.
           Fill the gaps after filter function.
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
            rows, **(aargs or {}),
        )

        return anim
    
    def sort(
        self,
        reverse: bool = True, # 1->0 by default
        **aargs,
    ) -> Animation:
        """Animation to sort rows according to conf.
           Used before NMS.
        """
        orig_x = self.mobs.get_x()
        orig_y = self.mobs.get_y()
        orig_top = self.mobs.get_top()

        # idx = sorted(
        #     range(len(self.objs)),
        #     key = lambda i: self.data[i][4],
        #     reverse = reverse,
        # )
        idx = np.argsort(self.data[:,4])
        if reverse:
            idx = idx[::-1]
        self.data = self.data[idx]
        self.objs = [self.objs[i] for i in idx]
        self.mobs = self._create_mobs()

        return ApplyMethod(
            self.arrange_as_matrix,
            orig_x,
            orig_y,
            **aargs,
        )
        # mobs = VGroup( VGroup(*row) for row in self.objs)   # vg of vg
        # mobs.generate_target()

        # self.generate_target()
        # self.target.arrange_as_matrix()

        # reposition target tensor
        # self._arrange_mobs(mobs.target)
        # mobs.target.set_x(orig_x).align_to(orig_top, UP)
        # arrange_as_matrix(
        #     cell_w=self.arrange_config['cell_width'],
        #     cell_h=self.arrange_config['cell_height'],
        #     center_x=orig_x,
        #     center_y=orig_y,
        # )(mobs.target)
        # mobs.target.arrange_as_matrix()
        # mobs.target.align_to(orig_top, UP)
        # self.mobs = mobs        # update mobs with sorted version

        # anim = MoveToTarget(self, **(aargs or {}))
        # return anim
    
    def split_into_classes(
        self,
        buff: float = 0.5,          # vertical buff by default
        horizontal: bool = False,   # vertical split by default
        **aargs,
    ) -> Animation:      # -> (n,6)*[3|2|1], 3 generally
        """Assume to be 3 classes by default.
           save ghost data/objs/mobs to popped out later.
        """
        ghost_data = {}     # {n -> np.array}
        ghost_objs = {}     # {n -> list of list of vmobject}
        ghost_mobs = {}     # {n -> vgroup of vmobject}

        keys = np.unique(self.data[:, 5])
        for k in keys:
            idx = np.where(self.data[:, 5] == k)[0]
            ghost_data[k] = self.data[idx]
            ghost_objs[k] = [self.objs[i] for i in idx]
            # ghost_mobs[k] = VGroup(
            #     *(mob for i in idx for mob in self[i])
            # )
            ghost_mobs[k] = VGroup(
                VGroup(mob for mob in self[i]) for i in idx 
            )   # vgroup of vgroup for now, flatten later

        # position reference
        orig_x = self.mobs.get_x()  # for horizontal split
        orig_y = self.mobs.get_y()  # for vertical split
        orig_left = self.mobs.get_left()

        mobs = VGroup(ghost_mobs[k] for k in keys)  # vg of vg of vg
        mobs.generate_target()

        for t in mobs.target:
            self._arrange_mobs(t)
        
        mobs.target.arrange(
            direction=DOWN,
            buff=buff,
        ).set_y(orig_y).align_to(orig_left, LEFT)

        # remember ghosts to pop out later
        self.ghost_keys = keys
        self.ghost_data = ghost_data
        self.ghost_objs = ghost_objs
        # flatten mobs first
        for k in keys:
            ghost_mobs[k] = VGroup(mob for row in ghost_mobs[k] for mob in row)
        self.ghost_mobs = ghost_mobs
        
        anim = MoveToTarget(mobs, **(aargs or {}))
        return anim
        
        # # color setup for test
        # anims = AnimationGroup(
        #     vg.animate.set_color(random_color())
        #     for vg in ghost_mobs.values()
        # )
        # return anims

    def pop_ghosts(
        self,
    ) -> list:      # a list of Tensor2d
        """Assume to be 3 classes by default.
           Pop out a list of Tensor2d from ghosts content.
           TODO, more general and better naming...
        """
        res = []
        for k in self.ghost_keys:
            data = self.ghost_data[k]
            objs = self.ghost_objs[k]
            mobs = self.ghost_mobs[k]
            formatters = self.formatters
            col_ratios = self.col_ratios
            decimal_config = self.decimal_config
            arrange_config = self.arrange_config
            res.append(Tensor2D(
                data,
                objs,
                mobs,
                formatters,
                col_ratios,
                decimal_config,
                arrange_config,
            ))
        
        return res
    
    def apply_filter_nms_anim(
        self,
        scene,
        shift: float = 3.5,
        iou_thresh: float = 0.1,
        run_time_ratio: float = 1.0,
    ):
        """Apply NMS filter.
        """
        keep_data = np.empty((0, self.data.shape[1]))
        cand_idxs = list(range(self.data.shape[0]))
        keep_idxs = []
        keep_objs = []
        keep_mobs = VGroup()
        # nms_done = False

        while len(cand_idxs) > 0:
            k_idx = cand_idxs.pop(0)
            k_data = self.data[k_idx]
            k_box = k_data[:4]
            k_objs = [mob.copy() for mob in self.objs[k_idx]]
            k_mobs = VGroup(*k_objs)

            keep_idxs.append(k_idx)
            keep_data = np.vstack([keep_data, k_data])
            keep_objs.append(k_objs)
            keep_mobs.add(k_mobs)

            # show copy of best candidate
            self.add(k_mobs)

            # shift out best copy
            scene.play(AnimationGroup(
                ApplyMethod(
                    self[k_idx].set_opacity,
                    0.2,
                ),
                ApplyMethod(
                    k_mobs.shift,
                    RIGHT*shift,
                    rate_func=rate_functions.ease_out_back,
                ),
                run_time=1.0*run_time_ratio,
            ))

            # check if the last row shifted out
            if len(cand_idxs) == 0:
                break
            
            # compute ious between best and candidates
            cand_boxes = self.data[cand_idxs, :4]
            ious = compute_iou(k_box, cand_boxes)
            survive_mask = ious <= iou_thresh

            # compute passing cand_idxs
            auth_idxs = cand_idxs
            cand_idxs = [x for x, s in zip(cand_idxs, survive_mask) if s]
            
            mob_line = Line(
                start=k_mobs.get_left()-[0.1,0,0],
                end=self[auth_idxs[0]].get_right()+[0.1,0,0],
                stroke_width=2.4,
                stroke_color=WHITE,    # WHITE initially
            ).set_opacity(0.2)
            mob_iou = DecimalNumber(
                ious[0],
                num_decimal_places=2,
                align_to_dot=True,
                font_size=20,
                color=PURE_GREEN if survive_mask[0] else PURE_RED,
            ).move_to(mob_line)

            # create the first connection and iou
            scene.play(Succession(
                Create(
                    mob_line,
                    run_time=1.0*run_time_ratio,
                ),
                Create(
                    mob_iou,
                    run_time=1.0*run_time_ratio,
                ),
                Wait(1.0*run_time_ratio),
            ))

            # verify the first connection
            if survive_mask[0]:
                scene.play(AnimationGroup(
                    mob_iou.animate(
                        run_time=1.0*run_time_ratio,
                    ).set_color(PURE_GREEN),
                ))
                scene.wait(1.0*run_time_ratio)
            else:
                scene.play(AnimationGroup(
                    ApplyMethod(
                        self[auth_idxs[0]].set_opacity,
                        0.2,    # TODO, fade out factor
                        run_time=1.0*run_time_ratio,
                    ),
                    mob_iou.animate(
                        run_time=1.0*run_time_ratio,
                    ).set_color(PURE_RED),
                ))
                scene.wait(1.0*run_time_ratio)
            
            # done if only one connection available
            if len(auth_idxs) == 1:
                scene.play(
                    Uncreate(mob_iou, run_time=1.0*run_time_ratio),
                )
                scene.play(
                    Uncreate(mob_line, run_time=1.0*run_time_ratio),
                )
                scene.wait(1.0*run_time_ratio)
                continue

            for idx, survive, iou in zip(auth_idxs[1:], survive_mask[1:], ious[1:]):
                mob_line_target = mob_line.copy().put_start_and_end_on(
                    start=mob_line.get_start(),
                    end=self[idx].get_right()+[0.1,0,0],
                )
                scene.play(AnimationGroup(
                    Transform(
                        mob_line,
                        mob_line_target,
                        run_time=1.0*run_time_ratio,
                    ),
                    mob_iou.animate(
                        run_time=1.0*run_time_ratio,
                    ).move_to(mob_line_target),
                ))
                scene.play(
                    ChangeDecimalToValue(
                        mob_iou,
                        iou,
                        run_time=1.0*run_time_ratio,
                    )
                )
                if survive:
                    scene.play(AnimationGroup(
                        mob_iou.animate(
                            run_time=1.0*run_time_ratio,
                        ).set_color(PURE_GREEN),
                    ))
                    scene.wait(1.0*run_time_ratio)
                else:
                    scene.play(AnimationGroup(
                        ApplyMethod(
                            self[idx].set_opacity,
                            0.2,    # TODO, fadeout factor
                            run_time=1.0*run_time_ratio,
                        ),
                        mob_iou.animate(
                            run_time=1.0*run_time_ratio,
                        ).set_color(PURE_RED),
                    ))
                    scene.wait(1.0*run_time_ratio)

            scene.play(
                Uncreate(mob_iou, run_time=1.0*run_time_ratio),
            )
            scene.play(
                Uncreate(mob_line, run_time=1.0*run_time_ratio),
            )
            scene.wait(1.0*run_time_ratio)

        # pop mobs and construct a new Tensor
        self.remove(*keep_mobs)
        result = Tensor2D(
            data=keep_data,
            objs=keep_objs,
            mobs=keep_mobs,
            formatters=self.formatters,
            col_ratios=self.col_ratios,
            decimal_config=self.decimal_config,
            arrange_config=self.arrange_config,
        )
        return result
    
class Demo(Scene):
    def construct(self):
        tensor = Tensor2D(
            data=[
                # np.random.randint(0,999,(20,4)),
                random_boxes(20),
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

        cols_a = tensor[:,4]
        cols_b = tensor[:,5]
        cols_c = tensor[:,6]
        self.play(AnimationGroup(
            *(Succession(
                m.animate.scale(2.0).set_color(KK_COLORS[0]),
                ApplyMethod(m.scale, 0.5),
            ) for m in cols_a),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.play(AnimationGroup(
            *(Succession(
                m.animate.scale(2.0).set_color(KK_COLORS[1]),
                ApplyMethod(m.scale, 0.5),
            ) for m in cols_b),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.play(AnimationGroup(
            *(Succession(
                m.animate.scale(2.0).set_color(KK_COLORS[2]),
                ApplyMethod(m.scale, 0.5),
            ) for m in cols_c),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.5)

        # self.play(AnimationGroup(
        #     tensor[:,4].animate.set_color(KK_COLORS[0]),
        #     tensor[:,5].animate.set_color(KK_COLORS[1]),
        #     tensor[:,6].animate.set_color(KK_COLORS[2]),
        # ))
        # self.wait()

        self.play(tensor.apply_whole_take_max(
            aargs={'rate_func': rate_functions.ease_out_back,}, # TODO: rate_func works?
            gargs={'lag_ratio': 0.2, 'run_time': 1.5}
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

        self.play(tensor[:,4:].animate(
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
        # self.play(tensor.apply_whole_filter_conf(
        #     conf=0.7,
        #     aargs={},
        #     gargs={'lag_ratio':0.5, 'run_time':1.0},
        # ))
        # self.wait()

        # self.play(tensor.rearrange_after_filter(
        #     run_time=1.0,
        #     rate_func=rate_functions.ease_out_back,
        # ))
        # self.wait()

        # TODO: setup colors according to cls

        self.play(tensor.sort(
            reverse=True,
            run_time=1.0,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait()

        # conf = tensor[:, 4]
        # self.play(AnimationGroup(
        #     *(c.animate(
        #         rate_func=rate_functions.there_and_back,
        #     ).scale(2.0) for c in conf),
        #     lag_ratio=0.3,
        #     run_time=1.0,
        # ))
        # self.wait()
        # self.play(tensor[:, 4].animate(
        #     lag_ratio=0.1,
        #     run_time=2.0,
        #     rate_func=rate_functions.there_and_back,
        # ).scale(2.5))
        # self.wait()

        # # split into classes
        # self.play(tensor.split_into_classes(
        #     buff=0.5,
        #     run_time=1.0,
        # ))
        # self.wait()

        # tensor_vg = tensor.pop_ghosts()
        # ta, tb, tc = tensor_vg
        # tensor_vg = VGroup(*tensor_vg)
        # self.play(tensor_vg.animate.arrange(RIGHT))
        # self.wait()

        # # for test new tensors
        # self.play(AnimationGroup(
        #     ta[:, 2].animate.set_color(GREEN),
        #     tb[1:3, 2:4].animate.set_color(RED),
        #     tc[1, :].animate.set_color(BLUE),
        # ))
        # self.wait()

        nms = tensor.apply_filter_nms_anim(
            scene=self,
            shift=3.5,
            iou_thresh=0.08,
            run_time_ratio=0.1,
        )
        self.wait()

        self.play(ApplyMethod(
            nms.arrange_as_matrix,
            nms.get_x(),
            tensor.get_y(),
            rate_func=rate_functions.ease_in_out_back,
        ))
        self.wait()

        # tensor = tensor.pop_nms_anim()  # FIXME, naming

        # # TODO, need elegant way..
        # while True:
        #     # self.play(tensor.apply_once_nms(
        #     #     iou_thresh=0.05,
        #     # ))
        #     # self.wait(0.5)
        #     self.play(tensor.nms_take_best(
        #         shift=3.6,
        #         run_time=0.3,
        #     ))
        #     self.wait(0.5)

        #     if tensor.nms_done:
        #         break

        #     # self.play(tensor.nms_verify_candidates(
        #     tensor.nms_verify_candidates(
        #         self,
        #         iou_thresh=0.05,
        #         aargs={},
        #         gargs={},
        #     )
        #     self.wait(0.5)

        #     if tensor.nms_done:
        #         break

# class Demo2(Scene):
#     def construct(self):
#         vg = VGroup(
#             VGroup(Square().scale(0.2) for _ in range(4))
#               for _ in range(3)
#         )
#         self.play(Write(vg))
#         self.wait()
#         self.play(ApplyFunction(arrange_as_matrix(
#             center_x=vg.get_x(),
#             center_y=vg.get_y(),
#         ), vg))
#         self.wait()

        
#         self.play(ApplyFunction(arrange_as_matrix(
#             cell_w=1.2,
#             cell_h=0.9,
#             center_x=vg.get_x(),
#             center_y=vg.get_y(),
#         ), vg))
#         self.wait()

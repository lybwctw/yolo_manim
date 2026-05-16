from __future__ import annotations
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

# helper functions
def create_formatters(data: np.ndarray) -> list:
    if np.issubdtype(data.dtype, np.integer):
        formatters = ['{:>3.0f}'] * data.shape[1]
    elif np.issubdtype(data.dtype, np.floating):
        formatters = ['{:.2f}'] * data.shape[1]
    return formatters

def create_col_ratios(data: np.ndarray) -> list:
    if np.issubdtype(data.dtype, np.integer):
        col_ratios = [0.8] * data.shape[1]
    elif np.issubdtype(data.dtype, np.floating):
        col_ratios = [1.0] * data.shape[1]
    return col_ratios


class Tensor2D(VMobject):
    """TODO: fade input before animation?
    """
    def __init__(
        self,
        data: np.ndarray,
        formatters: list | None = None,
        col_ratios: list | None = None,
        decimal_config: dict = {},
        cell_width: float | None = None,
        cell_height: float | None = None,
        objs: list | None = None,
        mobs: VGroup | None = None,
    ):
        """Init by providing all members.
        """
        super().__init__()
        self.data = data                # raw np data

        self.formatters = formatters or create_formatters(data)
        self.col_ratios = col_ratios or create_col_ratios(data)
        self.decimal_config = {**DECIMAL_CONFIG, **decimal_config}
        self.cell_width = cell_width or self.decimal_config['font_size']*0.06
        self.cell_height = cell_height or self.decimal_config['font_size']*0.02

        if objs is None:
            # arrange as matrix if newly created
            self.objs = self.create_objs()
            self.mobs = self.create_mobs()
            self.arrange_matrix(ORIGIN)
        else:
            # donot arrange if provided
            self.objs = objs
            self.mobs = mobs

        self.add(self.mobs)
    
    def create_objs(
        self,
    ) -> list:
        """Create a list of list of vmobjects
           based on raw data, formatters and decimal_config.
        """
        objs = []
        for row in self.data.tolist():
            row_objs = []
            for i,d in enumerate(row):
                mob = Text(
                    self.formatters[i].format(d),
                    **self.decimal_config,
                )
                row_objs.append(mob)
            objs.append(row_objs)
        return objs

    def create_mobs(
        self,
    ) -> VGroup:
        """Create a vg of vg of vmobjects based on objs.
        """
        return VGroup( *(VGroup(*row) for row in self.objs))

    def arrange_matrix(
        self,
        point: np.ndarray = ORIGIN,     # target center point
    ) -> Self:
        """Arrange internal mobs into matrix.
           Assume that self.mobs is a vg of vg.
        """
        center_x, center_y, _ = point
        for i, row in enumerate(self.mobs):
            for j, mob in enumerate(row):
                mob.move_to(ORIGIN, aligned_edge=RIGHT)
                mob.shift(
                    self.cell_height*DOWN*i +
                    sum(self.col_ratios[:j+1]) * self.cell_width * RIGHT
                )
        self.mobs.move_to(np.array([center_x, center_y, 0]))
        return Self
    
    def arrange_as_matrix(
        self,
        center_x: float | None = None,      # target cx
        center_y: float | None = None,      # target cy
    ) -> Self:
        center_x = center_x or self.get_x()
        center_y = center_y or self.get_y()
        for i, row in enumerate(self.mobs):
            for j, mob in enumerate(row):
                mob.move_to(ORIGIN, aligned_edge=RIGHT)
                mob.shift(
                    self.cell_height*DOWN*i +
                    sum(self.col_ratios[:j+1]) * self.cell_width * RIGHT
                )
    
    def into_take_max(
        self,
        scene: Scene,
        offset: np.ndarray = RIGHT,
        run_time_ratio: float = 1.0,
    ) -> Tensor2D:
        """[Internal animation]
           Replace the last n-4 cols with max.
        """
        # containers for building new tensor
        res_data = np.empty((0, 6))     # always 4+2
        res_objs = []
        res_mobs = VGroup()

        # containers for animation
        mobs_xyxy_c = VGroup()
        mobs_cmax_c = VGroup()
        mobs_cothers = VGroup()
        mobs_cls_c = VGroup()

        for data_row, obj_row in zip(self.data, self.objs):
            _max_idx = data_row[4:].argmax()    # local max index
            max_idx = _max_idx + 4              # global max index

            # original data
            data_xyxy = data_row[:4]
            data_cmax = data_row[max_idx]

            # new data row
            data_c = np.concat([data_xyxy, [data_cmax, _max_idx]])

            # old objs/mobs
            obj_xyxy = obj_row[:4]
            mob_xyxy = VGroup(*obj_xyxy)
            obj_cmax = obj_row[max_idx]
            mob_cmax = obj_cmax
            obj_cothers = [obj_row[i] for i in range(len(obj_row)) if i != max_idx][4:]
            mob_cothers = VGroup(*obj_cothers)

            # new objs/mobs
            obj_xyxy_c = [obj.copy() for obj in obj_xyxy]
            mob_xyxy_c = VGroup(*obj_xyxy_c)
            obj_cmax_c = obj_cmax.copy()
            mob_cmax_c = obj_cmax_c
            obj_cls_c = Text(
                self.formatters[0].format(_max_idx),    # use local max index
                **self.decimal_config,
            )
            mob_cls_c = obj_cls_c

            # update group containers
            res_data = np.vstack([res_data, data_c])
            res_objs.append(obj_xyxy_c + [obj_cmax_c, obj_cls_c])
            res_mobs.add(VGroup(*mob_xyxy_c, mob_cmax_c, obj_cls_c))
            mobs_xyxy_c.add(mob_xyxy_c)
            mobs_cmax_c.add(mob_cmax_c)
            mobs_cothers.add(mob_cothers)
            mobs_cls_c.add(mob_cls_c)

        # fade out those non-max conf
        scene.play(AnimationGroup(
            *(others.animate.set_opacity(0.2)
             for others in mobs_cothers),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(0.5*run_time_ratio)

        # shift out xyxy
        scene.play(AnimationGroup(
            *(xyxy.animate(
                rate_func=rate_functions.ease_out_back,
            ).shift(offset) for xyxy in mobs_xyxy_c),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(0.5*run_time_ratio)

        # shift out max conf
        scene.play(AnimationGroup(
            *(mconf.animate(
                rate_func=rate_functions.ease_out_back,
            ).next_to(xyxy, RIGHT) for mconf, xyxy in zip(
                mobs_cmax_c, mobs_xyxy_c
            )),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(0.5*run_time_ratio)

        # create max cls index col
        for mob, ref in zip(mobs_cls_c, mobs_cmax_c):
            mob.next_to(ref, RIGHT)
        scene.play(GrowFromCenter(  # or Create?
            mobs_cls_c,
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(0.5*run_time_ratio)

        # build Tensor2D
        result = Tensor2D(
            data=res_data,
            formatters=self.formatters[:5] + [self.formatters[0]],
            col_ratios=self.col_ratios[:5] + [self.col_ratios[0]*0.6],    # TODO: small ratio for cls
            decimal_config=self.decimal_config,
            cell_width=self.cell_width,
            cell_height=self.cell_height,
            objs=res_objs,
            mobs=res_mobs,
        )
        scene.add(result)       # auto add after creation
        return result

    def into_filter_conf(
        self,
        scene: Scene,
        conf_thresh: float = 0.25,
        offset: np.ndarray = RIGHT,
        run_time_ratio: float = 1.0,
    ) -> Tensor2D:
        """[Internal animation]
           Filter out rows with small conf score.
        """
        # containers for building new tensor
        res_data = np.empty((0, 6))     # always 4+2
        res_objs = []
        res_mobs = VGroup()

        # containers for animation
        mobs_failed = VGroup()

        for data_row, obj_row, mob_row in zip(self.data, self.objs, self.mobs):
            failed = data_row[4] < conf_thresh
            if failed:
                mobs_failed.add(mob_row)
            else:
                res_data = np.vstack([res_data, data_row])
                obj_row_c = [obj.copy() for obj in obj_row]
                mob_row_c = VGroup(*obj_row_c)
                res_objs.append(obj_row_c)
                res_mobs.add(mob_row_c)
        
        # fade out those failed
        scene.play(AnimationGroup(
            *(mobs.animate.set_opacity(0.2)
              for mobs in mobs_failed),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(0.5*run_time_ratio)

        # shift out passed ones
        scene.play(AnimationGroup(
            *(line.animate(
                rate_func=rate_functions.ease_out_back,
            ).shift(offset) for line in res_mobs),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(0.5*run_time_ratio)

        # build Tensor2D
        result = Tensor2D(
            data=res_data,
            formatters=self.formatters,
            col_ratios=self.col_ratios,
            decimal_config=self.decimal_config,
            cell_width=self.cell_width,
            cell_height=self.cell_height,
            objs=res_objs,
            mobs=res_mobs,
        )
        scene.add(result)       # auto add after creation

        # arrange animation to fill gaps
        scene.play(ApplyMethod(
            result.arrange_matrix,
            np.array([result.get_x(), self.get_y(), 0]),
            rate_func=rate_functions.ease_out_back,
        ))
        scene.wait(0.5*run_time_ratio)
        
        return result


    def into_splitted(
        self,
        scene: Scene,
        offset: np.ndarray = RIGHT,
        buff: float = 0.25,
        run_time_ratio: float = 1.0,
    ) -> list:
        """[Internal animation]
           Split into multiple Tensor2D based on cls index.
           NOTE: Assume that col [5] is cls index.
        """
        # containers for building new tensors
        res_data = {}       # idx -> np array of (n, 6)
        res_objs = {}       # idx -> list of list
        res_mobs = {}       # idx -> vg of vg

        clss = np.unique(self.data[:, 5])
        for cls in clss:
            idxs = np.where(self.data[:, 5] == cls)[0]
            res_data[cls] = self.data[idxs].copy()
            res_objs[cls] = [ [obj.copy() for obj in self.objs[i]] for i in idxs ]
            res_mobs[cls] = VGroup( VGroup(*row) for row in res_objs[cls])

        tensors = []
        for cls in clss:
            tensor = Tensor2D(
                data=res_data[cls],
                formatters=self.formatters,
                col_ratios=self.col_ratios,
                decimal_config=self.decimal_config,
                cell_width=self.cell_width,
                cell_height=self.cell_height,
                objs=res_objs[cls],
                mobs=res_mobs[cls],
            )
            tensors.append(tensor)
            scene.add(tensor)       # auto add after creation
        
        # prepare animation target
        for tensor in tensors:
            tensor.generate_target()
            tensor.target.arrange_matrix(
                point=tensor.get_center(),
            )   # FIXME: why Self.shift failed?
            tensor.target.shift(offset)
        targets = VGroup(tensor.target for tensor in tensors)
        targets.arrange(DOWN, buff=buff, center=False)
        targets.set_y(self.get_y())

        # line by line animation
        for tensor in tensors:
            scene.play(AnimationGroup(
                *(Transform(
                    r1, r2,
                    rate_func=rate_functions.ease_out_back,
                    run_time=0.2*run_time_ratio,
                ) for r1, r2 in zip(tensor.rows, tensor.target.rows)),
                lag_ratio=0.5,
            ))
        # scene.play(AnimationGroup(
        #     *(MoveToTarget(
        #         tensor,
        #         run_time=1.0*run_time_ratio,
        #         lag_ratio=0.5,
        #         # rate_func=rate_functions.ease_out_back,
        #     ) for tensor in tensors),
        #     lag_ratio=0.5,
        # ))
        return tensors

    def into_sort(
        self,
        scene: Scene,
        reverse: bool = True,
        offset: np.ndarray = RIGHT,
        run_time_ratio: float = 1.0,
    ) -> Tensor2D:
        """[Internal animation]
           Sort rows according to conf col [4].
        """
        idxs = np.argsort(self.data[:,4])
        if reverse:
            idxs = idxs[::-1]
        
        # build tensor members at a time
        res_data = self.data[idxs]
        res_objs = [
            [obj.copy() for obj in self.objs[i]] for i in idxs
        ]
        res_mobs = VGroup( VGroup(*row) for row in res_objs)

        # build result tensor first
        result = Tensor2D(
            data=res_data,
            formatters=self.formatters,
            col_ratios=self.col_ratios,
            decimal_config=self.decimal_config,
            cell_width=self.cell_width,
            cell_height=self.cell_height,
            objs=res_objs,
            mobs=res_mobs,
        )

        # shift target and arrange
        result.generate_target()
        result.target.shift(offset)
        result.target.arrange_matrix(
            point=result.target.get_center(),
        )

        # line by line animation
        scene.play(AnimationGroup(
            *(Transform(
                r1, r2,
                rate_func=rate_functions.ease_out_back,
                run_time=0.2*run_time_ratio,
            ) for r1, r2 in zip(result.rows, result.target.rows)),
            lag_ratio=0.5,
        ))
        return result

    def into_filter_nms(
        self,
        scene: Scene,
        iou_thresh: float = 0.75,
        offset: np.ndarray = RIGHT,
        run_time_ratio: float = 1.0,
    ) -> Tensor2D:
        """[Internal animation]
           Apply NMS filter.
        """
        # containers for building new tensor
        res_data = np.empty((0, 6))     # always 4+2
        res_objs = []
        res_mobs = VGroup()
        
        cand_idxs = list(range(len(self.objs)))

        while len(cand_idxs) > 0:
            k_idx = cand_idxs.pop(0)
            k_data = self.data[k_idx]
            k_box = k_data[:4]
            k_objs = [mob.copy() for mob in self.objs[k_idx]]
            k_mobs = VGroup(*k_objs)

            # update output tensor's member
            res_data = np.vstack([res_data, k_data])
            res_objs.append(k_objs)
            res_mobs.add(k_mobs)

            # self.add(k_mobs)

            # shift out current best, fade original
            scene.play(AnimationGroup(
                ApplyMethod(
                    self[k_idx].set_opacity,
                    0.2,
                ),
                ApplyMethod(
                    k_mobs.shift,
                    RIGHT*offset,
                    rate_func=rate_functions.ease_out_back,
                ),
                run_time=0.5*run_time_ratio,
            ))

            # done if the last shifted out
            if len(cand_idxs) == 0:
                break

            # compute ious between best and candidates
            cand_boxes = self.data[cand_idxs, :4]
            ious = compute_iou(k_box, cand_boxes)
            survive_mask = ious <= iou_thresh

            # create initial line and iou mobs
            mob_line = Line(
                start=k_mobs.get_left()-[0.1,0,0],
                end=self[cand_idxs[0]].get_right()+[0.1,0,0],
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
            
            for _idx, (idx, survive, iou) in enumerate(zip(cand_idxs, survive_mask, ious)):
                if _idx == 0:
                    # create for the first connection
                    scene.play(Succession(
                        Create(
                            mob_line,
                            run_time=0.2*run_time_ratio,
                        ),
                        Create(
                            mob_iou,
                            run_time=0.2*run_time_ratio,
                        ),
                    ))
                    # scene.wait(1.0*run_time_ratio)
                else:
                    # transform for the other connections
                    mob_line_target = mob_line.copy().put_start_and_end_on(
                        start=mob_line.get_start(),
                        end=self[idx].get_right()+[0.1,0,0],
                    )
                    scene.play(AnimationGroup(
                        Transform(
                            mob_line,
                            mob_line_target,
                            run_time=0.2*run_time_ratio,
                        ),
                        mob_iou.animate(
                            run_time=0.2*run_time_ratio,
                        ).move_to(mob_line_target),
                    ))
                    # scene.wait(1.0*run_time_ratio)

                    # change iou to current value
                    scene.play(
                        ChangeDecimalToValue(
                            mob_iou,
                            iou,
                            run_time=0.2*run_time_ratio,
                        )
                    )
                    # scene.wait(1.0*run_time_ratio)

                # verify connection
                if survive:
                    scene.play(AnimationGroup(
                        mob_iou.animate(
                            run_time=0.2*run_time_ratio,
                        ).set_color(PURE_GREEN),
                    ))
                    # scene.wait(1.0*run_time_ratio)
                else:
                    scene.play(AnimationGroup(
                        ApplyMethod(
                            self[idx].set_opacity,
                            0.2,    # TODO, fadeout factor
                            run_time=0.2*run_time_ratio,
                        ),
                        mob_iou.animate(
                            run_time=0.2*run_time_ratio,
                        ).set_color(PURE_RED),
                    ))
                    # scene.wait(1.0*run_time_ratio)

            # uncreate the last connection
            scene.play(Succession(
                Uncreate(
                    mob_iou,
                    run_time=0.5*run_time_ratio,
                ),
                Uncreate(
                    mob_line,
                    run_time=0.5*run_time_ratio,
                ),
            ))
            scene.wait(1.0*run_time_ratio)

            # NOTE: filter cand_idxs using survive_mask
            cand_idxs = [x for x, s in zip(cand_idxs, survive_mask) if s]
        
        # build Tensor2D
        result = Tensor2D(
            data=res_data,
            formatters=self.formatters,
            col_ratios=self.col_ratios,
            decimal_config=self.decimal_config,
            cell_width=self.cell_width,
            cell_height=self.cell_height,
            objs=res_objs,
            mobs=res_mobs,
        )
        scene.add(result)       # auto add after creation

        # arrange animation to fill gaps
        scene.play(ApplyMethod(
            result.arrange_matrix,
            np.array([result.get_x(), self.get_y(), 0]),
            rate_func=rate_functions.ease_out_back,
        ))
        scene.wait(0.5*run_time_ratio)

        return result


    # def apply_take_max():
    # def apply_filter_conf():
    # def apply_sort():
    # def apply_filter_nms():

    def __getitem__(
        self,
        idx,
    ) -> VMobject:
        """Indexing utils.
           Prerequisites:
                ndims, dimensions of data
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

    
    @property
    def rows(self):
        return self.mobs

    @property
    def shape(self) -> tuple:
        return self.data.shape

    @property
    def ndim(self) -> int:
        return len(self.shape)
    
    @classmethod
    def from_list(
        cls,
        data_list: list,
        decimal_config: dict = {},          # auto or override
        cell_width: float | None = None,    # auto or override
        cell_height: float | None = None,   # auto or override
    ):
        """Build Tensor2D from a list of arrays.
        """
        # create raw data
        data_raw = np.concat(data_list, axis=-1)

        # create formatters and col_ratios
        formatters = [d for data in data_list for d in create_formatters(data)]
        col_ratios = [d for data in data_list for d in create_col_ratios(data)]
        
        return Tensor2D(
            data=data_raw,
            formatters=formatters,
            col_ratios=col_ratios,
            decimal_config=decimal_config,
            cell_width=cell_width,
            cell_height=cell_height,
        )
    
    @classmethod
    def from_ref(
        cls,
        data,
        objs,
        mobs,
        ref,
    ):
        pass



class Demo(Scene):
    def construct(self):
        GAP = 4

        # build raw output tensor
        tensor_output = Tensor2D.from_list(
            [
                # np.random.randint(0, 640, (25, 4)),
                random_boxes(25),
                np.random.uniform(0, 1, (25, 3))
            ],
            decimal_config={'font_size': 12},
            cell_width=0.6,
        ).shift(LEFT*4)
        self.add(tensor_output)
        self.wait(0.2)

        # apply take max step
        tensor_cmax = tensor_output.into_take_max(
            scene=self,
            offset=RIGHT*GAP,
            run_time_ratio=1.2,
        )
        self.wait()

        self.play(Uncreate(tensor_output, run_time=0.5))
        self.wait()

        self.play(tensor_cmax.animate.shift(LEFT*GAP))
        self.wait()

        tensor_nms = tensor_cmax.into_filter_nms(
            scene=self,
            iou_thresh=0.2,
            offset=RIGHT*GAP,
            run_time_ratio=0.5,
        )
        self.wait(0.5)

        self.play(tensor_nms.animate.shift(RIGHT*3))
        self.wait(0.5)
        self.play(tensor_nms[2:8,3:].animate.set_color(GREEN))
        self.wait(0.5)

        # tensor_conf = tensor_cmax.into_filter_conf(
        #     scene=self,
        #     conf=0.7,
        #     offset=RIGHT*3,
        #     run_time_ratio=1.2,
        # )
        # self.wait()

        # tensor_sort = tensor_conf.into_sort(
        #     scene=self,
        #     offset=RIGHT*3,
        #     run_time_ratio=1.2,
        # )
        # self.wait(0.5)

        # tensors = tensor_sort.into_splitted(
        #     scene=self,
        #     offset=RIGHT*3,
        #     buff=0.3,
        #     run_time_ratio=1.2,
        # )
        # self.wait()

        # for tensor in tensors:
        #     tensor.into_filter_conf(
        #         self,
        #         conf=0.7,
        #         offset=RIGHT*GAP,
        #         run_time_ratio=0.8,
        #     )
        #     self.wait(0.5)
        # self.wait()

        # self.play(AnimationGroup(
        #     *(tensor.animate.set_color(random_color()) for tensor in tensors),
        #     lag_ratio=0.3,
        #     run_time=1.0,
        # ))
        # self.wait()
        # tensors_vg = VGroup(*tensors)

        # # apply append cls, inplace
        # tensor_cmax.apply_append_cls(
        #     self,
        # )
        # self.wait()

        # # switch input
        # self.play(Unwrite(tensor_output))
        # self.play(tensor_cmax.animate.shift(
        #     LEFT*5,
        # ))
        # self.wait()

        # # apply conf filter
        # tensor_conf = tensor_cmax.into_filter_conf(
        #     self,
        #     5*RIGHT,
        # )
        # self.wait()

        # # switch input
        # self.play(Unwrite(tensor_cmax))
        # self.play(tensor_conf.animate.shift(
        #     LEFT*5,
        # ))
        # self.wait()

        # # apply split classes, inplace
        # tensor_a, tensor_b, tensor_c = tensor_conf.into_multi_classes(
        #     self,
        #     keep_original=False,
        # )
        # self.wait()

        # # switch input
        # self.play(Unwrite(tensor_conf))
        # self.play(AnimationGroup(
        #     tensor_a.animate.shift(LEFT*5),
        #     tensor_b.animate.shift(LEFT*5),
        #     tensor_c.animate.shift(LEFT*5),
        # ))
        # self.wait()

        # # apply sort for each tensor, inplace
        # tensor_a.apply_sort(
        #     self,
        # )
        # tensor_b.apply_sort(
        #     self,
        # )
        # tensor_c.apply_sort(
        #     self,
        # )
        # self.wait()

        # # apply nms filter for each tensor
        # tensor_a_nms = tensor_a.into_filter_nms(
        #     self,
        #     5*RIGHT,
        # )
        # tensor_b_nms = tensor_b.into_filter_nms(
        #     self,
        #     5*RIGHT,
        # )
        # tensor_c_nms = tensor_c.into_filter_nms(
        #     self,
        #     5*RIGHT,
        # )
        # self.wait()

        # # concat into a single tensor
        # tensor_nms = Tensor2D.from_tensors(
        #     [tensor_a_nms, tensor_b_nms, tensor_c_nms],
        # )
        # self.play(ApplyMethod(
        #     tensor_nms.arrange_as_matrix,
        # ))
        # self.wait()

# class Demo2(Scene):
#     def construct(self):
#         tensor = Tensor2D.from_list(
#             [
#                 np.random.randint(0, 640, (10,4)),
#                 np.random.uniform(0, 1, (10, 3)),
#             ],
#             decimal_config={
#                 'font_size': 18,
#                 # 'color': PURE_GREEN,
#             },
#             cell_width=0.8,
#         )
#         self.play(Write(tensor, run_time=0.5))
#         self.wait()

#         # tensor.cell_width = 1.1
#         # tensor.cell_height = 0.6
#         # self.play(ApplyMethod(
#         #     tensor.arrange_matrix,
#         #     LEFT*3,
#         #     run_time=0.5,
#         # ))
#         # self.wait()
#         self.play(AnimationGroup(
#             *(row.animate.set_color(random_color()) for row in tensor.mobs),
#             run_time=0.5,
#         ))
#         self.wait()
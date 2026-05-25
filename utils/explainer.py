from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.anchor_point import AnchorPoint
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import SingleAnnotation
from utils.line_matrix import LineMatrix
from utils.general import tensor_to_line_matrix, compute_iou
from utils.general import sf2dir
# from utils.tensor_2d import Tensor2D
from utils.constants import *

import random
import numpy as np
import os

TEXT_XY_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 15,
}

SF_TO_DIR = {
    8:  os.path.join(DIR_NUMPY, '008_80x80'),
    16: os.path.join(DIR_NUMPY, '016_40x40'),
    32: os.path.join(DIR_NUMPY, '032_20x20'),
    64: os.path.join(DIR_NUMPY, '064_10x10'),
    160: os.path.join(DIR_NUMPY, '160_04x04'),
}

class Explainer(VGroup):
    """Class for explaining YOLO output design.
    """
    def __init__(
        self,
        background: ImageRaw | ImagePad | None = None,
        reg_3d: np.ndarray = np.ones((4,4,64)),     # (h, w, 64)
        dist_3d: np.ndarray = np.ones((4,4,4)),     # (h, w, 4)
        prob_3d: np.ndarray = np.ones((4,4,3)),     # (h, w, 3)
        sf_nominal: int = 32,                       # 8|16|32
    ):
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        """
        super().__init__()
        self.background = background
        self.sf_nominal = sf_nominal

        assert reg_3d.shape[:2] == dist_3d.shape[:2] == prob_3d.shape[:2]

        h, w = dist_3d.shape[:2]

        reg_2d = reg_3d.reshape(h*w, -1)        # (h*w, 64)
        dist_2d = dist_3d.reshape(h*w, -1)      # (h*w, 4)
        prob_2d = prob_3d.reshape(h*w, -1)      # (h*w, 3)

        ys, xs = np.meshgrid(
            np.arange(h),
            np.arange(w),
            indexing='ij',
        )
        indices_3d = np.stack([ys, xs], axis=-1)
        indices_2d = indices_3d.reshape(-1, 2)

        xs = xs + 0.5
        ys = ys + 0.5

        center_3d = np.stack([ys, xs], axis=-1)
        center_2d = center_3d.reshape(-1, 2)

        xs_2d = xs.reshape(-1)
        ys_2d = ys.reshape(-1)

        # dist_2d = dist_3d.reshape(-1, 4)
        # prob_2d = prob_3d.reshape(-1, 3)

        x1 = xs_2d - dist_2d[:, 0]
        y1 = ys_2d - dist_2d[:, 1]
        x2 = xs_2d + dist_2d[:, 2]
        y2 = ys_2d + dist_2d[:, 3]

        xyxy_2d = np.stack([x1, y1, x2, y2], axis=-1)
        xyxy_3d = xyxy_2d.reshape(h, w, 4)

        xyxycls_2d = np.concat([xyxy_2d, prob_2d], axis=-1)
        # xyxycls_3d = xyxycls_2d.reshape(h, w, 4+3)
        xyxycls_3d = xyxycls_2d.reshape(h, w, -1)

        # init core members
        self.shape = (h, w)
        self.indices_3d = indices_3d        # (h,w, 2)
        self.indices_2d = indices_2d        # (h*w, 2), TODO: update?
        self.center_3d = center_3d          # (h,w, 2)
        self.center_2d = center_2d          # (h*w, 2), TODO: update?
        self.reg_3d = reg_3d                # (h,w, 64)
        self.reg_2d = reg_2d                # (h*w, 64)
        self.dist_3d = dist_3d              # (h,w, 4)
        self.dist_2d = dist_2d              # (h*w, 4), TODO: update?
        self.xyxy_3d = xyxy_3d              # (h,w, 4)
        self.xyxy_2d = xyxy_2d              # (h*w, 4), TODO: update?
        self.prob_3d = prob_3d              # (h,w, 3)
        self.prob_2d = prob_2d              # (h*w, 3), TODO: update?
        self.xyxycls_3d = xyxycls_3d        # (h,w, 7)
        self.xyxycls_2d = xyxycls_2d        # (h*w, 7), TODO: update?
        self.data = xyxycls_2d.copy()       # (h*w, 7), for manipulation

        # FIXME, more elegant way?
        self.tmp_txts = None

    def create_grid(
        self,
    ) -> VMobject:
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = explainer.create_grid()
        """
        grid = Rectangle(
            width=self.background.width,
            height=self.background.height,
            stroke_width=1,
            grid_xstep=self.sf_screen,
            grid_ystep=self.sf_screen,
        )
        grid.grid_lines.set_stroke(width=1)
        grid.move_to(
            self.background.get_corner(UL),
            aligned_edge=UL,
        )

        return grid

    def show_grid(
        self,
        **aargs,
    ) -> Animation:
        """
        Show the stride grid over the background.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_grid())
        """
        self.grid = self.create_grid()
        self.add(self.grid)

        return Write(self.grid, **aargs)

    def hide_grid(
        self,
        **aargs,
    ) -> Animation:
        """
        Hide the stride grid.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.hide_grid())
        """
        self.remove(self.grid)
        return Unwrite(self.grid, **aargs)

    def create_anchor_points(
        self,
    ) -> VGroup:
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        result = explainer.create_anchor_points()
        """
        anchor_points = VGroup(*[
            AnchorPoint(
                point=self.background.get_corner(UL)+
                    self.center_3d[i,j][0]*DOWN*self.sf_screen+
                    self.center_3d[i,j][1]*RIGHT*self.sf_screen,
                reg=self.reg_3d[i,j].reshape(4,-1),
                dist=self.dist_3d[i,j],
                xyxy=self.xyxy_3d[i,j],
                prob=self.prob_3d[i,j],
                index=self.indices_3d[i,j],
                sf_nominal=self.sf_nominal,
                sf_screen=self.sf_screen,
            ) for i in range(self.shape[0])
            for j in range(self.shape[1])
        ])

        return anchor_points

    def show_anchor_points(
        self,
        **aargs,
    ) -> Animation:
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.show_anchor_points())
        """
        self.anchor_points = self.create_anchor_points()
        self.add(self.anchor_points)
        return Write(self.anchor_points,**aargs)

    def to_rects(
        self,
        rect_config: dict = {}, # rect config
        aargs: dict = {},       # to_rect args
        gargs: dict = {},       # group args
    ) -> Animation:
        """
        Capture target for all anchor points.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        """
        anims = AnimationGroup(
            *(ap.to_rect(
                rect_config,
                **aargs,
            ) for ap in self.anchor_points),
            **gargs,
        )
        return anims

    def to_dots(
        self,
        dot_config: dict = {},  # dot config
        aargs: dict = {},       # animation args
        gargs: dict = {},       # group args
    ) -> Animation:
        """
        Back to dot for all anchor points.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_dots())
        """
        anims = AnimationGroup(
            *(ap.to_dot(
                dot_config,
                **aargs,
            ) for ap in self.anchor_points),
            **gargs,
        )
        return anims

    def show_arrows(
        self,
        arrow_config: dict={},
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> Animation:
        """
        Show arrows for all anchor points.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.show_arrows())
        """
        anim = AnimationGroup(
            *(ap.show_arrows(
                arrow_config=arrow_config,
                aargs=aargs,
                gargs=gargs,
            ) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def hide_arrows(
        self,
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """
        Hide Arrows for all anchor points.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.hide_arrows())
        """
        anim = AnimationGroup(
            *(ap.hide_arrows(
                **aargs,
            ) for ap in self.anchor_points),
            **gargs,
        )
        return anim

    def show_pbars(
        self,
        pbar_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> Animation:
        """
        Show pbars for each anchor points.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.show_pbars())
        """
        anim = AnimationGroup(
            *(ap.show_pbars(
                pbar_config=pbar_config,
                aargs=aargs,
                gargs=gargs,
            ) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def sync_pbars(
        self,
        pbar_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> Animation:
        """
        Sync pbars into current prob for all anchor points.
        Used after updating explainer.prob.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.sync_pbars())
        """
        anim = AnimationGroup(
            *(ap.sync_pbars(
                pbar_config=pbar_config,
                aargs=aargs,
                gargs=gargs,
            ) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def hide_pbars(
        self,
        aargs: dict = {},
        gargs: dict = {},
        ggargs: dict = {},
    ) -> Animation:
        """
        Hide pbars for all anchor points.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.hide_pbars())
        """
        anim = AnimationGroup(
            *(ap.hide_pbars(
                aargs=aargs,
                gargs=gargs,
            ) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def show_multi_labels(
        self,
        include_text: bool = True,  # show conf text or not
        label_config: dict = {},    # font size 12 by default
        box_config: dict = {},
        aargs: dict = {},
        gargs: dict = {},
    ) -> Animation:
        """
        Show multi-labels for all anchor points.
                   Assume that rects is ready.


        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        self.play(explainer.show_multi_labels())
        """
        anim = AnimationGroup(
            *(ap.show_multi_labels(
                include_text=include_text,
                label_config=label_config,
                box_config=box_config,
                **aargs,
            ) for ap in self.anchor_points),
            **gargs,
        )
        return anim

    def show_rect_mlabels(
        self,
        rect_config: dict = {},
        label_config: dict = {},
        box_config: dict = {},
        rargs: dict = {},       # to_rect animation args
        largs: dict = {},       # show_multi_labels animation args
        gargs: dict = {},       # ap.show_rect_mlabels group args
        ggargs: dict = {},      # group of ap.show_rect_mlabels group args
    ) -> Animation:
        """
        FIXME: display issue.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.to_rects())
        self.play(explainer.show_rect_mlabels())
        """
        anim = AnimationGroup(
            *(ap.show_rect_mlabels(
                rect_config=rect_config,
                label_config=label_config,
                box_config=box_config,
                rargs=rargs,
                largs=largs,
                gargs=gargs,
            ) for ap in self.anchor_points),
            **ggargs,
        )
        return anim

    def apply_max_select(
        self,
        scene: Scene,
        run_time_ratio: float = 1.0,
    ) -> None:
        """
        [Internal animation]
                   Apply max conf filter.
                   Keep max label for all anchor points.
                   cls and conf created here.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        result = explainer.apply_max_select(scene=self)
        """
        res_data = np.empty((0, 6))     # always 4+2

        max_idxs = []
        for row in self.data:
            max_idx = row[4:].argmax()    # local max index
            max_idxs.append(max_idx)

            row_n = np.concat([row[:4], [row[max_idx+4], max_idx]])  # (x1,y1,x2,y2,conf,cls)
            res_data = np.vstack([res_data, row_n])

        # update internal data
        self.data = res_data

        # show take max animation
        anims = AnimationGroup(
            *(ap.apply_max_select(
                max_idx=max_idx,
                aargs={},
                gargs={},
            ) for ap, max_idx in zip(self.anchor_points, max_idxs)),
            run_time=1.0*run_time_ratio,
        )
        scene.play(anims)

    def show_3d_aps(
        self,
        scene: ThreeDScene,     # NOTE: only work for 3d scene
        offset: float = 5.0,    # distance between bg and conf 1.0
        run_time_ratio: float = 1.0,
    ) -> None:
        """
        [Internal animation]
                   Show anchor points in a 3d scene.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.show_3d_aps(scene=self))
        """
        # change view point
        scene.move_camera(
            phi=90*DEGREES,
            theta=-180*DEGREES,
            gamma=-90*DEGREES,
            run_time=1.0 * run_time_ratio,
            added_anims=[
                AnimationGroup(
                    self.animate.shift(IN*offset),
                    self.background.animate.shift(IN*offset),
                ),
            ],
        )
        scene.wait(1.0*run_time_ratio)

        for ap in self.anchor_points:
            ap.save_state()

        # cool animation to show distribution of conf
        scene.play(AnimationGroup(
            *(ap.animate(
                rate_func=rate_functions.ease_out_back,
                ).shift(OUT*10*ap.conf)
                for ap in self.anchor_points),
            run_time=5.0 * run_time_ratio,
            lag_ratio=0.5,
            rate_func=rate_functions.ease_in_out_quart,
        ))
        scene.wait(1.0*run_time_ratio)

        # restore anchor points
        scene.play(AnimationGroup(
            *(ap.animate(
                rate_func=rate_functions.ease_in_out_quart,
                ).restore()
                for ap in self.anchor_points),
            run_time=1.0 * run_time_ratio,
            lag_ratio=0.0,
        ))
        scene.wait(1.0*run_time_ratio)

        # change view back
        scene.move_camera(
            phi=0*DEGREES,
            theta=-90*DEGREES,
            gamma=0*DEGREES,
            run_time=1.0*run_time_ratio,
            added_anims=[
                AnimationGroup(
                    self.animate.shift(OUT*offset),
                    self.background.animate.shift(OUT*offset),
                ),
            ],
        )
        scene.wait(1.0*run_time_ratio)

    def apply_conf_filter(
        self,
        scene: Scene,
        conf_thresh: float = 0.25,
        run_time_ratio: float = 1.0,
    ) -> None:
        """
        [Internal animation]
                   Apply conf filter inplace.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        result = explainer.apply_conf_filter(scene=self)
        """
        res_data = np.empty((0, self.data.shape[1]))

        remove_idxs = []
        remove_aps = VGroup()
        for idx, row in enumerate(self.data):
            if row[4] < conf_thresh:
                remove_idxs.append(idx)
                remove_aps.add(self.anchor_points[idx])
            else:
                res_data = np.vstack([res_data, row])

        # update internal data
        self.data = res_data

        # fade and unwrite all low conf aps
        if remove_aps:
            scene.play(AnimationGroup(
                *(ApplyMethod(ap.use_fade, 0.8)
                for ap in remove_aps),
                lag_ratio=0.3,
                run_time=1.0*run_time_ratio,
            ))
            scene.wait(1.0*run_time_ratio)
            scene.play(AnimationGroup(
                *(Unwrite(ap) for ap in remove_aps[::-1]),  # reverse for better visual effect
                lag_ratio=0.3,
                run_time=1.0*run_time_ratio,
            ))
            scene.wait(1.0*run_time_ratio)

            # remove aps from group
            self.anchor_points.remove(*remove_aps)

    def apply_sort(
        self,
        scene: Scene,
    ) -> None:
        """
        Sort aps according to conf.
                   Cool expansion->sorting animation.
                   No significant change after sort.
                   Nothing for now.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = explainer.apply_sort(scene=self)
        """
        pass

    def take_aps_with_cls(
        self,
        cls: int = -1,  # NMS between all classes by default
    ) -> tuple:
        """
        Take aps with specific cls, return their indices and the rest.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = explainer.take_aps_with_cls()
        """
        work_idxs = []
        other_idxs = []
        for idx, row in enumerate(self.data):
            if cls == -1 or int(row[5]) == cls:
                work_idxs.append(idx)
            else:
                other_idxs.append(idx)
        return work_idxs, other_idxs

    def apply_nms_filter(
        self,
        scene: ThreeDScene,             # only works for 3d scene
        cls: int = -1,                  # NMS between all classes by default
        iou_thresh: float = 0.75,       # IOU threshold for NMS
        offset: float = 2.0,            # keep space offset
        run_time_ratio: float = 1.0,
    ) -> None:
        """
        [Internal animation]
                   Apply NMS filter for specific class or for all.
                   Sort aps and append, sort data and append.
                   TODO: fast mode, filter candidates all at onces.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        result = explainer.apply_nms_filter(scene=self)
        """
        work_idxs, other_idxs = self.take_aps_with_cls(cls)
        if len(work_idxs) == 0:
            return

        work_aps = VGroup(self.anchor_points[idx] for idx in work_idxs)
        work_data = self.data[work_idxs]
        other_aps = VGroup(self.anchor_points[idx] for idx in other_idxs)
        other_data = self.data[other_idxs]

        # sort working aps and data according to conf
        idxs = np.argsort(work_data[:,4])[::-1]         # sorted idxs
        work_data = work_data[idxs]                     # sorted data
        work_aps = VGroup(*(work_aps[i] for i in idxs)) # sorted aps

        # fade other aps before NMS
        if other_aps:
            other_aps.save_state()
            scene.play(AnimationGroup(
                *(ap.animate.use_fade(0.9) for ap in other_aps),
                lag_ratio=0.0,
                run_time=1.0*run_time_ratio,
            ))
            # scene.play(other_aps.animate(
            #     lag_ratio=0.0,      # fade all at once
            #     run_time=1.0 * run_time_ratio,
            # ).fade(0.9)) # send to back
            scene.wait(1.0 * run_time_ratio)

        # NMS animations
        res_data = np.empty((0, work_data.shape[1]))
        res_aps = VGroup()
        cand_idxs = list(range(len(work_aps)))
        while len(cand_idxs) > 0:
            k_idx = cand_idxs.pop(0)
            k_data = work_data[k_idx]
            k_box = k_data[:4]
            k_ap = work_aps[k_idx]

            res_data = np.vstack([res_data, k_data])
            res_aps.add(k_ap)

            # shift out current best ap and stress it
            scene.play(k_ap.animate(
                run_time=1.0*run_time_ratio,
                # rate_func=rate_functions.ease_out_back,
            ).shift(OUT*offset))
            k_ap.set_z_index(1)     # bring to front
            k_ap.save_state()       # save state for kept aps
            scene.play(k_ap.animate(
                run_time=1.0*run_time_ratio,
            ).use_color(
                color=PURE_YELLOW,
                font_color=BLACK,
            ))
            # scene.wait(1.0*run_time_ratio)

            # done if the last shifted out
            if len(cand_idxs) == 0:
                # NOTE: optional fade of out the last ap
                scene.play(k_ap.animate(
                    run_time=1.0*run_time_ratio,
                ).use_fade(0.8))
                break

            # compute ious between best and candidates
            cand_boxes = work_data[cand_idxs, :4]
            ious = compute_iou(k_box, cand_boxes)
            survive_mask = ious <= iou_thresh

            for idx, survive, iou in zip(cand_idxs, survive_mask, ious):
                # shift out to verify
                work_aps[idx].save_state()
                scene.play(work_aps[idx].animate(
                    run_time=1.0*run_time_ratio,
                ).shift(OUT*offset))
                # scene.wait(0.5*run_time_ratio)

                # TODO: verify animation, show iou?

                # back or quit
                if survive:
                    # scene.play(ApplyMethod(
                    #     work_aps[idx].use_color, PURE_GREEN,
                    #     run_time=0.5*run_time_ratio,
                    # ))
                    scene.play(work_aps[idx].animate(
                        run_time=0.5*run_time_ratio,
                    ).restore())
                    # scene.play(work_aps[idx].animate(
                    #     run_time=0.5*run_time_ratio,
                    # ).shift(IN*offset))
                    # scene.wait(0.5*run_time_ratio)
                else:
                    scene.play(ApplyMethod(
                        work_aps[idx].use_color, PURE_RED,
                        run_time=1.0*run_time_ratio,
                    ))
                    scene.play(Unwrite(
                        work_aps[idx],
                        run_time=1.0*run_time_ratio,
                    ))
                    # scene.remove(work_aps[idx]) # remove from scene?
                    # scene.wait(0.5*run_time_ratio)

            # fade current best ap
            scene.play(k_ap.animate(
                run_time=1.0*run_time_ratio,
            ).use_fade(0.8))
            # scene.wait(0.5*run_time_ratio)

            # NOTE: filter cand_idxs using survive_mask
            cand_idxs = [x for x, s in zip(cand_idxs, survive_mask) if s]

        # restore opacity and color of all kept aps
        scene.play(AnimationGroup(
            *(ap.animate.restore() for ap in res_aps),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))
        scene.wait(1.0*run_time_ratio)

        # shift back those kept
        scene.play(AnimationGroup(
            *(ap.animate.shift(IN*offset) for ap in res_aps),
            run_time=1.0*run_time_ratio,
            lag_ratio=0.5,
        ))

        # restore other aps
        if other_aps:
            scene.play(other_aps.animate(
                lag_ratio=0.0,      # back all at once
                run_time=1.0 * run_time_ratio,
            ).restore())
            scene.wait(1.0 * run_time_ratio)

        # rebuild anchor_points and data
        self.anchor_points = VGroup(*other_aps, *res_aps)
        self.data = np.vstack([other_data, res_data])

        return None

    def apply_max_count_filter(
        self,
        scene: Scene,
    ) -> None:
        """
        Apply max count filter.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = explainer.apply_max_count_filter(scene=self)
        """
        pass

    def apply_scale_back(
        self,
        scene: Scene,
    ) -> None:
        """
        Apply scale back.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = explainer.apply_scale_back(scene=self)
        """
        pass

    def apply_keep_random(
        self,
        scene: Scene,
        ratio: float = 0.5,             # ratio of anchor points to keep
        run_time_ratio: float = 1.0,
    ) -> None:
        """
        [Internal animation]
                   Keep random subset of anchor points based on ratio.
                   Used to simulate filtering processes.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        result = explainer.apply_keep_random(scene=self)
        """
        n_keep = max(1, int(self.data.shape[0] * ratio))
        k_idxs = random.sample(range(self.data.shape[0]), n_keep)

        aps_to_remove = [
            ap for i, ap in enumerate(self.anchor_points)
              if i not in k_idxs
        ]

        if aps_to_remove:
            scene.play(AnimationGroup(
                *(Unwrite(ap) for ap in aps_to_remove),
                lag_ratio=0.5,
                run_time=1.0*run_time_ratio,
            ))
            self.anchor_points.remove(*aps_to_remove)

        self.data = self.data[k_idxs]

    def hide_anchor_points(
        self,
        **aargs,
    ) -> Animation:
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.hide_anchor_points())
        """
        self.remove(self.anchor_points)
        return Unwrite(self.anchor_points,**aargs)

    def random_ap(
        self,
        idx: int | None = None,     # can be provided
    ) -> tuple:
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        result = explainer.random_ap()
        """
        if idx is None:
            idx = random.randrange(len(self.anchor_points))
        sap = self.anchor_points[idx]
        others = VGroup(*[
            ap for i, ap in enumerate(self.anchor_points)
            if i != idx
        ])
        return sap, others

    # def collect_in_out_aps(
    #     self,
    #     annotation: VGroup | None,      # VGroup of SingleAnnotation
    # ) -> tuple:
    #     """FIXME, collect aps inside/outside a group of SingleAnnotation.
    #     """
    #     def _inside(point, anno):
    #         x, y, _ = point
    #         return (
    #             anno.bbox.get_left()[0] <= x <= anno.bbox.get_right()[0]
    #             and anno.bbox.get_bottom()[1] <= y <= anno.bbox.get_top()[1]
    #         )
    #     in_aps = VGroup()
    #     out_aps = VGroup()
    #     for ap in self.anchor_points:
    #         if any(_inside(ap.get_center(), anno) for anno in annotation):
    #             in_aps.add(ap)
    #         else:
    #             out_aps.add(ap)
    #     return in_aps, out_aps

    # def collect_focus_ap(
    #     self,
    #     idx: int = 0,                   # sample anchor point index
    # ) -> tuple:
    #     """Collect sample ap and others as VGroup.
    #     """
    #     sample_ap = self.anchor_points[idx]
    #     others = VGroup(*(ap for i, ap in enumerate(self.anchor_points) if i!=idx))
    #     return sample_ap, others

    # def collect_nth_result(
    #     self,
    #     idx: int = 0,                   # sample result index
    # ) -> list:
    #     """Collect specific result as a list.
    #     TODO: rename, exposure problem
    #     """
    #     res = self.xyxy.reshape(-1, 4)[idx].tolist()
    #     res = [int(t) for t in res]
    #     return res

    # def show_point_from_xy(
    #     self,
    #     idx: int = 0,                   # index of anchor point
    #     direction: np.ndarray = UL,     # corner direction of ap's rect, UL/DR
    #     pargs: dict = {},               # path animation args
    #     targs: dict = {},               # text animation args
    #     gargs: dict = {},               # group animation args
    # ) -> Animation:
    #     """Animation illustrating x,y -> point
    #         TODO, config separation
    #     """
    #     # create two paths into (x,y)
    #     ap = self.anchor_points[idx]
    #     px = VMobject().set_points_as_corners([
    #         self.background.get_corner(UL),
    #         np.array([ap.get_corner(direction)[0], self.background.get_top()[1], 0]),
    #         ap.get_corner(direction),
    #     ]).set_stroke(color=PURE_YELLOW, width=3)
    #     py = VMobject().set_points_as_corners([
    #         self.background.get_corner(UL),
    #         np.array([self.background.get_left()[0], ap.get_corner(direction)[1], 0]),
    #         ap.get_corner(direction),
    #     ]).set_stroke(color=PURE_YELLOW, width=3)

    #     # create x y texts
    #     # TODO: only UL and DR are available now
    #     if np.array_equal(direction, UL):
    #         _tx = str(ap.xyxy[0])
    #         _ty = str(ap.xyxy[1])
    #     elif np.array_equal(direction, DR):
    #         _tx = str(ap.xyxy[2])
    #         _ty = str(ap.xyxy[3])
    #     tx = Text(
    #         _tx,
    #         color=WHITE,
    #         **TEXT_XY_CONFIG,
    #     ).next_to(px, UP, buff=0.2)
    #     ty = Text(
    #         _ty,
    #         color=WHITE,
    #         **TEXT_XY_CONFIG,
    #     ).next_to(px, LEFT, buff=0.2)

    #     # TODO, more elegant way of storing tmp text?
    #     if self.tmp_txts is None:
    #         self.tmp_txts = VGroup(tx, ty)
    #     else:
    #         self.tmp_txts.add(tx, ty)

    #     anim = AnimationGroup(
    #         AnimationGroup(
    #             ShowPassingFlash(px, **pargs,),
    #             Write(tx, **targs),
    #             **gargs,
    #         ),
    #         AnimationGroup(
    #             ShowPassingFlash(py, **pargs,),
    #             Write(ty, **targs),
    #             **gargs,
    #         ),
    #     )
    #     return anim

    # def hide_xy_txts(
    #     self,
    #     **aargs,
    # ) -> Animation:
    #     mobs = self.tmp_txts
    #     self.tmp_txts = None
    #     return Unwrite(mobs, **aargs)

    # def create_distance_tensor(
    #     self,
    #     font_size: int=8,               # small for tensor
    # ) -> VGroup:
    #     dists = VGroup()
    #     for ap in self.anchor_points:
    #         dist = ap.create_ordered_distance(font_size=font_size)
    #         dists.add(dist)
    #     return dists

    # def create_xyxy_tensor(
    #     self,
    #     font_size: int=8,               # small for tensor
    # ) -> VGroup:
    #     xyxys = VGroup()
    #     for ap in self.anchor_points:
    #         xyxy = ap.create_ordered_xyxy(font_size=font_size)
    #         xyxys.add(xyxy)
    #     return xyxys

    # def create_probs_tensor(
    #     self,
    #     font_size: int=8,
    # ) -> VGroup:
    #     probs = VGroup()
    #     for ap in self.anchor_points:
    #         ps = ap.create_ordered_probs(font_size=font_size)
    #         probs.add(ps)
    #     return probs

    # def create_line_matrix(
    #     self,
    #     n: int=4,              # n lines in a rows
    # ):
    #     """Create 2d LineMatrix according to xyxy shape.
    #     """
    #     matrix = LineMatrix(
    #         (self.shape[0]*self.shape[1], n),
    #     )
    #     return matrix

    def check_clip(
        self,
    ) -> list:
        """
        Check which aps remain after clipping.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        result = explainer.check_clip()
        """
        idxs = [idx for idx in range(len(self.anchor_points))
            if self.anchor_points[idx].check_clip(self.background)]
        return idxs

    def apply_clip(
        self,
        scene: Scene,
        run_time_ratio: float = 1.0,
    ) -> None:
        """
        [Internal Animation]
                   Clip aps crossing border, remove if outside.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        self.play(explainer.to_rects())
        result = explainer.apply_clip(scene=self)
        """
        idxs_remain = self.check_clip()   # on background by default
        idxs_remove = [idx for idx in range(len(self.anchor_points)) if idx not in idxs_remain]
        aps_remain = [ self.anchor_points[idx] for idx in idxs_remain ]
        aps_remove = [ self.anchor_points[idx] for idx in idxs_remove ]

        if aps_remove:
            scene.play(AnimationGroup(
                *(Unwrite(ap) for ap in aps_remove),
                lag_ratio=0.5,
                run_time=1.0*run_time_ratio,
            ))
            self.anchor_points.remove(*aps_remove)

        scene.play(AnimationGroup(
            *(ap.do_clip() for ap in aps_remain),
            lag_ratio=0.5,
            run_time=1.0*run_time_ratio,
        ))
        self.data = self.data[idxs_remain]

    def xyxyccc(
        self,
    ) -> Tensor2D:
        """
        Combined xyxy and cls info, (h*w, 7)

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = explainer.xyxyccc()
        """
        data = [
            self._compute_xyxy_2d(),
            self._compute_cls_2d(),
        ]
        return Tensor2D(
            data=data,
            decimal_config={
                'font_size': 4.3,
                'color': WHITE,
            },
        )

    @property
    def sf_screen(self) -> float:
        """
        Screen distance / unit distance.
                   Assume that width and height direction share the same factor.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        value = explainer.sf_screen
        """
        return self.background.width / self.shape[1]

    @property
    def dots(self) -> VGroup:
        """
        Fast reference to all dots

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        value = explainer.dots
        """
        vg = VGroup(*(ap.mob for ap in self.anchor_points))
        return vg

    @property
    def prob(self):
        """
        Only expose 2d version to user.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        value = explainer.prob
        """
        return self.prob_2d

    # @property
    # def shape(self):
    #     """Height of the internal data, changing.
    #     """
    #     return self.data.shape

    @prob.setter
    def prob(self, prob: np.ndarray):
        """
        Update global prob_2d and anchor points.
                   Expect immediate sync_pbars.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        self.play(explainer.show_anchor_points())
        explainer.prob = np.random.uniform(0, 1, explainer.prob_2d.shape)
        """
        assert prob.ndim == 2
        self.prob_2d = prob
        # self.prob_3d = prob.reshape(*self.shape, -1)
        for prob, ap in zip(self.prob_2d, self.anchor_points):
            ap.prob = prob

    # TODO, setters and sync animations for other members

    @staticmethod
    def from_random(
        background,
        dist_range: tuple = (0, 3),
        prob_range: tuple = (0, 1),
        shape: tuple = (4, 4),
        sf_nominal: int | None = None,
    ) -> Explainer:
        """
        Create random explainer.

        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = Explainer.from_random(background=Square())
        """
        dist_3d = np.random.uniform(dist_range[0], dist_range[1], shape+(4,))
        prob_3d = np.random.uniform(prob_range[0], prob_range[1], shape+(3,))

        sf_nominal = sf_nominal or (640 // shape[0])

        return Explainer(
            background=background,
            dist_3d=dist_3d,
            prob_3d=prob_3d,
            sf_nominal=sf_nominal,
        )

    @staticmethod
    def from_file(
        background,
        version: int = 32,      # 8 | 16 | 32 | 64 | 160
        sf_nominal: int | None = None,
    ) -> Explainer:
        """
        Example
        -------
        explainer = Explainer.from_random(background=Square())
        result = Explainer.from_file(background=Square())
        """
        dir_array = SF_TO_DIR[version]

        path_reg = os.path.join(dir_array, 'box_softmax.npy')
        path_dist = os.path.join(dir_array, 'box_dist.npy')
        path_prob = os.path.join(dir_array, 'cls_sigmoid.npy')

        reg_3d = np.load(path_reg)
        dist_3d = np.load(path_dist)
        prob_3d = np.load(path_prob)

        sf_nominal = sf_nominal or (640//dist_3d.shape[0])

        explainer = Explainer(
            background=background,
            reg_3d=reg_3d,
            dist_3d=dist_3d,
            prob_3d=prob_3d,
            sf_nominal=sf_nominal,
        )
        return explainer

class Demo(Scene):
    def construct(self):
        sq = Square(
            stroke_opacity=0,
            fill_opacity=0.3,
        ).scale(2.)
        explainer = Explainer.from_random(
            background=sq,
            dist_range=(0.3,1.0),
            prob_range=(0,1),
            shape=(5,5),
            sf_nominal=32,
        )

        system = Group(sq, explainer)
        self.add(system)

        self.play(explainer.show_anchor_points(
            run_time=0.5,
        ))
        self.wait()

        self.play(explainer.show_rect_mlabels(
            rect_config={},
            label_config={
                'fill_opacity': 0.8,
                'stroke_opacity': 0.8,
            },
            rargs={'rate_func': rate_functions.ease_out_back},
            largs={'lag_ratio': 0.0},
            gargs={'lag_ratio': 0.3},
            ggargs={'lag_ratio': 0.1, 'run_time': 2.0},
        ))
        self.wait()

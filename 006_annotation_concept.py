import numpy as np
from manim import *

from utils.general import import_mobs, export_mobs
from utils.layers_fake import LayersFake
from utils.comment import Comment
from utils.yolo_annotation import YoloAnnotation, SingleAnnotation
from utils.layers_fake import LayersFake

from utils.constants import *

from typing import Callable

# coord system
TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 20,
    'color': WHITE,
}
DOT_CONFIG = {
    'color': WHITE,
    'radius': 0.05,
}

# class mapping table
TABLE_MAP_CONFIG = {'font_size': 18, 'color': GRAY}

# result data table
TABLE_RES_HEAD_CONFIG = {'font_size': 18, 'color': GRAY}
TABLE_RES_ROW_CONFIG = {'font_size': 18, 'color': WHITE}
TABLE_RES_HEAD_FORMATTER = '{:<6s} {:<6s} {:<6s} {:<6s} {:<6s}'
TABLE_RES_HEAD_VALUES_XYXY = ['class', 'x1', 'y1', 'x2', 'y2']
TABLE_RES_HEAD_VALUES_XYWH = ['class', 'cx', 'cy', 'w', 'h']
TABLE_RES_ROW_FORMATTER_NORM = '{:<6d} {:<6.2f} {:<6.2f} {:<6.2f} {:<6.2f}'
TABLE_RES_ROW_FORMATTER_ABS = '{:<6d} {:<6d} {:<6d} {:<6d} {:<6d}'

# path
PATH_STROKE_CONFIG = {
    'width': 3,
    'color': PURE_YELLOW,
    'opacity': 1.0,
}

def coord_to_text(x, y):
    return '(' + str(x) + ',' + str(y) + ')'

def create_data_table(
    head_values,
    row_formatter,
    row_values,
) -> VGroup:
    return VGroup(
        Comment(
            formatter=TABLE_RES_HEAD_FORMATTER,
            values=head_values,
            **TABLE_RES_HEAD_CONFIG,
        ),
        *(Comment(
            formatter=row_formatter,
            values=row_value,
            **TABLE_RES_ROW_CONFIG,
        ) for row_value in row_values),
    ).arrange(
        DOWN,
        buff=0.2,
        aligned_edge=LEFT,
    )

def f1_xyxy(
    sano: SingleAnnotation,
    axes: Axes,
) -> tuple:
    point = sano.get_box_corner(UL)
    x, y = axes.p2c(point)
    base_x =axes.c2p(x, 0)
    base_y = axes.c2p(0, y)
    origin = axes.c2p(0, 0)
    return point, base_x, base_y, origin

def f2_xyxy(
    sano: SingleAnnotation,
    axes: Axes,
) -> tuple:
    point = sano.get_box_corner(DR)
    x, y = axes.p2c(point)
    base_x =axes.c2p(x, 0)
    base_y = axes.c2p(0, y)
    origin = axes.c2p(0, 0)
    return point, base_x, base_y, origin

def f1_xywh(
    sano: SingleAnnotation,
    axes: Axes,
) -> tuple:
    point = sano.get_box_corner(ORIGIN)
    x, y = axes.p2c(point)
    base_x =axes.c2p(x, 0)
    base_y = axes.c2p(0, y)
    origin = axes.c2p(0, 0)
    return point, base_x, base_y, origin

def f2_xywh(
    sano: SingleAnnotation,
    axes: Axes,     # not used 
) -> tuple:
    corner_ul = sano.get_box_corner(UL)
    corner_ur = sano.get_box_corner(UR)
    corner_dl = sano.get_box_corner(DL)
    corner_dr = sano.get_box_corner(DR)
    return corner_ul, corner_ur, corner_dl, corner_dr

def points_to_paths(
    p1, p2, p3, p4,
) -> tuple:
    path_1 = VMobject().set_points_as_corners([
        p1, p2, p4,
    ]).set_stroke(**PATH_STROKE_CONFIG)
    path_2 = VMobject().set_points_as_corners([
        p1, p3, p4,
    ]).set_stroke(**PATH_STROKE_CONFIG)
    return path_1, path_2

def loop_sanos_animation(
    scene: Scene,
    data: list,
    sanos: VGroup,
    axes: Axes,             # not used maybe
    table_res: VGroup,
    table_map: VGroup,
    f1: Callable,           # callable output 4 points
    f2: Callable,           # callable output 4 points
    floating: bool,         # if shape text should be float
    wt: float,              # unit wait time
) -> None:
    """General loop animation routine for different
       options of YOLO annotation.
    """
    n_sanos = len(sanos)

    # for restore at the end
    sanos.save_state()
    table_res.save_state()
    table_map.save_state()

    for idx in range(n_sanos):
        # prepare assets
        sano = sanos[idx]
        t0, t1, t2, t3, t4 = data[idx]
        target_sanos = sanos.saved_state.copy()
        target_res = table_res.saved_state.copy()
        target_map = table_map.saved_state.copy()
        for i in range(n_sanos):
            if i != idx:
                target_sanos[i].fade(0.8)
                target_res[i+1].fade(0.8)    # skip head
        for i in range(len(target_map)):
            if i != t0:
                target_map[i].fade(0.8)
        pa1, pa2, pa3, pa4 = f1(sano, axes)
        pb1, pb2, pb3, pb4 = f2(sano, axes)
        path_a1, path_a2 = points_to_paths(pa1, pa2, pa3, pa4)
        path_b1, path_b2 = points_to_paths(pb1, pb2, pb3, pb4)

        fstr = '{:.2}' if floating else '{:d}'
        ta1, ta2, tb1, tb2 = [
            Text(
                text=fstr.format(t),
                **TEXT_CONFIG,
            ) for t in (t1, t2, t3, t4)
        ]
        ta1.next_to(path_a1, UP, buff=0.15)
        ta2.next_to(path_a2, LEFT, buff=0.15)
        tb1.next_to(path_b1, UP, buff=0.15)
        tb2.next_to(path_b2, LEFT, buff=0.15)

        scene.play(AnimationGroup(
            Transform(
                sanos,
                target_sanos,
            ),
            Transform(
                table_res,
                target_res,
            ),
            run_time=wt,
        ))
        scene.wait(wt)

        # focus on row in mapping table
        scene.play(Transform(
            table_map,
            target_map,
            run_time=wt,
        ))
        scene.wait(wt)

        # show first group of paths and texts
        scene.play(AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(path_a1, time_width=3.0),
                Write(ta1),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                ShowPassingFlash(path_a2, time_width=3.0),
                Write(ta2),
                lag_ratio=0.5,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        scene.wait(wt)
        scene.play(AnimationGroup(
            Unwrite(ta1),
            Unwrite(ta2),
            lag_ratio=0.0,
            run_time=wt,
        ))
        scene.wait(wt)

        # show second group of paths and texts
        scene.play(AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(path_b1, time_width=3.0),
                Write(tb1),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                ShowPassingFlash(path_b2, time_width=3.0),
                Write(tb2),
                lag_ratio=0.5,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        scene.wait(wt)
        scene.play(AnimationGroup(
            Unwrite(tb1),
            Unwrite(tb2),
            lag_ratio=0.0,
            run_time=wt,
        ))
        scene.wait(wt)

    # fade back
    scene.play(AnimationGroup(
        sanos.animate.restore(),
        table_res.animate.restore(),
        table_map.animate.restore(),
        lag_ratio=0.0,
        run_time=wt,
    ))
    scene.wait(wt)


wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init mobs from previous',
            skip_animations=True,
        )
        # ************************************************************
        (
            annotation,         # Group(ImagePad, YoloAnnotation)
        ) = import_mobs('005')
        
        # for fast reference
        w_n = annotation[0].width_nominal
        h_n = annotation[0].height_nominal
        sanos = annotation[1].mobs
        n_sanos = len(sanos)

        # position info assets
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 6],
            x_length=annotation.width+0.5,
            y_length=annotation.height+0.5,
            x_axis_config={
                'include_ticks': False,
                'tip_width': 0.2,
                'tip_height': 0.2,
                'scaling': LinearBase(100),
            },
            y_axis_config={
                'include_ticks': False,
                'tip_width': 0.2,
                'tip_height': 0.2,
                'scaling': LinearBase(100),
            },
            img_rotate=True,
        ).fade(0.5)
        axes.shift(annotation.get_corner(UL) - axes.get_origin())
        ax_labels = axes.get_axis_labels().scale(0.8).fade(0.5)
        ax_labels[0].next_to(axes.x_axis, RIGHT)
        ax_labels[1].next_to(axes.y_axis, DOWN)
        # key dots
        dot_ul = Dot(**DOT_CONFIG).move_to(annotation.get_corner(UL))
        dot_ur = Dot(**DOT_CONFIG).move_to(annotation.get_corner(UR))
        dot_dl = Dot(**DOT_CONFIG).move_to(annotation.get_corner(DL))
        dot_dr = Dot(**DOT_CONFIG).move_to(annotation.get_corner(DR))
        key_dots = VGroup(dot_ul, dot_ur, dot_dl, dot_dr)
        # key coords
        coord_ul = Text(
            coord_to_text(0, 0),
            **TEXT_CONFIG,
        ).next_to(annotation.get_corner(UL), UL)
        coord_ur = Text(
            coord_to_text(w_n-1, 0),
            **TEXT_CONFIG,
        ).next_to(annotation.get_corner(UR), UR)
        coord_dl = Text(
            coord_to_text(0, h_n-1),
            **TEXT_CONFIG,
        ).next_to(annotation.get_corner(DL), DL)
        coord_dr = Text(
            coord_to_text(w_n-1, h_n-1),
            **TEXT_CONFIG,
        ).next_to(annotation.get_corner(DR), DR)
        key_coords = VGroup(coord_ul, coord_ur, coord_dl, coord_dr)

        # class info assets
        table_mapping = VGroup(
            Comment(
                formatter='{:<6s}->{}',
                values=[name, idx],
                colors=[KK_COLORS[idx], WHITE],
                **TABLE_MAP_CONFIG,
            ) for idx, name in enumerate(KK_NAMES)
        ).arrange(
            DOWN,
            buff=0.3,
            aligned_edge=LEFT,
        ).to_corner(
            UR,
            buff=0.5,
        )

        # result table assets
        table_cxyxy_abs = create_data_table(
            head_values=TABLE_RES_HEAD_VALUES_XYXY,
            row_formatter=TABLE_RES_ROW_FORMATTER_ABS,
            row_values=annotation[1].cxyxy_abs,
        ).shift(RIGHT*20)
        table_cxywh_abs = create_data_table(
            head_values=TABLE_RES_HEAD_VALUES_XYWH,
            row_formatter=TABLE_RES_ROW_FORMATTER_ABS,
            row_values=annotation[1].cxywh_abs,
        )
        table_cxyxy_norm = create_data_table(
            head_values=TABLE_RES_HEAD_VALUES_XYXY,
            row_formatter=TABLE_RES_ROW_FORMATTER_NORM,
            row_values=annotation[1].cxyxy_norm,
        )
        table_cxywh_norm = create_data_table(
            head_values=TABLE_RES_HEAD_VALUES_XYWH,
            row_formatter=TABLE_RES_ROW_FORMATTER_NORM,
            row_values=annotation[1].cxywh_norm,
        )

        # result tensor
        tout_final = LayersFake(
            n=1,
            width=1.5,
            height=2.5,
            width_nominal=5,
            height_nominal='n',
            buff=0.12,      # useless
            expanded=True,
        )

        # show background + annotation
        self.add(annotation)
        self.wait()
        
        # ************************************************************
        self.next_section(
            'two aspects: position info and class info',
            skip_animations=True,
        )
        # ************************************************************
        labels = annotation[1].get_labels()
        boxes = annotation[1].get_boxes()
        labels.save_state()
        boxes.save_state()

        # focus on position of all sano
        self.play(labels.animate(
            run_time=wt,
        ).fade(0.8))
        self.wait(wt)

        # focus on class of all sano
        self.play(AnimationGroup(
            labels.animate.restore(),
            boxes.animate.fade(0.8),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait()

        # back to original
        self.play(boxes.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'position first, coord system for annotation',
            skip_animations=True,
        )
        # ************************************************************
        # temp assets
        path_left = VMobject()
        path_left.set_points_as_corners([
            annotation.get_corner(UR),
            annotation.get_corner(UL),
        ]).set_stroke(color=ManimColor("#FFFF00"))  # pure yellow
        path_up = VMobject()
        path_up.set_points_as_corners([
            annotation.get_corner(DL),
            annotation.get_corner(UL),
        ]).set_stroke(color=ManimColor("#FFFF00"))  # pure yellow
        shape_w = Text(
            str(w_n),   # from background
            **TEXT_CONFIG,
        ).next_to(annotation, UP)
        shape_h = Text(
            str(h_n),  # from background
            **TEXT_CONFIG,
        ).next_to(annotation, LEFT)

        # fade labels for a while
        self.play(labels.animate(
            run_time=wt,
        ).fade(0.8))
        self.wait(wt)

        # customized version of show shape
        self.play(AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(
                    path_left,
                    time_width=2,
                ),
                Write(shape_w),
                lag_ratio=0.3,
            ),
            AnimationGroup(
                ShowPassingFlash(
                    path_up,
                    time_width=2,
                ),
                Write(shape_h),
                lag_ratio=0.3,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show axes and labels
        self.play(Succession(
            Write(axes, lag_ratio=0.0),
            Write(ax_labels, lag_ratio=0.0),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'key dots and coords',
            skip_animations=True,
        )
        # ************************************************************
        # remove shape texts
        self.play(AnimationGroup(
            Unwrite(shape_w),
            Unwrite(shape_h),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # introduce key dots
        self.play(AnimationGroup(
            *(Write(dot) for dot in key_dots),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # introduce key coords
        self.play(AnimationGroup(
            *(Write(coord) for coord in key_coords),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # only keep axes for computation usage later
        self.play(AnimationGroup(
            Unwrite(ax_labels, lag_ratio=0.0),
            Unwrite(key_dots, lag_ratio=0.0),
            Unwrite(key_coords, lag_ratio=0.0),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        annotation.add(axes)    # Group(ImageRaw, YoloAnnotation, Axes)

        # ************************************************************
        self.next_section(
            'on class info: mapping table',
            skip_animations=True,
        )
        # ************************************************************
        # focus on labels
        self.play(AnimationGroup(
            labels.animate.restore(),
            boxes.animate.fade(0.8),
            run_time=wt,
        ))
        self.wait(wt)

        # introduce class mapping table
        self.play(Create(
            table_mapping,
            run_time=wt,
        ))
        self.wait(wt)

        # restore boxes
        self.play(boxes.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop on digitalization: cxyxy_abs',
            skip_animations=True,
        )
        # ************************************************************
        # shift in cxyxy_abs
        mobs = Group(
            annotation, table_cxyxy_abs,
        )
        mobs.generate_target()
        mobs.target[0].scale(0.8)
        mobs.target.arrange(
            RIGHT,
            buff=0.8,
        )
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        loop_sanos_animation(
            scene=self,
            data=annotation[1].cxyxy_abs,
            sanos=sanos,
            axes=axes,
            table_res=table_cxyxy_abs,
            table_map=table_mapping,
            f1=f1_xyxy,
            f2=f2_xyxy,
            floating=False,
            wt=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop on digitalization: cxywh_abs',
            skip_animations=True,
        )
        # ************************************************************
        # transform from cxyxy_abs into cxywh_abs
        table_cxywh_abs.align_to(table_cxyxy_abs, UL)
        self.play(ReplacementTransform(
            table_cxyxy_abs,
            table_cxywh_abs,
            run_time=wt,
        ))
        self.wait(wt)

        loop_sanos_animation(
            scene=self,
            data=annotation[1].cxywh_abs,
            sanos=sanos,
            axes=axes,
            table_res=table_cxywh_abs,
            table_map=table_mapping,
            f1=f1_xywh,
            f2=f2_xywh,
            floating=False,
            wt=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop on digitalization: cxyxy_norm',
            skip_animations=True,
        )
        # ************************************************************
        # transform from cxywh_abs into cxyxy_norm
        table_cxyxy_norm.align_to(table_cxywh_abs, UL)
        self.play(ReplacementTransform(
            table_cxywh_abs,
            table_cxyxy_norm,
            run_time=wt,
        ))
        self.wait(wt)

        loop_sanos_animation(
            scene=self,
            data=annotation[1].cxyxy_norm,
            sanos=sanos,
            axes=axes,
            table_res=table_cxyxy_norm,
            table_map=table_mapping,
            f1=f1_xyxy,
            f2=f2_xyxy,
            floating=True,
            wt=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop on digitalization: cxywh_norm',
            skip_animations=True,
        )
        # ************************************************************
        # transform from cxyxy_norm into cxywh_norm
        table_cxywh_norm.align_to(table_cxyxy_norm, UL)
        self.play(ReplacementTransform(
            table_cxyxy_norm,
            table_cxywh_norm,
            run_time=wt,
        ))
        self.wait(wt)

        loop_sanos_animation(
            scene=self,
            data=annotation[1].cxywh_norm,
            sanos=sanos,
            axes=axes,
            table_res=table_cxywh_norm,
            table_map=table_mapping,
            f1=f1_xywh,
            f2=f2_xywh,
            floating=True,
            wt=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through video frames',
            skip_animations=False,
        )
        # ************************************************************
        # remove axes, map table, head of result table
        self.play(AnimationGroup(
            Unwrite(axes),
            Unwrite(table_cxywh_norm[0]),
            Unwrite(table_mapping),
            run_time=wt,
        ))
        annotation.remove(axes)     # NOTE: geometry center issue
        self.wait(wt)

        # FIXME: align raw table into background
        table_cxywh_norm.remove(table_cxywh_norm[0])
        self.play(table_cxywh_norm.animate(
            run_time=wt,
        ).set_y(annotation[0].get_y()))
        self.wait(wt)

        # TODO: loop through frames

        # ************************************************************
        self.next_section(
            'from numbers into fake tensor',
            skip_animations=False,
        )
        # ************************************************************
        tout_final.move_to(table_cxywh_norm)
        self.play(ReplacementTransform(
            table_cxywh_norm,
            tout_final,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = Group(
            annotation, tout_final
        )
        export_mobs(__file__, mobs)
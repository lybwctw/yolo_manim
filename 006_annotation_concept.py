import numpy as np
from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.layers_fake import LayersFake
from utils.comment import Comment

# # constants
# CLASSES = ['kunkun', 'coke', 'pepsi']

# def create_class_mapping(clss):
#     table = Table(
#         [[c] for c in clss],
#         row_labels=[Integer(i) for i in range(len(clss))],
#         element_to_mobject_config={},
#         include_outer_lines=True,
#     )
#     table.data = clss   # save raw data as a list
#     # do not scale and shift during init
#     # table.scale(0.3)
#     table.remove(*table.get_vertical_lines())
#     table.get_horizontal_lines().set_opacity(0.3)
#     table.get_horizontal_lines().set_stroke(width=2)
#     return table

# # deprecated
# def hybrid_vmobject(item, **cfg):
#     if isinstance(item, int):
#         return Integer(item, **cfg)
#     else:
#         # setup decimal config here
#         cfg['num_decimal_places'] = 2
#         return DecimalNumber(item, **cfg)

# def create_annotation_table(head, data, hybrid):
#     if hybrid:
#         vmobject_type = hybrid_vmobject
#     else:
#         vmobject_type = Integer
#     head = [Text(h) for h in head]
#     table = Table(
#         data,
#         col_labels=head,
#         element_to_mobject=vmobject_type,
#         element_to_mobject_config={},
#         include_outer_lines=True,
#     )
#     # table.scale(0.4)
#     table.remove(*table.get_vertical_lines())
#     table.get_horizontal_lines().set_stroke(width=3)
#     return table

# def create_paths(axes, pos):
#     x, y = axes.p2c(pos)
#     base_x = axes.c2p(x, 0)
#     base_y = axes.c2p(0, y)
#     origin = axes.c2p(0, 0)
#     path_x = VMobject().set_points_as_corners([
#         pos, base_x, origin,
#     ])
#     path_y = VMobject().set_points_as_corners([
#         pos, base_y, origin,
#     ])
#     paths = VGroup(path_x, path_y)
#     # shared properties of paths
#     paths.set_color(YELLOW).set_stroke(width=2)
#     return paths

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

def create_paths_to_axes(
    point,
    axes,
    stroke_config: dict = {},
):
    x, y = axes.p2c(point)
    base_x = axes.c2p(x, 0)
    base_y = axes.c2p(0, y)
    origin = axes.c2p(0, 0)
    stroke_config = {**PATH_STROKE_CONFIG, **stroke_config}
    path_x = VMobject().set_points_as_corners([
        point, base_x, origin,
    ]).set_stroke(**stroke_config)
    path_y = VMobject().set_points_as_corners([
        point, base_y, origin,
    ]).set_stroke(**stroke_config)
    return path_x, path_y

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
        class_mapping = VGroup(
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
        ).to_corner(UR, buff=0.5)

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
            class_mapping,
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
            skip_animations=False,
        )
        # ************************************************************
        # shift in grayed cxyxy_abs table
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

        # loop through each sano
        n_sanos = len(annotation[1].mobs)
        sanos_source = annotation[1].mobs.save_state()
        result_source = table_cxyxy_abs.save_state()
        mapping_source = class_mapping.save_state()
        for idx in range(n_sanos):
            # prepare target assets
            sano = sanos_source[idx]
            sanos_target = sanos_source.saved_state.copy()
            result_target = result_source.saved_state.copy()
            mapping_target = mapping_source.saved_state.copy()
            for i in range(n_sanos):
                if i != idx:
                    sanos_target[i].fade(0.8)
                    result_target[i+1].fade(0.8)    # skip head
            for i in range(len(mapping_target)):
                if i != annotation[1].cls[idx]:
                    mapping_target[i].fade(0.8)
            path_x1y1_x, path_x1y1_y = create_paths_to_axes(
                point=sano.get_box_corner(UL),
                axes=axes,
                stroke_config={},
            )
            path_x2y2_x, path_x2y2_y = create_paths_to_axes(
                point=sano.get_box_corner(DR),
                axes=axes,
                stroke_config={},
            )
            shape_x1y1_x = Text(
                text='{:d}'.format(annotation[1].cxyxy_abs[idx][1]),
                **TEXT_CONFIG,
            ).next_to(path_x1y1_x, UP, buff=0.2)
            shape_x1y1_y = Text(
                text='{:d}'.format(annotation[1].cxyxy_abs[idx][2]),
                **TEXT_CONFIG,
            ).next_to(path_x1y1_y, LEFT, buff=0.2)
            shape_x2y2_x = Text(
                text='{:d}'.format(annotation[1].cxyxy_abs[idx][3]),
                **TEXT_CONFIG,
            ).next_to(path_x2y2_x, UP, buff=0.2)
            shape_x2y2_y = Text(
                text='{:d}'.format(annotation[1].cxyxy_abs[idx][4]),
                **TEXT_CONFIG,
            ).next_to(path_x2y2_y, LEFT, buff=0.2)

            # focus on current sano and current result
            self.play(AnimationGroup(
                Transform(
                    sanos_source,
                    sanos_target,
                ),
                Transform(
                    result_source,
                    result_target,
                ),
                run_time=wt,
            ))
            self.wait(wt)

            # focus on line in mapping table
            self.play(Transform(
                mapping_source,
                mapping_target,
                run_time=wt,
            ))
            self.wait(wt)

            # show x1 y1 in coord system
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path_x1y1_x, time_width=3.0),
                    Write(shape_x1y1_x),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path_x1y1_y, time_width=3.0),
                    Write(shape_x1y1_y),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)
            self.play(AnimationGroup(
                Unwrite(shape_x1y1_x),
                Unwrite(shape_x1y1_y),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

            # show x2 y2 in coord system
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path_x2y2_x, time_width=3.0),
                    Write(shape_x2y2_x),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path_x2y2_y, time_width=3.0),
                    Write(shape_x2y2_y),
                    lag_ratio=0.5,
                ),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)
            self.play(AnimationGroup(
                Unwrite(shape_x2y2_x),
                Unwrite(shape_x2y2_y),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

        # table_cxywh_abs.align_to(table_cxywh_norm, UL)
        # self.play(ReplacementTransform(
        #     table_cxywh_norm,
        #     table_cxywh_abs,
        #     run_time=wt,
        # ))

        # table_cxyxy_norm.align_to(table_cxywh_abs, UL)
        # self.play(ReplacementTransform(
        #     table_cxywh_abs,
        #     table_cxyxy_norm,
        #     run_time=wt,
        # ))

        # table_cxyxy_abs.align_to(table_cxyxy_norm, UL)
        # self.play(ReplacementTransform(
        #     table_cxyxy_norm,
        #     table_cxyxy_abs,
        #     run_time=wt,
        # ))
        # self.wait()

        # # # introduce faded annotation table
        # # cls, xywh_norm = annotation.cls, annotation.xywh
        # # img_w, img_h = annotation._w, annotation._h
        # # _cx, _cy, _w, _h = xywh_norm.T
        # # _x1, _y1, _x2, _y2 = _cx-_w/2, _cy-_h/2, _cx+_w/2, _cy+_h/2
        # # xyxy_norm = np.stack([_x1, _y1, _x2, _y2], axis=1)
        # # xywh = np.stack([
        # #     _cx*img_w, _cy*img_h, _w*img_w, _h*img_h,
        # # ], axis=1)
        # # xyxy = np.stack([
        # #     _x1*img_w, _y1*img_h, _x2*img_w, _y2*img_h
        # # ], axis=1)
        # # cls = np.array(cls).reshape(-1, 1)
        # # xyxy_norm = np.concat([cls, xyxy_norm], axis=1)
        # # xyxy = np.concat([cls, xyxy], axis=1).astype(np.int32)
        # # xywh_norm = np.concat([cls, xywh_norm], axis=1)
        # # xywh = np.concat([cls, xywh], axis=1).astype(np.int32)

        # # table_xyxy = create_annotation_table(
        # #     ['class', 'x1', 'y1', 'x2', 'y2'],
        # #     xyxy,
        # #     hybrid=False,
        # # ).scale(0.4).set_opacity(0.3).shift(RIGHT * 10)
        # # table_xywh = create_annotation_table(
        # #     ['class', 'cx', 'cy', 'w', 'h'],
        # #     xywh,
        # #     hybrid=False,
        # # ).scale(0.4).set_opacity(0.3)

        # # # ************************************************************
        # # self.next_section(
        # #     'xyxy way of annotation, pixel based',
        # #     skip_animations=True,
        # # )
        # # # ************************************************************
        # # # introduce transparent xyxy table
        # # manager = Group(
        # #     *[annotation, table_xyxy],
        # # )
        # # manager.generate_target()
        # # manager.target.arrange(buff=0.5)
        # # manager.target[0].align_to(manager[0], UP)  # align top of annotation
        # # self.play(MoveToTarget(manager))
        # # self.wait()

        # # # show xyxy head
        # # _head = table_xyxy.get_rows()[0]
        # # self.play(_head.animate.set_opacity(1.0))
        # # self.wait()

        # # labels = VGroup(*[
        # #     VGroup(d['text'], d['bbox']) for d in annotation.labels
        # # ])
        # # labels_copy = labels.copy()
        # # cmap_copy = cmap.copy()
        # # table_xyxy_copy = table_xyxy.copy().set_opacity(1.0)
        # # tmp_labels = []     # remove these temp labels after done transform
        # # # loop through class and xyxy for each label
        # # for i, _label in enumerate(labels):
        # #     _text, _bbox = _label

        # #     # focus on current label (text+bbox)
        # #     labels_target = labels_copy.copy()
        # #     for j in [a for a in range(len(labels)) if a!=i]:
        # #         labels_target[j].fade(0.8)
        # #     self.play(Transform(labels, labels_target))
        # #     # self.wait()

        # #     # focus on matching line in cmap
        # #     cmap_target = cmap_copy.copy()
        # #     idx_target = cmap_copy.data.index(_text.original_text)
        # #     row_target = cmap_target.get_rows()[idx_target]
        # #     for j in [a for a in range(len(cmap_target.get_rows())) if a!=idx_target]:
        # #         cmap_target.get_rows()[j].fade(0.8)
        # #     self.play(Transform(cmap, cmap_target))
        # #     self.wait()

        # #     # collect row index into table
        # #     cls_label = row_target[0].copy()
        # #     self.play(Transform(
        # #         cls_label,
        # #         table_xyxy_copy.get_entries((i+2,1)),
        # #     ))
        # #     self.wait()

        # #     # prepare x1y1x2y2 mobs
        # #     path_ul_x, path_ul_y = create_paths(axes, _bbox.get_corner(UL))
        # #     path_dr_x, path_dr_y = create_paths(axes, _bbox.get_corner(DR))

        # #     x1_label = table_xyxy_copy.get_entries((i+2,2)).copy().next_to(path_ul_x,UP*0.7)
        # #     y1_label = table_xyxy_copy.get_entries((i+2,3)).copy().next_to(path_ul_y,LEFT*0.7)
        # #     x2_label = table_xyxy_copy.get_entries((i+2,4)).copy().next_to(path_dr_x,UP*0.7)
        # #     y2_label = table_xyxy_copy.get_entries((i+2,5)).copy().next_to(path_dr_y,LEFT*0.7)

        # #     # show x1y1
        # #     self.play(AnimationGroup(
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_ul_x, run_time=2, time_width=2,),
        # #             Write(x1_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_ul_y, run_time=2, time_width=2,),
        # #             Write(y1_label),
        # #             lag_ratio=0.5,
        # #         )
        # #     ))

        # #     # transform x1y1 into xyxy table
        # #     self.play(AnimationGroup(
        # #         Transform(x1_label, table_xyxy_copy.get_entries((i+2,2))),
        # #         Transform(y1_label, table_xyxy_copy.get_entries((i+2,3))),
        # #     ))

        # #     # show x2y2
        # #     self.play(AnimationGroup(
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_dr_x, run_time=2, time_width=2, ),
        # #             Write(x2_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_dr_y, run_time=2, time_width=2, ),
        # #             Write(y2_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #     ))

        # #     # transform x2y2 into xyxy table
        # #     self.play(AnimationGroup(
        # #         Transform(x2_label, table_xyxy_copy.get_entries((i + 2, 4))),
        # #         Transform(y2_label, table_xyxy_copy.get_entries((i + 2, 5))),
        # #     ))

        # #     # remember those will be removed later
        # #     tmp_labels.extend([cls_label, x1_label, x2_label, y1_label, y2_label])

        # # # make all opaque
        # # self.play(AnimationGroup(
        # #     Transform(labels, labels_copy),
        # #     Transform(table_xyxy, table_xyxy_copy),
        # #     Transform(cmap, cmap_copy),
        # # ))
        # # self.wait()

        # # # only table_xyxy left after clean
        # # self.remove(*tmp_labels)        # not working if remove a vgroup

        # # # ************************************************************
        # # self.next_section(
        # #     'transform xyxy into normed version',
        # #     skip_animations=True,
        # # )
        # # # ************************************************************
        # # # show shapes of annotation
        # # self.play(annotation.show_passing_flash())
        # # self.wait()

        # # # add /w and /h for xyxy
        # # _w, _h = annotation._w, annotation._h
        # # divs = []
        # # for row in table_xyxy.get_rows()[1:]:
        # #     div_w = MathTex('/'+str(_w)).scale(0.3).next_to(row[1], RIGHT, buff=0)
        # #     div_h = MathTex('/'+str(_h)).scale(0.3).next_to(row[2], RIGHT, buff=0)
        # #     div_w2 = div_w.copy().next_to(row[3], RIGHT, buff=0)
        # #     div_h2 = div_h.copy().next_to(row[4], RIGHT, buff=0)
        # #     divs.append(VGroup(div_w, div_h, div_w2, div_h2))
        # # divs = VGroup(*divs).shift(DOWN*0.05).set_color(GRAY)
        # # self.play(Write(divs, lag_ratio=0.0))
        # # self.wait()

        # # # replace int version with float version
        # # for i, row in enumerate(table_xyxy.get_rows()[1:]):
        # #     for j, item in enumerate(row[1:]):
        # #         _input = VGroup(item, divs[i][j])
        # #         _output = DecimalNumber(
        # #             xyxy_norm[i][j+1],    # class index as first for each row
        # #             num_decimal_places=2,
        # #         ).scale(0.4).move_to(item)
        # #         self.play(Transform(_input, _output, run_time=0.2))
        # #         table_xyxy.add(_input)      # make decimal part of table
        # # # decimal_mobs = VGroup(*decimal_mobs)
        # # # self.wait()
        # # self.play(annotation.unwrite_shape_texts())
        # # self.wait()

        # # # ************************************************************
        # # self.next_section(
        # #     'xywh way of annotation, pixel based',
        # #     skip_animations=True,
        # # )
        # # # ************************************************************
        # # # introduce transparent xywh table
        # # table_xywh.move_to(table_xyxy)
        # # self.play(Unwrite(table_xyxy, lag_ratio=0, run_time=0.3,))
        # # self.wait(0.3)
        # # self.play(Write(table_xywh, lag_ratio=0, run_time=0.3,))
        # # self.wait(0.3)
        # # # self.play(ReplacementTransform(table_xyxy, table_xywh))
        # # # self.wait()

        # # # show xywh head
        # # _head = table_xywh.get_rows()[0]
        # # self.play(_head.animate.set_opacity(1.0))
        # # self.wait()

        # # # labels, labels_copy, cmap_copy already created

        # # table_xywh_copy = table_xywh.copy().set_opacity(1.0)
        # # tmp_labels = []
        # # for i, _label in enumerate(labels):
        # #     _text, _bbox = _label

        # #     # focus on current label (text+bbox)
        # #     labels_target = labels_copy.copy()
        # #     for j in [a for a in range(len(labels)) if a!=i]:
        # #         labels_target[j].fade(0.8)
        # #     self.play(Transform(labels, labels_target))
        # #     # self.wait()

        # #     # focus on matching line in cmap
        # #     cmap_target = cmap_copy.copy()
        # #     idx_target = cmap_copy.data.index(_text.original_text)
        # #     row_target = cmap_target.get_rows()[idx_target]
        # #     for j in [a for a in range(len(cmap_target.get_rows())) if a != idx_target]:
        # #         cmap_target.get_rows()[j].fade(0.8)
        # #     self.play(Transform(cmap, cmap_target))
        # #     self.wait()

        # #     # collect row index into table
        # #     cls_label = row_target[0].copy()
        # #     self.play(Transform(
        # #         cls_label,
        # #         table_xyxy_copy.get_entries((i + 2, 1)),
        # #     ))
        # #     self.wait()

        # #     # prepare cxcywh mobs
        # #     path_c_x, path_c_y = create_paths(axes, _bbox.get_center())
        # #     path_w = VMobject().set_points_as_corners([
        # #         _bbox.get_corner(UL), _bbox.get_corner(UR),
        # #     ]).set_color(YELLOW).set_stroke(width=2)
        # #     path_h = VMobject().set_points_as_corners([
        # #         _bbox.get_corner(UL), _bbox.get_corner(DL),
        # #     ]).set_color(YELLOW).set_stroke(width=2)

        # #     cx_label = table_xywh_copy.get_entries((i+2,2)).copy().next_to(path_c_x,UP*0.7)
        # #     cy_label = table_xywh_copy.get_entries((i+2,3)).copy().next_to(path_c_y,LEFT*0.7)
        # #     w_label = table_xywh_copy.get_entries((i+2,4)).copy().next_to(path_w,UP*0.7)
        # #     h_label = table_xywh_copy.get_entries((i+2,5)).copy().next_to(path_h,LEFT*0.7)

        # #     # show cx cy
        # #     self.play(AnimationGroup(
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_c_x, run_time=2, time_width=2,),
        # #             Write(cx_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_c_y, run_time=2, time_width=2, ),
        # #             Write(cy_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #     ))

        # #     # transform cxcy into xywh table
        # #     self.play(AnimationGroup(
        # #         Transform(cx_label, table_xywh_copy.get_entries((i + 2, 2))),
        # #         Transform(cy_label, table_xywh_copy.get_entries((i + 2, 3))),
        # #     ))

        # #     # show wh
        # #     self.play(AnimationGroup(
        # #         _text.animate.set_opacity(0.1),
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_w, run_time=2, time_width=2,),
        # #             Write(w_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #         AnimationGroup(
        # #             ShowPassingFlash(path_h, run_time=2, time_width=2, ),
        # #             Write(h_label),
        # #             lag_ratio=0.5,
        # #         ),
        # #     ))

        # #     # transform wh into xywh table
        # #     self.play(AnimationGroup(
        # #         Transform(w_label, table_xywh_copy.get_entries((i+2,4))),
        # #         Transform(h_label, table_xywh_copy.get_entries((i+2,5))),
        # #     ))

        # #     # remember those will be removed later
        # #     tmp_labels.extend([cls_label, cx_label, cy_label, w_label, h_label])

        # # # make all opaque
        # # self.play(AnimationGroup(
        # #     Transform(labels, labels_copy),
        # #     Transform(table_xywh, table_xywh_copy),
        # #     Transform(cmap, cmap_copy),
        # # ))
        # # self.wait()

        # # # only table_xywh left after clean
        # # self.remove(*tmp_labels)        # not working if remove a vgroup

        # # # ************************************************************
        # # self.next_section(
        # #     'transform xywh into normed version',
        # #     skip_animations=True,
        # # )
        # # # ************************************************************
        # # # show shapes of annotation
        # # self.play(annotation.show_passing_flash())
        # # self.wait()

        # # # add /w and /h for xyxy
        # # _w, _h = annotation._w, annotation._h
        # # divs = []
        # # for row in table_xywh.get_rows()[1:]:
        # #     div_w = MathTex('/' + str(_w)).scale(0.3).next_to(row[1], RIGHT, buff=0)
        # #     div_h = MathTex('/' + str(_h)).scale(0.3).next_to(row[2], RIGHT, buff=0)
        # #     div_w2 = div_w.copy().next_to(row[3], RIGHT, buff=0)
        # #     div_h2 = div_h.copy().next_to(row[4], RIGHT, buff=0)
        # #     divs.append(VGroup(div_w, div_h, div_w2, div_h2))
        # # divs = VGroup(*divs).shift(DOWN * 0.05).set_color(GRAY)
        # # self.play(Write(divs, lag_ratio=0.0))
        # # self.wait()

        # # # replace int version with float version
        # # for i, row in enumerate(table_xywh.get_rows()[1:]):
        # #     for j, item in enumerate(row[1:]):
        # #         _input = VGroup(item, divs[i][j])
        # #         _output = DecimalNumber(
        # #             xyxy_norm[i][j + 1],  # class index as first for each row
        # #             num_decimal_places=2,
        # #         ).scale(0.4).move_to(item)
        # #         self.play(Transform(_input, _output, run_time=0.2))
        # #         table_xywh.add(_input)  # make decimal part of table
        # # # self.wait()
        # # self.play(annotation.unwrite_shape_texts())
        # # self.wait()

        # # # ************************************************************
        # # self.next_section(
        # #     'prepare for next scene, extension and focus back',
        # #     skip_animations=True,
        # # )
        # # # ************************************************************
        # # # self.play(Unwrite(cmap, lag_ratio=0, run_time=0.3, ))
        # # # self.play(Unwrite(table_xywh, lag_ratio=0, run_time=0.3, ))
        # # # self.wait()
        # # everything = Group(
        # #     annotation,
        # #     cmap,
        # #     table_xywh,
        # # )
        # # save_everything(S006_EVERYTHING, everything)

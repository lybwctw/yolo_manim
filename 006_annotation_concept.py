import numpy as np
from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything
from utils.layers_fake import LayersFake

# FIXME, dynamic annotation!!!

# constants
CLASSES = ['kunkun', 'coke', 'pepsi']

def create_class_mapping(clss):
    table = Table(
        [[c] for c in clss],
        row_labels=[Integer(i) for i in range(len(clss))],
        element_to_mobject_config={},
        include_outer_lines=True,
    )
    table.data = clss   # save raw data as a list
    # do not scale and shift during init
    # table.scale(0.3)
    table.remove(*table.get_vertical_lines())
    table.get_horizontal_lines().set_opacity(0.3)
    table.get_horizontal_lines().set_stroke(width=2)
    return table

# deprecated
def hybrid_vmobject(item, **cfg):
    if isinstance(item, int):
        return Integer(item, **cfg)
    else:
        # setup decimal config here
        cfg['num_decimal_places'] = 2
        return DecimalNumber(item, **cfg)

def create_annotation_table(head, data, hybrid):
    if hybrid:
        vmobject_type = hybrid_vmobject
    else:
        vmobject_type = Integer
    head = [Text(h) for h in head]
    table = Table(
        data,
        col_labels=head,
        element_to_mobject=vmobject_type,
        element_to_mobject_config={},
        include_outer_lines=True,
    )
    # table.scale(0.4)
    table.remove(*table.get_vertical_lines())
    table.get_horizontal_lines().set_stroke(width=3)
    return table

def create_paths(axes, pos):
    x, y = axes.p2c(pos)
    base_x = axes.c2p(x, 0)
    base_y = axes.c2p(0, y)
    origin = axes.c2p(0, 0)
    path_x = VMobject().set_points_as_corners([
        pos, base_x, origin,
    ])
    path_y = VMobject().set_points_as_corners([
        pos, base_y, origin,
    ])
    paths = VGroup(path_x, path_y)
    # shared properties of paths
    paths.set_color(YELLOW).set_stroke(width=2)
    return paths

class MainScene(Scene):
    def construct(self) -> None:
        # constants
        FONT_SIZE_COORDS = 20

        # ************************************************************
        self.next_section(
            'coordinate assets',
            skip_animations=True,
        )
        # ************************************************************
        (
            _, annotation, _, _, _, _, _,
        ) = load_everything(S005_EVERYTHING)

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
        )
        axes.shift(annotation.get_corner(UL) - axes.get_origin())

        ax_labels = axes.get_axis_labels().scale(0.8)
        ax_labels[0].next_to(axes.x_axis, RIGHT)
        ax_labels[1].next_to(axes.y_axis, DOWN)

        # corner dots
        dot_ul = Dot().move_to(annotation.get_corner(UL))
        dot_ur = Dot().move_to(annotation.get_corner(UR))
        dot_dl = Dot().move_to(annotation.get_corner(DL))
        dot_dr = Dot().move_to(annotation.get_corner(DR))
        dots = VGroup(dot_ul, dot_ur, dot_dl, dot_dr)

        # corner dots coords
        _w, _h = annotation._w, annotation._h
        coord_ul = Text(
            '(' + '0' + ',' + '0' + ')',
            font_size=FONT_SIZE_COORDS,
        ).next_to(annotation.get_corner(UL), UL)
        coord_ur = Text(
            '(' + str(_w-1) + ',' + '0' + ')',
            font_size=FONT_SIZE_COORDS,
        ).next_to(annotation.get_corner(UR), UR)
        coord_dl = Text(
            '(' + '0' + ',' + str(_h-1) + ')',
            font_size=FONT_SIZE_COORDS,
        ).next_to(annotation.get_corner(DL), DL)
        coord_dr = Text(
            '(' + str(_w-1) + ',' + str(_h-1) + ')',
            font_size=FONT_SIZE_COORDS,
        ).next_to(annotation.get_corner(DR), DR)
        coords = VGroup(coord_ul, coord_ur, coord_dl, coord_dr)

        # customized shape text
        shape_w = Text(
            str(_w),
            font_size=FONT_SIZE_COORDS,
        ).next_to(annotation, UP)
        shape_h = Text(
            str(_h),
            font_size=FONT_SIZE_COORDS,
        ).next_to(annotation, LEFT)
        shapes_annotation = VGroup(shape_w, shape_h)

        # ************************************************************
        self.next_section(
            'coordinate system of image annotation',
            skip_animations=True,
        )
        # ************************************************************
        # show raw annotation
        self.add(annotation)
        self.wait()

        # show shapes, customized ShowPassingFlash
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
        self.play(
            AnimationGroup(
                ShowPassingFlash(path_left, run_time=2, time_width=2),
                Write(shape_w, run_time=1.),
                lag_ratio=0.3,
            ),
            AnimationGroup(
                ShowPassingFlash(path_up, run_time=2, time_width=2),
                Write(shape_h, run_time=1.),
                lag_ratio=0.3,
            ),
        )
        # self.wait()

        # show axes
        self.play(Succession(
            Write(axes, lag_ratio=0.),
            Write(ax_labels, lag_ratio=0.),
        ))
        self.wait()

        # show corner dots and coords
        self.play(AnimationGroup(
            Unwrite(ax_labels, lag_ratio=0.),
            axes.animate.set_opacity(0.3),
            TransformMatchingShapes(shape_w, coord_ur),
            TransformMatchingShapes(shape_h, coord_dl),
            Write(dots),
            Write(coord_ul),
            Write(coord_dr),
        ))
        self.wait()

        # FIXME, problem when unwrite transformed coords?
        # hide coord system
        self.play(AnimationGroup(
            Unwrite(axes, lag_ratio=0.),
            Unwrite(coords, lag_ratio=0.),
            Unwrite(dots, lag_ratio=0.),
        ))
        self.wait()

        # axes' pos will be used later by annotation
        annotation.add(axes)

        # ************************************************************
        self.next_section(
            'stress label text and label bbox respectively',
            skip_animations=True,
        )
        # ************************************************************
        _texts = annotation.get_texts()
        _bboxes = annotation.get_bboxes()
        _texts.save_state()
        _bboxes.save_state()
        # emphasize all texts
        self.play(AnimationGroup(
            _bboxes.animate.set_opacity(0.1),
        ))
        self.wait()
        # emphasize all bboxes
        self.play(AnimationGroup(
            _texts.animate.set_opacity(0.1),
            _bboxes.animate.restore(),
        ))
        self.wait()
        # go back
        self.play(AnimationGroup(
            _texts.animate.restore(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'prepare annotation table assets',
            skip_animations=True,
        )
        # ************************************************************
        # introduce class mapping table
        cmap = create_class_mapping(CLASSES).scale(0.3)
        cmap.to_corner(UR, buff=0.5).shift(RIGHT*0.1+DOWN*0.3)
        self.play(Create(cmap))
        self.wait()

        # introduce faded annotation table
        cls, xywh_norm = annotation.cls, annotation.xywh
        img_w, img_h = annotation._w, annotation._h
        _cx, _cy, _w, _h = xywh_norm.T
        _x1, _y1, _x2, _y2 = _cx-_w/2, _cy-_h/2, _cx+_w/2, _cy+_h/2
        xyxy_norm = np.stack([_x1, _y1, _x2, _y2], axis=1)
        xywh = np.stack([
            _cx*img_w, _cy*img_h, _w*img_w, _h*img_h,
        ], axis=1)
        xyxy = np.stack([
            _x1*img_w, _y1*img_h, _x2*img_w, _y2*img_h
        ], axis=1)
        cls = np.array(cls).reshape(-1, 1)
        xyxy_norm = np.concat([cls, xyxy_norm], axis=1)
        xyxy = np.concat([cls, xyxy], axis=1).astype(np.int32)
        xywh_norm = np.concat([cls, xywh_norm], axis=1)
        xywh = np.concat([cls, xywh], axis=1).astype(np.int32)

        table_xyxy = create_annotation_table(
            ['class', 'x1', 'y1', 'x2', 'y2'],
            xyxy,
            hybrid=False,
        ).scale(0.4).set_opacity(0.3).shift(RIGHT * 10)
        table_xywh = create_annotation_table(
            ['class', 'cx', 'cy', 'w', 'h'],
            xywh,
            hybrid=False,
        ).scale(0.4).set_opacity(0.3)

        # ************************************************************
        self.next_section(
            'xyxy way of annotation, pixel based',
            skip_animations=True,
        )
        # ************************************************************
        # introduce transparent xyxy table
        manager = Group(
            *[annotation, table_xyxy],
        )
        manager.generate_target()
        manager.target.arrange(buff=0.5)
        manager.target[0].align_to(manager[0], UP)  # align top of annotation
        self.play(MoveToTarget(manager))
        self.wait()

        # show xyxy head
        _head = table_xyxy.get_rows()[0]
        self.play(_head.animate.set_opacity(1.0))
        self.wait()

        labels = VGroup(*[
            VGroup(d['text'], d['bbox']) for d in annotation.labels
        ])
        labels_copy = labels.copy()
        cmap_copy = cmap.copy()
        table_xyxy_copy = table_xyxy.copy().set_opacity(1.0)
        tmp_labels = []     # remove these temp labels after done transform
        # loop through class and xyxy for each label
        for i, _label in enumerate(labels):
            _text, _bbox = _label

            # focus on current label (text+bbox)
            labels_target = labels_copy.copy()
            for j in [a for a in range(len(labels)) if a!=i]:
                labels_target[j].fade(0.8)
            self.play(Transform(labels, labels_target))
            # self.wait()

            # focus on matching line in cmap
            cmap_target = cmap_copy.copy()
            idx_target = cmap_copy.data.index(_text.original_text)
            row_target = cmap_target.get_rows()[idx_target]
            for j in [a for a in range(len(cmap_target.get_rows())) if a!=idx_target]:
                cmap_target.get_rows()[j].fade(0.8)
            self.play(Transform(cmap, cmap_target))
            self.wait()

            # collect row index into table
            cls_label = row_target[0].copy()
            self.play(Transform(
                cls_label,
                table_xyxy_copy.get_entries((i+2,1)),
            ))
            self.wait()

            # prepare x1y1x2y2 mobs
            path_ul_x, path_ul_y = create_paths(axes, _bbox.get_corner(UL))
            path_dr_x, path_dr_y = create_paths(axes, _bbox.get_corner(DR))

            x1_label = table_xyxy_copy.get_entries((i+2,2)).copy().next_to(path_ul_x,UP*0.7)
            y1_label = table_xyxy_copy.get_entries((i+2,3)).copy().next_to(path_ul_y,LEFT*0.7)
            x2_label = table_xyxy_copy.get_entries((i+2,4)).copy().next_to(path_dr_x,UP*0.7)
            y2_label = table_xyxy_copy.get_entries((i+2,5)).copy().next_to(path_dr_y,LEFT*0.7)

            # show x1y1
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path_ul_x, run_time=2, time_width=2,),
                    Write(x1_label),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path_ul_y, run_time=2, time_width=2,),
                    Write(y1_label),
                    lag_ratio=0.5,
                )
            ))

            # transform x1y1 into xyxy table
            self.play(AnimationGroup(
                Transform(x1_label, table_xyxy_copy.get_entries((i+2,2))),
                Transform(y1_label, table_xyxy_copy.get_entries((i+2,3))),
            ))

            # show x2y2
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path_dr_x, run_time=2, time_width=2, ),
                    Write(x2_label),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path_dr_y, run_time=2, time_width=2, ),
                    Write(y2_label),
                    lag_ratio=0.5,
                ),
            ))

            # transform x2y2 into xyxy table
            self.play(AnimationGroup(
                Transform(x2_label, table_xyxy_copy.get_entries((i + 2, 4))),
                Transform(y2_label, table_xyxy_copy.get_entries((i + 2, 5))),
            ))

            # remember those will be removed later
            tmp_labels.extend([cls_label, x1_label, x2_label, y1_label, y2_label])

        # make all opaque
        self.play(AnimationGroup(
            Transform(labels, labels_copy),
            Transform(table_xyxy, table_xyxy_copy),
            Transform(cmap, cmap_copy),
        ))
        self.wait()

        # only table_xyxy left after clean
        self.remove(*tmp_labels)        # not working if remove a vgroup

        # ************************************************************
        self.next_section(
            'transform xyxy into normed version',
            skip_animations=True,
        )
        # ************************************************************
        # show shapes of annotation
        self.play(annotation.show_passing_flash())
        self.wait()

        # add /w and /h for xyxy
        _w, _h = annotation._w, annotation._h
        divs = []
        for row in table_xyxy.get_rows()[1:]:
            div_w = MathTex('/'+str(_w)).scale(0.3).next_to(row[1], RIGHT, buff=0)
            div_h = MathTex('/'+str(_h)).scale(0.3).next_to(row[2], RIGHT, buff=0)
            div_w2 = div_w.copy().next_to(row[3], RIGHT, buff=0)
            div_h2 = div_h.copy().next_to(row[4], RIGHT, buff=0)
            divs.append(VGroup(div_w, div_h, div_w2, div_h2))
        divs = VGroup(*divs).shift(DOWN*0.05).set_color(GRAY)
        self.play(Write(divs, lag_ratio=0.0))
        self.wait()

        # replace int version with float version
        for i, row in enumerate(table_xyxy.get_rows()[1:]):
            for j, item in enumerate(row[1:]):
                _input = VGroup(item, divs[i][j])
                _output = DecimalNumber(
                    xyxy_norm[i][j+1],    # class index as first for each row
                    num_decimal_places=2,
                ).scale(0.4).move_to(item)
                self.play(Transform(_input, _output, run_time=0.2))
                table_xyxy.add(_input)      # make decimal part of table
        # decimal_mobs = VGroup(*decimal_mobs)
        # self.wait()
        self.play(annotation.unwrite_shape_texts())
        self.wait()

        # ************************************************************
        self.next_section(
            'xywh way of annotation, pixel based',
            skip_animations=True,
        )
        # ************************************************************
        # introduce transparent xywh table
        table_xywh.move_to(table_xyxy)
        self.play(Unwrite(table_xyxy, lag_ratio=0, run_time=0.3,))
        self.wait(0.3)
        self.play(Write(table_xywh, lag_ratio=0, run_time=0.3,))
        self.wait(0.3)
        # self.play(ReplacementTransform(table_xyxy, table_xywh))
        # self.wait()

        # show xywh head
        _head = table_xywh.get_rows()[0]
        self.play(_head.animate.set_opacity(1.0))
        self.wait()

        # labels, labels_copy, cmap_copy already created

        table_xywh_copy = table_xywh.copy().set_opacity(1.0)
        tmp_labels = []
        for i, _label in enumerate(labels):
            _text, _bbox = _label

            # focus on current label (text+bbox)
            labels_target = labels_copy.copy()
            for j in [a for a in range(len(labels)) if a!=i]:
                labels_target[j].fade(0.8)
            self.play(Transform(labels, labels_target))
            # self.wait()

            # focus on matching line in cmap
            cmap_target = cmap_copy.copy()
            idx_target = cmap_copy.data.index(_text.original_text)
            row_target = cmap_target.get_rows()[idx_target]
            for j in [a for a in range(len(cmap_target.get_rows())) if a != idx_target]:
                cmap_target.get_rows()[j].fade(0.8)
            self.play(Transform(cmap, cmap_target))
            self.wait()

            # collect row index into table
            cls_label = row_target[0].copy()
            self.play(Transform(
                cls_label,
                table_xyxy_copy.get_entries((i + 2, 1)),
            ))
            self.wait()

            # prepare cxcywh mobs
            path_c_x, path_c_y = create_paths(axes, _bbox.get_center())
            path_w = VMobject().set_points_as_corners([
                _bbox.get_corner(UL), _bbox.get_corner(UR),
            ]).set_color(YELLOW).set_stroke(width=2)
            path_h = VMobject().set_points_as_corners([
                _bbox.get_corner(UL), _bbox.get_corner(DL),
            ]).set_color(YELLOW).set_stroke(width=2)

            cx_label = table_xywh_copy.get_entries((i+2,2)).copy().next_to(path_c_x,UP*0.7)
            cy_label = table_xywh_copy.get_entries((i+2,3)).copy().next_to(path_c_y,LEFT*0.7)
            w_label = table_xywh_copy.get_entries((i+2,4)).copy().next_to(path_w,UP*0.7)
            h_label = table_xywh_copy.get_entries((i+2,5)).copy().next_to(path_h,LEFT*0.7)

            # show cx cy
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path_c_x, run_time=2, time_width=2,),
                    Write(cx_label),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path_c_y, run_time=2, time_width=2, ),
                    Write(cy_label),
                    lag_ratio=0.5,
                ),
            ))

            # transform cxcy into xywh table
            self.play(AnimationGroup(
                Transform(cx_label, table_xywh_copy.get_entries((i + 2, 2))),
                Transform(cy_label, table_xywh_copy.get_entries((i + 2, 3))),
            ))

            # show wh
            self.play(AnimationGroup(
                _text.animate.set_opacity(0.1),
                AnimationGroup(
                    ShowPassingFlash(path_w, run_time=2, time_width=2,),
                    Write(w_label),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path_h, run_time=2, time_width=2, ),
                    Write(h_label),
                    lag_ratio=0.5,
                ),
            ))

            # transform wh into xywh table
            self.play(AnimationGroup(
                Transform(w_label, table_xywh_copy.get_entries((i+2,4))),
                Transform(h_label, table_xywh_copy.get_entries((i+2,5))),
            ))

            # remember those will be removed later
            tmp_labels.extend([cls_label, cx_label, cy_label, w_label, h_label])

        # make all opaque
        self.play(AnimationGroup(
            Transform(labels, labels_copy),
            Transform(table_xywh, table_xywh_copy),
            Transform(cmap, cmap_copy),
        ))
        self.wait()

        # only table_xywh left after clean
        self.remove(*tmp_labels)        # not working if remove a vgroup

        # ************************************************************
        self.next_section(
            'transform xywh into normed version',
            skip_animations=False,
        )
        # ************************************************************
        # show shapes of annotation
        self.play(annotation.show_passing_flash())
        self.wait()

        # add /w and /h for xyxy
        _w, _h = annotation._w, annotation._h
        divs = []
        for row in table_xywh.get_rows()[1:]:
            div_w = MathTex('/' + str(_w)).scale(0.3).next_to(row[1], RIGHT, buff=0)
            div_h = MathTex('/' + str(_h)).scale(0.3).next_to(row[2], RIGHT, buff=0)
            div_w2 = div_w.copy().next_to(row[3], RIGHT, buff=0)
            div_h2 = div_h.copy().next_to(row[4], RIGHT, buff=0)
            divs.append(VGroup(div_w, div_h, div_w2, div_h2))
        divs = VGroup(*divs).shift(DOWN * 0.05).set_color(GRAY)
        self.play(Write(divs, lag_ratio=0.0))
        self.wait()

        # replace int version with float version
        for i, row in enumerate(table_xywh.get_rows()[1:]):
            for j, item in enumerate(row[1:]):
                _input = VGroup(item, divs[i][j])
                _output = DecimalNumber(
                    xyxy_norm[i][j + 1],  # class index as first for each row
                    num_decimal_places=2,
                ).scale(0.4).move_to(item)
                self.play(Transform(_input, _output, run_time=0.2))
                table_xywh.add(_input)  # make decimal part of table
        # self.wait()
        self.play(annotation.unwrite_shape_texts())
        self.wait()

        # ************************************************************
        self.next_section(
            'prepare for next scene, extension and focus back',
            skip_animations=False,
        )
        # ************************************************************
        # self.play(Unwrite(cmap, lag_ratio=0, run_time=0.3, ))
        # self.play(Unwrite(table_xywh, lag_ratio=0, run_time=0.3, ))
        # self.wait()
        everything = Group(
            annotation,
            cmap,
            table_xywh,
        )
        save_everything(S006_EVERYTHING, everything)

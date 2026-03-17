import numpy as np
from manim import *

from utils.constants import S005_EVERYTHING
from utils.general import load_everything

# FIXME, dynamic annotation!!!

class MainScene(Scene):
    def construct(self) -> None:
        # constants
        FONT_SIZE_COORDS = 20

        # ************************************************************
        self.next_section(
            'coordinate assets',
            skip_animations=False,
        )
        # ************************************************************
        (
            _, annotation, _, _, _,
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
            skip_animations=False,
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

        # add coord system to annotation?

        # ************************************************************
        self.next_section(
            'digitalize label class and label position',
            skip_animations=False,
        )
        # ************************************************************
        # emphasize class
        # emphasize position

        # introduce class mapping

        # loop through text of labels

        # loop through bbox of labels

        # ************************************************************
        self.next_section(
            'digitalize position',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'prepare 4 tables',
            skip_animations=False,
        )
        # ************************************************************
        _w, _h = annotation._w, annotation._h
        _xywh_norm = annotation.label[:, 1:]
        _xywh_full = (_xywh_norm * np.array([_w, _h, _w, _h])).astype(np.int32)
        _xyxy_norm = np.empty_like(_xywh_norm)
        _xyxy_norm[:, 0] = _xywh_norm[:, 0] - _xywh_norm[:, 2] / 2  # x1
        _xyxy_norm[:, 1] = _xywh_norm[:, 1] - _xywh_norm[:, 3] / 2  # y1
        _xyxy_norm[:, 2] = _xywh_norm[:, 0] + _xywh_norm[:, 2] / 2  # x2
        _xyxy_norm[:, 3] = _xywh_norm[:, 1] + _xywh_norm[:, 3] / 2  # y2
        _xyxy_full = (_xyxy_norm * np.array([_w, _h, _w, _h])).astype(np.int32)

        xyxy_full_tab = IntegerTable(
            _xyxy_full,
            col_labels=[
                Text('x1'), Text('y1'), Text('x2'), Text('y2'),
            ],
            # element_to_mobject_config={
            #     'num_decimal_places': 2,
            # }
        ).scale(0.5).shift(RIGHT * 10)
        xyxy_full_tab.remove(*xyxy_full_tab.get_vertical_lines())
        # TODO, make copy on other tables
        xyxy_full_tab_copy = xyxy_full_tab.copy()
        xyxy_full_tab.get_rows()[1:].set_opacity(0.2)

        xyxy_norm_tab = DecimalTable(
            _xyxy_norm,
            col_labels=[
                Text('x1'), Text('y1'), Text('x2'), Text('y2'),
            ],
            element_to_mobject_config={
                'num_decimal_places': 2,
            }
        ).scale(0.5).shift(RIGHT * 10)

        xywh_full_tab = IntegerTable(
            _xywh_full,
            col_labels=[
                Text('cx'), Text('cy'), Text('w'), Text('h'),
            ],
            # element_to_mobject_config={
            #     'num_decimal_places': 2,
            # }
        ).scale(0.5).shift(RIGHT * 10)

        xywh_norm_tab = DecimalTable(
            _xywh_norm,
            col_labels=[
                Text('cx'), Text('cy'), Text('w'), Text('h'),
            ],
            element_to_mobject_config={
                'num_decimal_places': 2,
            }
        ).scale(0.5).shift(RIGHT * 10)

        # ************************************************************
        self.next_section(
            'explain x1y1x2y2 full, loop',
            skip_animations=True,
        )
        # ************************************************************
        manager = Group(annotation, xyxy_full_tab)
        manager.generate_target()
        manager.target.arrange().center()
        manager.target[0].align_to(manager[0], UP)     # make annotation align horizontally
        self.play(MoveToTarget(manager))
        xyxy_full_tab_copy.move_to(xyxy_full_tab)       # TODO, on other tables
        self.wait()

        # TODO, make items transparent

        # fadeout labels
        self.play(annotation.hide_text())
        self.wait()

        # TODO, show x1y1x2y2, loop, transform into table

        # explain x1y1x2y2 annotation for each box
        for i in range(len(annotation.labels)):
            ref_box = annotation.labels[i]['bbox']
            _x1_label = xyxy_full_tab_copy.get_entries((i+2, 1)).copy()
            _y1_label = xyxy_full_tab_copy.get_entries((i+2, 2)).copy()
            _x2_label = xyxy_full_tab_copy.get_entries((i+2, 3)).copy()
            _y2_label = xyxy_full_tab_copy.get_entries((i+2, 4)).copy()
            # dot_x1y1 = Dot().move_to(ref_box.get_corner(UL)).scale(0.5).set_z_index(1)

            _x1, _y1 = axes.p2c(ref_box.get_corner(UL))
            _x2, _y2 = axes.p2c(ref_box.get_corner(DR))
            _x1_label.next_to(axes.c2p(_x1/2,0), UP*.7)
            _y1_label.next_to(axes.c2p(0,_y1/2), LEFT*.7)
            _x2_label.next_to(axes.c2p(_x2 / 2, 0), UP * .7)
            _y2_label.next_to(axes.c2p(0, _y2 / 2), LEFT * .7)

            _start_x1y1 = axes.c2p(_x1, _y1)
            _start_x2y2 = axes.c2p(_x2, _y2)
            _x1_base = axes.c2p(_x1, 0)
            _y1_base = axes.c2p(0, _y1)
            _x2_base = axes.c2p(_x2, 0)
            _y2_base = axes.c2p(0, _y2)
            _origin = axes.c2p(0, 0)
            path1_x1y1 = VMobject()
            path1_x1y1.set_points_as_corners([
                _start_x1y1,
                _x1_base,
                _origin,
            ]).set_color(YELLOW).set_stroke(width=2)
            path2_x1y1 = VMobject()
            path2_x1y1.set_points_as_corners([
                _start_x1y1,
                _y1_base,
                _origin,
            ]).set_color(YELLOW).set_stroke(width=2)

            path1_x2y2 = VMobject()
            path1_x2y2.set_points_as_corners([
                _start_x2y2,
                _x2_base,
                _origin,
            ]).set_color(YELLOW).set_stroke(width=2)
            path2_x2y2 = VMobject()
            path2_x2y2.set_points_as_corners([
                _start_x2y2,
                _y2_base,
                _origin,
            ]).set_color(YELLOW).set_stroke(width=2)

            # show x1 y1 labels
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path1_x1y1, run_time=2, time_width=2,),
                    Write(_x1_label),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path2_x1y1, run_time=2, time_width=2,),
                    Write(_y1_label),
                    lag_ratio=0.5,
                ),
            ))
            # self.wait()

            # transform x1y1 labels into target
            self.play(AnimationGroup(
                Transform(_x1_label, xyxy_full_tab_copy.get_entries((i+2, 1))),
                Transform(_y1_label, xyxy_full_tab_copy.get_entries((i+2, 2))),
            ))
            # self.wait()

            # show x2 y2 labels
            self.play(AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path1_x2y2, run_time=2, time_width=2, ),
                    Write(_x2_label),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path2_x2y2, run_time=2, time_width=2, ),
                    Write(_y2_label),
                    lag_ratio=0.5,
                ),
            ))
            # self.wait()

            # transform x2y2 labels into target
            self.play(AnimationGroup(
                Transform(_x2_label, xyxy_full_tab_copy.get_entries((i+2, 3))),
                Transform(_y2_label, xyxy_full_tab_copy.get_entries((i+2, 4))),
            ))
            # self.wait()

        # ************************************************************
        self.next_section(
            'explain cxcywh full, loop',
            skip_animations=True,
        )
        # ************************************************************
        _xyxy_norm = np.empty_like(_xywh_norm)
        _xyxy_norm[:, 0] = _xywh_norm[:, 0] - _xywh_norm[:, 2] / 2  # x1
        _xyxy_norm[:, 1] = _xywh_norm[:, 1] - _xywh_norm[:, 3] / 2  # y1
        _xyxy_norm[:, 2] = _xywh_norm[:, 0] + _xywh_norm[:, 2] / 2  # x2
        _xyxy_norm[:, 3] = _xywh_norm[:, 1] + _xywh_norm[:, 3] / 2  # y2
        _xyxy_full = (_xyxy_norm * np.array([_w, _h, _w, _h])).astype(np.int32)
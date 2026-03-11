import numpy as np
from manim import *

from utils.constants import S005_EVERYTHING
from utils.general import load_everything


class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'show annotation shape',
            skip_animations=True,
        )
        # ************************************************************
        (
            _, annotation, _, _, _,
        ) = load_everything(S005_EVERYTHING)
        self.add(annotation)

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

        ax_labels = axes.get_axis_labels()

        self.play(annotation.show_passing_flash())

        # ************************************************************
        self.next_section(
            'show axes and common coords',
            skip_animations=True,
        )
        # ************************************************************
        self.play(Write(axes, lag_ratio=0.0))
        self.wait()

        self.play(Write(ax_labels))
        self.wait()
        self.play(Unwrite(ax_labels))
        self.wait()

        # show TR and DL coords
        tr_label = Text(
            '(959,0)',
            font_size=20,
        ).next_to(annotation.get_corner(UR), UP)
        dl_label = Text(
            '(0,539)',
            font_size=20,
        ).next_to(annotation.get_corner(DL), LEFT)
        self.play(AnimationGroup(
            ReplacementTransform(annotation.shape_texts[1], tr_label),
            ReplacementTransform(annotation.shape_texts[0], dl_label),
        ))
        self.wait()

        # show origin and DR coords
        or_label = Text(
            '(0,0)',
            font_size=20,
        ).next_to(annotation.get_corner(UL), UL)
        dr_label = Text(
            '(959,539)',
            font_size=20,
        ).next_to(annotation.get_corner(DR), DOWN)
        self.play(AnimationGroup(
            Write(or_label),
            Write(dr_label),
        ))
        self.wait()

        # unwrite all coords
        self.play(AnimationGroup(
            Unwrite(or_label),
            Unwrite(tr_label),
            Unwrite(dr_label),
            Unwrite(dl_label),
        ))
        self.wait()

        annotation.add(axes)        # make axes child of annotation

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
            skip_animations=False,
        )
        # ************************************************************
        # first table prologue
        manager = Group(annotation, xyxy_full_tab)
        manager.generate_target()
        manager.target.arrange().center()
        self.play(MoveToTarget(manager))
        xyxy_full_tab_copy.move_to(xyxy_full_tab)       # TODO, on other tables
        self.wait()

        # TODO, make items transparent

        # fadeout labels
        self.play(annotation.hide_text())
        self.wait()

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
            skip_animations=False,
        )
        # ************************************************************
        _xyxy_norm = np.empty_like(_xywh_norm)
        _xyxy_norm[:, 0] = _xywh_norm[:, 0] - _xywh_norm[:, 2] / 2  # x1
        _xyxy_norm[:, 1] = _xywh_norm[:, 1] - _xywh_norm[:, 3] / 2  # y1
        _xyxy_norm[:, 2] = _xywh_norm[:, 0] + _xywh_norm[:, 2] / 2  # x2
        _xyxy_norm[:, 3] = _xywh_norm[:, 1] + _xywh_norm[:, 3] / 2  # y2
        _xyxy_full = (_xyxy_norm * np.array([_w, _h, _w, _h])).astype(np.int32)
from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground
from utils.anchor_point import AnchorPoint

import torch

def create_grid_cells(ref, n):
    # TODO, make rectangular ref work
    sq = Square(
        stroke_width=1,
        side_length=ref.width,
        grid_xstep=ref.width/n,
        grid_ystep=ref.width/n,
    )
    sq.move_to(ref)
    sq.grid_lines.set_stroke(width=1)
    return sq

def rect_from_point(point, left, up, right, down, **kwargs):
    x, y, z = point

    x_min = x - left
    x_max = x + right
    y_min = y - down
    y_max = y + up

    rect = Rectangle(
        width=x_max - x_min,
        height=y_max - y_min,
        stroke_width=1,
        stroke_opacity=0.3,
        **kwargs
    )

    rect.move_to([
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        z
    ])

    return rect

def create_anchor_points(ref, n, offsets):
    dx, dy = ref.width / n, ref.height / n
    aps = VGroup(*[
            AnchorPoint(
                ref.get_corner(UL)
                + DOWN * dx * (i + 0.5)
                + RIGHT * dy * (j + 0.5),   # position
                offsets[i*n+j],             # offset
            )
            for i in range(n)
            for j in range(n)
        ])
    return aps

def yolo_box_to_rect(img, cx, cy, w, h, **kwargs):
    x = cx * img.width
    y = cy * img.height

    rect = Rectangle(
        width=w * img.width,
        height=h * img.height,
        stroke_color=PURE_YELLOW,
        stroke_width=2,
        **kwargs
    )

    rect.move_to(img.get_corner(UL) + RIGHT * x + DOWN * y)
    return rect

def point_in_rect(point, rect):
    x, y, _ = point

    return (
        rect.get_left()[0] <= x <= rect.get_right()[0]
        and rect.get_bottom()[1] <= y <= rect.get_top()[1]
    )

def load_tensors():
    # sequence of directions: left, up, right, down
    pre_box = torch.load('assets/tensors/_pre_box.pt', weights_only=True, map_location='cpu')  # 1, 64, 8400
    norm_box = torch.load('assets/tensors/_norm_box.pt', weights_only=True, map_location='cpu')  # 1, 64, 8400
    dist_box = torch.load('assets/tensors/_dist_box.pt', weights_only=True, map_location='cpu')  # 1, 4, 8400
    decoded_box = torch.load('assets/tensors/_decoded_box.pt', weights_only=True, map_location='cpu')  # 1, 4, 8400

    pre_cls = torch.load('assets/tensors/_pre_cls.pt', weights_only=True, map_location='cpu')  # 1, 3, 8400
    norm_cls = torch.load('assets/tensors/_norm_cls.pt', weights_only=True, map_location='cpu')  # 1, 3, 8400

    return pre_box, norm_box, dist_box, decoded_box, pre_cls, norm_cls

class MainScene(Scene):
    def construct(self) -> None:
        (
            background,
        ) = load_everything(S012_EVERYTHING)
        # FIXME, manually setup background shape
        background._w = 640
        background._h = 640

        pre_box, norm_box, dist_box, decoded_box, pre_cls, norm_cls = load_tensors()

        # ************************************************************
        self.next_section(
            'init, show background shape before output design',
            skip_animations=True,
        )
        # ************************************************************
        self.add(background)
        self.wait()
        self.play(background.show_passing_flash())
        self.wait()

        # ************************************************************
        self.next_section(
            'from grid cells to anchor points',
            skip_animations=True,
        )
        # ************************************************************
        # create grid cells
        grid = create_grid_cells(background.background, 20)
        self.play(Write(grid))
        self.wait()

        # create anchors points, based on tensor content
        anchors = create_anchor_points(
            background,
            20,
            dist_box[0, :, 8000:].transpose(0, 1)
        )
        self.play(Write(anchors, lag_ratio=0.02))
        self.wait()
        self.play(AnimationGroup(
            background.unwrite_shape_texts(),
            Unwrite(grid),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'anchor point capture thinking',
            skip_animations=True,
        )
        # ************************************************************
        dd = float(background.width) / 20       # TODO, make 20 variable

        self.play(AnimationGroup(
            *(anchor.to_rect(
                dd,
                stroke_width=1,
                stroke_opacity=0.3,
                stroke_color=WHITE,
            ) for anchor in anchors),
            lag_ratio=0.003,
        ))
        self.wait()
        self.play(AnimationGroup(
            *(anchor.to_dot() for anchor in anchors),
            lag_ratio=0.003,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'identify important anchor points ',
            skip_animations=False,
        )
        # ************************************************************
        # plot reference bboxes
        bboxes = VGroup(
            *(yolo_box_to_rect(background.background, cx, cy, w, h) for _,cx,cy,w,h in background.data),
        )
        self.play(Write(bboxes))
        self.wait()
        # stress those anchors inside rects
        inside_anchors = VGroup(
            *(dot for dot in anchors if any(point_in_rect(dot.dot.get_center(),rect) for rect in bboxes))
        )

        # identify those anchors inside reference bboxes
        self.play(AnimationGroup(
            dot.animate.set_color(RED) for dot in inside_anchors
        ))
        self.wait()

        # let inside anchors capture
        self.play(AnimationGroup(
            *(anchor.to_rect(
                dd,
                stroke_width=1,
                stroke_opacity=1.0,
                stroke_color=RED,
            ) for anchor in inside_anchors),
            lag_ratio=0.03,
        ))
        self.wait()

        # back to background + anchor points
        self.play(AnimationGroup(
            *(anchor.to_dot() for anchor in inside_anchors),
            lag_ratio=0.03,
        ))
        self.wait()
        self.play(AnimationGroup(
            *(anchor.animate.set_color(WHITE) for anchor in inside_anchors),
            Unwrite(bboxes),
        ))
        self.wait()

        # TODO: which target to capture? inside/inside-multiple/outside

        # ************************************************************
        self.next_section(
            'focus on one specific anchor',
            skip_animations=False,
        )
        # ************************************************************

        # output design 1: 640-scale distance

        # output design 2: fm-32 distance, yolo26

        # output design 3: prob distribution, yolov8/yolo11/..

        # decode step roughly, before tensor introduction

        # save for next scene

from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground

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

def create_anchor_points(ref, n):
    dx, dy = ref.width / n, ref.height / n
    dots = VGroup(*[
            Dot(
                ref.get_corner(UL)
                + DOWN * dx * (i + 0.5)
                + RIGHT * dy * (j + 0.5),
                radius=0.03
            )
            for i in range(n)
            for j in range(n)
        ])
    return dots

class MainScene(Scene):
    def construct(self) -> None:
        (
            background,
        ) = load_everything(S012_EVERYTHING)
        # FIXME, manually setup background shape
        background._w = 640
        background._h = 640

        self.add(background)
        self.wait()
        self.play(background.show_passing_flash())
        self.wait()

        # create grid cells
        grid = create_grid_cells(background.background, 20)
        self.play(Write(grid))
        self.wait()

        # create anchors points, fade out grid cells
        anchors = create_anchor_points(background, 20)
        self.play(Write(anchors))
        self.wait()
        self.play(AnimationGroup(
            background.unwrite_shape_texts(),
            Unwrite(grid),
        ))
        self.wait()

        # capture thinking

        # which target to capture? inside/inside-multiple/outside

        # output design 1: 640-scale distance

        # output design 2: fm-32 distance, yolo26

        # output design 3: prob distribution, yolov8/yolo11/..

        # decode step roughly, before tensor introduction

        # save for next scene

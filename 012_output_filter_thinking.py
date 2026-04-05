from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground

def random_rectangles_in_region(
    n,
    top_left,
    bottom_right,
    min_size=0.1,
    max_size=0.8,
):
    x_min, y_max, _ = top_left
    x_max, y_min, _ = bottom_right

    rects = VGroup()

    for _ in range(n):
        w = np.random.uniform(min_size, max_size)
        h = np.random.uniform(min_size, max_size)

        # sample center so rectangle stays inside
        cx = np.random.uniform(x_min + w/2, x_max - w/2)
        cy = np.random.uniform(y_min + h/2, y_max - h/2)

        rect = Rectangle(width=w, height=h, stroke_width=1.)
        rect.move_to([cx, cy, 0])

        rects.add(rect)

    return rects

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        (
            image_raw, ac_ab, image_repad, ac_bc, image_norm, _, annotation_repad, ac_yz, annotation_final,
            ac_a1, _, ac_b2, _, ac_c3, _, ac_y8, _, ac_z9,
            lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_repad, ac_89, lf_output_final,
        ) = load_everything(S011_EVERYTHING)

        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_repad, ac_yz, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_repad, ac_89, lf_output_final],
        )
        self.add(manager)
        self.wait()

        # ************************************************************
        self.next_section(
            'generate background_tmp from annotation_repad',
            skip_animations=False,
        )
        # ************************************************************
        background_tmp = RepadBackground(annotation_repad)  # store copy of annotation_repad components
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), background_tmp, annotation_repad, ac_yz, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, VMobject(), lf_output_repad, ac_89, lf_output_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=10,
            # buff=1.0,
        ).scale(0.8).center()
        # TODO, make starting background_tmp opacity 0.0
        self.play(MoveToTarget(manager))
        self.wait()

        # generate lot of random bboxes
        rects_tmp = random_rectangles_in_region(
            20,
            background_tmp.get_corner(UL),
            background_tmp.get_corner(DR),
        )
        self.play(Write(rects_tmp))
        background_tmp.add(rects_tmp)   # make rects move with background_tmp
        self.wait()

        # ************************************************************
        self.next_section(
            'generate lf_output_tmp from lf_output_repad',
            skip_animations=False,
        )
        # ************************************************************
        lf_output_tmp = lf_output_repad.copy()
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), background_tmp, annotation_repad, ac_yz,
              annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_tmp, lf_output_repad, ac_89, lf_output_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=10,
            # buff=1.0,
        ).scale(1.0).center()
        manager.target[26].stretch_to_fit_height(1.5)     # stretch lf_output_tmp means it's the full version
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'focus on background_tmp',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), background_tmp, annotation_repad, ac_yz,
              annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_tmp, lf_output_repad, ac_89,
              lf_output_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=10,
            buff=10,
        )
        manager.target.shift(-manager.target[6].get_center())
        manager.target[6].scale(6.0)
        self.play(MoveToTarget(manager))
        self.play(Unwrite(rects_tmp, lag_ratio=0))
        background_tmp.remove(rects_tmp)
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            background_tmp,
        )
        save_everything(S012_EVERYTHING, everything)
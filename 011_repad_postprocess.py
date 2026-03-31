from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation, AnnotationRepad

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        (
            image_raw, ac_ab, image_repad, ac_bc, image_norm, annotation_final,
            ac_a1, ac_b2, ac_c3, ac_z9,
            lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_final,
        ) = load_everything(S010_EVERYTHING)
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_final],
        )
        self.add(manager)

        # ************************************************************
        self.next_section(
            'generate annotation_copy from annotation_final',
            skip_animations=False,
        )
        # ************************************************************
        annotation_copy = annotation_final.copy()
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_copy, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, VMobject(), lf_output_final],
        )
        manager.generate_target()
        manager.target[6].scale(2/3)    # scale annotation_copy
        manager.target.arrange_in_grid(
            rows=3,
            cols=8,
            # buff=1.0,
        ).scale(0.9).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'pad annotation_copy into annotation_repad',
            skip_animations=False,
        )
        # ************************************************************
        annotation_repad = AnnotationRepad(annotation_copy, False)
        self.play(annotation_repad.show_paddings())
        self.wait()

        # ************************************************************
        self.next_section(
            'generate lf_output_repad from lf_output_final',
            skip_animations=False,
        )
        # ************************************************************
        lf_output_repad = lf_output_final.copy()
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_repad, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_repad, lf_output_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=8,
            # buff=1.0,
        ).scale(1.0).center()
        # FIXME, minor shift or the whole map
        self.play(MoveToTarget(manager))
        self.wait()

        # TODO, show axes of annotation_repad and annotation_final?

        # ************************************************************
        self.next_section(
            'introduce remaining acs',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME, not robust way of scale
        ac_yz = ArrowComment(False, RIGHT, '?').scale_to_fit_width(ac_ab.width).shift(UP*10)
        ac_y8 = ArrowComment(True, DOWN, '?').scale_to_fit_height(ac_a1.height).shift(RIGHT*10)
        ac_89 = ArrowComment(False, RIGHT, '?').scale_to_fit_width(ac_ab.width).shift(DOWN*10)
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_repad, ac_yz, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_repad, ac_89, lf_output_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=9,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'loop through different output shapes, finally back',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'save for next scene',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_repad, ac_yz, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_repad, ac_89, lf_output_final],
        )
        save_everything(S011_EVERYTHING, everything)
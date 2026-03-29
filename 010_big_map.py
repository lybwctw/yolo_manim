from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        (
            image_raw, image_repad, image_norm,
            lf_image_raw, lf_image_repad, lf_image_norm,
        ) = load_everything(S009_EVERYTHING)

        (
            _, annotation_final,
            _, _,
            _, _, lf_output_final,
        ) = load_everything(S007_EVERYTHING)

        manager = Group(
            *[image_raw, image_repad, image_norm],
            *[lf_image_raw, lf_image_repad, lf_image_norm],
        )
        self.add(manager)
        self.wait()

        ac_ab = ArrowComment(False, RIGHT, '?').shift(UP*20)
        ac_bc = ArrowComment(False, RIGHT, '?').shift(UP*20)
        ac_a1 = ArrowComment(True, DOWN, '?').shift(LEFT*20)
        ac_b2 = ArrowComment(True, DOWN, '?').shift(LEFT*20)
        ac_c3 = ArrowComment(True, DOWN, '?').shift(LEFT*20)
        ac_12 = ArrowComment(False, RIGHT, '?').shift(DOWN*20)
        ac_23 = ArrowComment(False, RIGHT, '?').shift(DOWN*20)
        ac_game = ArrowComment(False, RIGHT, '?').shift(DOWN*20)
        ac_z9 = ArrowComment(True, DOWN, '?').shift(RIGHT*20)   # FIXME, unknown highlight

        ac_all = VGroup(
            ac_ab, ac_bc,
            ac_a1, ac_b2, ac_c3,  ac_z9,
            ac_12, ac_23, ac_game,
        ).scale(0.5)

        everything = Group(
            *ac_all,
            image_raw, image_repad, image_norm, annotation_final,
            lf_image_raw, lf_image_repad, lf_image_norm, lf_output_final,
        )

        # ************************************************************
        self.next_section(
            'back to input side big map',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm],
        )
        manager.generate_target()
        scale_manager_target(
            manager,
            everything,
            scale=0.9,
        )
        manager.target.arrange_in_grid(
            rows=3,
            cols=5,
            # buff=1.0,
        ).center()
        # remove internal digits to make the big map clean
        manager.target[12].remove(manager.target[12].fake_internal)
        manager.target[14].remove(manager.target[14].fake_internal)

        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'back to complete big map',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_final],
        )
        manager.generate_target()
        scale_manager_target(
            manager,
            everything,
            scale=0.8,
        )
        manager.target.arrange_in_grid(
            rows=3,
            cols=7,
            # buff=1.0,
        ).center()
        manager.target[19].shift(RIGHT*.5)  # adjust ac_game
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'show all shapes',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            ac_all.animate.set_opacity(0.1),    # FIXME, differentiate ud and lr arrows
            image_raw.show_passing_flash(),
            image_repad.show_passing_flash(),
            image_norm.show_passing_flash(),
            annotation_final.show_passing_flash(),
            lf_image_raw.show_passing_flash(),
            lf_image_repad.show_passing_flash(),
            lf_image_norm.show_passing_flash(),
            lf_output_final.show_passing_flash(),
        ))
        self.wait()
        self.play(AnimationGroup(
            ac_all.animate.set_opacity(1.0),  # FIXME, differentiate ud and lr arrows
            image_raw.unwrite_shape_texts(),
            image_repad.unwrite_shape_texts(),
            image_norm.unwrite_shape_texts(),
            annotation_final.unwrite_shape_texts(),
            lf_image_raw.unwrite_shape_texts(),
            lf_image_repad.unwrite_shape_texts(),
            lf_image_norm.unwrite_shape_texts(),
            lf_output_final.unwrite_shape_texts(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene',
            skip_animations=False,
        )
        # ************************************************************
        # starting everything or ending everything?
        everything = Group(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, annotation_final],
            *[ac_a1, ac_b2, ac_c3, ac_z9],
            *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_final],
        )
        save_everything(S010_EVERYTHING, everything)
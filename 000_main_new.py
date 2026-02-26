from manim import *

from utils.constants import *
from utils.image_repad import ImageRepad
from utils.tile_comment import TileComment
from utils.layers_fake import LayersFake
from utils.grid_annotation_box import GridAnnotationBox
from utils.grid_annotation_cls import GridAnnotationCls
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation

class MainScene(Scene):
    def scale_align(self, manager, everything, scales):
        if 'all' in scales:
            for mob in manager.target:
                mob.scale(scales['all'])
            for mob in everything:
                if mob not in manager:
                    mob.scale(scales['all'])
        else:
            for mob in manager.target:
                if type(mob) in scales:
                    mob.scale(scales[type(mob)])
            for mob in everything:
                if mob not in manager:
                    if type(mob) in scales:
                        mob.scale(scales[type(mob)])

    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init assets',
            skip_animations=True,
        )
        # ************************************************************
        image_raw = ImageRepad(PATH_IMAGE_RAW).shift(INIT_SHIFT_IMAGE_RAW)
        lf_input_raw = LayersFake(image_raw).shift(INIT_SHIFT_LF_INPUT_RAW)
        tile_input = TileComment('digits').shift(INIT_SHIFT_TILE_OUTPUT)

        image_repad = ImageRepad(image_raw)
        lf_input_repad = LayersFake(image_repad)

        image_norm = ImageRepad(image_repad)
        lf_input_norm = LayersFake(image_norm)

        annotation_32_box = GridAnnotationBox(PATH_TENSOR_32_BOX)
        lf_output_32_box = LayersFake(annotation_32_box)

        annotation_32_cls = GridAnnotationCls(PATH_TENSOR_32_CLS)
        lf_output_32_cls = LayersFake(annotation_32_cls)

        annotation_32_decode = ImageAnnotation(PATH_TXT_DECODE, image_repad)
        lf_output_32_decode = LayersFake(annotation_32_decode)

        annotation_repad = ImageAnnotation(PATH_TXT_RES, image_repad).shift(INIT_SHIFT_ANNOTATION_REPAD)
        lf_output_repad = LayersFake(annotation_repad).shift(INIT_SHIFT_LF_OUTPUT_REPAD)

        annotation_final = ImageAnnotation(PATH_TXT_RES, image_raw).shift(INIT_SHIFT_ANNOTATION_FINAL)
        lf_output_final = LayersFake(annotation_final).shift(INIT_SHIFT_LF_OUTPUT_FINAL)
        tile_output = TileComment('digits').shift(INIT_SHIFT_TILE_OUTPUT)

        ac_ab = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_AB)
        ac_bc = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_BC)
        ac_wx = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_WX)
        ac_xy = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_XY)
        ac_yz = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_YZ)

        ac_a1 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_A1)
        ac_b2 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_B2)
        ac_c3 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_C3)
        ac_v5 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_V5)
        ac_w6 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_W6)
        ac_x7 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_X7)
        ac_y8 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_Y8)
        ac_z9 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_Z9)

        ac_12 = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_12)
        ac_23 = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_23)
        ac_game = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_GAME)
        ac_67 = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_67)
        ac_78 = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_78)
        ac_89 = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_89)

        everything = VGroup(
            image_raw, lf_input_raw, tile_input,
            image_repad, lf_input_repad,
            image_norm, lf_input_norm,
            annotation_32_box, lf_output_32_box,
            annotation_32_cls, lf_output_32_cls,
            annotation_32_decode, lf_output_32_decode,
            annotation_repad, lf_output_repad,
            annotation_final, lf_output_final, tile_output,
            ac_ab, ac_bc, ac_wx, ac_xy, ac_yz,
            ac_a1, ac_b2, ac_c3, ac_v5, ac_w6, ac_x7, ac_y8, ac_z9,
            ac_12, ac_23, ac_game, ac_67, ac_78, ac_89,
        )
        # ************************************************************
        self.next_section(
            'start scene',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, ac_game, annotation_final],
        ).center()

        self.add(manager)
        self.wait()

        # ************************************************************
        self.next_section(
            'split image and annotation',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, ac_game, annotation_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=1,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'introduce digit game',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[tile_input, ac_game, tile_output],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'focus on image_raw',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[tile_input, ac_game, tile_output],
        )
        manager.save_state()    # for back to the big map later
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        manager.target.shift(-manager.target[0].get_center())
        manager.target[0].scale(2.0)        # FIXME, or scale_to_fit_width?
        self.play(MoveToTarget(manager))
        self.wait()

        # share state for scene 001
        self.save_state(S001_IMAGE_RAW, image_raw.width)

        # ************************************************************
        self.next_section(
            'focus back to the big map',
            skip_animations=True,
        )
        # ************************************************************
        self.play(manager.animate.restore())
        self.wait()

        # ************************************************************
        self.next_section(
            'replace tile_input with lf_input_raw',
            skip_animations=True,
        )
        # ************************************************************
        lf_input_raw.match_x(tile_input, ORIGIN)
        lf_input_raw.generate_target()
        lf_input_raw.target.move_to(tile_input)
        tile_input.generate_target()
        tile_input.target.shift(LEFT*10)
        self.play(AnimationGroup(
            MoveToTarget(tile_input),
            MoveToTarget(lf_input_raw),
        ))
        self.remove(tile_input)     # tile_input not needed any more
        self.wait()

        # ************************************************************
        self.next_section(
            'focus on annotation_final',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[lf_input_raw, ac_game, tile_output],
        )
        manager.save_state()  # for back to the big map later
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        manager.target.shift(-manager.target[2].get_center())
        manager.target[2].scale(2.0)  # FIXME, or scale_to_fit_width?
        self.play(MoveToTarget(manager))
        self.wait()

        # share state for scene 002
        self.save_state(S002_ANNOTATION_FINAL, annotation_final.width)

        # ************************************************************
        self.next_section(
            'focus back to the big map',
            skip_animations=True,
        )
        # ************************************************************
        self.play(manager.animate.restore())
        self.wait()

        # ************************************************************
        self.next_section(
            'replace tile_output with lf_input_raw',
            skip_animations=True,
        )
        # ************************************************************
        lf_output_final.match_x(tile_output, ORIGIN)
        lf_output_final.generate_target()
        lf_output_final.target.move_to(tile_output)
        tile_output.generate_target()
        tile_output.target.shift(RIGHT*10)
        self.play(AnimationGroup(
            MoveToTarget(tile_output),
            MoveToTarget(lf_output_final),
        ))
        self.remove(tile_output)  # tile_output not needed any more
        self.wait()

        # ************************************************************
        self.next_section(
            'two preferences of modern AI',
            skip_animations=True,
        )
        # ************************************************************
        # TODO .. fast switching of input and output

        # ************************************************************
        self.next_section(
            'focus on image_raw and lf_input_raw',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            VGroup(*[manager[0], manager[3], lf_input_raw]),
            VGroup(*[manager[1], manager[4], manager[7]]),
            VGroup(*[manager[2], manager[5], lf_output_final]),
        )
        manager.generate_target()
        manager.target.arrange(
            direction=RIGHT,
            buff=10.0,
        )
        manager.target.shift(-manager.target[0].get_center())
        self.play(MoveToTarget(manager))
        self.wait()

        # play the source->target animation
        # focus back
        # insert the target

        # ************************************************************
        self.next_section(
            'image_repad generated from image_raw',
            skip_animations=True,
        )
        # ************************************************************
        # TODO, make the repad smaller, and pad
        image_repad.move_to(image_raw)
        manager = VGroup(
            *[image_raw, image_repad],
            *[ac_a1, VMobject()],
            *[lf_input_raw, VMobject()],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=2,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'lf_input_repad generated from lf_input_raw',
            skip_animations=True,
        )
        # ************************************************************
        # TODO, make the repad smaller, and pad
        lf_input_repad.move_to(lf_input_raw)
        manager = VGroup(
            *[image_raw, VMobject(), image_repad],
            *[ac_a1, VMobject(), VMobject()],
            *[lf_input_raw, VMobject(), lf_input_repad],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'lf_input_norm generated from lf_input_repad',
            skip_animations=True,
        )
        # ************************************************************
        lf_input_norm.move_to(lf_input_repad)
        manager = VGroup(
            *[image_raw, image_repad, VMobject()],
            *[ac_a1, VMobject(), VMobject()],
            *[lf_input_raw, lf_input_repad, lf_input_norm],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'image_norm generated from image_repad',
            skip_animations=True,
        )
        # ************************************************************
        image_norm.move_to(image_repad)
        manager = VGroup(
            *[image_raw, image_repad, image_norm],
            *[ac_a1, VMobject(), VMobject()],
            *[lf_input_raw, lf_input_repad, lf_input_norm],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'insert arrows with comment',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3],
            *[lf_input_raw, ac_12, lf_input_repad, ac_23, lf_input_norm],
        )
        manager.generate_target()
        self.scale_align(
            manager,
            everything,
            {'all': 0.7}
        )
        # for mob in manager.target:
        #     mob.scale(0.7)
        manager.target.arrange_in_grid(
            rows=3,
            cols=5,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'focus back',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_z9],
            *[lf_input_raw, ac_12, lf_input_repad, ac_23, lf_input_norm, ac_game, lf_output_final],
        )
        manager.generate_target()
        self.scale_align(
            manager,
            everything,
            {'all': 0.8}
        )
        manager.target.arrange_in_grid(
            rows=3,
            cols=7,
            # buff=10.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'insert annotation_repad and lf_output_repad',
            skip_animations=True,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_repad, ac_yz, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_input_raw, ac_12, lf_input_repad, ac_23, lf_input_norm, ac_game, lf_output_repad, ac_89, lf_output_final],
        )
        manager.generate_target()
        self.scale_align(
            manager,
            everything,
            {'all': 0.8}
        )
        manager.target.arrange_in_grid(
            rows=3,
            cols=9,
            # buff=10.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'still problem with output',
            skip_animations=True,
        )
        # ************************************************************
        # TODO .. fast switching of output

        # ************************************************************
        self.next_section(
            'focus on annotation_repad',
            skip_animations=False,
        )
        # ************************************************************
        manager = VGroup(
            *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), annotation_repad, ac_yz, annotation_final],
            *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), ac_y8, VMobject(), ac_z9],
            *[lf_input_raw, ac_12, lf_input_repad, ac_23, lf_input_norm, ac_game, lf_output_repad, ac_89,
              lf_output_final],
        )
        manager.save_state()
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=9,
            buff=10.0,
        )
        manager.target.shift(-manager.target[6].get_center())
        # scale single for immediate focus back instead of further scale
        manager.target[6].scale(3.0)    # FIXME, or scale_to_fit_width
        self.play(MoveToTarget(manager))
        self.wait()

        # share state for scene 003
        self.save_state(S003_ANNOTATION_REPAD, annotation_repad.width)

        # ************************************************************
        self.next_section(
            'focus back to the big map',
            skip_animations=False,
        )
        # ************************************************************
        self.play(manager.animate.restore())
        self.wait()

    def save_state(self, key, value):
        with open(key, 'w') as f:
            f.write(str(value))
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
    def scale_manager_target(self, manager, everything, scale):
        """
        scale mobs in manager.target
        scale mobs in everything while not in manager
        """
        for mob in manager.target:
            mob.scale(scale)
        for mob in everything:
            if mob not in manager:
                mob.scale(scale)

    def construct(self) -> None:
        image_raw = ImageRepad(PATH_IMAGE_RAW).shift(INIT_POS_IMAGE_RAW)
        lf_input_raw = LayersFake(image_raw).shift(INIT_POS_LF_INPUT_RAW)
        tile_input = TileComment('digits').shift(INIT_POS_TILE_OUTPUT)

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

        annotation_repad = ImageAnnotation(PATH_TXT_RES, image_repad).shift(INIT_POS_ANNOTATION_REPAD)
        lf_output_repad = LayersFake(annotation_repad).shift(INIT_POS_LF_OUTPUT_REPAD)

        annotation_final = ImageAnnotation(PATH_TXT_RES, image_raw).shift(INIT_POS_ANNOTATION_FINAL)
        lf_output_final = LayersFake(annotation_final).shift(INIT_POS_LF_OUTPUT_FINAL)
        tile_output = TileComment('digits').shift(INIT_POS_TILE_OUTPUT)

        ac_ab = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_AB)
        ac_bc = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_BC)
        ac_wx = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_WX)
        ac_xy = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_XY)
        ac_yz = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_YZ)

        ac_a1 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_A1)
        ac_b2 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_B2)
        ac_c3 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_C3)
        ac_v5 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_V5)
        ac_w6 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_W6)
        ac_x7 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_X7)
        ac_y8 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_Y8)
        ac_z9 = ArrowComment(True, DOWN, '?').shift(INIT_POS_AC_Z9)

        ac_12 = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_12)
        ac_23 = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_23)
        ac_game = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_GAME)
        ac_67 = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_67)
        ac_78 = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_78)
        ac_89 = ArrowComment(False, RIGHT, '?').shift(INIT_POS_AC_89)

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
            'overlapped image_raw and annotation_final',
            skip_animations=False,
        )
        # ************************************************************
        image_raw.move_to(INIT_POS_IMAGE_RAW)
        image_raw.scale_to_fit_width(INIT_WIDTH_IMAGE_RAW)
        annotation_final.move_to(INIT_WIDTH_ANNOTATION_FINAL)
        annotation_final.scale_to_fit_width(INIT_WIDTH_ANNOTATION_FINAL)
        ac_game.move_to(INIT_POS_AC_GAME)
        ac_game.scale_to_fit_width(INIT_WIDTH_AC_GAME)

        manager = VGroup(
            *[image_raw, ac_game, annotation_final],
        )

        self.add(manager)
        self.wait()

        # ************************************************************
        self.next_section(
            'split image_raw and annotation_final',
            skip_animations=False,
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
            'introduce tile_input and tile_output',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'focus on image_raw, save scale factor',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        # focus back should be implemented in the separate scene
        self.next_section(
            's001, explain RGB color space',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'generate lf_input_raw from image_raw',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'generate lf_input_raw from image_raw',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'focus back to big map',
            skip_animations=False,
        )
        # ************************************************************
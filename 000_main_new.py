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
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init assets',
            skip_animations=True,
        )
        # ************************************************************
        image_raw = ImageRepad(PATH_IMAGE_RAW)
        lf_input_raw = LayersFake(image_raw)
        tile_input = TileComment('digits').shift(INIT_SHIFT_TILE_OUTPUT)

        image_repad = ImageRepad(image_raw)
        lf_input_repad = LayersFake(image_repad)

        lf_input_norm = LayersFake(lf_input_repad)

        annotation_32_box = GridAnnotationBox(PATH_TENSOR_32_BOX)
        lf_output_32_box = LayersFake(annotation_32_box)

        annotation_32_cls = GridAnnotationCls(PATH_TENSOR_32_CLS)
        lf_output_32_cls = LayersFake(annotation_32_cls)

        annotation_32_decode = ImageAnnotation(PATH_TXT_DECODE, image_repad)
        lf_output_32_decode = LayersFake(annotation_32_decode)

        annotation_repad = ImageAnnotation(PATH_TXT_RES, image_repad)
        lf_output_repad = LayersFake(annotation_repad)

        annotation_final = ImageAnnotation(PATH_TXT_RES, image_raw)
        lf_output_final = LayersFake(annotation_final)
        tile_output = TileComment('digits').shift(INIT_SHIFT_TILE_OUTPUT)

        ac_ab = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_AB)
        ac_wx = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_WX)
        ac_xy = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_XY)
        ac_yz = ArrowComment(False, RIGHT, '?').shift(INIT_SHIFT_AC_YZ)

        ac_a1 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_A1)
        ac_b2 = ArrowComment(True, DOWN, '?').shift(INIT_SHIFT_AC_B2)
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

        # ************************************************************
        self.next_section(
            'start scene',
            skip_animations=False,
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
            'introduce digit game',
            skip_animations=False,
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
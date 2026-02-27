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
        image_raw = ImageRepad(PATH_IMAGE_RAW).shift(INIT_SHIFT_IMAGE_RAW)
        lf_input_raw = LayersFake(image_raw).shift(INIT_SHIFT_LF_INPUT_RAW)
        tile_input = TileComment('digits').shift(INIT_SHIFT_TILE_OUTPUT)

        # ************************************************************
        self.next_section(
            'overlapped image_raw and annotation_final',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'split image_raw and annotation_final',
            skip_animations=False,
        )
        # ************************************************************

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
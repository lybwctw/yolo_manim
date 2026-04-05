from manim import *
from utils.constants import *
from utils.image_pad import ImageRaw, ImageRepad
from utils.tile_comment import TileComment
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import ImageAnnotation
from utils.general import save_everything, load_everything, load_central_cells
from utils.color_cell import ColorCell


class MainScene(MovingCameraScene):
    def construct(self) -> None:
        (
            image_raw, tile_input,
            annotation_final, tile_output,
            ac_a1, ac_z9,
            ac_game,
        ) = load_everything(S000_EVERYTHING)

        # ************************************************************
        self.next_section(
            'starting image',
            skip_animations=False,
        )
        # ************************************************************
        # self.add(image_raw)
        # self.wait()

        # ************************************************************
        self.next_section(
            'zoom',
            skip_animations=False,
        )
        # ************************************************************
        _image_raw = image_raw.image.copy()
        _image_raw.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        self.add(_image_raw)
        self.wait()
        self.play(_image_raw.animate.scale_to_fit_height(360/2))
        self.wait()

        # ************************************************************
        self.next_section(
            'show pixel cells',
            skip_animations=False,
        )
        # ************************************************************
        cells = load_central_cells(
            PATH_IMAGE_640,
            rows=16,
            cols=30,
            target_height=config.frame_height,
        )
        cells.shuffle()

        self.play(Write(cells))
        self.remove(_image_raw)

        # maybe floating effect of pixels?

        # ************************************************************
        self.next_section(
            'save for next scene, extension and focus back',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            _image_raw,
            cells,
        )
        save_everything(S001_EVERYTHING, everything)
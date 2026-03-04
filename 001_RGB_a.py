from manim import *
from utils.constants import *
from utils.image_repad import ImageRaw, ImageRepad
from utils.tile_comment import TileComment
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation
from utils.general import save_everything, load_everything, scale_manager_target
from utils.color_cell import ColorCell

import cv2

def load_central_cells(path, rows, cols):
    """
    Load central pixels and convert into cells vmobjects
    """
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    r0 = (h - rows) // 2
    c0 = (w - cols) // 2
    ps = img[r0:r0+rows, c0:c0+cols]

    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            r, g, b = ps[i, j]
            cells.add(ColorCell(r, g, b))
    cells.arrange_in_grid(
        rows=rows,
        cols=cols,
        buff=0,
    ).scale_to_fit_height(config.frame_height)

    return cells

class MainScene(MovingCameraScene):
    def construct(self) -> None:
        (
            image_raw, tile_input,
            annotation_final, tile_output,
            ac_a1, ac_z9,
            ac_game,
        ) = load_everything(S001_EVERYTHING)

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
        ).shuffle()

        self.play(Write(cells))
        self.remove(_image_raw)

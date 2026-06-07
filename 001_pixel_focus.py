from manim import *
from utils.constants import *
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.general import import_mobs, export_mobs
from utils.color_cell import load_central_cells

wt = SHORT_DURATION
class MainScene(MovingCameraScene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init from previous',
            skip_animations=False,
        )
        # ************************************************************
        (
            sin_raw,
        ) = import_mobs('000', 'b')
        self.add(sin_raw)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'zoom in',
            skip_animations=False,
        )
        # ************************************************************
        self.play(sin_raw.animate(
            run_time=wt,
        ).scale_to_fit_height(360/2))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show pixel cells',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME: to do with 360/2
        cells = load_central_cells(
            PATH_IMAGE_640,                 
            rows=16,
            cols=30,
            target_height=config.frame_height,
        )
        cells.shuffle()

        self.play(Write(
            cells,
            run_time=wt,
        ))
        self.remove(sin_raw)

        # TODO: floating effect of pixels?

        # ************************************************************
        self.next_section(
            'save mobs, used by 004',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            sin_raw,
            cells,
        )
        export_mobs(__file__, mobs)     # NOTE: used by 004
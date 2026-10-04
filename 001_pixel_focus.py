from manim import *
from utils.constants import *

from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.general import import_mobs, export_mobs
from utils.color_cell import load_central_cells

SESSION_SCALE = 2.0

wt = SHORT_DURATION
class MainScene(MovingCameraScene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('000')
        (
            iv_input, iv_output,
            ac_left,  ac_right,
            tv_input_cn, ac_game,  tv_output_cn,
        ) = mobs
        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on image input',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            iv_input, Mobject(), iv_output,
            ac_left,   Mobject(), ac_right,
            tv_input_cn, ac_game,  tv_output_cn,
        )
        mobs.save_state()
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        mobs.target.shift(-mobs.target[0].get_center())
        mobs.target[0].scale(SESSION_SCALE)

        # focus animation
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'zoom in on image input',
            skip_animations=False,
        )
        # ************************************************************
        self.play(iv_input.animate(
            run_time=wt,
        ).scale_to_fit_height(360/2))
        self.wait(wt)

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

        self.play(Write(
            cells,
            run_time=wt,
        ))
        self.wait(wt)
        self.remove(iv_input)

        # ************************************************************
        self.next_section(
            'export',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            iv_input,
            cells,
        )
        export_mobs(__file__, mobs)
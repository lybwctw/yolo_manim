from manim import *
from utils.constants import *

from utils.image_raw import ImageRaw
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.general import export_mobs

TEXT_EN_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
    'color': WHITE,
}
TEXT_CN_CONFIG = {
    'font': 'Source Han Sans SC',
    'font_size': 32,
    'color': WHITE,
}

SESSION_SCALE = 0.5

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'start with image',
            skip_animations=False,
        )
        # ************************************************************
        # pretend to be 960x540, but actually 640x360
        iv_input = ImageRaw(
            path=PATH_IMAGE_640,
            width_nominal=960,
            height_nominal=540,
        ).scale_to_fit_width(config.frame_width/2)

        self.play(FadeIn(
            iv_input,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'object detection task',
            skip_animations=False,
        )
        # ************************************************************
        annotation = YoloAnnotation(
            background=iv_input,
            annotation=PATH_LABEL,
        )
        self.play(Write(
            annotation,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'switch frames, there and back',
            skip_animations=False,
        )
        # ************************************************************
        # TODO

        # ************************************************************
        self.next_section(
            'split input and output',
            skip_animations=False,
        )
        # ************************************************************
        # prepare assets
        annotation_bg = iv_input.copy().fade(0.6)
        annotation.background = annotation_bg
        iv_output = Group(annotation_bg, annotation)
        ac_game = ArrowComment(False, RIGHT).set_opacity(0.0)
        mobs = Group(
            iv_input, ac_game, iv_output,
        )
        mobs.generate_target()
        mobs.target.arrange(
            RIGHT,
            # buff=1.0,
        ).scale(SESSION_SCALE).center()
        mobs.target[1].set_opacity(1.0)

        # split animation
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)
        
        # ************************************************************
        self.next_section(
            'turn into digit game',
            skip_animations=False,
        )
        # ************************************************************
        # prepare assets
        tv_input_cn = Text(
            text='一堆数字',
            **TEXT_CN_CONFIG,
        ).shift(DOWN*10).set_x(
            iv_input.get_x()
        )
        tv_output_cn = tv_input_cn.copy().set_x(
            iv_output.get_x()
        )
        tv_input_en = Text(
            text='values',
            **TEXT_EN_CONFIG,
        ).shift(DOWN*10).set_x(
            iv_input.get_x()
        )
        tv_output_en = tv_input_en.copy().set_x(
            iv_output.get_x()
        )
        ac_left = ArrowComment(True, DOWN).shift(LEFT*10).scale(SESSION_SCALE)
        ac_right = ArrowComment(True, UP).shift(RIGHT*10).scale(SESSION_SCALE)
        mobs = Group(
            iv_input, Mobject(), iv_output,
            ac_left,   Mobject(), ac_right,
            tv_input_cn, ac_game,  tv_output_cn,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
        ).center()

        # introduce animation
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'export',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            iv_input, iv_output,
            ac_left, ac_right,
            tv_input_cn, ac_game, tv_output_cn,
        )
        export_mobs(__file__, mobs)
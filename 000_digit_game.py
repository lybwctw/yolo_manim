from manim import *
from utils.constants import *
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.general import export_mobs

TEXT_EN_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
    'color': WHITE,
}
TEXT_CN_CONFIG = {
}

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'start with image and annotation',
            skip_animations=False,
        )
        # ************************************************************
        sin_raw = ImageRaw(
            path=PATH_IMAGE_640,        # fake 960
            width_nominal=960,
            height_nominal=540,
        ).scale(1.5)                    # half of frame height
        annotation_bg = sin_raw.copy().fade(0.7)
        annotation = YoloAnnotation(
            background=annotation_bg,
            annotation=PATH_LABEL,
        )
        sout_final = Group(annotation_bg, annotation)
        tin_raw = Text(
            text='numbers',
            **TEXT_EN_CONFIG,
        ).shift(DOWN*10)
        tout_final = Text(
            text='numbers',
            **TEXT_EN_CONFIG,
        ).shift(DOWN*10)
        
        ac_a1 = ArrowComment(False, DOWN).shift(LEFT*10).scale(0.6)
        ac_z9 = ArrowComment(False, UP).shift(RIGHT*10).scale(0.6)
        ac_game = ArrowComment(False, RIGHT).set_opacity(0.0)

        self.add(ac_game, annotation_bg, sin_raw)
        self.wait(wt)
        self.play(Write(
            annotation,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'split input and output',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            sin_raw, ac_game, sout_final,
        )
        mobs.generate_target()
        mobs.target.arrange(
            direction=RIGHT,
            # buff=1.0,
        ).scale(0.6)
        mobs.target[1].set_opacity(1.0)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait()
        
        # ************************************************************
        self.next_section(
            'introduce tile_input and tile_output',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            sin_raw, Mobject(), sout_final,
            ac_a1,   Mobject(), ac_z9,
            tin_raw, ac_game,  tout_final,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on image_raw',
            skip_animations=False,
        )
        # ************************************************************
        mobs.save_state()

        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        mobs.target.shift(-mobs.target[0].get_center())
        mobs.target[0].scale_to_fit_height(J000_IMAGE_HEIGHT)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        export_mobs(__file__, mobs, 'a')     # NOTE: used by 005

        mobs = Group(
            sin_raw,
        )
        export_mobs(__file__, mobs, 'b')     # NOTE: used by 001
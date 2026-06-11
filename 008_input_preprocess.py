from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.image_pad import ImagePad
from utils.image_raw import ImageRaw
from utils.show_shape import ShowShape, HideShape

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init from previous',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('007')
        (
            sin_raw, tin_raw,
        ) = mobs

        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'resize sin_raw from intuition view',
            skip_animations=False,
        )
        # ************************************************************
        sin_resize = sin_raw.copy()     # ImageRaw
        self.play(sin_resize.animate(
            run_time=wt,
        ).shift(RIGHT*5).scale(2/3))        # TODO, constant offset and sf?
        sin_resize.width_nominal = 640
        sin_resize.height_nominal = 360
        self.wait(wt)

        # show shapes of step input and output
        self.play(AnimationGroup(
            ShowShape(sin_raw, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(sin_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'resize tin_raw from tensor view',
            skip_animations=False,
        )
        # ***********************************************************
        tin_resize = tin_raw.copy()
        # self.play(tin_resize.animate(
        #     run_time=wt,
        # ).shift(RIGHT*5).scale(2/3))
        # separate scale thus gap kept
        tin_resize.generate_target()
        tin_resize.target.shift(RIGHT*5)
        for rect in tin_resize.target.rects:
            rect.scale(2/3)
        self.play(MoveToTarget(
            tin_resize,
            run_time=wt,
        ))
        tin_resize.width_nominal = 640
        tin_resize.height_nominal = 360
        self.wait(wt)

        # show shapes of step input and output
        self.play(AnimationGroup(
            ShowShape(tin_raw, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tin_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean shapes and make room in the right',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in 
              (sin_raw, tin_raw, sin_resize, tin_resize)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            sin_raw.animate.shift(LEFT*2.0),        # FIXME: manual offset
            tin_raw.animate.shift(LEFT*2.0),
            sin_resize.animate.set_x(0),
            tin_resize.animate.set_x(0),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'pad sin_resize in intuition view',
            skip_animations=False,
        )
        # ************************************************************
        # make a copy of resized image
        sin_pad = ImagePad(
            image_raw=sin_resize.copy(),
            padded=False,
        )
        self.play(sin_pad.animate(
            run_time=wt,
        ).shift(RIGHT*4))       # TODO: constant offset?
        self.wait(wt)

        # generate paddings for the copy
        self.play(sin_pad.show_natural_paddings(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes for intuition series
        self.play(AnimationGroup(
            ShowShape(sin_raw, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(sin_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(sin_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'pad tin_resize in tensor view',
            skip_animations=False,
        )
        # ************************************************************
        # make a copy of resized tensor
        tin_pad = tin_resize.copy()
        self.play(tin_pad.animate(
            run_time=wt,
        ).shift(RIGHT*4))       # TODO: constant offset?
        self.wait(wt)

        # generate paddings for the copy
        self.play(tin_pad.stretch_to_fit_square(
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes for tensor view
        self.play(AnimationGroup(
            ShowShape(tin_raw, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tin_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tin_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean shapes and make room in the right',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in 
              (sin_raw, tin_raw, sin_resize, tin_resize, sin_pad, tin_pad)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = Group(
            sin_raw, sin_resize, sin_pad,
            tin_raw, tin_resize, tin_pad, 
        )
        self.play(mobs.animate(
            lag_ratio=0.0,
            run_time=wt,
        ).scale(0.8).shift(LEFT*1.5))       # FIXME: manual offset
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'implicit new norm in tensor view',
            skip_animations=False,
        )
        # ************************************************************
        # make a copy of pad tensor
        tin_norm = tin_pad.copy()
        self.play(tin_norm.animate(
            run_time=wt,
        ).shift(RIGHT*3))
        self.wait(wt)

        # show shapes for tensor view
        self.play(AnimationGroup(
            ShowShape(tin_raw, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tin_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tin_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tin_norm, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'implicit new norm in intuition view',
            skip_animations=False,
        )
        # ************************************************************
        # make a copy of pad image
        sin_norm = sin_pad.copy()
        self.play(sin_norm.animate(
            run_time=wt,
        ).shift(RIGHT*3))
        self.wait(wt)

        # show shapes for intuition view
        self.play(AnimationGroup(
            ShowShape(sin_raw, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(sin_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(sin_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(sin_norm, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean shapes and export',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in 
              (sin_raw, tin_raw, sin_resize, tin_resize, sin_pad, tin_pad, sin_norm, tin_norm)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = Group(
            sin_raw, sin_resize, sin_pad, sin_norm,
            tin_raw, tin_resize, tin_pad, tin_norm,
        )
        export_mobs(__file__, mobs)     # NOTE: used by 010
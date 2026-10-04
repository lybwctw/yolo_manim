from manim import *
from utils.constants import *

from utils.general import import_mobs, export_mobs
from utils.yolo_annotation import YoloAnnotation
from utils.arrow_comment import ArrowComment
from utils.layers_fake import LayersFake
from utils.show_shape import ShowShape, HideShape

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init partially from previous',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('000')
        (
            iv_input, iv_output,
            ac_left, ac_right,
            _tv_input, ac_game, tv_output,
        ) = mobs

        ac_mobs = VGroup(
            ac_left, ac_right, ac_game,
        )

        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce tensor for raw input',
            skip_animations=False,
        )
        # ************************************************************
        # real time tensor size
        tv_input = LayersFake(
            n=3,
            ref=iv_input,
            width_nominal=960,
            height_nominal=540,
            buff=0.05,
            expanded=False,
        ).scale(1.0).shift(DOWN*10).set_x(iv_input.get_x())

        # replace abstract numbers with tensor
        mobs = Group(
            iv_input, Mobject(), iv_output,
            ac_left, Mobject(), ac_right,
            tv_input, ac_game, tv_output,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).scale(1.0).center()
        self.play(AnimationGroup(
            MoveToTarget(mobs),
            _tv_input.animate.shift(LEFT*10),
            run_time=wt,
        ))
        self.play(tv_input.expand(
            run_time=wt,
        ))
        self.wait(wt)

        # prepare for show shape
        ac_mobs.save_state()
        self.play(ac_mobs.animate(
            run_time=wt,
        ).fade(0.8))

        # show shape on both image and tensor
        self.play(AnimationGroup(
            *(ShowShape(
                mob,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
                aargs={'run_time': wt},
            ) for mob in (iv_input, tv_input)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shape on both image and tensor
        self.play(AnimationGroup(
            *(HideShape(
                mob,
                aargs={'run_time': wt},
            ) for mob in (iv_input, tv_input)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # get back those faded
        self.play(ac_mobs.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on annotation representation',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'focus on annotation representation',
            skip_animations=False,
        )
        # ************************************************************
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        mobs.target.shift(-mobs.target[2].get_center())
        mobs.target[2].scale_to_fit_width(config.frame_width/2)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = Group(
            iv_output,
        )
        export_mobs(__file__, mobs)
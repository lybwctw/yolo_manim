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
        mobs = import_mobs('000', 'a')
        (
            sin_raw,        _, sout_final,
            ac_a1,          _, ac_z9,
            _tin_raw, ac_game, tout_final,
        ) = mobs

        ac_mobs = VGroup(
            ac_a1, ac_z9, ac_game,
        )

        # ************************************************************
        self.next_section(
            'from focused raw to big map',
            skip_animations=False,
        )
        # ************************************************************
        self.add(mobs)
        self.wait(wt)

        # animate.restore failed
        self.play(Transform(
            mobs,
            mobs.saved_state,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce tensor for raw input',
            skip_animations=False,
        )
        # ************************************************************
        # real time tensor size
        tin_raw = LayersFake(
            n=3,
            ref=sin_raw,
            width_nominal=960,
            height_nominal=540,
            buff=0.12,
            expanded=False,
        ).scale(0.95).shift(DOWN*10)

        # replace abstract numbers with tensor
        mobs = Group(
            sin_raw, Mobject(), sout_final,
            ac_a1,   Mobject(), ac_z9,
            tin_raw, ac_game,   tout_final,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).scale(0.8).center()
        self.play(AnimationGroup(
            MoveToTarget(mobs),
            _tin_raw.animate.shift(LEFT*10),
            run_time=wt,
        ))
        self.play(tin_raw.expand(
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
            ) for mob in (sin_raw, tin_raw)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shape on both image and tensor
        self.play(AnimationGroup(
            *(HideShape(
                mob,
                aargs={'run_time': wt},
            ) for mob in (sin_raw, tin_raw)),
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
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        mobs.target.shift(-mobs.target[2].get_center())
        mobs.target[2].scale_to_fit_height(J005_ANNO_HEIGHT)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        export_mobs(__file__, mobs)
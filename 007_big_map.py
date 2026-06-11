from manim import *
from utils.constants import *
from utils.arrow_comment import ArrowComment
from utils.general import import_mobs, export_mobs
from utils.show_shape import ShowShape, HideShape
from utils.layers_fake import LayersFake
from utils.image_raw import ImageRaw

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init partially from previous',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('006')
        (
            sout_final, tout_final,
        ) = mobs

        # init the rest of map based on loaded
        sin_raw = sout_final[0].copy().move_to(LEFT*10)
        sin_raw.image.set_opacity(1.0)      # can't change opacity directly

        tin_raw = LayersFake(
            ref=sin_raw,
            width_nominal=960,
            height_nominal=540,
            buff=0.12,              # TODO: buff constants?
            expanded=True,
        ).scale(0.95).move_to(LEFT*10)

        ac_a1 = ArrowComment(False, DOWN).move_to(LEFT*10).scale(0.8)
        ac_z9 = ArrowComment(False, UP).move_to(RIGHT*10).scale(0.8)
        ac_game = ArrowComment(False, RIGHT).move_to(DOWN*10).scale(0.8)

        # for reference
        ac_all = VGroup(
            ac_a1, ac_z9, ac_game
        )

        # show starting mobs
        self.add(mobs)
        self.wait(wt)

        # ***********************************************************
        self.next_section(
            'back to big map',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            sin_raw, Mobject(), sout_final,
            ac_a1,   Mobject(), ac_z9,
            tin_raw, ac_game,   tout_final,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=0.6,
        ).scale(0.55).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show tensor shapes',
            skip_animations=False,
        )
        # ************************************************************
        # fade arrows to make scene cleaner
        ac_all.save_state()
        self.play(ac_all.animate(
            run_time=wt,
        ).fade(0.8))

        # show shapes
        self.play(AnimationGroup(
            ShowShape(
                tin_raw,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            ),
            ShowShape(
                tout_final,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            ),
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            HideShape(tin_raw),
            HideShape(tout_final),
            run_time=wt,
        ))
        self.wait(wt)

        # restore arrows
        self.play(ac_all.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through different maps',
            skip_animations=False,
        )
        # ************************************************************
        # TODO....

        # ************************************************************
        self.next_section(
            'focus on input of both views',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            sout_final.animate.shift(RIGHT*10),
            ac_a1.animate.shift(LEFT*10),
            ac_z9.animate.shift(RIGHT*10),
            ac_game.animate.shift(RIGHT*10),
            tout_final.animate.shift(RIGHT*10),
            run_time=wt,
        ))
        self.wait(wt)

        mobs = Group(
            sin_raw, tin_raw,
        )
        export_mobs(__file__, mobs)     # NOTE: used by 008
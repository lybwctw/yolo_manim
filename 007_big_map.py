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
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('005')
        (
            iv_input, iv_output,
            ac_left, ac_right,
            tv_input, ac_game, _tv_output,
        ) = mobs

        ac_all = VGroup(
            ac_left, ac_game, ac_right,
        )

        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'replace text result with tensor',
            skip_animations=False,
        )
        # ************************************************************
        # prepare assets
        tv_output = LayersFake(
            n=1,
            width=0.5,
            height=1.5,
            width_nominal=5,
            height_nominal='n',
            buff=0.12,      # useless
            expanded=True,
        ).shift(DOWN*10).set_x(iv_output.get_x())

        # replace abstract values with tensor
        self.play(AnimationGroup(
            tv_output.animate.next_to(
                ac_right, DOWN,
                buff=0.6,
            ),
            _tv_output.animate.shift(
                RIGHT*10,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        # mobs = Group(
        #     iv_input, Mobject(), iv_output,
        #     ac_left, Mobject(), ac_right,
        #     tv_input, ac_game, tv_output,
        # )
        # mobs.generate_target()
        # mobs.target.arrange_in_grid(
        #     rows=3,
        #     cols=3,
        #     # buff=1.0,
        # ).scale(1.0).center()
        # self.play(AnimationGroup(
        #     MoveToTarget(mobs),
        #     _tv_output.animate.shift(RIGHT*10),
        #     run_time=wt,
        # ))
        # self.wait(wt)

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
                tv_input,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            ),
            ShowShape(
                tv_output,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            ),
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            HideShape(tv_input),
            HideShape(tv_output),
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
            'loop through frames',
            skip_animations=False,
        )
        # ************************************************************
        # TODO

        # ************************************************************
        self.next_section(
            'export',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            iv_input, iv_output,
            ac_left, ac_right,
            tv_input, ac_game, tv_output,
        )
        export_mobs(__file__, mobs)
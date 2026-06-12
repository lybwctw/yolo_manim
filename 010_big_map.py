from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.layers_fake import LayersFake
from utils.show_shape import ShowShape, HideShape

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init partially from previous',
            skip_animations=True,
        )
        # ************************************************************
        # input series
        mobs = import_mobs('008')
        (
            sin_raw, sin_resize, sin_pad, sin_norm,
            tin_raw, tin_resize, tin_pad, tin_norm,
        ) = mobs

        # output series
        annotation_bg = sin_raw.copy().fade(0.7)
        annotation = YoloAnnotation(
            background=annotation_bg,
            annotation=PATH_LABEL,
        )
        sout_final = Group(annotation_bg, annotation).move_to(RIGHT*10)
        tout_final = LayersFake(
            n=1,
            width=0.6,
            height=1.0,
            width_nominal=5,
            height_nominal='n',
            # buff=0.12,      # useless
            expanded=True,
        ).shift(RIGHT*10)

        # not added, for reference
        ac_ref_right = ArrowComment(False, RIGHT).scale(0.4)
        ac_ref_down = ArrowComment(True, DOWN).scale(0.4)
        ac_ab, ac_bc, ac_cd = (
            ac_ref_right.copy().move_to(UP*20),
            ac_ref_right.copy().move_to(UP*20),
            ac_ref_right.copy().move_to(UP*20),
        )
        ac_12, ac_23, ac_34 = (
            ac_ref_right.copy().move_to(DOWN*20),
            ac_ref_right.copy().move_to(DOWN*20),
            ac_ref_right.copy().move_to(DOWN*20),
        )
        ac_game = ac_ref_right.copy().move_to(DOWN*20).set_color(PURE_RED)
        ac_a1, ac_b2, ac_c3, ac_d4, ac_z9 = (
            ac_ref_down.copy().move_to(LEFT*20),
            ac_ref_down.copy().move_to(LEFT*20),
            ac_ref_down.copy().move_to(LEFT*20),
            ac_ref_down.copy().move_to(LEFT*20),
            ac_ref_down.copy().move_to(RIGHT*20),
        )

        ac_all = VGroup(
            ac_ab, ac_bc, ac_cd,
            ac_a1, ac_b2, ac_c3, ac_d4, ac_z9,
            ac_12, ac_23, ac_34, ac_game,
        )

        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            'back to big map, including arrows',
            skip_animations=True,
        )
        # ************************************************************
        mobs = Group(
            sin_raw, ac_ab,     sin_resize, ac_bc,     sin_pad, ac_cd,     sin_norm, Mobject(), sout_final,
            ac_a1,   Mobject(), ac_b2,      Mobject(), ac_c3,   Mobject(), ac_d4,    Mobject(), ac_z9,
            tin_raw, ac_12,     tin_resize, ac_23,     tin_pad, ac_34,     tin_norm, ac_game,   tout_final,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=9,
            # buff=0.1,
        ).scale(0.8)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show shapes of all tensor',
            skip_animations=True,
        )
        # ************************************************************
        # fade arrows
        ac_all.save_state()
        self.play(ac_all.animate(
            rum_time=wt,
        ).fade(0.8))        # TODO: make 0.8 one of fade constants

        # show shapes
        self.play(AnimationGroup(
            *(ShowShape(mob, text_config=SMALL_SHAPE_TEXT_CONFIG)
             for mob in (
                sin_raw, sin_resize, sin_pad, sin_norm,
                tin_raw, tin_resize, tin_pad, tin_norm, tout_final,
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in (
                sin_raw, sin_resize, sin_pad, sin_norm,
                tin_raw, tin_resize, tin_pad, tin_norm, tout_final,
             )),
            lag_ratio=0.5,
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
            'simplify preprocess steps',
            skip_animations=False,
        )
        # ************************************************************
        mobs_up = Group(ac_ab, sin_resize, ac_bc, sin_pad, ac_cd)
        mobs_mid = VGroup(ac_b2, ac_c3)
        mobs_down = Group(ac_12, tin_resize, ac_23, tin_pad, ac_34)

        aci_a = ac_ab.copy().move_to(UP*10)
        aci_1 = ac_12.copy().move_to(DOWN*10)

        mobs = Group(
            sin_raw, aci_a,     sin_norm, Mobject(), sout_final,
            ac_a1,   Mobject(), ac_d4,    Mobject(), ac_z9,
            tin_raw, aci_1,     tin_norm, ac_game,   tout_final,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=5,
            # buff=0.3,
        ).center().scale(1.3)

        # tweak position of new arrows
        aci_a.align_to(mobs.target[1], LEFT)
        aci_1.align_to(mobs.target[11], LEFT)

        # replace multiple preprocess steps with one
        self.play(AnimationGroup(
            MoveToTarget(
                mobs,
                run_time=wt,
            ),
            mobs_up.animate.shift(UP*10),
            mobs_down.animate.shift(DOWN*10),
            Unwrite(mobs_mid),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        export_mobs(__file__, mobs)         # NOTE: used by 011

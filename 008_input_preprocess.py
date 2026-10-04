from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.image_pad import ImagePad
from utils.image_raw import ImageRaw
from utils.show_shape import ShowShape, HideShape
from utils.arrow_comment import ArrowComment

SESSION_SCALE_1 = 0.7
SESSION_SCALE_2 = 0.8

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        mobs = import_mobs('007')
        (
            iv_input, iv_output,
            ac_left, ac_right,
            tv_input, ac_game, tv_output,
        ) = mobs

        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on input of both views',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(mob.animate.shift(RIGHT*10) for mob in (
                iv_output, ac_right, ac_game, tv_output,
            )),
            ac_left.animate.shift(LEFT*10),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'resize iv_input from intuition view',
            skip_animations=True,
        )
        # ************************************************************
        iv_resize = iv_input.copy()     # ImageRaw
        self.play(iv_resize.animate(
            run_time=wt,
        ).shift(RIGHT*5).scale(2/3))        # TODO, constant offset and sf?
        iv_resize.width_nominal = 640
        iv_resize.height_nominal = 360
        self.wait(wt)

        # show shapes of step input and output
        self.play(AnimationGroup(
            ShowShape(iv_input, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(iv_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'resize tv_input from tensor view',
            skip_animations=True,
        )
        # ***********************************************************
        tv_resize = tv_input.copy()
        tv_resize.generate_target()
        tv_resize.target.shift(RIGHT*5)
        for rect in tv_resize.target.rects:
            rect.scale(2/3)
        self.play(MoveToTarget(
            tv_resize,
            run_time=wt,
        ))
        tv_resize.width_nominal = 640
        tv_resize.height_nominal = 360
        self.wait(wt)

        # show shapes of step input and output
        self.play(AnimationGroup(
            ShowShape(tv_input, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tv_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean shapes and make room in the right',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in 
              (iv_input, tv_input, iv_resize, tv_resize)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            iv_input.animate.shift(LEFT*2.0),        # FIXME: manual offset
            tv_input.animate.shift(LEFT*2.0),
            iv_resize.animate.set_x(0),
            tv_resize.animate.set_x(0),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'pad iv_resize in intuition view',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of resized image
        iv_pad = ImagePad(
            image_raw=iv_resize.copy(),
            padded=False,
        )
        self.play(iv_pad.animate(
            run_time=wt,
        ).shift(RIGHT*4))       # TODO: constant offset?
        self.wait(wt)

        # generate paddings for the copy
        self.play(iv_pad.show_natural_paddings(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes for intuition series
        self.play(AnimationGroup(
            ShowShape(iv_input, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(iv_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(iv_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'pad tv_resize in tensor view',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of resized tensor
        tv_pad = tv_resize.copy()
        self.play(tv_pad.animate(
            run_time=wt,
        ).shift(RIGHT*4))       # TODO: constant offset?
        self.wait(wt)

        # generate paddings for the copy
        self.play(tv_pad.stretch_to_fit_square(
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes for tensor view
        self.play(AnimationGroup(
            ShowShape(tv_input, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tv_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tv_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean shapes and make room in the right',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in 
              (iv_input, tv_input, iv_resize, tv_resize, iv_pad, tv_pad)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = Group(
            iv_input, iv_resize, iv_pad,
            tv_input, tv_resize, tv_pad, 
        )
        self.play(mobs.animate(
            lag_ratio=0.0,
            run_time=wt,
        ).scale(SESSION_SCALE_1).shift(LEFT*1.2))       # FIXME: manual offset
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'implicit new norm in tensor view',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of pad tensor
        tv_norm = tv_pad.copy()
        self.play(tv_norm.animate(
            run_time=wt,
        ).shift(RIGHT*3))
        self.wait(wt)

        # show shapes for tensor view
        self.play(AnimationGroup(
            ShowShape(tv_input, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tv_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tv_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(tv_norm, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'implicit new norm in intuition view',
            skip_animations=True,
        )
        # ************************************************************
        # make a copy of pad image
        iv_norm = iv_pad.copy()
        self.play(iv_norm.animate(
            run_time=wt,
        ).shift(RIGHT*3))
        self.wait(wt)

        # show shapes for intuition view
        self.play(AnimationGroup(
            ShowShape(iv_input, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(iv_resize, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(iv_pad, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(iv_norm, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean shapes',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in 
              (iv_input, tv_input, iv_resize, tv_resize, iv_pad, tv_pad, iv_norm, tv_norm)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'prepare assets for big map',
            skip_animations=True,
        )
        # ************************************************************
        iv_output.scale(SESSION_SCALE_1)
        tv_output.scale(SESSION_SCALE_1)

        ac_ref_lr = ArrowComment(False, RIGHT).scale(0.3)
        ac_ref_ud = ArrowComment(True, DOWN).scale(0.3)
        ac_ab, ac_bc, ac_cd = (
            ac_ref_lr.copy().move_to(UP*20),
            ac_ref_lr.copy().move_to(UP*20),
            ac_ref_lr.copy().move_to(UP*20),
        )
        ac_12, ac_23, ac_34 = (
            ac_ref_lr.copy().move_to(DOWN*20),
            ac_ref_lr.copy().move_to(DOWN*20),
            ac_ref_lr.copy().move_to(DOWN*20),
        )
        ac_game = ac_ref_lr.copy().move_to(DOWN*20).set_color(PURE_RED)
        ac_a1, ac_b2, ac_c3, ac_d4, ac_z9 = (
            ac_ref_ud.copy().move_to(LEFT*20),
            ac_ref_ud.copy().move_to(LEFT*20),
            ac_ref_ud.copy().move_to(LEFT*20),
            ac_ref_ud.copy().move_to(LEFT*20),
            ac_ref_ud.copy().move_to(RIGHT*20),
        )
        ac_all = VGroup(
            ac_ab, ac_bc, ac_cd,
            ac_a1, ac_b2, ac_c3, ac_d4, ac_z9,
            ac_12, ac_23, ac_34, ac_game,
        )

        # ************************************************************
        self.next_section(
            'back to big map',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            iv_input, ac_ab,     iv_resize, ac_bc,     iv_pad,  ac_cd,     iv_norm, Mobject(), iv_output,
            ac_a1,    Mobject(), ac_b2,     Mobject(), ac_c3,   Mobject(), ac_d4,   Mobject(), ac_z9,
            tv_input, ac_12,     tv_resize, ac_23,     tv_pad,  ac_34,     tv_norm, ac_game,   tv_output,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=9,
            # buff=0.1,
        ).scale(SESSION_SCALE_2).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'shapes on tensor view',
            skip_animations=False,
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
                tv_input, tv_resize, tv_pad, tv_norm, tv_output,
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape(mob) for mob in (
                tv_input, tv_resize, tv_pad, tv_norm, tv_output,
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
            'export',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            iv_input, ac_ab, iv_resize, ac_bc, iv_pad, ac_cd, iv_norm,          iv_output,
            ac_a1,           ac_b2,            ac_c3,         ac_d4,            ac_z9,
            tv_input, ac_12, tv_resize, ac_23, tv_pad, ac_34, tv_norm, ac_game, tv_output,
        )
        export_mobs(__file__, mobs)
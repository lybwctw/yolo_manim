from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.show_shape import ShowShape, HideShape

SESSION_SCALE_1 = 0.9
SESSION_SCALE_2 = 1.2

ARROW_CONFIG = {
    'buff': 0.0,
    'stroke_width': 2.0,
    'tip_length': 0.1,
}

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('008')
        (
            iv_input, aci_1, iv_resize, aci_2, iv_pad, aci_3, iv_norm,           iv_output,
            acm_1,           acm_2,            acm_3,         acm_4,             acm_9,
            tv_input, act_1, tv_resize, act_2, tv_pad, act_3, tv_norm, act_game, tv_output,
        ) = mobs

        self.add(mobs)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert scaled output before final output',
            skip_animations=False,
        )
        # ************************************************************
        iv_output_scaled = iv_output.copy().scale_to_fit_width(iv_norm.width)
        bg_scaled, anno_scaled = iv_output_scaled
        bg_scaled = ImagePad(
            image_raw=bg_scaled.set_opacity(1.0),
            width_nominal=640,
            height_nominal=360,
            padded=True,
        ).fade(0.7)             # TODO: make this a constant
        anno_scaled.background = bg_scaled
        iv_output_scaled = Group(bg_scaled, anno_scaled).move_to(UP*20)

        tv_output_scaled = tv_output.copy().move_to(DOWN*20)
        aci_9 = aci_1.copy().move_to(UP*20)
        act_9 = act_1.copy().move_to(DOWN*20)
        acm_8 = acm_9.copy().move_to(RIGHT*20)

        mobs = Group(
            iv_input, aci_1,     iv_resize, aci_2,     iv_pad, aci_3,     iv_norm, Mobject(), iv_output_scaled, aci_9,     iv_output,
            acm_1,    Mobject(), acm_2,     Mobject(), acm_3,  Mobject(), acm_4,   Mobject(), acm_8,            Mobject(), acm_9,
            tv_input, act_1,     tv_resize, act_2,     tv_pad, act_3,     tv_norm, act_game,  tv_output_scaled, act_9,     tv_output,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=11,
            # buff=0.3,
        ).center().scale(SESSION_SCALE_1)
        
        # insert scaled output
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            # rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show mini axes for scaled output and final output',
            skip_animations=False,
        )
        # ************************************************************
        origin_scaled = iv_output_scaled.get_corner(UL)
        width_scaled = iv_output_scaled.width
        height_scaled = iv_output_scaled.height
        origin_final = iv_output.get_corner(UL)
        width_final = iv_output.width
        height_final = iv_output.height

        axes_direct = VGroup(
            Arrow(
                start=origin_scaled,
                end=origin_scaled+(width_scaled+0.2)*RIGHT,
                **ARROW_CONFIG,
            ),
            Arrow(
                origin_scaled,
                origin_scaled+(height_scaled+0.1)*DOWN,
                **ARROW_CONFIG,
            ),
        )
        axes_final = VGroup(
            Arrow(
                start=origin_final,
                end=origin_final+(width_final+0.2)*RIGHT,
                **ARROW_CONFIG,
            ),
            Arrow(
                origin_final,
                origin_final+(height_final+0.1)*DOWN,
                **ARROW_CONFIG,
            ),
        )
        self.play(AnimationGroup(
            *(GrowArrow(arrow) for arrow in axes_direct),
            *(GrowArrow(arrow) for arrow in axes_final),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(AnimationGroup(
            Unwrite(axes_direct),
            Unwrite(axes_final),
            lag_ratio=0.0,
            run_time=wt,
        ))
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
            'simplified preprocess steps',
            skip_animations=False,
        )
        # ************************************************************
        mobs_up = Group(aci_1, iv_resize, aci_2, iv_pad)
        mobs_mid = VGroup(acm_2, acm_3)
        mobs_down = Group(act_1, tv_resize, act_2, tv_pad)

        mobs = Group(
            iv_input, aci_3,     iv_norm, Mobject(), iv_output_scaled, aci_9,     iv_output,
            acm_1,    Mobject(), acm_4,   Mobject(), acm_8,            Mobject(), acm_9,
            tv_input, act_3,     tv_norm, act_game,  tv_output_scaled, act_9,     tv_output,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=7,
            # buff=0.3,
        ).center().scale(SESSION_SCALE_2)

        # simplify animation
        self.play(AnimationGroup(
            MoveToTarget(
                mobs,
                run_time=wt,
            ),
            mobs_up.animate.shift(UP*20),
            mobs_down.animate.shift(DOWN*20),
            Unwrite(mobs_mid),
            lag_ratio=0.0,
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
            iv_input, aci_3, iv_norm,           iv_output_scaled, aci_9, iv_output,
            acm_1,           acm_4,             acm_8,                   acm_9,
            tv_input, act_3, tv_norm, act_game, tv_output_scaled, act_9, tv_output,
        )
        export_mobs(__file__, mobs)
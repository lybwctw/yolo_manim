from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.show_shape import ShowShape, HideShape

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
            'init from previous',
            skip_animations=False,
        )
        # new naming system for arrows:
        # aci -> arrow comment for intuition view
        # acm -> arrow comment in the mid
        # act -> arrow comment for tensor view
        # ************************************************************
        mobs = import_mobs('010')
        (
            sin_raw, aci_1, sin_norm, _,        sout_final,
            acm_1,   _,     acm_2,    _,        acm_9,
            tin_raw, act_1, tin_norm, act_game, tout_final,
        ) = mobs
        
        # sout_direct = sin_norm.copy().move_to(UP*5)
        sout_direct = sout_final.copy().scale_to_fit_width(sin_norm.width)
        direct_bg, direct_anno = sout_direct
        direct_bg = ImagePad(
            image_raw=direct_bg.set_opacity(1.0),
            width_nominal=640,
            height_nominal=360,
            padded=True,
        ).fade(0.7)             # TODO: make this a constant
        direct_anno.background = direct_bg
        sout_direct = Group(direct_bg, direct_anno).move_to(UP*5)

        tout_direct = tout_final.copy().move_to(DOWN*5)
        aci_9 = aci_1.copy().move_to(UP*5)
        act_9 = act_1.copy().move_to(DOWN*5)
        acm_8 = acm_9.copy().move_to(RIGHT*5)

        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            'insert direct output before final output',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            sin_raw, aci_1,     sin_norm, Mobject(), sout_direct, aci_9,     sout_final,
            acm_1,   Mobject(), acm_2,    Mobject(), acm_8,       Mobject(), acm_9,
            tin_raw, act_1,     tin_norm, act_game,  tout_direct, act_9,     tout_final,
        )

        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=7,
            # buff=0.3,
        ).center().scale(0.9)
        
        # tweak position of new mobs
        sout_direct.align_to(mobs.target[4], LEFT)
        aci_9.align_to(mobs.target[5], LEFT)
        tout_direct.align_to(mobs.target[18], LEFT)
        act_9.align_to(mobs.target[19], LEFT)

        # insert direct output without annotation
        # NOTE: first time bouncy effect
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show mini axes for direct output and final output',
            skip_animations=False,
        )
        # ************************************************************
        origin_direct = sout_direct.get_corner(UL)
        width_direct = sout_direct.width
        height_direct = sout_direct.height
        origin_final = sout_final.get_corner(UL)
        width_final = sout_final.width
        height_final = sout_final.height

        axes_direct = VGroup(
            Arrow(
                start=origin_direct,
                end=origin_direct+(width_direct+0.2)*RIGHT,
                **ARROW_CONFIG,
            ),
            Arrow(
                origin_direct,
                origin_direct+(height_direct+0.1)*DOWN,
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
            'loop through frames and back',
            skip_animations=False,
        )
        # ************************************************************
        # TODO... loop

        # TODO: start with correct answer
        # build raw outputs based including answers
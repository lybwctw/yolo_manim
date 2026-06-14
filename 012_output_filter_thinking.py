from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation, random_sano_copy
from utils.repad_background import RepadBackground
from utils.show_shape import ShowShape, HideShape

import random

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('011')
        (
            sin_raw, aci_1, sin_norm, _,        sout_pp, aci_9, sout_final,
            acm_1,   _,     acm_2,    _,        acm_8,   _,     acm_9,
            tin_raw, act_1, tin_norm, act_game, tout_pp, act_9, tout_final,
        ) = mobs

        # TODO: make 5 constant variable?
        sout_direct = sout_pp.copy().move_to(UP*5)
        tout_direct = tout_pp.copy().move_to(DOWN*5)
        aci_8 = aci_9.copy().move_to(UP*5)
        act_8 = act_9.copy().move_to(DOWN*5)
        acm_7 = acm_8.copy().move_to(RIGHT*5)

        ac_all = VGroup(
            aci_1, aci_8, aci_9,
            acm_1, acm_2, acm_7, acm_8, acm_9,
            act_1, act_game, act_8, act_9,
        )

        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            'insert a copy of direct output',
            skip_animations=False,
        )
        # ************************************************************
        mobs = Group(
            sin_raw, aci_1,     sin_norm, Mobject(), sout_direct, aci_8,     sout_pp, aci_9,     sout_final,
            acm_1,   Mobject(), acm_2,    Mobject(), acm_7,       Mobject(), acm_8,   Mobject(), acm_9,
            tin_raw, act_1,     tin_norm, act_game,  tout_direct, act_8,     tout_pp, act_9,     tout_final,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=9,
            # buff=0.3,
        ).center().scale(0.9)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert a lot of random predictions in direct output',
            skip_animations=False,
        )
        # ************************************************************
        # update in intuition view
        sanos_ref = sout_direct[1].mobs
        sanos_new = VGroup()
        for _ in range(100):
            sano_ref = random.choice(sanos_ref)
            sano_new = random_sano_copy(
                sano=sano_ref,
                background=sout_direct[0],
                range_w=[0.1, 0.4],
                range_h=[0.1, 0.3],
            )
            sanos_new.add(sano_new)

        self.play(Write(
            sanos_new,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # update in tensor view
        self.play(AnimationGroup(
            tout_direct.animate(
                run_time=wt,
            ).stretch_to_fit_height(
                tout_direct.height*1.5,
            ),
            tout_pp.animate(
                run_time=wt,
            ).stretch_to_fit_height(
                tout_direct.height*0.7,
            ),
            tout_final.animate(
                run_time=wt,
            ).stretch_to_fit_height(
                tout_direct.height*0.7,
            ),
        ))
        tout_direct.height_nominal = '?' # unknown direct number
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'append random conf for all ylabels',
            skip_animations=False,
        )
        # ************************************************************
        # append conf for labels in direct output
        confs_new = [f'{random.random():.2f}' for _ in range(len(sanos_new))]
        confs_ref = [f'{random.random():.2f}' for _ in range(len(sanos_ref))]
        sanos_pp = sout_pp[1].mobs
        sanos_final = sout_final[1].mobs
        self.play(AnimationGroup(
            *(sano.label.update_text(
                text=sano.label.text + ' ' + conf,
            ) for sano, conf in zip(sanos_new, confs_new)),
            *(sano.label.update_text(
                text=sano.label.text + ' ' + conf,
            ) for sano, conf in zip(sanos_ref, confs_ref)),
            lag_ratio=0.1,
            run_time=wt,
        ))
        self.wait(wt)

        # append conf for labels in pp output and final output
        self.play(AnimationGroup(
            *(sano.label.update_text(
                text=sano.label.text + ' ' + conf,
            ) for sano, conf in zip(sanos_pp, confs_ref)),
            *(sano.label.update_text(
                text=sano.label.text + ' ' + conf,
            ) for sano, conf in zip(sanos_final, confs_ref)),
            lag_ratio=0.1,
            run_time=wt,
        ))
        self.wait(wt)

        # make output tensors wider
        self.play(AnimationGroup(
            tout_direct.animate.stretch_to_fit_width(
                tout_direct.width+0.1,
            ),
            tout_pp.animate.stretch_to_fit_width(
                tout_pp.width+0.1,
            ),
            tout_final.animate.stretch_to_fit_width(
                tout_final.width+0.1,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        tout_direct.width_nominal = 6
        tout_pp.width_nominal = 6
        tout_final.width_nominal = 6
        self.wait(wt)

        # show shapes for all tensors again
        ac_all.save_state()
        self.play(ac_all.animate(
            lag_ratio=0.5,
            run_time=wt,
        ).fade(0.8))
        self.wait(wt)
        self.play(AnimationGroup(
            ShowShape(tin_raw, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tin_norm, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tout_direct, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tout_pp, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tout_final, text_config=SMALL_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            HideShape(tin_raw),
            HideShape(tin_norm),
            HideShape(tout_direct),
            HideShape(tout_pp),
            HideShape(tout_final),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        # NOTE: ignoring arrows is better
        # self.play(ac_all.animate(
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ).restore())
        # self.wait(wt)

        # NOTE: mobs not used by following scenes
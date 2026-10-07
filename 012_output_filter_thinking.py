from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation, random_sano_copy
from utils.repad_background import RepadBackground
from utils.show_shape import ShowShape, HideShape

import random

SESSION_SCALE = 0.9

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
            iv_input, aci_1, iv_norm,           iv_output_scaled, aci_9, iv_output,
            acm_1,           acm_2,             acm_8,                   acm_9,
            tv_input, act_1, tv_norm, act_game, tv_output_scaled, act_9, tv_output,
        ) = mobs

        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            'insert unfiltered output before scaled output',
            skip_animations=False,
        )
        # ************************************************************
        iv_output_unfiltered = iv_output_scaled.copy().move_to(UP*20)
        tv_otuput_unfiltered = tv_output_scaled.copy().move_to(DOWN*20)
        aci_8 = aci_9.copy().move_to(UP*20)
        act_8 = act_9.copy().move_to(DOWN*20)
        acm_7 = acm_8.copy().move_to(RIGHT*20)

        ac_all = VGroup(
            aci_1, aci_8, aci_9,
            acm_1, acm_2, acm_7, acm_8, acm_9,
            act_1, act_game, act_8, act_9,
        )

        mobs = Group(
            iv_input, aci_1,     iv_norm, Mobject(), iv_output_unfiltered, aci_8,     iv_output_scaled, aci_9,     iv_output,
            acm_1,    Mobject(), acm_2,   Mobject(), acm_7,                Mobject(), acm_8,            Mobject(), acm_9,
            tv_input, act_1,     tv_norm, act_game,  tv_otuput_unfiltered, act_8,     tv_output_scaled, act_9,     tv_output,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=9,
            # buff=0.3,
        ).center().scale(SESSION_SCALE)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            # rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'random extra sanos for unfiltered output',
            skip_animations=False,
        )
        # ************************************************************
        # update in intuition view
        sanos_ref = iv_output_unfiltered[1].mobs
        sanos_new = VGroup()
        for _ in range(100):
            sano_ref = random.choice(sanos_ref)
            sano_new = random_sano_copy(
                sano=sano_ref,
                background=iv_output_unfiltered[0],
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
            tv_otuput_unfiltered.animate(
                run_time=wt,
            ).stretch_to_fit_height(
                tv_otuput_unfiltered.height*1.5,
            ).stretch_to_fit_width(
                tv_otuput_unfiltered.width*1.5,
            ),
            tv_output_scaled.animate(
                run_time=wt,
            ).stretch_to_fit_height(
                tv_otuput_unfiltered.height*0.7,
            ),
            tv_output.animate(
                run_time=wt,
            ).stretch_to_fit_height(
                tv_otuput_unfiltered.height*0.7,
            ),
        ))
        tv_otuput_unfiltered.width_nominal = '?' # unknown output width
        tv_otuput_unfiltered.height_nominal = '?' # unknown output height
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'append random conf for all ylabels',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # append conf for labels in direct output
        # confs_new = [f'{random.random():.2f}' for _ in range(len(sanos_new))]
        # confs_ref = [f'{random.random():.2f}' for _ in range(len(sanos_ref))]
        # sanos_pp = iv_output_scaled[1].mobs
        # sanos_final = iv_output[1].mobs
        # self.play(AnimationGroup(
        #     *(sano.label.update_text(
        #         text=sano.label.text + ' ' + conf,
        #     ) for sano, conf in zip(sanos_new, confs_new)),
        #     *(sano.label.update_text(
        #         text=sano.label.text + ' ' + conf,
        #     ) for sano, conf in zip(sanos_ref, confs_ref)),
        #     lag_ratio=0.1,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # append conf for labels in pp output and final output
        # self.play(AnimationGroup(
        #     *(sano.label.update_text(
        #         text=sano.label.text + ' ' + conf,
        #     ) for sano, conf in zip(sanos_pp, confs_ref)),
        #     *(sano.label.update_text(
        #         text=sano.label.text + ' ' + conf,
        #     ) for sano, conf in zip(sanos_final, confs_ref)),
        #     lag_ratio=0.1,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # make output tensors wider
        # self.play(AnimationGroup(
        #     tv_otuput_unfiltered.animate.stretch_to_fit_width(
        #         tv_otuput_unfiltered.width+0.1,
        #     ),
        #     tv_output_scaled.animate.stretch_to_fit_width(
        #         tv_output_scaled.width+0.1,
        #     ),
        #     tv_output.animate.stretch_to_fit_width(
        #         tv_output.width+0.1,
        #     ),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # tv_otuput_unfiltered.width_nominal = 6
        # tv_output_scaled.width_nominal = 6
        # tv_output.width_nominal = 6
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'shapes of tensors',
            skip_animations=False,
        )
        # ************************************************************
        # fade arrows
        ac_all.save_state()
        self.play(ac_all.animate(
            lag_ratio=0.0,
            run_time=wt,
        ).fade(0.8))
        self.wait(wt)

        # show shapes
        self.play(AnimationGroup(
            ShowShape(tv_input, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tv_norm, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tv_otuput_unfiltered, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tv_output_scaled, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ShowShape(tv_output, text_config=SMALL_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            HideShape(tv_input),
            HideShape(tv_norm),
            HideShape(tv_otuput_unfiltered),
            HideShape(tv_output_scaled),
            HideShape(tv_output),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        
        # restore arrows
        self.play(ac_all.animate(
            lag_ratio=0.0,
            run_time=wt,
        ).restore())
        self.wait(wt)

        # # NOTE: mobs not used by following scenes
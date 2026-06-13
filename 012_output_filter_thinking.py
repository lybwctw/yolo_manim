from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation, random_sano_copy
from utils.repad_background import RepadBackground

import random

def random_rectangles_in_region(
    n,
    top_left,
    bottom_right,
    min_size=0.1,
    max_size=0.8,
):
    x_min, y_max, _ = top_left
    x_max, y_min, _ = bottom_right

    rects = VGroup()

    for _ in range(n):
        w = np.random.uniform(min_size, max_size)
        h = np.random.uniform(min_size, max_size)

        # sample center so rectangle stays inside
        cx = np.random.uniform(x_min + w/2, x_max - w/2)
        cy = np.random.uniform(y_min + h/2, y_max - h/2)

        rect = Rectangle(width=w, height=h, stroke_width=1.)
        rect.move_to([cx, cy, 0])

        rects.add(rect)

    return rects

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
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'focus on background_tmp',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # manager = Group(
        #     *[image_raw, ac_ab, image_repad, ac_bc, image_norm, VMobject(), background_tmp, annotation_repad, ac_yz,
        #       annotation_final],
        #     *[ac_a1, VMobject(), ac_b2, VMobject(), ac_c3, VMobject(), VMobject(), ac_y8, VMobject(), ac_z9],
        #     *[lf_image_raw, ac_12, lf_image_repad, ac_23, lf_image_norm, ac_game, lf_output_tmp, lf_output_repad, ac_89,
        #       lf_output_final],
        # )
        # manager.generate_target()
        # manager.target.arrange_in_grid(
        #     rows=3,
        #     cols=10,
        #     buff=10,
        # )
        # manager.target.shift(-manager.target[6].get_center())
        # manager.target[6].scale(6.0)
        # self.play(MoveToTarget(manager))
        # self.play(Unwrite(rects_tmp, lag_ratio=0))
        # background_tmp.remove(rects_tmp)
        # self.wait()

        # # ************************************************************
        # self.next_section(
        #     'save for next scene',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # everything = Group(
        #     background_tmp,
        # )
        # save_everything(S012_EVERYTHING, everything)
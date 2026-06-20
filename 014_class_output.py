from manim import *

from utils.arrow_comment import ArrowComment
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import YoloAnnotation
from utils.anchor_point import AnchorPoint
from utils.explainer import Explainer
from utils.general import export_mobs
from utils.layers_fake import LayersFake
from utils.show_shape import ShowShape, HideShape
from utils.constants import *

import random

# ---------------- anchor point related -------------------
AP_DOT_CONFIG_FOCUS = {
    'stroke_color': WHITE,
    'stroke_opacity': 1.0,
}
AP_DOT_CONFIG_OTHERS = {
    'stroke_color': GRAY,
    'stroke_opacity': 0.5,
}
AP_RECT_CONFIG_FOCUS = {
    'stroke_color': WHITE,
    'stroke_opacity': 1.0,
}
AP_RECT_CONFIG_OTHERS = {
    'stroke_color': GRAY,
    'stroke_opacity': 0.3,
    'stroke_width': 1.0,
}

# ---------------- explainer related -------------------

# ---------------- tensor related -------------------
# NOTE: same as 013
TENSOR_PROB_CONFIG = {
    'side_length': 0.15,
    'stroke_width': 2.0,
    'stroke_opacity': 1.0,
    'fill_opacity': 0.7,
}
TENSOR_PROB_2D_CONFIG = {
    'line_width': 0.3,
    'stroke_width': 1.0,
    'stroke_opacity': 1.0,
    'stroke_color': WHITE,
}
TENSOR_BUFF_RATIO = 0.5

# ---------------- util functions -------------------
def random_target(
    ap: AnchorPoint,
    annotation: YoloAnnotation,
):
    cands = []
    for box, cls in zip(annotation.get_boxes(), annotation.cls):
        if ap.inside_box(box):
            cands.append(cls)
    if len(cands) == 0:
        return None
    else:
        return random.choice(cands)

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init background and and explainer new',
            skip_animations=True,
        )
        # ************************************************************
        background = ImagePad(padded=True)
        background.scale(1.3)

        explainer = Explainer.from_file(
            background=background,
            version=32,
            sf_nominal=32,
        )

        annotation = YoloAnnotation(
            background=background.image,
            annotation=PATH_LABEL,
        )

        system = Group(background, explainer)
        self.add(system)
        self.wait(wt)

        self.play(background.animate(
            run_time=wt,
        ).set_opacity(0.2))
        self.wait(wt)

        # show shape as a first hint
        self.play(ShowShape(
            background,
            text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            aargs={'run_time': wt},
        ))
        self.wait(wt)
        self.play(HideShape(
            background,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'multiple prob prediction thinking',
            skip_animations=True,
        )
        # ************************************************************
        # show anchor points
        self.play(explainer.show_anchor_points(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # fade anchor points
        self.play(AnimationGroup(
            *(ap.mob.animate.set_style(
                stroke_opacity=0.0,
            ) for ap in explainer.anchor_points),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # show pbars based on anchor points
        self.play(explainer.show_pbars(
            random=True,
            pbar_config={},
            aargs={},
            gargs={'lag_ratio': 0.0, 'run_time': wt},
        ))
        self.wait(wt)

        # sync to random pbars multiple times
        for i in range(5):
            self.play(explainer.sync_pbars(
                random=True,
                pbar_config={},
                aargs={},
            gargs={'lag_ratio': 0.0, 'run_time': wt},
            ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'expected inside anchor point pbars',
            skip_animations=True,
        )
        # ************************************************************
        # hide pbars, back to anchor points
        self.play(AnimationGroup(
            explainer.hide_pbars(
                aargs={},
                gargs={'lag_ratio': 0.0},
            ),
            AnimationGroup(
                *(ap.mob.animate.set_style(
                    stroke_opacity=1.0,
                ) for ap in explainer.anchor_points),
                lag_ratio=0.0,
            ),
            run_time=wt,
        ))
        self.wait(wt)

        # show true annotation
        self.play(Write(
            annotation,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # focus on important anchor points
        aps_in, aps_out = explainer.collect_aps(
            func=lambda ap: any(ap.inside_box(box) for box in annotation.get_boxes()),
        )
        self.play(AnimationGroup(
            AnimationGroup(
                *(ap.mob.animate.set_style(
                    **AP_DOT_CONFIG_FOCUS,
                ) for ap in aps_in),
                lag_ratio=0,
                run_time=wt,
            ),
            AnimationGroup(
                *(ap.mob.animate.set_style(
                    **AP_DOT_CONFIG_OTHERS,
                ) for ap in aps_out),
                lag_ratio=0,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # hide labels and fade boxes
        self.play(AnimationGroup(
            *(label.animate.set_opacity(opacity=0)
                for label in annotation.get_labels()),
            *(box.animate.fade(0.5)
              for box in annotation.get_boxes()),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # FIXME: show EXPECTED pbars (use real ones?)
        self.play(AnimationGroup(
            *(AnimationGroup(
                ap.show_pbars(
                    random=True,
                    target=random_target(ap, annotation),
                    pbar_config={},
                ),
                ap.mob.animate.set_style(
                    stroke_opacity=0.0,
                )
            ) for ap in aps_in),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # clean up
        # FIXME: fade anchor points?
        self.play(AnimationGroup(
            *(AnimationGroup(
                ap.hide_pbars(),
                ap.to_dot(),
            ) for ap in aps_in),
            Unwrite(
                annotation,
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(ap.to_dot()
              for ap in explainer.anchor_points),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'prob: explainer to tensor',
            skip_animations=True,
        )
        # ************************************************************
        # scale and shift explainer
        self.play(system.animate(
            run_time=wt,
        ).scale(0.5).shift(UP*2))    # same as box counterpart
        self.wait(wt)

        # renaming
        system_prob = system
        background_prob = system_prob[0]
        explainer_prob = system_prob[1]

        # synced creation: probs + tensor
        tensor_prob = explainer_prob.create_tensor_prob(
            cell_config=TENSOR_PROB_CONFIG,
            buff_ratio=TENSOR_BUFF_RATIO,
        )
        tensor_prob.shift(DOWN*4)
        self.play(AnimationGroup(
            *(AnimationGroup(
                ap.show_pbars(
                    random=True,
                    pbar_config={},
                ),
                ap.mob.animate.set_style(
                    stroke_opacity=0.0,
                ),
                Write(series),
            ) for ap, series in zip(
                explainer_prob.anchor_points,
                tensor_prob,
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # TODO: show "annotation" on each layer of tensor?

        # ************************************************************
        self.next_section(
            'reshape prob tensor to 2d version',
            skip_animations=True,
        )
        # ************************************************************
        # make room for reshaped xyxy tensor
        self.play(AnimationGroup(
            system_prob.animate.shift(LEFT*1.5),
            tensor_prob.animate.shift(LEFT*1.5),
            run_time=wt,
        ))
        self.wait(wt)

        # create 2d version prob tenso
        tensor_prob_2d_target = explainer_prob.create_tensor_prob_2d(
            line_config=TENSOR_PROB_2D_CONFIG,
            w_buff_ratio=0.1,               # buff between rows
            h_buff_ratio=0.017,             # buff between cols
        ).move_to(RIGHT*3.0)

        # transform prob into prob_2d
        tensor_prob_2d = tensor_prob.copy()
        self.play(AnimationGroup(
            *(Transform(stack, row) for stack, row in zip(
                tensor_prob_2d, tensor_prob_2d_target
            )),
            lag_ratio=0.5,
            run_time=wt,                    # NOTE: make this long
            rate_func=rate_functions.ease_in_circ,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'simplify tensor_prob/tensor_prob_2d' \
            'into t32_prob/t32_prob_2dA',
            skip_animations=False,
        )
        # ************************************************************
        # replace tensor_prob with t32_prob
        t32_prob = LayersFake(
            n=len(tensor_prob[0]),
            ref=VGroup(tensor_prob[0][0], tensor_prob[-1][0]),
            expanded=True,
            buff=0.075,         # based on tensor_prob's buff
            width_nominal=20,
            height_nominal=20,
            depth_nominal=len(tensor_prob[0]),
            rect_config={},
        ).move_to(tensor_prob)
        self.play(AnimationGroup(
            Unwrite(tensor_prob),
            Write(t32_prob),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # replace tensor_prob_2d with t32_prob_2d
        t32_prob_2d = LayersFake(
            n=1,
            width=0.8,
            height=3.0,
            expanded=True,
            # buff=0.075,
            width_nominal=3,
            height_nominal=400,
            depth_nominal=1,
            rect_config={},
        ).set_x(
            tensor_prob_2d.get_x(),
        ).set_y(
            t32_prob.get_y(),
        )

        self.play(ReplacementTransform(
            tensor_prob_2d,
            t32_prob_2d,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'simplify system_prob into s32_prob',
            skip_animations=False,
        )
        # ************************************************************
        # clean up system_prob
        self.play(explainer_prob.hide_pbars(
            aargs={},
            gargs={'lag_ratio': 0.0},
        ))
        self.play(explainer.hide_anchor_points(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        self.remove(explainer_prob)

        # create e32_prob -> s32_prob
        e32_prob = Explainer.from_file(
            background=background_prob,
            version=160,
            dot_config={},
            rect_config={},
        )
        s32_prob = Group(background_prob, e32_prob)
        self.add(e32_prob)

        # show anchor points of new explainer
        self.play(e32_prob.show_anchor_points(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # show pbars for mini explainer
        self.play(AnimationGroup(
            AnimationGroup(
                *(ap.mob.animate.set_style(
                    stroke_opacity=0.0,
                ) for ap in e32_prob.anchor_points),
            ),
            e32_prob.show_pbars(
                random=False,
                pbar_config={},
                aargs={},
                gargs={'lag_ratio': 0.0},
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'into big map',
            skip_animations=False,
        )
        # ************************************************************
        ac_game = ArrowComment(False, RIGHT).scale(0.8).move_to(LEFT*10).set_color(PURE_RED)
        act_9 = ArrowComment(False, RIGHT).scale(0.8).move_to(DOWN*5)
        acm_8 = ArrowComment(True, DOWN).scale(0.8).move_to(RIGHT*10)

        # show big map without s32_prob_2d
        mobs = Group(
            Mobject(), s32_prob, Mobject(), Mobject(),
            Mobject(), acm_8,    Mobject(), Mobject(),
            ac_game,   t32_prob, act_9,     t32_prob_2d,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=4,
            buff=0.5,
        ).scale(0.5).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # introduce s32_prob_2d
        aci_9 = act_9.copy().move_to(UP*5)
        acm_9 = acm_8.copy().move_to(RIGHT*5)
        s32_prob_2d = s32_prob.copy().move_to(UP*5)
        mobs = Group(
            Mobject(), s32_prob, aci_9,     s32_prob_2d,
            Mobject(), acm_8,    Mobject(), acm_9,
            ac_game,   t32_prob, act_9,     t32_prob_2d,
        )
        mobs.generate_target()
        mobs.target.arrange_in_grid(
            rows=3,
            cols=4,
            buff=0.5,
        ).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
            rate_func=rate_functions.ease_out_back,
        ))
        self.wait(wt)

        # show shapes for tensors
        ac_all = VGroup(
            aci_9,
            acm_8, acm_9,
            ac_game, act_9,
        ).save_state()
        self.play(ac_all.animate(
            run_time=wt,
        ).fade(0.8))
        self.play(AnimationGroup(
            ShowShape(t32_prob, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_prob_2d, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes for tensors
        self.play(AnimationGroup(
            HideShape(t32_prob),
            HideShape(t32_prob_2d),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(ac_all.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        export_mobs(__file__, mobs)     # NOTE: used by 015
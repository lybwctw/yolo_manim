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
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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

        # ************************************************************
        self.next_section(
            'sample, pbars numbers',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'OPTIONAL: loop through several samples',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'prob: explainer to tensor',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'prob_2d: explainer to tensor',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'simplify ...',
            skip_animations=False,
        )
        # ************************************************************
        # # start with anchor points
        # self.play(explainer.show_anchor_points(lag_ratio=0))
        # self.wait()
        # self.play(AnimationGroup(
        #     *(ap.animate.set_pattern(opacity=0.1)
        #       for ap in explainer.anchor_points),
        #       lag_ratio=0,
        #       run_time=1.0,
        # ))
        # self.wait(0.5)

        # # generate random pbars
        # self.play(explainer.show_pbars())
        # self.wait()

        # # FIXME! no valid class capture for 20x20 feature map
        # # from random pbars to ideal pbars
        # self.play(explainer.to_probs(data_cls))
        # self.wait()

        
        # # ************************************************************
        # self.next_section(
        #     'generate tensor_probs',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # show tensor probs in the right
        # # TODO, loop through each pbars, rate_functions.there_and_back
        # self.play(explainer_bg.animate.scale(0.8).shift(LEFT*3))
        # tensor_probs = explainer.create_probs_tensor().shift(RIGHT*6)
        # self.wait()
        # self.play(Write(tensor_probs, lag_ratio=0.02, run_time=2.0))
        # self.wait()

        # # scale and rearrange into up-down
        # manager = Group(explainer_bg, tensor_probs)
        # manager.generate_target()
        # manager.target.scale(0.6).arrange(DOWN,buff=0.45).shift(LEFT*2)
        # manager.target[1].align_to(manager.target[0][0].background, LEFT)   # adjustment
        # self.play(MoveToTarget(manager, run_time=1.0))
        # self.wait(0.5)

        # #  transform probs into reshaped 2d version
        # tensor_probs_2d = tensor_probs.copy()
        # self.add(tensor_probs)  # TODO, fadein animation?
        # line_matrix = explainer.create_line_matrix(n=3).scale(0.07).shift(RIGHT*3.5)
        # self.play(tensor_to_line_matrix(
        #     tensor=tensor_probs_2d,
        #     lmatrix=line_matrix,
        #     targs={},
        #     gargs={'lag_ratio':0.02, 'run_time':0.1,},
        #     ggargs={'lag_ratio':0.05, 'run_time':2.1,},
        # ))
        # self.wait(0.3)

        # # ************************************************************
        # self.next_section(
        #     'simplify tensor_probs/tensor_probs_2d' \
        #     'into lf_output_32_cls/lf_output_32_cls_2d',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # create lf_output_32_cls
        # lf_output_32_cls = LayersFake(
        #     n=3,
        #     ref=tensor_probs,
        #     width_nominal=20,
        #     height_nominal=20,
        #     buff=0.05,
        #     expanded=True,
        # ).move_to(tensor_probs).scale(0.95)

        # # create lf_output_32_cls_2d
        # lf_output_32_cls_2d = LayersFake(
        #     n=1,
        #     ref=tensor_probs_2d,
        #     width_nominal=3,
        #     height_nominal=400,
        #     expanded=True,
        # ).move_to(tensor_probs_2d)

        # # simplify tensor_probs/tensor_probs_2d
        # self.play(AnimationGroup(
        #     Unwrite(tensor_probs, lag_ratio=0, run_time=1.0),
        #     Write(lf_output_32_cls, run_time=1.0),
        #     Unwrite(tensor_probs_2d, lag_ratio=0, run_time=1.0),
        #     Write(lf_output_32_cls_2d, run_time=1.0)
        # ))
        # self.wait(0.5)

        # # ************************************************************
        # self.next_section(
        #     'simplify explainer_dist and explainer_xyxy ' \
        #     'into 4x4 mini version',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # clean explainer
        # self.play(explainer.hide_pbars(
        #     aargs={},
        #     gargs={},
        #     ggargs={'lag_ratio':0, 'run_time':1.0},
        # ))
        # self.wait(0.5)
        # self.play(explainer.hide_anchor_points(
        #     lag_ratio=0, run_time=0.5,
        # ))
        # self.wait(0.5)
        # self.remove(explainer)

        # # create mini version of explainer
        # explainer = ExplainerBbox(
        #     background=background,
        #     data=np.load(MINI_32_DIST_PATH),
        #     data_cls=np.load(MINI_32_PROB_PATH),
        #     sf_nominal=32,
        # )
        # explainer_bg = Group(explainer, background)

        # # dim anchor points, show pbars
        # self.play(AnimationGroup(
        #     explainer.show_anchor_points(
        #         lag_ratio=0, run_time=0.5,
        #     )
        # ))
        # self.wait(0.5)
        # self.play(AnimationGroup(
        #     *(ap.animate.set_pattern(opacity=0.1)
        #       for ap in explainer.anchor_points),
        #       lag_ratio=0,
        #       run_time=1.0,
        # ))
        
        # self.play(explainer.show_pbars(
        #     aargs={},
        #     gargs={},
        #     ggargs={},
        # ))
        # self.wait(0.5)

        # # ************************************************************
        # self.next_section(
        #     'save for next scene which go back to big map',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # everything = Group(
        #     explainer_bg,
        #     lf_output_32_cls,
        #     lf_output_32_cls_2d,
        # )
        # save_everything(S015_EVERYTHING, everything)
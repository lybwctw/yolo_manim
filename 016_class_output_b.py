from manim import *

from utils.constants import *
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.general import load_everything
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.layers_fake import LayersFake

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'rearrange class output 32 without DFL',
            skip_animations=False,
        )
        # ************************************************************
        (
            explainer_bg,
            lf_output_32_cls,
            lf_output_32_cls_2d,
        ) = load_everything(S015_EVERYTHING)
        explainer_bg: Group
        lf_output_32_cls: LayersFake
        lf_output_32_cls_2d: LayersFake

        ac_ab = ArrowComment(False, RIGHT, '?').shift(UP*50)
        ac_a1 = ArrowComment(True, DOWN, '?').shift(LEFT*50)
        ac_b2 = ArrowComment(True, DOWN, '?').shift(RIGHT*50)
        ac_game = ArrowComment(False, RIGHT, '?').shift(LEFT*50)    # TODO, should stand out
        ac_12 = ArrowComment(False, RIGHT, '?').shift(DOWN*10)
        ac_23 = ArrowComment(False, RIGHT, '?').shift(RIGHT*10)
        ac_all = VGroup(
            ac_ab,
            ac_a1, ac_b2,
            ac_game, ac_12, ac_23,
        )
        ac_all.scale(0.5)

        self.add(
            explainer_bg,
            lf_output_32_cls,
            lf_output_32_cls_2d,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'rearrange class output 32 without DFL',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[explainer_bg, explainer_bg[1].copy().set_opacity(0)],
            *[lf_output_32_cls, lf_output_32_cls_2d],
        )
        manager.generate_target()
        manager.target[3]\
            .stretch_to_fit_height(3.0)\
            .stretch_to_fit_width(0.8)
        manager.target.arrange_in_grid(
            rows=2,
            cols=2,
            buff=0.85,
        ).scale(0.8).center()

        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'generate counterpart of lf_output_32_cls_2d',
            skip_animations=False,
        )
        # ************************************************************
        explainer_bg_2d = explainer_bg.copy()
        self.play(FadeIn(explainer_bg_2d, run_time=0.3))
        manager = Group(
            *[explainer_bg, explainer_bg_2d],
            *[lf_output_32_cls, lf_output_32_cls_2d],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=2,
            cols=2,
            buff=0.85,
        ).scale(0.9).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'insert arrows',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[VMobject(), explainer_bg, ac_ab, explainer_bg_2d, VMobject()],
            *[VMobject(), ac_a1, VMobject(), ac_b2, VMobject()],
            *[ac_game, lf_output_32_cls, ac_12, lf_output_32_cls_2d, ac_23],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=5,
            # buff=0.85,
        ).scale(0.9).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'show shapes and back',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            ac_all.animate.set_opacity(0.1),
            lf_output_32_cls.show_passing_flash(),
            lf_output_32_cls_2d.show_passing_flash(),
        ))
        self.wait()

        self.play(AnimationGroup(
            AnimationGroup(
                lf_output_32_cls.unwrite_shape_texts(),
                lf_output_32_cls_2d.unwrite_shape_texts(),
            ),
            ac_all.animate.set_opacity(1.0),
            lag_ratio=0.5,
        ))
        self.wait()
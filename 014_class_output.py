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
            'rearrange bbox output 32 without DFL',
            skip_animations=False,
        )
        # ************************************************************
        (
            explainer_dist_bg,
            explainer_xyxy_bg,
            lf_output_32_dist,
            lf_output_32_xyxy,
            lf_output_32_xyxy_2d,
        ) = load_everything(S013_EVERYTHING)
        explainer_dist_bg: Group
        explainer_xyxy_bg: Group
        lf_output_32_dist: LayersFake
        lf_output_32_xyxy: LayersFake
        lf_output_32_xyxy_2d: LayersFake

        self.add(
            explainer_dist_bg,
            explainer_xyxy_bg,
            lf_output_32_dist,
            lf_output_32_xyxy,
            lf_output_32_xyxy_2d,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'rearrange bbox output 32 without DFL',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[explainer_dist_bg, explainer_xyxy_bg, explainer_xyxy_bg[1].copy().set_opacity(0)],
            *[lf_output_32_dist, lf_output_32_xyxy, lf_output_32_xyxy_2d],
        )
        manager.generate_target()
        manager.target[5]\
            .stretch_to_fit_height(3.0)\
            .stretch_to_fit_width(0.8)
        manager.target.arrange_in_grid(
            rows=2,
            cols=3,
            buff=0.85,
        ).scale(0.8).center()

        self.play(MoveToTarget(manager))
        self.wait()

        # # show shapes of layers fake
        # self.play(AnimationGroup(
        #     lf_output_32_dist.show_passing_flash(),
        #     lf_output_32_xyxy.show_passing_flash(),
        # ))
        # self.wait()

        # ************************************************************
        self.next_section(
            'patching the big map',
            skip_animations=False,
        )
        # ************************************************************
        explainer_xyxy_2d_bg = explainer_xyxy_bg.copy()
        self.play(FadeIn(explainer_xyxy_2d_bg, run_time=0.3))
        manager = Group(
            *[explainer_dist_bg, explainer_xyxy_bg, explainer_xyxy_2d_bg],
            *[lf_output_32_dist, lf_output_32_xyxy, lf_output_32_xyxy_2d],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=2,
            cols=3,
            buff=0.85,
        ).scale(0.9).center()
        self.play(MoveToTarget(manager))
        self.wait()
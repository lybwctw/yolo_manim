from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.explainer_bbox import ExplainerBbox, load_explainer

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init background according to 017',
            skip_animations=False,
        )
        # ************************************************************
        everything = load_everything(S017_EVERYTHING_PP)
        (
            background,
        ) = everything
        self.add(everything)
        self.wait()

        # ************************************************************
        self.next_section(
            'generate 20x20 bbox+cls, intuition + tensor',
            skip_animations=False,
        )
        explainer = load_explainer(
            background=background,
            version='general',
        )
        self.add(explainer)
        self.play(explainer.show_anchor_points(lag_ratio=0))
        self.wait()
        self.play(explainer.to_rects())
        self.wait()
        
        # ************************************************************
        # generate 20x20 anchor

        # generate 20x20 bbox

        # generate 20x20 pbars

        # ************************************************************
        self.next_section(
            'generate 20x20 bbox+cls',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'filter out some for clearer postprocess demonstration',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'pick the max prob + class',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'conf filtering',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'NMS filtering',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'scale back',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, verify ultralytics's bug on scale back

        # ************************************************************
        self.next_section(
            'pick max variant: multi-label',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'NMS variant: class-ignorant',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'extra postprocess: max_det',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            '...',
            skip_animations=False,
        )
        # ************************************************************
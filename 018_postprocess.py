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
            skip_animations=True,
        )
        # ************************************************************
        everything = load_everything(S017_EVERYTHING_PP)
        (
            background,
        ) = everything
        self.add(everything)
        self.wait()

        explainer = load_explainer(
            background=background,
            version='general',
        )
        self.add(explainer)

        # ************************************************************
        self.next_section(
            'generate 20x20 bbox+cls',
            skip_animations=True,
        )
        # ************************************************************
        # show anchor points
        self.play(explainer.show_anchor_points(lag_ratio=0))
        self.wait()

        # show both rect and multi labels together
        self.play(explainer.show_rect_mlabels(
            rect_config={'width': 0.3,},
            label_config={'fill_opacity': 0.3, 'stroke_opacity': 0.0,},
            rargs={'run_time': 0.3,},
            largs={'run_time': 0.3,},
            gargs={'lag_ratio': 0.8, 'run_time': 0.5,},
            ggargs={'lag_ratio': 0.1, 'run_time': 10, 'rate_func': rate_functions.ease_in_out_expo,},
        ))

        # ************************************************************
        self.next_section(
            'filter out some for clearer postprocess demonstration',
            skip_animations=False,
        )
        # ************************************************************
        self.play(explainer.keep_ratio(
            ratio=0.2,
            aargs={},
            gargs={'lag_ratio': 0.1, 'run_time': 1.5,},
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'generate 2d tensor as the fake raw output',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, maybe, show conf in each label?
        tensor_raw = explainer.create_2d_tensor(
            font_size=6,
        )
        tensor_raw.center().shift(RIGHT*2)
        self.play(Write(tensor_raw, lag_ratio=0.1))
        self.wait()

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
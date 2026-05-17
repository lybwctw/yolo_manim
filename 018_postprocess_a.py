from manim import *

from utils.constants import *
from utils.general import load_everything
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.image_pad import ImagePad

FAST_RT = 0.1

CONF_THRESH = 0.7
IOU_THRESH = 0.2

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'start with xyxyccc format',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME: use background from 017 for better continuity
        background = ImagePad(padded=True).scale(1.0).set_opacity(0.2)
        # FIXME: use random 10x10 for now
        explainer = Explainer.from_file(
            background=background,
            version='mini',
            sf_nominal=64,
        )
        system = Group(background, explainer)
        self.add(system)
        self.wait(FAST_RT)

        self.play(explainer.show_anchor_points(
            run_time=FAST_RT,
        ))
        self.wait(FAST_RT)

        self.play(explainer.to_rects(
            gargs={'run_time': FAST_RT},
        ))
        self.wait(FAST_RT)

        self.play(explainer.show_multi_labels(
            label_config={'font_size': 8},
            gargs={'run_time': FAST_RT},
        ))
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply take max',
            skip_animations=False,
        )
        # ************************************************************
        explainer.apply_max_select(
            scene=self,
            run_time_ratio=FAST_RT,
        )
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply conf filter',
            skip_animations=False,
        )
        # ************************************************************
        explainer.apply_conf_filter(
            self,
            conf_thresh=CONF_THRESH,
            run_time_ratio=1.0,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'apply class split',
            skip_animations=False,
        )
        # ************************************************************
        # nothing for now

        # ************************************************************
        self.next_section(
            'sort each class',
            skip_animations=False,
        )
        # ************************************************************
        # nothing for now
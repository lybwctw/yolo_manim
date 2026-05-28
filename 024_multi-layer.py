from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs
from utils.image_pad import ImagePad
from utils.explainer import Explainer

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'stride 32 explainers/systems',
            skip_animations=False,
        )
        # ************************************************************
        background = ImagePad(padded=True).set_opacity(0.1)
        e32 = Explainer.from_file(
            background=background,
            version=32,
        )
        s32 = Group(background, e32)
        self.add(s32)
        self.wait()

        self.play(e32.show_anchor_points(
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait()
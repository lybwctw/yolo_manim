from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
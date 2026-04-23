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
            'init all mobs according to 019',
            skip_animations=False,
        )
        # ************************************************************
        everything = load_everything(S019_EVERYTHING)
        (
            image_raw, ac_ab, image_pad, _, system_dist, system_probs, ac_cd, system_merged, ac_de, system_scale_back,
            tensor_raw, ac_12, tensor_pad, ac_game, tensor_32_dist, tensor_32_probs, ac_34, tensor_merged_2d, ac_45, tensor_scale_back,
        ) = everything

        self.add(everything)
        self.wait()
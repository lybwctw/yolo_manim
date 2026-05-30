from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs according to 023',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('023')
        (
            sin_raw, aci_a, sin_pad,            s32_reg, s32_prob, aco_a, s32_merged_2d, aco_b, s32_back,
            tin_raw, aci_1, tin_pad, ac_game,   t32_reg, t32_prob, aco_1, t32_merged_2d, aco_2, t32_back,
        ) = mobs
        
        self.add(mobs)
        self.wait()
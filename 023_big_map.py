from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs

GAP_POSTPROCESS = 0.2

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs according to 020',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('020')
        (
            s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d,
            s32_prob, acc_ab, s32_prob_2d,
            marrow_out_iview,
            s32_merged_2d, ac_a, s32_max, ac_b, s32_conf, ac_c, s32_nms, ac_d, s32_back,
            marrow_in_tview,
            t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d,
            t32_prob, acc_12, t32_prob_2d,
            marrow_out_tview,
            t32_merged_2d, ac_1, t32_max, ac_2, t32_conf, ac_3, t32_nms, ac_4, t32_back,
        ) = mobs

        self.add(mobs)
        self.wait()

        # ************************************************************
        self.next_section(
            'insert s32_reg at the start of both view',
            skip_animations=False,
        )
        # ************************************************************
        # scale down to make root in the left
        self.play(mobs.animate(
            run_time=0.5,
        ).scale(0.93).shift(RIGHT*0.5))
        self.wait(1.0)
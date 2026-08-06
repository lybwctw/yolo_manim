from manim import *

from utils.mtensor import MTensor1D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_1D = 1.5

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # cards
        cards, _ = import_mobs('029a')
        (
            card_i1,
            card_i2,
            card_m,
            card_o1,
        ) = cards

        # raw tensors
        t_i1 = torch.randn(9)
        t_i2 = torch.randn(9)
        t_o1 = t_i1 + t_i2

        # tensor mobs
        tensor_i1 = MTensor1D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).shift(UP*TENSOR_VGAP_1D*2)
        tensor_i2 = MTensor1D(
            array=t_i2,
            **MEDIUM_CUBE_CONFIG,
        ).shift(UP*TENSOR_VGAP_1D)
        tensor_o1 = MTensor1D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).shift(DOWN*TENSOR_VGAP_1D)
        VGroup(tensor_i1, tensor_i2, tensor_o1).center()

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce cube inputs',
            skip_animations=False,
        )
        # ************************************************************
        # create input tensors
        self.play(AnimationGroup(
            tensor_i1.create(
                direction=RIGHT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={'lag_ratio': 0.5},
            ),
            tensor_i2.create(
                direction=RIGHT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={'lag_ratio': 0.5},
            ),
            lag_ratio=0.8,
            run_time=wt,
        ))

        # create card summaries
        self.play(AnimationGroup(
            card_i1.expand_summary(summary=t2s(t_i1)),
            card_i2.expand_summary(summary=t2s(t_i2)),
            lag_ratio=0.8,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output',
            skip_animations=False,
        )
        # ************************************************************
        # prepare for highlight
        tensor_i1.prepare_highlight_loop()
        tensor_i2.prepare_highlight_loop()
        masks_in = np.eye(t_i1.shape[0], dtype=bool)

        # focus on first inputs
        self.play(AnimationGroup(
            tensor_i1.highlight(masks_in[0]),
            tensor_i2.highlight(masks_in[0]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # generate first output
        self.play(GrowFromCenter(
            tensor_o1[0],
            rate_func=rate_functions.ease_out_back,
            run_time=wt,
        ))

        # loop into last output
        self.play(AnimationGroup(
            tensor_i1.highlight_loop(
                masks=masks_in[1:],
                back=False,
                rate_func=smooth,
            ),
            tensor_i2.highlight_loop(
                masks=masks_in[1:],
                back=False,
                rate_func=smooth,
            ),
            Succession(
                *(GrowFromCenter(
                    tensor_o1[i],
                    rate_func=rate_functions.ease_out_back,
                ) for i in range(1, tensor_o1.shape[0])),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # back to original hl states
        self.play(AnimationGroup(
            tensor_i1.highlight(),
            tensor_i2.highlight(),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # show output card shape
        self.play(card_o1.expand_summary(
            summary=t2s(t_o1),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        # remove tensors 
        self.play(AnimationGroup(
            *(tmob.uncreate(
                direction=RIGHT,
                anim=ShrinkToCenter,
                gargs={'lag_ratio': 0.5},
            ) for tmob in [tensor_i1, tensor_i2, tensor_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink card summaries
        self.play(AnimationGroup(
            *(cmob.shrink_summary()
              for cmob in [card_i1, card_i2, card_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
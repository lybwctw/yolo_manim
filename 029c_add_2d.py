from manim import *

from utils.mtensor import MTensor2D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_2D = 1.5

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
        cards = import_mobs('029b')
        (
            card_i1,
            card_i2,
            card_m,
            card_o1,
        ) = cards

        # raw tensors
        t_i1 = torch.randn(4,5)
        t_i2 = torch.randn(4,5)
        t_o1 = t_i1 + t_i2

        # tensor mobs
        tensor_i1 = MTensor2D(
            array=t_i1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).shift(UP*TENSOR_VGAP_2D*2)
        tensor_i2 = MTensor2D(
            array=t_i2,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).shift(UP*TENSOR_VGAP_2D)
        tensor_o1 = MTensor2D(
            array=t_o1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).shift(DOWN*TENSOR_VGAP_2D)
        VGroup(tensor_i1, tensor_i2, tensor_o1).center()

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=False,
        )
        # ************************************************************
        # introduce input 1
        self.play(AnimationGroup(
            tensor_i1.create(
                style='layer',
                direction=RIGHT,
            ),
            card_i1.expand_summary(
                t2s(t_i1),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # introduce input 2
        self.play(AnimationGroup(
            tensor_i2.create(
                style='layer',
                direction=RIGHT,
            ),
            card_i2.expand_summary(
                t2s(t_i2),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'detailed computation',
            skip_animations=False,
        )
        # ************************************************************
        # compute into output 1
        h, w = tensor_i1.shape
        masks = np.eye(h*w, dtype=bool).reshape(h*w, h, w)
        self.play(AnimationGroup(
            tensor_i1.highlight_loop(masks=masks, back=False),
            tensor_i2.highlight_loop(masks=masks, back=False),
            Succession(
                *(GrowFromCenter(
                    mob,
                    rate_func=rate_functions.ease_out_back,
                ) for mob in tensor_o1.mobs),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*2,
        ))

        # highlight back input
        self.play(AnimationGroup(
            tensor_i1.highlight(),
            tensor_i2.highlight(),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # expand output card
        self.play(card_o1.expand_summary(
            t2s(t_o1),
            run_time=wt,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        # remove tensors 
        self.play(AnimationGroup(
            *(tmob.uncreate(
                style='layer',
                direction=RIGHT,
                anim=Unwrite,
            ) for tmob in [tensor_i1, tensor_i2, tensor_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink tensor cards
        self.play(AnimationGroup(
            *(cmob.shrink_summary()
              for cmob in [card_i1, card_i2, card_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
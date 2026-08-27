from manim import *

from utils.mtensor import MTensor3D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_3D = 1.2
TENSOR_HGAP_3D = 0.8

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
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
        t_i1 = torch.randn(3,4,5)
        t_i2 = torch.randn(3,4,5)
        t_o1 = t_i1 + t_i2

        # tensor mobs
        tensor_i1 = MTensor3D(
            array=t_i1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ).align_to(
            LEFT*TENSOR_HGAP_3D,
            RIGHT,
        )
        tensor_i2 = MTensor3D(
            array=t_i2,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ).align_to(
            RIGHT*TENSOR_HGAP_3D,
            LEFT,
        )
        tensor_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )
        VGroup(tensor_i1, tensor_i2, tensor_o1).center()

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce inputs',
            skip_animations=True,
        )
        # ************************************************************
        # introduce input 1
        self.play(AnimationGroup(
            tensor_i1.create(
                style='beam',
                direction=OUT,
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
                style='beam',
                direction=OUT,
            ),
            card_i2.expand_summary(
                t2s(t_i2),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # ************************************************************
        self.next_section(
            'detailed computation',
            skip_animations=True,
        )
        # ************************************************************
        # compute into output 1
        c, h, w = tensor_i1.shape
        masks = np.eye(c*h*w, dtype=bool).reshape(c*h*w, c, h, w)
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
            'vectorized thinking',
            skip_animations=False,
        )
        # ************************************************************
        # remove output tensor
        tensor_o1.save_state()
        self.play(AnimationGroup(
            tensor_o1.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # input breath
        self.play(AnimationGroup(
            tensor_i1.breath(style='whole'),
            tensor_i2.breath(style='whole'),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # output pop
        tensor_o1.restore()
        self.play(AnimationGroup(
            tensor_o1.create(
                style='whole',
            ),
            card_o1.expand_summary(
                t2s(t_o1),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'unmatched inputs',
            skip_animations=False,
        )
        # ************************************************************
        # clean input 1 and output
        self.play(AnimationGroup(
            *(tmob.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ) for tmob in [tensor_i1, tensor_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink tensor cards
        self.play(AnimationGroup(
            *(cmob.shrink_summary()
              for cmob in [card_i1, card_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # new input 1
        t_i1 = torch.randn(4,3,2)
        tensor_i1 = MTensor3D(
            array=t_i1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_i2,
            LEFT,
            buff=TENSOR_HGAP_3D*2,
        )

        # introduce new input 1
        self.play(AnimationGroup(
            tensor_i1.create(
                style='beam',
                direction=OUT,
            ),
            card_i1.expand_summary(
                t2s(t_i1),
                run_time=wt,
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # failed breath and generation
        self.play(AnimationGroup(
            tensor_i1.breath(style='whole'),
            tensor_i2.breath(style='whole'),
            card_m.suggest_failure(),
            lag_ratio=0.0,
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
                style='beam',
                direction=IN,
                anim=Unwrite,
            ) for tmob in [tensor_i1, tensor_i2]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink tensor cards
        self.play(AnimationGroup(
            *(cmob.shrink_summary()
              for cmob in [card_i1, card_i2]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # remove tensor cards
        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_i2, UP),
            detach_to_ref(card_o1, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))
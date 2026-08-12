from manim import *

from utils.mtensor import MTensor3D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_3D = 1.0
TENSOR_HGAP_3D = 1.0
TENSOR_EGAP_3D = 1.0

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
        cards = import_mobs('031c')
        (
            card_i1, card_i2, card_i3, card_m, card_o1,
        ) = cards

        # show initial mobs
        self.set_camera_orientation(
            zoom=0.8,                   # a little bit farther
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,4,5)(2,4,5) -[0]- (5,4,5)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(3,4,5)
        t_i2 = torch.randn(2,4,5)
        t_o1 = torch.cat([t_i1, t_i2], dim=0)

        # input tensor mob
        tensor_is = VGroup(
            MTensor3D(
                array=t,
                mode='cube',
                **MEDIUM_TENSOR_CONFIG,
            ) for t in [t_i1, t_i2]
        ).arrange(
            IN,
            buff=TENSOR_EGAP_3D,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        )
        tensor_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        # show input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                style='beam',
                direction=OUT,
            ) for tmob in tensor_is),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # remove redundant input card
        card_is = VGroup(card_i1, card_i2)
        self.play(AnimationGroup(
            detach_to_ref(card_i3, LEFT),
            attach_to_ref(card_is, card_m, UP),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # expand input cards summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
              for cmob, t in zip(
                [card_i1, card_i2],
                [t_i1, t_i2]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # update params
        self.play(card_m.update_params(
            {
                'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # concat animation
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(
            tensor_is_copy.target,
            [0, 3],
        ):
            tmob.align_to(
                tensor_o1[idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.replace(tensor_is_copy, tensor_o1)
        self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1),
            run_time=wt,
        ))
        self.wait(wt)

        # clean output
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [tensor_o1],
                [card_o1]
            )),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,4,5)(2,4,5) -[1]- FAILURE',
            skip_animations=False,
        )
        # ************************************************************
        # update params
        self.play(card_m.update_params(
            {
                'dim': 1,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # reposition input tensor
        self.play(tensor_is.animate(
            run_time=wt,
        ).arrange(
            DOWN,
            buff=TENSOR_VGAP_3D,
        ).align_to(
            LEFT*TENSOR_HGAP_3D,
            RIGHT,
        ))
        self.wait(wt)

        # failed concat animation
        orig_center = tensor_is.get_center()
        self.play(AnimationGroup(
            tensor_is.animate(
                rate_func=rate_functions.there_and_back,
            ).arrange(
                DOWN,
                buff=TENSOR_VGAP_3D*0.5,
            ).move_to(orig_center),
            card_m.suggest_failure(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # clean input 1
        self.play(AnimationGroup(
            tensor_is[0].uncreate(
                style='beam',
                direction=IN,
            ),
            card_i1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(2,3,5)(2,4,5) -[1]- (2,7,5)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.rand(2,3,5)
        t_o1 = torch.cat([t_i1, t_i2], dim=1)

        # new tensor mob
        tensor_i1 = MTensor3D(
            array=t_i1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_is[1],
            UP,
            buff=TENSOR_VGAP_3D,
        )
        tensor_is = VGroup(tensor_i1, tensor_is[1])
        tensor_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            RIGHT*TENSOR_HGAP_3D,
            LEFT,
        )

        # show input tensor 1
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
        self.wait(wt)

        # concat animation
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(
            tensor_is_copy.target,
            [0, 3],
        ):
            tmob.align_to(
                tensor_o1[:,idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.replace(tensor_is_copy, tensor_o1)

        # expand output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1),
            run_time=wt,
        ))
        self.wait(wt)

        # clean output and input 2
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
            ) for tmob, cmob in zip(
                [tensor_is[1], tensor_o1],
                [card_i2, card_o1]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(2,3,5)(2,3,2) -[2]- (2,3,7)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i2 = torch.randn(2,3,2)
        t_o1 = torch.cat([t_i1, t_i2], dim=2)

        # new tensor mob
        tensor_i2 = MTensor3D(
            array=t_i2,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_is[0],
            RIGHT,
            buff=TENSOR_HGAP_3D,
        )
        tensor_is = VGroup(tensor_is[0], tensor_i2)
        tensor_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        # show input tensor 2
        self.play(AnimationGroup(
            tensor_i2.create(
                style='beam',
                direction=OUT,
            ),
            card_i2.expand_summary(
                t2s(t_i2),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # update params
        self.play(card_m.update_params(
            {
                'dim': 2,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # reposition input tensors
        self.play(tensor_is.animate(
            run_time=wt,
        ).center().align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ))
        self.wait(wt)

        # concat animation
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(
            tensor_is_copy.target,
            [0, 5],
        ):
            tmob.align_to(
                tensor_o1[:,:,idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.replace(tensor_is_copy, tensor_o1)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1),
            run_time=wt,
        ))
        self.wait(wt)

        # clean output and input 2
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                ),
                cmob.shrink_summary(),
            ) for tmob, cmob in zip(
                [tensor_is[1], tensor_o1],
                [card_i2, card_o1],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,3,5)(2,3,5)(4,3,5) -[0]- (9,3,5)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i2 = t_i1     # old first -> new second
        t_i1 = torch.randn(3,3,5)
        t_i3 = torch.randn(4,3,5)
        t_o1 = torch.cat([t_i1, t_i2, t_i3], dim=0)

        # new tensor mob
        tensor_i2 = tensor_i1
        tensor_i1 = MTensor3D(
            array=t_i1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_i2,
            OUT,
            TENSOR_EGAP_3D,
        )
        tensor_i3 = MTensor3D(
            array=t_i3,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_i2,
            IN,
            TENSOR_EGAP_3D,
        )
        tensor_is = VGroup(
            tensor_i1,
            tensor_i2,
            tensor_i3,
        )
        tensor_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )
        
        # update params
        self.play(card_m.update_params(
            {
                'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # TODO: zoom 0.7

        # show input tensor 1 and 3
        self.play(AnimationGroup(
            *(tmob.create(
                style='beam',
                direction=OUT,
            ) for tmob in [tensor_i1, tensor_i3]),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # new input card
        card_i3 = InfoCard('in_3').hide_to_corner(LEFT).align_to(
            card_i2,
            DOWN,
        )
        self.add_fixed_in_frame_mobjects(card_i3)
        self.play(AnimationGroup(
            attach_to_ref(
                card_i3,
                card_m,
                UP,
            ),
            attach_to_ref(
                VGroup(card_i1, card_i2),
                card_i2,
                UP,
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # expand input cards summary
        self.play(AnimationGroup(
            card_i1.update_summary(t2s(t_i1)),
            *(cmob.expand_summary(t2s(t))
              for cmob, t in zip(
                [card_i2, card_i3],
                [t_i2, t_i3]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # reposition input tensor
        self.play(tensor_is.animate(
            run_time=wt,
        ).center().align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ))

        # concat animation
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(
            tensor_is_copy.target,
            [0, 3, 5],
        ):
            tmob.align_to(
                tensor_o1[idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.replace(tensor_is_copy, tensor_o1)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1),
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
                direction=RIGHT,
                anim=Unwrite,
            ) for tmob in [*tensor_is, tensor_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink tensor cards
        self.play(AnimationGroup(
            *(cmob.shrink_summary()
              for cmob in [card_i1, card_i2, card_i3, card_o1]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # remove tensor cards
        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_i2, UP),
            detach_to_ref(card_i3, UP),
            detach_to_ref(card_o1, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(card_m.shrink_params(
            run_time=wt,
        ))
        self.wait(wt)
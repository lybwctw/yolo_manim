from manim import *

from utils.mtensor import MTensor2D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_2D = 1.5
TENSOR_EGAP_2D = 1.0
TENSOR_HGAP_2D = 1.0

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
        cards = import_mobs('031b')
        (
            card_i1, card_i2, card_i3, card_m, card_o1
        ) = cards

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,5)(4,5) -[0]- (8,5)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(3,5)
        t_i2 = torch.randn(4,5)
        t_o1 = torch.cat([t_i1, t_i2], dim=0)

        # input tensor mob
        tensor_is = VGroup(
            MTensor2D(
                array=t,
                mode='cube',
                style='erect',
                **MEDIUM_TENSOR_CONFIG,
            ) for t in [t_i1, t_i2]
        ).arrange(
            IN,
            buff=TENSOR_EGAP_2D,
        ).align_to(
            UP*TENSOR_VGAP_2D,
            DOWN,
        )
        tensor_o1 = MTensor2D(
            array=t_o1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_2D,
            UP,
        )

        # show input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                style='beam',
                direction=RIGHT,
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
                UL+OUT,
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.replace(tensor_is_copy, tensor_o1)
        self.wait(wt)

        # expand output summary
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
                    direction=RIGHT,
                    anim=Unwrite,
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
            '(3,5)(4,5) -[1]- FAILURE',
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
        orig_center = tensor_is.get_center()
        self.play(tensor_is.animate(
            run_time=wt,
        ).arrange(
            RIGHT,
            buff=TENSOR_HGAP_2D,
        ).move_to(orig_center))
        self.wait(wt)

        # failed concat animation
        self.play(AnimationGroup(
            tensor_is.animate(
                rate_func=rate_functions.there_and_back,
            ).arrange(
                RIGHT,
                buff=TENSOR_HGAP_2D*0.5,
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
                direction=RIGHT,
                anim=Unwrite,
            ),
            card_i1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(4,2)(4,5) -[1]- (4,7)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.rand(4,2)
        t_o1 = torch.cat([t_i1, t_i2], dim=1)

        # new tensor mob
        tensor_i1 = MTensor2D(
            array=t_i1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_is[1],
            LEFT,
            buff=TENSOR_HGAP_2D,
        )
        tensor_is = VGroup(tensor_i1, tensor_is[1])
        tensor_o1 = MTensor2D(
            array=t_o1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_2D,
            UP,
        )

        # show input tensor 1
        self.play(AnimationGroup(
            tensor_i1.create(
                style='beam',
                direction=RIGHT,
                run_time=wt,
            ),
            card_i1.expand_summary(
                t2s(t_i1),
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
            [0, 2],
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

        # clean output
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=RIGHT,
                    anim=Unwrite,
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
            '(4,2)(4,5)(4,3) -[1]- (4,10)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i3 = torch.randn(4,3)
        t_o1 = torch.cat([t_i1, t_i2, t_i3], dim=1)

        # input tensor mob
        tensor_i3 = MTensor2D(
            array=t_i3,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).next_to(
            tensor_is[1],
            RIGHT,
            buff=TENSOR_HGAP_2D,
        )
        tensor_is = VGroup(*tensor_is, tensor_i3)
        tensor_o1 = MTensor2D(
            array=t_o1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_2D,
            UP,
        )

        # show input tensor 3 and reposition
        self.play(tensor_i3.create(
            style='beam',
            direction=RIGHT,
            run_time=wt,
        ))
        orig_center = tensor_is[:2].get_center()
        self.play(tensor_is.animate(
            run_time=wt,
        ).move_to(orig_center))

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
            *(cmob.expand_summary(t2s(t))
              for cmob, t in zip(
                [card_i3],
                [t_i3]
            )),
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
            [0, 2, 7],
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

        # export
        mobs = VGroup(card_i1, card_i2, card_i3, card_m, card_o1)
        export_mobs(__file__, mobs)     # NOTE: used by next
        self.wait(wt)
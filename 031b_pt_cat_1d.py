from manim import *

from utils.mtensor import MTensor1D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

INIT_MODULE_PARAMS = {
    'dim': UNKNOWN,
}

TENSOR_VGAP_1D = 1.5
TENSOR_HGAP_1D = 1.0

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # module card
        card_m, _ = import_mobs('031a')

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card_m)
        self.wait(wt)

        self.add_fixed_in_frame_mobjects

        # expand module card
        self.play(card_m.expand_params(
            params=INIT_MODULE_PARAMS,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(5)(5) -[0]- (10)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(5)
        t_i2 = torch.randn(5)
        t_o1 = torch.cat([t_i1, t_i2], dim=0)

        # tensor mob
        tensor_is = VGroup(
            MTensor1D(
                array=t,
                mode='cube',
                style='horizontal',
            ) for t in [t_i1, t_i2]
        ).arrange(
            RIGHT,
            buff=TENSOR_HGAP_1D,
        ).shift(
            UP*TENSOR_VGAP_1D,
        )
        tensor_o1 = MTensor1D(
            array=t_o1,
            mode='cube',
            style='horizontal',
        ).shift(
            DOWN*TENSOR_VGAP_1D,
            UP,
        )

        # show input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                style='series',
                direction=RIGHT,
            ) for tmob in tensor_is),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # new input cards
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        card_i2 = InfoCard('in_2').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i1, card_i2)
        self.play(attach_to_ref(
            VGroup(card_i1, card_i2),
            card_m,
            UP,
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

        # update module card
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
            [0, 5],
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

        # new output card
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1)
        self.play(attach_to_ref(
            card_o1,
            card_m,
            DOWN,
            run_time=wt,
        ))

        # expand output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1),
            run_time=wt,
        ))
        self.wait(wt)

        # clean
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='series',
                    direction=RIGHT,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [*tensor_is, tensor_o1],
                [card_i1, card_i2, card_o1]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3)(9) -[0]- (12)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(3)
        t_i2 = torch.randn(9)
        t_o1 = torch.cat([t_i1, t_i2], dim=0)

        # tensor mob
        tensor_is = VGroup(
            MTensor1D(
                array=t,
                mode='cube',
                style='horizontal',
            ).shift(UP*TENSOR_VGAP_1D)
            for t in [t_i1, t_i2]
        ).arrange(
            RIGHT,
            buff=TENSOR_HGAP_1D,
        ).align_to(
            UP*TENSOR_VGAP_1D,
            DOWN,
        )
        tensor_o1 = MTensor1D(
            array=t_o1,
            mode='cube',
            style='horizontal',
        ).align_to(
            DOWN*TENSOR_VGAP_1D,
            UP,
        )

        # show input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                style='series',
                direction=RIGHT,
            ) for tmob in tensor_is),
            lag_ratio=0.5,
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
                UL+OUT
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

        # clean
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='series',
                    direction=RIGHT,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [*tensor_is, tensor_o1],
                [card_i1, card_i2, card_o1]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     '(4)(3)(6) -[0]- (13)',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # raw tensor
        # t_i1 = torch.randn(4)
        # t_i2 = torch.randn(3)
        # t_i3 = torch.randn(6)
        # t_o1 = torch.cat([t_i1, t_i2, t_i3], dim=0)

        # # input tensor mob
        # tensor_is = VGroup(
        #     MTensor1D(
        #         array=t,
        #         **MEDIUM_CUBE_CONFIG,
        #     ).shift(UP*TENSOR_VGAP_1D)
        #     for t in [t_i1, t_i2, t_i3]
        # ).arrange(
        #     RIGHT,
        #     buff=TENSOR_HGAP_1D,
        # ).align_to(
        #     UP*TENSOR_VGAP_1D,
        #     DOWN,
        # )

        # # output tensor mob
        # tensor_o1 = MTensor1D(
        #     array=t_o1,
        #     **MEDIUM_CUBE_CONFIG,
        # ).align_to(
        #     DOWN*TENSOR_VGAP_1D,
        #     UP,
        # )

        # # show input tensor
        # self.play(AnimationGroup(
        #     *(tmob.create(
        #         direction=RIGHT,
        #         anim=GrowFromCenter,
        #         aargs={'rate_func': rate_functions.ease_out_back},
        #         gargs={'lag_ratio': 0.5},
        #     ) for tmob in tensor_is),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))

        # # show input summary
        # card_i3 = InfoCard('in_3').hide_to_corner(LEFT).align_to(
        #     card_i2,
        #     DOWN,
        # )
        # self.add_fixed_in_frame_mobjects(card_i3)
        # self.play(AnimationGroup(
        #     attach_to_ref(
        #         card_i3,
        #         card_m,
        #         UP,
        #     ),
        #     attach_to_ref(
        #         VGroup(card_i1, card_i2),
        #         card_i2,
        #         UP,
        #         run_time=wt,
        #     ),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.play(AnimationGroup(
        #     *(cmob.expand_summary(t2s(t))
        #       for cmob, t in zip(
        #         [card_i1, card_i2, card_i3],
        #         [t_i1, t_i2, t_i3]
        #     )),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # show compute output
        # tensor_is_copy = tensor_is.copy()
        # self.play(FadeIn(
        #     tensor_is_copy,
        #     run_time=wt*0.1,
        # ))
        # tensor_is_copy.generate_target()
        # for tmob, idx in zip(tensor_is_copy.target, [0, 4, 7]):
        #     tmob.align_to(
        #         tensor_o1[idx:],
        #         UL+OUT
        #     )
        # self.play(MoveToTarget(
        #     tensor_is_copy,
        #     run_time=wt,
        # ))
        # self.remove(tensor_is_copy)
        # self.add(tensor_o1)
        # self.wait(wt)

        # # show output summary
        # self.play(card_o1.expand_summary(
        #     t2s(t_o1),
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # clean merged

        # # ************************************************************
        # self.next_section(
        #     'clean everything',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # self.play(AnimationGroup(
        #     *(AnimationGroup(
        #         tmob.uncreate(
        #             direction=RIGHT,
        #             anim=ShrinkToCenter,
        #             gargs={'lag_ratio': 0.5},
        #         ),
        #         cmob.shrink_summary(),
        #         lag_ratio=0.5,
        #     ) for tmob, cmob in zip(
        #         list(tensor_is) + [tensor_o1],
        #         [card_i1, card_i2, card_i3, card_o1]
        #     )),
        #     lag_ratio=0.5,
        #     run_time=wt,
        # ))

        # self.play(AnimationGroup(
        #     detach_to_ref(card_i1, UP),
        #     detach_to_ref(card_i2, UP),
        #     detach_to_ref(card_i3, UP),
        #     detach_to_ref(card_o1, DOWN),
        #     card_m.update_params(
        #         {
        #             'dim': UNKNOWN,
        #         },
        #     ),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.wait(wt)
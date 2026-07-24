from manim import *

from utils.mtensor import MTensor_1D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_1D = 1.5
TENSOR_HGAP_1D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # cards
        card_m, _ = import_mobs('030a')

        # input raw tensor
        t_i1 = torch.randn(10)

        # input tensor mob
        tensor_i1 = MTensor_1D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).shift(UP*TENSOR_VGAP_1D)

        # input card mob
        card_i1 = InfoCard('in_1').hide_to_corner(UP)

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_m,
            card_i1,
        )   # tensor not added while it's ok
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'input tensor and card',
            skip_animations=True,
        )
        # ************************************************************
        # input tensor
        self.play(tensor_i1.create(
            direction=RIGHT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))

        # input card
        self.play(attach_to_ref(
            card_i1,
            card_m,
            UP,
            run_time=wt,
        ))
        self.play(card_i1.expand_summary(
            t2s(t_i1),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output with 5|0',
            skip_animations=True,
        )
        # ************************************************************
        # params
        self.play(card_m.update_params(
            {
                'split_size': 5,
                'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw tensor
        t_o1, t_o2 = torch.split(t_i1, 5, dim=0)

        # tensor mob
        tensor_o1 = MTensor_1D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(tensor_i1, UL)
        tensor_o2 = MTensor_1D(
            array=t_o2,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(tensor_i1, UR)

        # fade in tensor
        tensor_os = VGroup(tensor_o1, tensor_o2)
        self.play(AnimationGroup(
            *(FadeIn(tensor_o) for tensor_o in tensor_os),
            lag_ratio=0.0,
            run_time=wt*0.1,
        ))

        # split animation
        tensor_os.generate_target()
        tensor_os.target.shift(DOWN*TENSOR_VGAP_1D*2)
        orig_center = tensor_os.target.get_center()
        tensor_os.target.arrange(RIGHT, buff=TENSOR_HGAP_1D).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))
        self.wait(wt)

        # new card
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        card_o2 = InfoCard('out_2').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1, card_o2)
        self.play(attach_to_ref(
            VGroup(card_o1, card_o2),
            card_m,
            DOWN,
            run_time=wt,
        ))

        # card summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                [card_o1, card_o2],
                [t_o1, t_o2]
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    direction=RIGHT,
                    anim=ShrinkToCenter,
                    gargs={'lag_ratio': 0.5},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [tensor_o1, tensor_o2],
                [card_o1, card_o2],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output with 3|0',
            skip_animations=True,
        )
        # ************************************************************
        # params
        self.play(card_m.update_params(
            {
                'split_size': 3,
                # 'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw tensor
        t_o1, t_o2, t_o3, t_o4 = torch.split(t_i1, 3, dim=0)

        # tensor mobs
        tensor_os = VGroup(
            MTensor_1D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ).align_to(tensor_i1[idx:], UL)
            for idx, t in zip(
                [0, 3, 6, 9],
                [t_o1, t_o2, t_o3, t_o4]
            )
        )

        # fade in tensor
        self.play(AnimationGroup(
            *(FadeIn(tensor_o) for tensor_o in tensor_os),
            lag_ratio=0.0,
            run_time=wt*0.1,
        ))

        # split animation
        tensor_os.generate_target()
        tensor_os.target.shift(DOWN*TENSOR_VGAP_1D*2)
        orig_center = tensor_os.target.get_center()
        tensor_os.target.arrange(RIGHT, buff=TENSOR_HGAP_1D).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))
        self.wait(wt)

        # new card
        card_o3 = InfoCard('out_3').hide_to_corner(DOWN)
        card_o4 = InfoCard('out_4').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o3, card_o4)
        self.play(attach_to_ref(
            VGroup(card_o3, card_o4),
            card_o2,
            DOWN,
            run_time=wt,
        ))

        # card summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                 [card_o1, card_o2, card_o3, card_o4],
                 [t_o1, t_o2, t_o3, t_o4],
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    direction=RIGHT,
                    anim=ShrinkToCenter,
                    gargs={'lag_ratio': 0.5},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                tensor_os,
                [card_o1, card_o2, card_o3, card_o4],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output with [1,3,4,2]|0',
            skip_animations=True,
        )
        # ************************************************************
        # params
        self.play(card_m.update_params(
            {
                'split_size': [1,3,4,2],
                # 'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw tensor
        t_o1, t_o2, t_o3, t_o4 = torch.split(t_i1, [1,3,4,2], dim=0)

        # tensor mobs
        tensor_os = VGroup(
            MTensor_1D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ).align_to(tensor_i1[idx:], UL)
            for idx, t in zip(
                [0, 1, 4, 8],
                [t_o1, t_o2, t_o3, t_o4]
            )
        )

        # fade in tensor
        self.play(AnimationGroup(
            *(FadeIn(tensor_o) for tensor_o in tensor_os),
            lag_ratio=0.0,
            run_time=wt*0.1,
        ))

        # split animation
        tensor_os.generate_target()
        tensor_os.target.shift(DOWN*TENSOR_VGAP_1D*2)
        orig_center = tensor_os.target.get_center()
        tensor_os.target.arrange(RIGHT, buff=TENSOR_HGAP_1D).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))
        self.wait(wt)

        # card summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                 [card_o1, card_o2, card_o3, card_o4],
                 [t_o1, t_o2, t_o3, t_o4],
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean merged
        
        # ************************************************************
        self.next_section(
            'clean everything',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    direction=RIGHT,
                    anim=ShrinkToCenter,
                    gargs={'lag_ratio': 0.5},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [tensor_i1] + list(tensor_os),
                [card_i1, card_o1, card_o2, card_o3, card_o4],
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))

        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_o1, DOWN),
            detach_to_ref(card_o2, DOWN),
            detach_to_ref(card_o3, DOWN),
            detach_to_ref(card_o4, DOWN),
            card_m.update_params(
                {
                    'split_size': UNKNOWN,
                    'dim': UNKNOWN,
                },
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
from manim import *

from utils.mtensor import MTensor_3D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_3D = 1.0
TENSOR_HGAP_3D = 1.0
TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # cards
        card_m, _ = import_mobs('030a')

        # input raw tensor
        t_i1 = torch.randn(4,5,6)

        # input tensor mob
        tensor_i1 = MTensor_3D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        )

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
            skip_animations=False,
        )
        # ************************************************************
        # input tensor
        self.play(tensor_i1.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
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
            'compute output with 2|0',
            skip_animations=False,
        )
        # ************************************************************
        # params
        self.play(card_m.update_params(
            {
                'split_size': 2,
                'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw tensor
        t_o1, t_o2 = torch.split(t_i1, 2, dim=0)

        # tensor mob
        tensor_os = VGroup(
            MTensor_3D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ).align_to(
                tensor_i1[idx:],
                UL+OUT,
            ) for t, idx in zip(
                [t_o1, t_o2],
                [0, 2]
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
        tensor_os.target.align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )
        orig_center = tensor_os.target.get_center()
        tensor_os.target.arrange(IN, buff=TENSOR_EGAP_3D).move_to(orig_center)
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
                    style='beam',
                    direction=IN,
                    anim=ShrinkToCenter,
                    gargs={},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                tensor_os,
                [card_o1, card_o2],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output with 3|0',
            skip_animations=False,
        )
        # ************************************************************
        # params
        self.play(card_m.update_params(
            {
                'split_size': 3,
                'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw tensor
        t_o1, t_o2 = torch.split(t_i1, 3, dim=0)

        # tensor mob
        tensor_os = VGroup(
            MTensor_3D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ).align_to(
                tensor_i1[idx:],
                UL+OUT,
            ) for t, idx in zip(
                [t_o1, t_o2],
                [0, 3]
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
        tensor_os.target.align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )
        orig_center = tensor_os.target.get_center()
        tensor_os.target.arrange(IN, buff=TENSOR_EGAP_3D).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))
        self.wait(wt)

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
                    style='beam',
                    direction=IN,
                    anim=ShrinkToCenter,
                    gargs={},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                tensor_os,
                [card_o1, card_o2],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output with 2|1',
            skip_animations=False,
        )
        # ************************************************************
        # params
        self.play(card_m.update_params(
            {
                'split_size': 2,
                'dim': 1,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw tensor
        t_o1, t_o2, t_o3 = torch.split(t_i1, 2, dim=1)

        # tensor mob
        tensor_os = VGroup(
            MTensor_3D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ).align_to(
                tensor_i1[:,idx:],
                UL+OUT,
            ) for t, idx in zip(
                [t_o1, t_o2, t_o3],
                [0, 2, 4]
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
        tensor_os.target[0].align_to(
            ORIGIN,
            UP,
        )
        tensor_os.target[1].next_to(
            tensor_os.target[0],
            DOWN,
            buff=TENSOR_VGAP_3D,
        )
        tensor_os.target[2].next_to(
            tensor_os.target[1],
            DOWN,
            buff=TENSOR_VGAP_3D,
        )
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))
        self.wait(wt)

        # new card
        card_o3 = InfoCard('out_3').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o3)
        self.play(attach_to_ref(
            card_o3,
            card_o2,
            DOWN,
            run_time=wt,
        ))

        # card summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                [card_o1, card_o2, card_o3],
                [t_o1, t_o2, t_o3]
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                    anim=ShrinkToCenter,
                    gargs={},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                tensor_os,
                [card_o1, card_o2, card_o3],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
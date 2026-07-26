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
            skip_animations=True,
        )
        # ************************************************************
        # cards
        card_m, _ = import_mobs('031a')

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_m,
        )   # tensor not added while it's ok
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,4,5)(2,4,5) -[0]- (5,4,5)',
            skip_animations=True,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(3,4,5)
        t_i2 = torch.randn(2,4,5)
        t_o1 = torch.cat([t_i1, t_i2], dim=0)

        # input tensor mob
        tensor_is = VGroup(
            MTensor_3D(
                array=t,
                **MEDIUM_CUBE_CONFIG,
            ) for t in [t_i1, t_i2]
        ).arrange(
            IN,
            buff=TENSOR_EGAP_3D,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        )

        # output tensor mob
        tensor_o1 = MTensor_3D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        # show input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                style='beam',
                direction=OUT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={},
            ) for tmob in tensor_is),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # show input summary
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        card_i2 = InfoCard('in_2').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i1, card_i2)
        self.play(attach_to_ref(
            VGroup(card_i1, card_i2),
            card_m,
            UP,
            run_time=wt,
        ))
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

        # show compute output
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(tensor_is_copy.target, [0, 3]):
            tmob.align_to(
                tensor_o1[idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.remove(tensor_is_copy)
        self.add(tensor_o1)
        self.wait(wt)

        # show output summary
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1)
        self.play(attach_to_ref(
            card_o1,
            card_m,
            DOWN,
            run_time=wt,
        ))
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
                    anim=ShrinkToCenter,
                    gargs={},
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
            skip_animations=True,
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

        # failed compute
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
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # clean input 1
        self.play(AnimationGroup(
            tensor_is[0].uncreate(
                style='beam',
                direction=IN,
                anim=ShrinkToCenter,
                gargs={},
            ),
            card_i1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(2,3,5)(2,4,5) -[1]- (2,7,5)',
            skip_animations=True,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.rand(2,3,5)
        t_o1 = torch.cat([t_i1, t_i2], dim=1)

        # input tensor mob
        tensor_i1 = MTensor_3D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).next_to(
            tensor_is[1],
            UP,
            buff=TENSOR_VGAP_3D,
        )
        tensor_is = VGroup(tensor_i1, tensor_is[1])

        # output tensor mob
        tensor_o1 = MTensor_3D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            RIGHT*TENSOR_HGAP_3D,
            LEFT,
        )

        # show input tensor
        self.play(tensor_i1.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
        ))

        # show input summary
        self.play(card_i1.expand_summary(
            t2s(t_i1),
            run_time=wt,
        ))
        self.wait(wt)

        # show compute output
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(tensor_is_copy.target, [0, 3]):
            tmob.align_to(
                tensor_o1[:,idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.remove(tensor_is_copy)
        self.add(tensor_o1)
        self.wait(wt)

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
                    anim=ShrinkToCenter,
                    gargs={},
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
            skip_animations=True,
        )
        # ************************************************************
        # raw tensor
        t_i2 = torch.randn(2,3,2)
        t_o1 = torch.cat([t_i1, t_i2], dim=2)

        tensor_i2 = MTensor_3D(
            array=t_i2,
            **MEDIUM_CUBE_CONFIG,
        ).next_to(
            tensor_is[0],
            RIGHT,
            buff=TENSOR_HGAP_3D,
        )
        tensor_is = VGroup(tensor_is[0], tensor_i2)

        # output tensor mob
        tensor_o1 = MTensor_3D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        # show input tensor
        self.play(tensor_i2.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
        ))

        # show input summary
        self.play(card_i2.expand_summary(
            t2s(t_i2),
            run_time=wt,
        ))
        self.wait(wt)

        # update params
        self.play(card_m.update_params(
            {
                'dim': 2,
            },
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
        self.wait(wt)

        # show compute output
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(tensor_is_copy.target, [0, 5]):
            tmob.align_to(
                tensor_o1[:,:,idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.remove(tensor_is_copy)
        self.add(tensor_o1)
        self.wait(wt)

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
                    anim=ShrinkToCenter,
                    gargs={},
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
            '(3,3,5)(2,3,5)(4,3,5) -[0]- (9,3,5)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i2 = t_i1
        t_i1 = torch.randn(3,3,5)
        t_i3 = torch.randn(4,3,5)
        t_o1 = torch.cat([t_i1, t_i2, t_i3], dim=0)

        # input tensor mob
        tensor_i2 = tensor_i1
        tensor_i1 = MTensor_3D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).next_to(
            tensor_i2,
            OUT,
            TENSOR_EGAP_3D,
        )
        tensor_i3 = MTensor_3D(
            array=t_i3,
            **MEDIUM_CUBE_CONFIG,
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

        # output tensor mob
        tensor_o1 = MTensor_3D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
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

        # show input tensor
        self.play(AnimationGroup(
            *(tmob.create(
                style='beam',
                direction=RIGHT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={},
            ) for tmob in [tensor_i1, tensor_i3]),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # show input summary
        card_i3 = InfoCard('in_3').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i3)
        card_i1.add(card_i1.smob)       # FIXME
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
        self.wait(wt)

        # show compute output
        tensor_is_copy = tensor_is.copy()
        self.play(FadeIn(
            tensor_is_copy,
            run_time=wt*0.1,
        ))
        tensor_is_copy.generate_target()
        for tmob, idx in zip(tensor_is_copy.target, [0, 3, 5]):
            tmob.align_to(
                tensor_o1[idx:],
                UL+OUT
            )
        self.play(MoveToTarget(
            tensor_is_copy,
            run_time=wt,
        ))
        self.remove(tensor_is_copy)
        self.add(tensor_o1)
        self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1),
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
                    style='beam',
                    direction=RIGHT,
                    anim=Unwrite,
                    gargs={},
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                list(tensor_is) + [tensor_o1],
                [card_i1, card_i2, card_i3, card_o1]
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))

        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_i2, UP),
            detach_to_ref(card_i3, UP),
            detach_to_ref(card_o1, DOWN),
            card_m.update_params(
                {
                    'dim': UNKNOWN,
                },
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
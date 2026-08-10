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
            skip_animations=True,
        )
        # ************************************************************
        # cards
        cards = import_mobs('030c')
        (
            card_i1, card_m, card_o1, card_o2,
        ) = cards

        # raw input tensor
        t_i1 = torch.randn(4,5,6)

        # input tensor mob
        tensor_i1 = MTensor3D(
            array=t_i1,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        )

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=True,
        )
        # ************************************************************
        # introduce input tensor
        self.play(AnimationGroup(
            tensor_i1.create(
                style='beam',
                direction=OUT,
            ),
            card_i1.expand_summary(
                t2s(t_i1),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(4,5,6) -[2|0]- (2,5,6)(2,5,6)',
            skip_animations=True,
        )
        # ************************************************************
        # update module card
        self.play(card_m.update_params(
            {
                'split_size': 2,
                'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw output tensors
        t_o1, t_o2 = torch.split(t_i1, 2, dim=0)

        # output tensor mobs
        tensor_os = VGroup(
            MTensor3D(
                array=t,
                mode='cube',
                **MEDIUM_TENSOR_CONFIG,
            ).align_to(tensor_i1[idx:], UL+OUT)
            for idx, t in zip(
                [0, 2],
                [t_o1, t_o2]
            )
        )

        # fade in out tensor mobs
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
        tensor_os.target.arrange(
            IN,
            buff=TENSOR_EGAP_3D,
        ).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))

        # expand output cards summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                 [card_o1, card_o2],
                 [t_o1, t_o2],
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean outputs
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
                tensor_os,
                [card_o1, card_o2],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(4,5,6) -[3|0]- (3,5,6)(1,5,6)',
            skip_animations=True,
        )
        # ************************************************************
        # update module card
        self.play(card_m.update_params(
            {
                'split_size': 3,
                # 'dim': 0,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw output tensors
        t_o1, t_o2 = torch.split(t_i1, 3, dim=0)

        # output tensor mobs
        tensor_os = VGroup(
            MTensor3D(
                array=t,
                mode='cube',
                **MEDIUM_TENSOR_CONFIG,
            ).align_to(tensor_i1[idx:], UL+OUT)
            for idx, t in zip(
                [0, 3],
                [t_o1, t_o2]
            )
        )

        # fade in out tensor mobs
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
        tensor_os.target.arrange(
            IN,
            buff=TENSOR_EGAP_3D,
        ).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))

        # expand output cards summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                 [card_o1, card_o2],
                 [t_o1, t_o2],
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean outputs
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
                tensor_os,
                [card_o1, card_o2],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(4,5,6) -[2|1]- (4,2,6),(4,2,6),(4,1,6)',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(card_m.update_params(
            {
                'split_size': 2,
                'dim': 1,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # reposition input tensor
        tensor_i1.save_state()
        self.play(tensor_i1.animate(
            run_time=wt,
        ).center().align_to(
            LEFT*TENSOR_HGAP_3D,
            RIGHT,
        ))

        # raw output tensors
        t_o1, t_o2, t_o3 = torch.split(t_i1, 2, dim=1)

        # output tensor mobs
        tensor_os = VGroup(
            MTensor3D(
                array=t,
                mode='cube',
                **MEDIUM_TENSOR_CONFIG,
            ).align_to(tensor_i1[:,idx:], UL+OUT)
            for idx, t in zip(
                [0, 2, 4],
                [t_o1, t_o2, t_o3]
            )
        )

        # fade in out tensor mobs
        self.play(AnimationGroup(
            *(FadeIn(tensor_o) for tensor_o in tensor_os),
            lag_ratio=0.0,
            run_time=wt*0.1,
        ))

        # split animation
        tensor_os.generate_target()
        tensor_os.target.align_to(
            RIGHT*TENSOR_HGAP_3D,
            LEFT,
        )
        orig_center = tensor_os.target.get_center()
        tensor_os.target.arrange(
            DOWN,
            buff=TENSOR_VGAP_3D,
        ).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))

        # new output card
        card_o3 = InfoCard('out_3').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o3)
        self.play(attach_to_ref(
            card_o3,
            card_o2,
            DOWN,
            run_time=wt,
        ))

        # expand output cards summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                [card_o1, card_o2, card_o3],
                [t_o1, t_o2, t_o3],
             )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean outputs
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=LEFT,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [*tensor_os],
                [card_o1, card_o2, card_o3],
            )),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # restore input tensor position
        self.play(tensor_i1.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(4,5,6) -[2|2]- (4,5,2),(4,5,2),(4,5,2)',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(card_m.update_params(
            {
                # 'split_size': 2,
                'dim': 2,
            },
            run_time=wt,
        ))
        self.wait(wt)

        # raw output tensors
        t_o1, t_o2, t_o3 = torch.split(t_i1, 2, dim=2)

        # output tensor mobs
        tensor_os = VGroup(
            MTensor3D(
                array=t,
                mode='cube',
                **MEDIUM_TENSOR_CONFIG,
            ).align_to(tensor_i1[:,:,idx:], UL+OUT)
            for idx, t in zip(
                [0, 2, 4],
                [t_o1, t_o2, t_o3]
            )
        )

        # fade in out tensor mobs
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
        tensor_os.target.arrange(
            RIGHT,
            buff=TENSOR_HGAP_3D,
        ).move_to(orig_center)
        self.play(MoveToTarget(
            tensor_os,
            run_time=wt,
        ))

        # expand output cards summary
        self.play(AnimationGroup(
            *(cmob.expand_summary(t2s(t))
             for cmob, t in zip(
                [card_o1, card_o2, card_o3],
                [t_o1, t_o2, t_o3],
             )),
            lag_ratio=0.5,
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
            ) for tmob in [tensor_i1, *tensor_os]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink tensor cards
        self.play(AnimationGroup(
            *(cmob.shrink_summary()
              for cmob in [card_i1, card_o1, card_o2, card_o3]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # remove tensor cards
        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_o1, DOWN),
            detach_to_ref(card_o2, DOWN),
            detach_to_ref(card_o3, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(card_m.shrink_params(
            run_time=wt,
        ))
        self.wait(wt)
from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
import torch
import numpy as np

TENSOR_VGAP_3D = 1.0
TENSOR_HGAP_3D = 0.7
# TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # module card
        card_module = import_mobs('035b')

        # raw module, no visible module
        torch_module = torch.nn.Sigmoid()

        # raw tensor
        t_i1 = torch.randn(1, 5, 3, 4)
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            TENSOR_VGAP_3D*UP,
            DOWN,
        )

        # output tensor mob
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            TENSOR_VGAP_3D*DOWN,
            UP,
        )

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=False,
        )
        # ************************************************************
        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        # self.wait(wt)

        # show input summary
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i1)
        self.play(attach_to_ref(
            card_i1,
            card_module,
            UP,
            run_time=wt,
        ))
        self.play(card_i1.expand_summary(
            t2s(t_i1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*5,
            ),
            mob_o1.create(
                style='series',
                direction=RIGHT,
                run_time=wt*5,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # show output summary
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1)
        self.play(attach_to_ref(
            card_o1,
            card_module,
            DOWN,
            run_time=wt,
        ))
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean input/output',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [mob_i1, mob_o1],
                [card_i1, card_o1],
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
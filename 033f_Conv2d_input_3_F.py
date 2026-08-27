from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
import torch

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load mobs and torch module
        (
            card_i1,
            card_module,
            card_o1,
            mob_module,
        ) = import_mobs('032e')
        mob_weight = mob_module.mt_weight
        torch_module = mob_module.module
        module_config = mob_module.module_config

        # raw tensor
        t_i1 = torch.randn(1, 3, 5, 6)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_module,
            UP,
            TENSOR_VGAP_3D,
        )

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(3,5,6) -[Conv2d]- FAILURE',
            skip_animations=False,
        )
        # ************************************************************
        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        self.wait(wt)

        # show input summary
        self.play(card_i1.expand_summary(
            t2s(t_i1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'failed compute loop',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_weight.breath(
                style='whole',
                lag_ratio=0.0,
            ),
            card_module.suggest_failure(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'i want another in_channels for module',
            skip_animations=False,
        )
        # ************************************************************
        # clean module weight
        # FIXME: or uncreate whole module?
        self.play(mob_weight.uncreate(
            style='beam',
            direction=IN,
            anim=Unwrite,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
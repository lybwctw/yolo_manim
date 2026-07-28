from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor_3D
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
            skip_animations=True,
        )
        # ************************************************************
        # load mobs and torch module
        (
            card_i1,
            card_module,
            card_o1,
            mob_module,
        ) = import_mobs('032b')
        torch_module = mob_module.module
        module_config = mob_module.module_config

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(4,5,6) -[Conv2d]- FAILURE',
            skip_animations=True,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(1, 4, 5, 6)

        # input tensor mob
        mob_i1 = MTensor_3D(
            array=t_i1.detach()[0],
            **SMALL_3D_CUBE_CONFIG,
        ).next_to(
            mob_module,
            UP,
            TENSOR_VGAP_3D,
        )

        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
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
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            AnimationGroup(
                *(mob.animate(
                    rate_func=rate_functions.there_and_back,
                ).scale(0.8)
                for mob in mob_i1.mobs),
                lag_ratio=0.0,
            ),
            card_module.suggest_failure(),
            lag_ratio=0.0,
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean module weights',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mob_module.mobs_weight.uncreate(
            style='beam',
            direction=IN,
            anim=Unwrite,
            gargs={},
            ggargs={
                'lag_ratio': 0.5,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        card_i1.add(card_i1.smob)       # FIXME

        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by 032f
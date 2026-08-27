from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *
import torch
import numpy as np

FONT_SIZE_FORMULA = 24
FORMULA_V_OFFSET = 2.5
FORMULA_V_OFFSET_FOCUS = 3.0
FORMULA_H_OFFSET_FOCUS = 2.2
SUB_BUFF = 0.1

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
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
        # load mobs and torch module
        (
            card_i1,
            card_module,
            card_o1,
            mob_module,
        ) = import_mobs('039c')
        torch_module = mob_module.module
        mob_running_mean = mob_module.mt_running_mean
        mob_running_var = mob_module.mt_running_var
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias
        module_config = mob_module.module_config

        # raw tensor
        t_i1 = torch.randn(1, 6, 4, 5)
        torch_module.eval()             # important
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_weight,
            UP,
            TENSOR_VGAP_3D,
        )

        # output tensor mob
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_module,
            DOWN,
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
            'show input',
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
            'loop into output, layer style',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.breath(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            mob_running_mean.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_running_var.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_weight.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_bias.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_o1.create(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))
        # self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        # remove input/output
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
        # self.wait(wt)

        # remove module
        self.play(AnimationGroup(
            *(mob.uncreate(
                style='series',
                direction=RIGHT,
            ) for mob in [
                mob_running_mean,
                mob_running_var,
                mob_weight,
                mob_bias,
            ]),
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
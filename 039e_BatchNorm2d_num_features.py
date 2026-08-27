from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *

from modules.pt_BatchNorm2d import *

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

NEW_CONFIG = {
    'num_features': 8,
    'eps': 1e-5,
    'momentum': 0.1,
    'affine': True,
    'track_running_stats': True,
}

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
        ) = import_mobs('039d')

        # raw module with random init
        module_config = NEW_CONFIG
        torch_module = torch.nn.BatchNorm2d(**module_config)

        # mob module, not random initialized
        # prepare for the init issue
        mob_module = PT_BatchNorm2d(
            module=torch_module,
            module_config=module_config,
            mtensor_dir=RIGHT,
            mtensor_gap=0.5,        # closer after introduction
        )
        mob_running_mean = mob_module.mt_running_mean
        mob_running_var = mob_module.mt_running_var
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # raw tensor
        t_i1 = torch.randn(1, 8, 3, 5)
        torch_module.eval()             # important
        t_o1 = torch_module(t_i1)

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
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'new module',
            skip_animations=False,
        )
        # ************************************************************
        # update module card config
        self.play(card_module.update_params(
            {
                'num_features': module_config['num_features'],
            },
            run_time=wt,
        ))
        self.wait(wt)

        # show new module
        self.play(mob_module.create(
            run_time=wt,
        ))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'tags on module params',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # tag assets
        # formula = MathTex(
        #     r"y = \frac{x-\mu}{\sqrt{\sigma^2+\epsilon}} \cdot \gamma + \beta",
        #     font_size=FONT_SIZE_FORMULA,
        # ).shift(UP*FORMULA_V_OFFSET)
        # tag_running_mean = NameTag(
        #     ref=p2f(self, mob_running_mean[-1].get_corner(DL+IN)),
        #     text='μ',
        #     leader_direction=DR,
        # )
        # tag_running_var = NameTag(
        #     ref=p2f(self, mob_running_var[-1].get_corner(DL+IN)),
        #     text='σ²',
        #     leader_direction=DR,
        # )
        # tag_weight = NameTag(
        #     ref=p2f(self, mob_weight[-1].get_corner(DL+IN)),
        #     text='γ',
        #     leader_direction=DR,
        # )
        # tag_bias = NameTag(
        #     ref=p2f(self, mob_bias[-1].get_corner(DL+IN)),
        #     text='β',
        #     leader_direction=DR,
        # )

        # # show tags
        # self.play(AnimationGroup(
        #     tag_running_mean.create(),
        #     tag_running_var.create(),
        #     tag_weight.create(),
        #     tag_bias.create(),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # hide tags
        # self.play(AnimationGroup(
        #     tag_running_mean.uncreate(),
        #     tag_running_var.uncreate(),
        #     tag_weight.uncreate(),
        #     tag_bias.uncreate(),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.wait(wt)

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

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_module,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
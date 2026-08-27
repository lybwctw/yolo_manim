from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *

from modules.pt_Conv2d import *

import torch
import numpy as np

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0
BIAS_GAP_BIG = 1.5
BIAS_GAP_SMALL = 0.8

INIT_CONFIG = {
    'in_channels': 4,
    'out_channels': 7,
    'kernel_size': 2,
    'stride': 1,
    'padding': 1,
    'bias': True,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

CONFIG_1 = {
    'in_channels': 5,           # updated
    'out_channels': 4,          # updated
    'kernel_size': 3,           # updated
    'stride': 1,
    'padding': 1,
    'bias': True,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

CONFIG_2 = {
    'in_channels': 6,           # updated
    'out_channels': 5,          # updated
    'kernel_size': 3,           # updated
    'stride': 1,
    'padding': 1,
    'bias': False,              # updated
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load cards and input
        (
            card_i1,
            card_module,
            card_o1,
            mob_module,
        ) = import_mobs('032p')

        # raw module and manim module
        module_config = INIT_CONFIG     # already synced with module mob
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

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
            'show exact values of module',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_weight.switch(
                style='beam',
                direction=IN,
                run_time=wt*3,
            ),
            mob_bias.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))

        # new view
        self.move_camera(
            **VIEW_INTRO,
            zoom=1.5,
            added_anims=[
                VGroup(mob_weight, mob_bias).animate.arrange(
                    DOWN,
                    buff=BIAS_GAP_BIG,      # more gap
                ),
            ],
            run_time=wt*3,
        )

        # FIXME: make groups closer
        vgs = VGroup(VGroup(mob_weight[i], mob_bias[i])
            for i in range(mob_weight.shape[0]))
        self.play(vgs.animate(
            run_time=wt,
        ).arrange(RIGHT, buff=0.3))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'tags on weight and bias',
            skip_animations=True,
        )
        # ************************************************************
        ref_weight = mob_weight[0].get_corner(UL+OUT)
        ref_bias = mob_bias[-1].get_corner(DR+OUT)
        tag_weight = NameTag(
            ref=p2f(self, ref_weight),
            text='weight',
            leader_direction=UR,
        )
        tag_bias = NameTag(
            ref=p2f(self, ref_bias),
            text='bias',
            leader_direction=DL,
        )
        self.play(AnimationGroup(
            tag_weight.create(),
            tag_bias.create(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'zero init thinking',
            skip_animations=True,
        )
        # ************************************************************
        t_weight = mob_weight.array
        t_bias = mob_bias.array
        z_weight = np.zeros_like(t_weight)
        z_bias = np.zeros_like(t_bias)

        # to zeros
        self.play(AnimationGroup(
            mob_weight.update_values(
                values=z_weight,
            ),
            mob_bias.update_values(
                values=z_bias,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # back to truth
        self.play(AnimationGroup(
            mob_weight.update_values(
                values=t_weight,
            ),
            mob_bias.update_values(
                values=t_bias,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'weight range and bias range',
            skip_animations=True,
        )
        # ************************************************************
        # init range mobs
        cin, ks = module_config['in_channels'], module_config['kernel_size']
        bound = 1 / (cin * ks * ks) ** 0.5
        range_weight = MathTex(
            rf"\left("
            rf"-\frac{{1}}{{\sqrt{{{cin}\times{ks}\times{ks}}}}},\;"
            rf"\frac{{1}}{{\sqrt{{{cin}\times{ks}\times{ks}}}}}"
            rf"\right)"
            rf"\approx (-{bound:.2f},\;{bound:.2f})"
        ).scale(0.4)
        range_bias = range_weight.copy()
        range_weight.next_to(tag_weight, RIGHT).shift(UP*0.2)
        range_bias.next_to(tag_bias, LEFT).shift(DOWN*0.2)

        # show range for weight
        self.add_fixed_in_frame_mobjects(range_weight)
        self.play(AnimationGroup(
            Write(range_weight),
            run_time=wt*3,
        ))
        self.wait(wt)

        # show range for bias
        self.add_fixed_in_frame_mobjects(range_bias)
        self.play(AnimationGroup(
            Write(range_bias),
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean current module',
            skip_animations=True,
        )
        # ************************************************************
        # clean range and tag
        self.play(AnimationGroup(
            Succession(
                Unwrite(range_weight),
                tag_weight.uncreate(),
            ),
            Succession(
                Unwrite(range_bias),
                tag_bias.uncreate(),
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # clean weight and bias
        self.play(AnimationGroup(
            mob_weight.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
                lag_ratio=0.5,          # between blocks
                run_time=wt,
            ),
            mob_bias.uncreate(
                style='series',
                direction=LEFT,
                anim=Unwrite,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'new module',
            skip_animations=True,
        )
        # ************************************************************
        # prepare mobs
        module_config = CONFIG_1
        torch_module = torch.nn.Conv2d(**module_config)
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=module_config,
            block_gap=0.5,
            bias_offset=BIAS_GAP_BIG,
            init_mode='card',
        ).center()
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # update params
        self.play(card_module.update_params(
            params={
                'in_channels': module_config['in_channels'],
                'out_channels': module_config['out_channels'],
                'kernel_size': module_config['kernel_size'],
            },
            run_time=wt,
        ))

        # show new module
        self.play(AnimationGroup(
            mob_module.create(
                wargs={'run_time': wt},
                bargs={'run_time': wt},
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'new tags',
            skip_animations=True,
        )
        # ************************************************************
        ref_weight = mob_weight[0].get_corner(UL+OUT)
        ref_bias = mob_bias[-1].get_corner(DR+OUT)
        tag_weight = NameTag(
            ref=p2f(self, ref_weight),
            text='weight',
            leader_direction=UR,
        )
        tag_bias = NameTag(
            ref=p2f(self, ref_bias),
            text='bias',
            leader_direction=DL,
        )
        self.play(AnimationGroup(
            tag_weight.create(),
            tag_bias.create(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # ************************************************************
        self.next_section(
            'new ranges',
            skip_animations=True,
        )
        # ************************************************************
        # init range mobs
        cin, ks = module_config['in_channels'], module_config['kernel_size']
        bound = 1 / (cin * ks * ks) ** 0.5
        range_weight = MathTex(
            rf"\left("
            rf"-\frac{{1}}{{\sqrt{{{cin}\times{ks}\times{ks}}}}},\;"
            rf"\frac{{1}}{{\sqrt{{{cin}\times{ks}\times{ks}}}}}"
            rf"\right)"
            rf"\approx (-{bound:.2f},\;{bound:.2f})"
        ).scale(0.4)
        range_bias = range_weight.copy()
        range_weight.next_to(tag_weight, RIGHT).shift(UP*0.2)
        range_bias.next_to(tag_bias, LEFT).shift(DOWN*0.2)

        # show ranges
        self.add_fixed_in_frame_mobjects(range_weight)
        self.add_fixed_in_frame_mobjects(range_bias)
        self.play(AnimationGroup(
            Write(range_weight),
            Write(range_bias),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean current module',
            skip_animations=False,
        )
        # ************************************************************
        # clean range and tag
        self.play(AnimationGroup(
            Succession(
                Unwrite(range_weight),
                tag_weight.uncreate(),
            ),
            Succession(
                Unwrite(range_bias),
                tag_bias.uncreate(),
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # clean weight and bias
        self.play(AnimationGroup(
            mob_weight.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
                lag_ratio=0.5,          # between blocks
                run_time=wt,
            ),
            mob_bias.uncreate(
                style='series',
                direction=LEFT,
                anim=Unwrite,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean cards',
            skip_animations=False,
        )
        # ************************************************************
        # remove tensor cards
        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_o1, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(card_module.shrink_params(
            run_time=wt,
        ))
        self.wait(wt)
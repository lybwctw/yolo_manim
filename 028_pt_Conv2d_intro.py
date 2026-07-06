from manim import *

from utils.modules_pt import PT_Conv2d
from utils.name_card import NameCard
from utils.mtensor import MTensor, MCube
from utils.show_shape import ShowShape, HideShape
from utils.general import export_mobs
from utils.constants import *
from utils.constant_modules import *

import torch

# TODO: reference image

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        self.set_camera_orientation(
            **VIEW_INTRO,
        )

        card = NameCard(
            name='conv2d',
            params={
                'in_channels': 6,
                'out_channels': 5,
                'kernel_size': 3,
                'stride': 1,
                'padding': 1,
                'bias': False,
                'dilation': 1,
                'groups': 1,
                'padding_mode': 'zeros',
            },
            levels={
                'in_channels': 0,
                'out_channels': 0,
                'kernel_size': 0,
                'stride': 0,
                'padding': 0,
                'bias': 0,
                'dilation': 1,
                'groups': 1,
                'padding_mode': 1,
            },
        ).to_edge(LEFT).shift(UP*.5).set_z_index(999)

        # real conv layer
        conv = torch.nn.Conv2d(
            in_channels=6,
            out_channels=5,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
            dilation=1,
            groups=1,
            padding_mode='zeros',
        )

        module = PT_Conv2d(
            array=conv.weight,
            size=SMALL_CUBE_SIZE,
            mode='cube',
            padding=0.0,
            buff=0.3,
            cube_config={},
            square_config={},
            decimal_config={'font_size': SMALL_FONT_SIZE},
        ).center()

        # ************************************************************
        self.next_section(
            'introduce cubes',
            skip_animations=False,
        )
        # ************************************************************
        self.play(module.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={
                'lag_ratio': 0.1,
                'run_time': wt,
            },
        ))
        self.add(module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce name card',
            skip_animations=False,
        )
        # ************************************************************
        self.camera.add_fixed_in_frame_mobjects(card)
        self.play(Create(
            card,
            run_time=wt,
        ))
        self.wait(wt)

        # show shapes on module
        self.play(ShowShape(
            module,
            text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # highlight option 1 and shape text 1
        op1 = card.value_mob('in_channels')
        st1 = module.shape_texts[1]
        self.play(AnimationGroup(
            op1.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st1.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight option 2 and shape text 0
        op2 = card.value_mob('out_channels')
        st2 = module.shape_texts[0]
        self.play(AnimationGroup(
            op2.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st2.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight option 3 and shape text 2&3
        op3 = card.value_mob('kernel_size')
        st3a = module.shape_texts[2]
        st3b = module.shape_texts[3]
        self.play(AnimationGroup(
            op3.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st3a.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            st3b.animate(
                rate_func=rate_functions.there_and_back,
            ).scale(2.0).set_color(PURE_RED),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes on module
        self.play(HideShape(
            module,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # prepare for compute demo
        self.move_camera(
            run_time=wt,
            **VIEW_COMPUTE,
        )
        self.wait(wt)

        mobs = Group(card, module)
        export_mobs(__file__, mobs)     # NOTE, used by 029

        # self.play(module.switch_mode(
        #     style='beam',
        #     direction=OUT,
        #     aargs={'lag_ratio': 0.5},
        #     gargs={},
        #     ggargs={
        #         'lag_ratio': 0.5,
        #         'run_time': wt,
        #     },
        # ))
        # self.wait(wt)
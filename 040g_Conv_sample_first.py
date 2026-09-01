# ************************************************************
# Visualize first Conv sample from yolov8 series (3 classes).
# ************************************************************
from manim import *
import csv
from pathlib import Path

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

from modules.ut_Conv import *
from modules.pt_Conv2d import *
from modules.pt_BatchNorm2d import *
from modules.ut_Conv import *

from ultralytics.nn.modules import Conv

SIDE_LENGTH_MINI = 0.2

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

wt = 0.5

class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load sample cards
        cards = import_mobs('040f')

        # show initial reference card
        self.set_camera_orientation(
            **VIEW_COMPUTE,
            zoom=1.0,
            focal_distance=80,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'start with [3 16 3 2 1]',
            skip_animations=False,
        )
        # ************************************************************
        # TODO: highlight current card
        # assets
        config_module = {
            'c1': 3,
            'c2': 16,
            'k': 3,
            's': 2,
            'p': 1,
        }

        # highlight first sample card
        mask = np.zeros(len(cards), dtype=bool)
        mask[0] = True
        self.play(highlight_card_index(
            cards=cards,
            mask=mask,
            run_time=wt,
        ))
        self.wait(wt)

        config_conv = Conv_2_conv_config(config_module)
        # config_bn =  Conv_2_bn_config(config_module)

        ut_module = Conv(**config_module)
        pt_conv = ut_module.conv
        pt_bn = ut_module.bn

        mm_conv = PT_Conv2d(
            module=pt_conv,
            module_config=config_conv,
            block_gap=0.2,
            weight_config={
                'side_length': SIDE_LENGTH_MINI,
            },
        )
        mm_bn = MTensor4D(
            array=np.random.randn(config_module['c2'],4,1,1),   # random value
            mode='cube',
            style='horizontal',
            side_length=SIDE_LENGTH_MINI,
        )
        for idx in range(mm_bn.shape[0]):
            mm_bn[idx].next_to(
                mm_conv.mt_weight[idx],
                DOWN,
                TENSOR_VGAP_SMALL,
            )

        VGroup(mm_conv, mm_bn).center()

        # show conv and bn
        self.play(AnimationGroup(
            mm_conv.mt_weight.create(
                style='beam',
                direction=OUT,
                lag_ratio=0.1,
                run_time=wt*2,
            ),
            mm_bn.create(
                style='layer',
                direction=OUT,
                lag_ratio=0.1,
                run_time=wt*2,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'replace MTensor with FTensor',
            skip_animations=False,
        )
        # ************************************************************
        ut_conv = UT_Conv(
            module_config=config_module,
            ref_conv=mm_conv.mt_weight,
            ref_bn=mm_bn,
            n=config_module['c2'],
        )
        self.play(AnimationGroup(
            mm_conv.mt_weight.uncreate(
                style='beam',
                direction=OUT,
                lag_ratio=0.0,
                run_time=wt,
            ),
            mm_bn.uncreate(
                style='layer',
                direction=OUT,
                lag_ratio=0.0,
                run_time=wt,
            ),
            ut_conv.create(
                direction='bottom',
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'shapes on conv and bn',
            skip_animations=False,
        )
        # ************************************************************
        # more space between conv and bn
        self.move_camera(
            zoom=0.9,
            added_anims=[
                ut_conv.conv_bn.animate(
                    run_time=wt,
                ).arrange(
                    DOWN,
                    buff=TENSOR_VGAP_LARGE,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # show shapes
        self.play(AnimationGroup(
            *(ShowShape3D(
                self,
                mob,
                view='compute',
                lag_ratio=0.5,
            ) for mob in ut_conv.conv_bn),
            lag_ratio=0.0,
            run_time=wt*5,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            *(HideShape3D(
                mob,
                lag_ratio=0.0,
            ) for mob in ut_conv.conv_bn),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # less space between conv and bn
        self.move_camera(
            zoom=1.0,
            added_anims=[
                ut_conv.conv_bn.animate(
                    run_time=wt,
                ).arrange(
                    DOWN,
                    buff=TENSOR_VGAP_SMALL,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'export',
            skip_animations=False,
        )
        # ************************************************************
        mobs = VGroup(cards, ut_conv)
        export_mobs(__file__, mobs)     # NOTE: used by next
        # self.wait(wt)
        # self.play(ut_conv.stretch_direction(
        #     direction='erect',
        #     size_scale=2.0,
        #     shape=(6, 16, 3, 3),
        #     lag_ratio=0.5,
        #     run_time=wt*4,
        # ))
        # self.wait(wt)

        # self.play(ut_conv.stretch_direction(
        #     direction='horizontal',
        #     size_scale=1/3,
        #     shape=(6, 16, 1, 1),
        #     lag_ratio=0.5,
        #     run_time=wt*4,
        # ))
        # self.wait(wt)
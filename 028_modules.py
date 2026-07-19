from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.general import export_mobs
from utils.constants import *
from utils.constants_3d import *

from modules.pt_add import create_ic_add
from modules.pt_split import create_ic_split
from modules.pt_cat import create_ic_cat
from modules.pt_Conv2d import create_ic_Conv2d
from modules.pt_MaxPool2d import create_ic_MaxPool2d
from modules.pt_activations import create_ic_Sigmoid, create_ic_ReLU, create_ic_SiLU, create_ic_Softmax
from modules.pt_Linear import create_ic_Linear
from modules.pt_BatchNorm2d import create_ic_BatchNorm2d

from modules.ut_Conv import create_ic_Conv
from modules.ut_Bottleneck import create_ic_Bottleneck
from modules.ut_C2f import create_ic_C2f
from modules.ut_SPPF import create_ic_SPPF
from modules.ut_Detect import create_ic_Detect

import torch

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # pytorch module cards
        ic_add = create_ic_add()
        ic_split = create_ic_split()
        ic_cat = create_ic_cat()
        ic_Conv2d = create_ic_Conv2d()
        ic_MaxPool2d = create_ic_MaxPool2d()
        ic_Sigmoid = create_ic_Sigmoid()
        ic_ReLU = create_ic_ReLU()
        ic_SiLU = create_ic_SiLU()
        ic_Softmax = create_ic_Softmax()
        ic_Linear = create_ic_Linear()
        ic_BatchNorm2d = create_ic_BatchNorm2d()

        # ultralytics module cards
        ic_Conv = create_ic_Conv()
        ic_Bottleneck = create_ic_Bottleneck()
        ic_C2f = create_ic_C2f()
        ic_SPPF = create_ic_SPPF()
        ic_Detect = create_ic_Detect()

        # arrange cards into three groups
        ics_m = VGroup(
            ic_add, ic_split, ic_cat,
        ).arrange(RIGHT)
        ics_t = VGroup(
            ic_Conv2d, ic_MaxPool2d, ic_Sigmoid, ic_ReLU, ic_SiLU, ic_Softmax, ic_Linear, ic_BatchNorm2d,
        ).arrange(RIGHT)
        ics_u = VGroup(
            ic_Conv, ic_Bottleneck, ic_C2f, ic_SPPF, ic_Detect,
        ).arrange(RIGHT)
        VGroup(
            ics_m, ics_t, ics_u,
        ).arrange(DOWN, buff=0.5)

        ics_all = VGroup(
            ic_add, ic_split, ic_cat,
            ic_Conv2d, ic_MaxPool2d, ic_Sigmoid, ic_ReLU, ic_SiLU, ic_Softmax, ic_Linear, ic_BatchNorm2d,
            ic_Conv, ic_Bottleneck, ic_C2f, ic_SPPF, ic_Detect,
        )

        # show starting cards
        self.play(AnimationGroup(
            *(GrowFromCenter(
                card,
                rate_func=rate_functions.ease_out_back,
            ) for card in ics_all),
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait()

        # into left
        self.play(ics_all.animate(
            lag_ratio=0.0,
            run_time=0.5,
        ).arrange(
            DOWN,
            buff=0.1,
            aligned_edge=LEFT,
        ).to_edge(
            LEFT,
            buff=CARD_EDGE_BUFF,
        ))
        self.wait()

        export_mobs(__file__, ics_all)      # used by 029
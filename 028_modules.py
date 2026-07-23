from manim import *

from utils.general import export_mobs
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

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
        ic_add = InfoCard('add', frame_config={'fill_color': TEAL})
        ic_split = InfoCard('split', frame_config={'fill_color': TEAL})
        ic_cat = InfoCard('cat', frame_config={'fill_color': TEAL})
        ic_Conv2d = InfoCard('Conv2d', frame_config={'fill_color': ORANGE})
        ic_MaxPool2d = InfoCard('MaxPool2d', frame_config={'fill_color': ORANGE})
        ic_Upsample = InfoCard('Upsample', frame_config={'fill_color': ORANGE})
        ic_Sigmoid = InfoCard('Sigmoid', frame_config={'fill_color': ORANGE})
        ic_ReLU = InfoCard('ReLU', frame_config={'fill_color': ORANGE})
        ic_SiLU = InfoCard('SiLU', frame_config={'fill_color': ORANGE})
        ic_Softmax = InfoCard('Softmax', frame_config={'fill_color': ORANGE})
        ic_Linear = InfoCard('Linear', frame_config={'fill_color': ORANGE})
        ic_BatchNorm2d = InfoCard('BatchNorm2d', frame_config={'fill_color': ORANGE})

        # ultralytics module cards
        ic_Conv = InfoCard('Conv', frame_config={'fill_color': PURE_BLUE})
        ic_Bottleneck = InfoCard('Bottleneck', frame_config={'fill_color': PURE_BLUE})
        ic_C2f = InfoCard('C2f', frame_config={'fill_color': PURE_BLUE})
        ic_SPPF = InfoCard('SPPF', frame_config={'fill_color': PURE_BLUE})
        ic_Detect = InfoCard('Detect', frame_config={'fill_color': PURE_BLUE})

        # arrange cards into three groups
        ics_m = VGroup(
            ic_add, ic_split, ic_cat,
        ).arrange(RIGHT)
        ics_t = VGroup(
            ic_Conv2d, ic_MaxPool2d, ic_Upsample, ic_Sigmoid, ic_ReLU, ic_SiLU, ic_Softmax, ic_Linear, ic_BatchNorm2d,
        ).arrange(RIGHT)
        ics_u = VGroup(
            ic_Conv, ic_Bottleneck, ic_C2f, ic_SPPF, ic_Detect,
        ).arrange(RIGHT)
        VGroup(
            ics_m, ics_t, ics_u,
        ).arrange(DOWN, buff=0.5)

        ics_all = VGroup(
            ic_add, ic_split, ic_cat,
            ic_Conv2d, ic_MaxPool2d, ic_Upsample, ic_Sigmoid, ic_ReLU, ic_SiLU, ic_Softmax, ic_Linear, ic_BatchNorm2d,
            ic_Conv, ic_Bottleneck, ic_C2f, ic_SPPF, ic_Detect,
        )

        # show starting cards
        self.play(AnimationGroup(
            *(GrowFromCenter(
                card,
                rate_func=rate_functions.ease_out_back,
            ) for card in ics_all),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait()

        # into left
        self.play(ics_all.animate(
            lag_ratio=0.0,
            run_time=wt,
            rate_func=rate_functions.exponential_decay,
        ).arrange(
            DOWN,
            buff=CARD_VGAP,
            aligned_edge=LEFT,
        ).to_edge(
            LEFT,
            buff=CARD_EDGE_BUFF,
        ))
        self.wait()

        export_mobs(__file__, ics_all)      # used by 029
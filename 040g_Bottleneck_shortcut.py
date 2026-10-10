# ************************************************************
# shortcut=True for Bottleneck.
# ************************************************************
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

from modules.ut_Conv import *
from modules.ut_Bottleneck import *

from ultralytics.nn.modules import Bottleneck

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
    # 'c1': 8,
    # 'c2': 8,
    # 'shortcut': False,
    # 'k': (3,3),
    # 'e': 1.0,
# }

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load cards, modules, tensors, graph
        (
            tc_i, mc, tc_o,
            mt_1, mm_cv1, mt_2, mm_cv2, mt_3,
            mg,
        ) = import_mobs('041f')

        # for convenience
        mts = VGroup(mt_1, mt_2, mt_3)

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.9)   # NOTE: last zoom is 0.9
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mts, mm_cv1, mm_cv2)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce shortcut=True',
            skip_animations=False,
        )
        # ************************************************************
        # update params
        self.play(
            mc.update_params(
                params={'shortcut': True},
                run_time=wt,
            )
        )
        self.wait(wt)

        # introduce add in graph
        self.play(mg.append_add(
            run_time=wt*2,
        ))
        self.play(mg.animate(
            run_time=wt,
        ).center().to_edge(
            RIGHT,
            MGRAPH_EDGE_BUFF,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'connect between input and mid2',
            skip_animations=False,
        )
        # ************************************************************
        # init curve
        ps = [
            mt_1.get_corner(LEFT)+LEFT,
            mt_1.get_corner(LEFT)+LEFT*2+DOWN*0.5,
            mt_2.get_corner(LEFT)+LEFT*3,
            mt_3.get_corner(LEFT)+LEFT*2+UP*0.5,
            mt_3.get_corner(LEFT)+LEFT,
        ]
        curve = VMobject(color=MAROON).set_points_smoothly(ps).set_z_index(999)

        # shrink output summary
        self.play(tc_o.shrink_summary(
            run_time=wt,
        ))
        self.wait(wt)

        # connect input and mid2
        self.play(Write(
            curve,
            run_time=wt*2,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce output after addition',
            skip_animations=False,
        )
        # ************************************************************
        mt_4 = mt_3.copy().next_to(mt_3, DOWN, TENSOR_VGAP_SMALL)

        # new perspective
        self.move_camera(
            zoom=0.85,
            frame_center=VGroup(mt_2,mm_cv2).get_center(),
            run_time=wt,
        )

        # generate final output
        self.play(Succession(
            AnimationGroup(
                mt_1.breath(),
                mt_3.breath(),
                lag_ratio=0.0,
                run_time=wt,
            ),
            GrowFromCenter(
                mt_4,
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))

        # summary and graph shape for new output
        self.play(Succession(
            mg.show_shape(
                '(8,5,6)',
                index=4,
                direction=LEFT,
                run_time=wt,
            ),
            tc_o.expand_summary(
                '(8,5,6)',
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean tensors in between',
            skip_animations=False,
        )
        # ************************************************************
        # clean curve
        self.play(Unwrite(curve, run_time=wt,))

        # clean mt_2 mt_3
        self.play(AnimationGroup(
            mt_2.uncreate(ref='bottom', run_time=wt),
            mt_3.uncreate(ref='bottom', run_time=wt),
            lag_ratio=0.0,
        ))

        # new perspective and rearrange
        mobs = VGroup(mt_1, mm_cv1, mm_cv2, mt_4)
        self.move_camera(
            zoom=1.0,
            frame_center=ORIGIN,
            added_anims=[
                mobs.animate(
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
            'simplified output generation',
            skip_animations=False,
        )
        # ************************************************************
        # TODO

        # ************************************************************
        self.next_section(
            'clean everything',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output and graph
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(ref='bottom'),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [mt_1, mt_4],
                [tc_i, tc_o],
            )),
            Unwrite(mg),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # remove input/output cards
        self.play(AnimationGroup(
            detach_to_ref(tc_i, UP),
            detach_to_ref(tc_o, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(mc.shrink_params(
            run_time=wt,
        ))

        # expand module summary
        self.play(mc.expand_summary(
            '8 8 T',
            direction='right',
            run_time=wt,
        ))
        self.wait(wt)

        # shrink module card
        self.play(mc.shrink_summary(
            run_time=wt,
        ))
        # self.wait(wt)

        # remove module mob
        self.play(AnimationGroup(
            mm_cv1.uncreate(
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.uncreate(
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # export
        export_mobs(__file__, mc)     # NOTE: used by next
# ************************************************************
# c1 and c2 for Bottleneck (shortcut=False).
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
    # 'e': 0.5,
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
        ) = import_mobs('041d')
        module_config = mg.module_config

        # # raw modules
        # m_module = Bottleneck(**module_config)
        # m_cv1 = m_module.cv1
        # m_cv2 = m_module.cv2

        # for convenience
        mts = VGroup(mt_1, mt_2, mt_3)

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mts, mm_cv1, mm_cv2)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[8 8] -> [16 8]',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c1': 16},
                run_time=wt,
            )
        )

        # update graph
        self.play(
            mg.mobs_card[0].update_summary(
                summary='16 4 3 1 1',
                run_time=wt,
            )
        )

        # update modules
        self.play(
            mm_cv1.ft_conv.stretch_3d(
                new_shape=(16,3,3),
                run_time=wt,
            )
        )
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            '[8 8] -> [16 16]',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c2': 16},
                run_time=wt,
            )
        )

        # update graph
        self.play(AnimationGroup(
            mg.mobs_card[0].update_summary(
                summary='16 8 3 1 1',
                run_time=wt,
            ),
            mg.mobs_card[1].update_summary(
                summary='8 16 3 1 1',
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # update module
        self.play(AnimationGroup(
            mm_cv1.ft_conv.stretch_blocks(
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv1.ft_bn.stretch_blocks(
                direction='out',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.ft_conv.stretch_blocks(
                direction='out',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.ft_bn.stretch_blocks(
                direction='out',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.play(
            mm_cv2.ft_conv.stretch_3d(
                new_shape=(8,3,3),
                run_time=wt,
            ),
        )
        self.move_camera(
            zoom=0.9,           # NOTE
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(16,5,6) -> (8,5,6) -> (16,5,6)',
            skip_animations=False,
        )
        # ************************************************************
        # update tensors
        self.play(AnimationGroup(
            mt_1.stretch_3d(new_shape=(16,5,6)),
            mt_2.stretch_3d(new_shape=(8,5,6)),
            mt_3.stretch_3d(new_shape=(16,5,6)),
            lag_ratio=0.5,
            run_time=wt*2,
        ))

        # show graph shapes
        self.play(mg.show_shapes(
            texts=['(16,5,6)', '(8,5,6)', '(16,5,6)'],
            indices=[0, 1, 2],
            directions=[LEFT]*3,
            lag_ratio=0.5,
            run_time=wt*2,
        ))

        # tensor cards summary
        self.play(AnimationGroup(
            tc_i.expand_summary('(16,5,6)'),
            tc_o.expand_summary('(16,5,6)'),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # lightup tensors
        self.play(AnimationGroup(
            mt_1.lightup(),
            mt_2.lightup(),
            mt_3.lightup(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # fade modules
        self.play(AnimationGroup(
            mm_cv1.ft_conv.tarnish(),
            mm_cv1.ft_bn.tarnish(),
            mm_cv2.ft_conv.tarnish(),
            mm_cv2.ft_bn.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            tc_i, mc, tc_o,
            mts[0], mm_cv1, mts[1], mm_cv2, mts[2],
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
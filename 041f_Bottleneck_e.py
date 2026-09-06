# ************************************************************
# e for Bottleneck (shortcut=False).
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
    # 'c1': 16,
    # 'c2': 16,
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
        ) = import_mobs('041e')

        # for convenience
        mts = VGroup(mt_1, mt_2, mt_3)

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE, zoom=0.9)   # NOTE: last zoom is 0.9
        self.add_fixed_in_frame_mobjects(tc_i, mc, tc_o, mg)
        self.add(mts, mm_cv1, mm_cv2)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'bottleneck curves',
            skip_animations=False,
        )
        # ************************************************************
        ps1 = [mt_1.get_corner(OUT), mt_2.get_corner(OUT), mt_3.get_corner(OUT)]
        ds1 = [Dot(p, radius=0.05, color=PURE_YELLOW).set_z_index(999) for p in ps1]
        ps2 = [mt_1.get_corner(IN), mt_2.get_corner(IN), mt_3.get_corner(IN)]
        ds2 = [Dot(p, radius=0.05, color=PURE_YELLOW).set_z_index(999) for p in ps2]

        curve_1 = VMobject(color=MAROON).set_points_smoothly(ps1).set_z_index(998)
        curve_2 = VMobject(color=MAROON).set_points_smoothly(ps2).set_z_index(998)

        # show top dots and curve
        self.play(Succession(
            AnimationGroup(
                *(Write(d) for d in ds1),
                lag_ratio=0.0,
            ),
            Write(curve_1),
            run_time=wt*3,
        ))

        # show bottom dots and curve
        self.play(Succession(
            AnimationGroup(
                *(Write(d) for d in ds2),
                lag_ratio=0.0,
            ),
            Write(curve_2),
            run_time=wt*3,
        ))
        self.wait(wt)

        # clean
        self.play(AnimationGroup(
            *(Unwrite(mob) for mob in [
                curve_1, curve_2, *ds1, *ds2,
            ]),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'e=0.25',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'e': 0.25},
                run_time=wt,
            )
        )
        self.wait(wt)

        # update graph
        self.play(AnimationGroup(
            mg.mobs_card[0].update_summary(
                summary='16 4 3 1 1',
                run_time=wt,
            ),
            mg.mobs_card[1].update_summary(
                summary='4 16 3 1 1',
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # update module
        self.play(AnimationGroup(
            mm_cv1.ft_conv.stretch_blocks(
                direction='in',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv1.ft_bn.stretch_blocks(
                direction='in',
                diff=2,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.ft_conv.stretch_3d(
                new_shape=(4,3,3),
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # update mid tensor and graph shape
        self.play(AnimationGroup(
            mt_2.stretch_3d(
                new_shape=(4,5,6),
            ),
            mg.update_shape(
                text='(4,5,6)',
                index=1,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'e=1.0',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'e': 1.0},
                run_time=wt,
            )
        )
        self.wait(wt)

        # update graph
        self.play(AnimationGroup(
            mg.mobs_card[0].update_summary(
                summary='16 16 3 1 1',
                run_time=wt,
            ),
            mg.mobs_card[1].update_summary(
                summary='16 16 3 1 1',
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # update module
        self.play(AnimationGroup(
            mm_cv1.ft_conv.stretch_blocks(
                direction='out',
                diff=6,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv1.ft_bn.stretch_blocks(
                direction='out',
                diff=6,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.ft_conv.stretch_3d(
                new_shape=(16,3,3),
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # update mid tensor and graph shape
        self.play(AnimationGroup(
            mt_2.stretch_3d(
                new_shape=(16,5,6),
            ),
            mg.update_shape(
                text='(16,5,6)',
                index=1,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[16 16 1.0] -> [8 8 1.0]',
            skip_animations=False,
        )
        # ************************************************************
        # update module card
        self.play(
            mc.update_params(
                params={'c1': 8, 'c2': 8},
                run_time=wt,
            )
        )
        self.wait(wt)

        # update graph
        self.play(AnimationGroup(
            mg.mobs_card[0].update_summary(
                summary='8 8 3 1 1',
                run_time=wt,
            ),
            mg.mobs_card[1].update_summary(
                summary='8 8 3 1 1',
                run_time=wt,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # update module
        self.play(AnimationGroup(
            mm_cv1.ft_conv.stretch_blocks(
                direction='in',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv1.ft_bn.stretch_blocks(
                direction='in',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.ft_conv.stretch_blocks(
                direction='in',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            mm_cv2.ft_bn.stretch_blocks(
                direction='in',
                diff=4,
                ref='center',
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.play(AnimationGroup(
            mm_cv1.ft_conv.stretch_3d(
                new_shape=(8,3,3),
                run_time=wt,
            ),
            mm_cv2.ft_conv.stretch_3d(
                new_shape=(8,3,3),
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # update mid tensor and graph shape
        self.play(Succession(
            AnimationGroup(
                mt_1.stretch_3d(new_shape=(8,5,6)),
                mt_2.stretch_3d(new_shape=(8,5,6)),
                mt_3.stretch_3d(new_shape=(8,5,6)),
            ),
            AnimationGroup(
                mg.update_shape(
                    text='(8,5,6)',
                    index=0,
                ),
                mg.update_shape(
                    text='(8,5,6)',
                    index=1,
                ),
                mg.update_shape(
                    text='(8,5,6)',
                    index=2,
                ),
            ),
            AnimationGroup(
                tc_i.update_summary(
                    summary='(8,5,6)',
                ),
                tc_o.update_summary(
                    summary='(8,5,6)',
                ),
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'highlight modules',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mm_cv1.ft_conv.lightup(),
            mm_cv1.ft_bn.lightup(),
            mm_cv2.ft_conv.lightup(),
            mm_cv2.ft_bn.lightup(),
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
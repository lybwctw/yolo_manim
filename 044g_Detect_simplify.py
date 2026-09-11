# ************************************************************
# Simplified view on Detect.
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

# from ultralytics.nn.modules import Detect

# INIT_CONFIG = {
#     'ch': 8,
#     'c2': 4,
#     'c3': 4,
#     'reg_max': 4,      # 4 probs for each direction (16 by default)
#     'nc': 3,           # 3 classes
# }

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load cards, modules, tensors, graph
        (
            tc_i, mc, card_o1, card_o2,
            mm_bs, mm_cs,
            mts,
            mg,
        ) = import_mobs('044f')
        module_config = mg.module_config

        # for convenience
        mm_b1, mm_b2, mm_b3 = mm_bs
        mm_c1, mm_c2, mm_c3 = mm_cs
        series_box = VGroup(
            *mm_bs,
            *mts[1:13],
        )
        series_cls = VGroup(
            *mm_cs,
            *mts[13:],
        )

        # show initial mobs
        camera_config = {
            **VIEW_COMPUTE,
            'phi': 40*DEGREES,
            'zoom': 0.6,
            # 'frame_center': DOWN*1.5,
        }

        # FIXME: initial camera setup hack
        self.set_camera_orientation(**camera_config)
        self.add_fixed_in_frame_mobjects(tc_i, mc, card_o1, card_o2, mg)
        self.add(mts, mm_bs, mm_cs)
        self.wait(wt*0.1)
        self.set_camera_orientation(frame_center=DOWN*1.5)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'get rid of mid tensors',
            skip_animations=True,
        )
        # ************************************************************
        # lightup all tensors
        self.play(AnimationGroup(
            *(mt.lightup() for mt in mts),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # remove mid tensors
        self.play(AnimationGroup(
            *(mt.uncreate(ref='center') for mt in mts[1:12]),
            *(mt.uncreate(ref='center') for mt in mts[13:-1]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'rearrange input/module/output',
            skip_animations=False,
        )
        # ************************************************************
        mm_bs.generate_target()
        mm_bs.target.arrange(
            DOWN,
            buff=TENSOR_VGAP_MINI,
        ).move_to(
            mm_bs,
            aligned_edge=UL,
        )

        mm_cs.generate_target()
        mm_cs.target.arrange(
            DOWN,
            buff=TENSOR_VGAP_MINI,
        ).move_to(
            mm_cs,
            aligned_edge=UL,
        )

        mts[12].generate_target()
        mts[12].target.next_to(
            mm_bs.target,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        mts[-1].generate_target()
        mts[-1].target.next_to(
            mm_cs.target,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        mts[0].generate_target()

        # center all targets
        mobs = VGroup(
            mts[0].target,
            mm_bs.target,
            mm_cs.target,
            mts[12].target,
            mts[-1].target,
        )
        mobs.center().shift(UP*0.5)

        # NOTE: new perspective
        camera_config = {
            **VIEW_COMPUTE,
            'phi': 50*DEGREES,
            'zoom': 0.85,
            'frame_center': ORIGIN,
        }
        self.move_camera(
            **camera_config,
            added_anims=[
                AnimationGroup(
                    MoveToTarget(mts[0]),
                    MoveToTarget(mm_bs),
                    MoveToTarget(mm_cs),
                    MoveToTarget(mts[12]),
                    MoveToTarget(mts[-1]),
                    lag_ratio=0.0,
                    run_time=wt,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'even simpler arrange',
            skip_animations=False,
        )
        # ************************************************************
        mts_input = mts[0]
        mts_output = VGroup(mts[12], mts[-1])
        mts_input.generate_target()
        mm_bs.generate_target()
        mm_cs.generate_target()
        mts_output.generate_target()

        # on output
        mts_output.target.arrange(
            RIGHT,
            buff=TENSOR_VGAP_SMALL,
        )

        # on global
        mtargets = VGroup(
            mts_input.target,
            mm_bs.target,
            mm_cs.target,
            mts_output.target,
        )
        mtargets.arrange(
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )

        # on input and output
        mts_input.target.next_to(
            mtargets[1],
            UP,
            TENSOR_VGAP_SMALL,
        )
        mts_output.target.next_to(
            mtargets[-2],
            DOWN,
            TENSOR_VGAP_SMALL*0.7,
        )

        # NOTE: new perspective
        self.move_camera(
            zoom=0.75,
            added_anims=[
                AnimationGroup(
                    MoveToTarget(mts_input),
                    MoveToTarget(mm_bs),
                    MoveToTarget(mm_cs),
                    MoveToTarget(mts_output),
                    lag_ratio=0.0,
                    run_time=wt,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean everything',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output and graph
        # NOTE: new perspective
        self.move_camera(
            zoom=0.85,
            added_anims=[
                AnimationGroup(
                    *(AnimationGroup(
                        tmob.uncreate(ref='bottom'),
                        cmob.shrink_summary(),
                        lag_ratio=0.5,
                    ) for tmob, cmob in zip(
                        [mts[0], mts[12], mts[-1]],
                        [tc_i, card_o1, card_o2],
                    )),
                    Unwrite(mg),
                    lag_ratio=0.0,
                    run_time=wt,
                ),
            ],
            run_time=wt,
        )

        # remove input/output cards
        self.play(AnimationGroup(
            detach_to_ref(tc_i, UP),
            detach_to_ref(card_o1, DOWN),
            detach_to_ref(card_o2, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(mc.shrink_params(
            run_time=wt,
        ))

        # expand module summary
        self.play(mc.expand_summary(
            '16 4 4 4 3',
            direction='right',
            run_time=wt,
        ))
        self.wait(wt)

        # remove module mob
        self.play(AnimationGroup(
            *(mm.uncreate(
                ref='center',
                lag_ratio=0.0,
                run_time=wt,
            ) for mm in (*mm_bs, *mm_cs)),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # export
        export_mobs(__file__, mc)     # NOTE: used by next, samples
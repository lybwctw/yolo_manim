# ************************************************************
# Detailed Compute loop for SPPF.
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

from ultralytics.nn.modules import SPPF

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

TENSOR_EGAP_MEDIUM = 1.0

# INIT_CONFIG = {
    # 'c1': 8,
    # 'c2': 8,
    # 'k': 5,
# }

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        mc, mg = import_mobs('043b')
        module_config = mg.module_config

        # raw modules
        m_module = SPPF(**module_config)
        m_cv1 = m_module.cv1
        m_cv2 = m_module.cv2
        m_m = m_module.m    # single MaxPool2d

        # raw tensors
        t_i = torch.randn(1, 8, 5, 6)
        t_m1 = m_cv1(t_i)
        t_m2 = m_m(t_m1)
        t_m3 = m_m(t_m2)
        t_m4 = m_m(t_m3)
        t_m5 = torch.concat([t_m1, t_m2, t_m3, t_m4], dim=1)
        t_o = m_cv2(t_m5)

        # module mobs (cv1, m, cv2)
        mm_cv1 = UT_Conv(
            module_config=SPPF_2_cv1_config(module_config),
            init_scale=1.0,
            opaque=True,
        )
        mm_cv2 = UT_Conv(
            module_config=SPPF_2_cv2_config(module_config),
            init_scale=1.0,
            opaque=True,
        )
        VGroup(mm_cv1, mm_cv2).arrange(
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        # tensor mobs
        mts = VGroup(
            FTensor3D(
                shape=t[0].shape,
                init_scale=0.8,
                opaque=True,
            ) for t in [
                t_i, t_m1, t_m2, t_m3, t_m4, t_m5, t_o,
            ]
        )

        increase_z_index_in_batch([
            mts[0],
            mm_cv1,
            mts[1],
            mts[2],
            mts[3],
            mts[4],
            mts[5],
            mm_cv2,
            mts[6],
        ])

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(mc, mg)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show sub modules',
            skip_animations=True,
        )
        # ************************************************************
        # highlight cv1 in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[0],
            run_time=wt,
        ))
        # self.wait(wt)

        # show cv1
        self.play(mm_cv1.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight 1st mp in graph
        self.play(mg.highlight(
            mask=masks[1],
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight 2nd mp in graph
        self.play(mg.highlight(
            mask=masks[2],
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight 3rd mp in graph
        self.play(mg.highlight(
            mask=masks[3],
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight concat in graph
        self.play(mg.highlight(
            mask=masks[4],
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight cv2 in graph
        self.play(mg.highlight(
            mask=masks[5],
            run_time=wt,
        ))
        # self.wait(wt)

        # show cv2
        self.play(mm_cv2.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight back
        self.play(mg.highlight(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show input',
            skip_animations=True,
        )
        # ************************************************************
        # show input tensor
        mts[0].next_to(
            mm_cv1,
            UP,
            TENSOR_VGAP_SMALL,
        )
        self.play(mts[0].create(
            ref='bottom',
            run_time=wt,
        ))

        # show input summary
        tc_i = InfoCard('in_1').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(tc_i)
        self.play(attach_to_ref(
            tc_i,
            mc,
            UP,
            run_time=wt,
        ))
        self.play(tc_i.expand_summary(
            t2s(t_i.detach()[0]),
            run_time=wt,
        ))

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_i.detach()[0]),
            index=0,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply cv1',
            skip_animations=True,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[0]),
            mm_cv2.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # make BIG space in the mid
        gap = mts[1].height * 5 + TENSOR_VGAP_MINI * 6
        mobs = VGroup(
            VGroup(mts[0], mm_cv1),
            mm_cv2,
        )
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=gap).shift(UP*1.2)   # NOTE
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # generate m1
        mts[1].next_to(
            mm_cv1,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(Succession(
            mm_cv1.breath(
                lag_ratio=0.0,
                run_time=wt,
            ),
            GrowFromCenter(
                mts[1],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m1.detach()[0]),
            index=1,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply first MaxPool2d',
            skip_animations=True,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[1]),
            mm_cv1.tarnish(),
            mts[0].tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # generate tensor
        mts[2].next_to(
            mts[1],
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(Succession(
            Wiggle(
                mg.cards_m[0],
                scale_value=1.2,
                run_time=wt*3,
            ),
            GrowFromCenter(
                mts[2],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m2.detach()[0]),
            index=2,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply second MaxPool2d',
            skip_animations=True,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[2]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # generate tensor
        mts[3].next_to(
            mts[2],
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(Succession(
            Wiggle(
                mg.cards_m[1],
                scale_value=1.2,
                run_time=wt*3,
            ),
            GrowFromCenter(
                mts[3],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m3.detach()[0]),
            index=3,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply third MaxPool2d',
            skip_animations=True,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[3]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # generate tensor
        mts[4].next_to(
            mts[3],
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(Succession(
            Wiggle(
                mg.cards_m[2],
                scale_value=1.2,
                run_time=wt*3,
            ),
            GrowFromCenter(
                mts[4],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m4.detach()[0]),
            index=4,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply concat',
            skip_animations=True,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[4]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # prepare copies
        mts_copy = mts[1:5].copy()
        mts_copy.set_opacity(0.5)
        self.play(FadeIn(
            mts_copy,
            run_time=wt*0.1,
        ))

        # pending copies before concat
        self.play(mts_copy.animate(
            run_time=wt*2,
            rate_func=rate_functions.ease_in_out_expo,
        ).arrange(
            IN,
            buff=1.0,
        ).next_to(
            mm_cv2,
            UP,
            buff=TENSOR_VGAP_MINI,
        ))
        # self.wait(wt)

        # 4 concat into 1
        self.play(mts_copy.animate(
            run_time=wt,
        ).arrange(
            IN,
            buff=0.0,
        ).next_to(
            mm_cv2,
            UP,
            buff=TENSOR_VGAP_MINI,
        ))
        self.wait(wt)

        # replace
        mts[5].move_to(mts_copy)
        self.play(AnimationGroup(
            FadeOut(mts_copy),
            FadeIn(mts[5]),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m5.detach()[0]),
            index=5,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply cv2',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[5]),
            mm_cv2.lightup(),
            mts[1].tarnish(),
            mts[2].tarnish(),
            mts[3].tarnish(),
            mts[4].tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # generate final tensor
        mts[6].next_to(
            mm_cv2,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(Succession(
            mm_cv2.breath(
                lag_ratio=0.0,
                run_time=wt,
            ),
            GrowFromCenter(
                mts[6],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_o.detach()[0]),
            index=6,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean job',
            skip_animations=False,
        )
        # ************************************************************
        # lightup everything
        self.play(AnimationGroup(
            mg.highlight(),
            mm_cv1.lightup(),
            *(mt.lightup() for mt in mts[:5]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show output summary
        tc_o = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(tc_o)
        self.play(attach_to_ref(
            tc_o,
            mc,
            DOWN,
            run_time=wt,
        ))
        self.play(tc_o.expand_summary(
            t2s(t_o.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            tc_i, mc, tc_o,
            mm_cv1, mm_cv2,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
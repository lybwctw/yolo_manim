# ************************************************************
# Detailed Compute loop for C2f.
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

from ultralytics.nn.modules import C2f

TENSOR_VGAP_SMALL = 0.5
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

TENSOR_EGAP_MEDIUM = 1.0

# INIT_CONFIG = {
    # 'c1': 8,
    # 'c2': 8,
    # 'n': 3,
    # 'shortcut': False,
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
        # load card and graph
        mc, mg = import_mobs('042b')
        module_config = mg.module_config

        # raw modules
        m_module = C2f(**module_config)
        m_cv1 = m_module.cv1
        m_cv2 = m_module.cv2
        m_m = m_module.m

        # raw tensors
        t_i = torch.randn(1, 8, 5, 6)
        t_m1 = m_cv1(t_i)
        t_m2, t_m3 = torch.split(t_m1, 4, dim=1)
        t_m4 = m_m[0](t_m3)
        t_m5 = m_m[1](t_m4)
        t_m6 = m_m[2](t_m5)
        t_m7 = torch.concat([t_m2, t_m3, t_m4, t_m5, t_m6], dim=1)
        t_o = m_cv2(t_m7)

        # module mobs (cv1, m, cv2)
        mm_cv1 = UT_Conv(
            module_config=C2f_2_cv1_config(module_config),
            init_scale=0.8,
            opaque=True,
        )
        mm_cv2 = UT_Conv(
            module_config=C2f_2_cv2_config(module_config),
            init_scale=0.8,
            opaque=True,
        )
        mm_m = VGroup(
            UT_Bottleneck(
                module_config=C2f_2_bottleneck_config(module_config),
                init_scale=0.8,
                opaque=True,
            ) for _ in range(module_config['n'])
        )
        mm_m1, mm_m2, mm_m3 = mm_m
        VGroup(mm_cv1, mm_m1, mm_m2, mm_m3, mm_cv2).arrange(
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
                t_i, t_m1, t_m2, t_m3, t_m4, t_m5, t_m6, t_m7, t_o,
            ]
        )

        increase_z_index_in_batch([
            mts[0],
            mm_cv1,
            mts[1],
            mts[2], mts[3],
            mm_m1,
            mts[4],
            mm_m2,
            mts[5],
            mm_m3,
            mts[6],
            mts[7],
            mm_cv2,
            mts[8],
        ])

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(mc, mg)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show sub modules',
            skip_animations=False,
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
        # self.wait(wt)

        # highlight split in graph
        self.play(mg.highlight(
            mask=masks[1],
            run_time=wt,
        ))
        self.wait(wt)

        # highlight m1 in graph
        self.play(mg.highlight(
            mask=masks[2],
            run_time=wt,
        ))
        # self.wait(wt)

        # create m1
        self.play(mm_m1.create(
            ref='center',
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight m2 in graph
        self.play(mg.highlight(
            mask=masks[3],
            run_time=wt,
        ))
        # self.wait(wt)

        # create m2
        self.play(mm_m2.create(
            ref='center',
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight m3 in graph
        self.play(mg.highlight(
            mask=masks[4],
            run_time=wt,
        ))
        # self.wait(wt)

        # create m3
        self.play(mm_m3.create(
            ref='center',
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight concat in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[5],
            run_time=wt,
        ))
        self.wait(wt)

        # highlight cv2 in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[6],
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
            skip_animations=False,
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
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[0]),
            *(mm.tarnish() for mm in [
                mm_m1, mm_m2, mm_m3, mm_cv2,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # make space in the mid
        gap = mts[1].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1),
            VGroup(mm_m1, mm_m2, mm_m3, mm_cv2),
        )
        self.play(mobs.animate(
            run_time=wt,
        ).arrange(
            DOWN,
            buff=gap,
        ))
        # mobs.generate_target()
        # mobs.target.arrange(
        #     DOWN,
        #     buff=gap,
        # )
        # self.play(MoveToTarget(mobs, run_time=wt))
        self.wait(wt)

        # generate m1
        mts[1].next_to(
            mm_cv1,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
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
            'apply split',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[1]),
            mts[0].tarnish(),
            mm_cv1.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # space in the mid
        gap = mts[2].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1, mts[1]),
            VGroup(mm_m1, mm_m2, mm_m3, mm_cv2),
        )
        self.play(mobs.animate(
            run_time=wt,
        ).arrange(
            DOWN,
            buff=gap,
        ))
        self.wait(wt)

        # split animation
        mts[2].move_to(mts[1]).align_to(mts[1], OUT)
        mts[3].move_to(mts[1]).align_to(mts[1], IN)
        self.play(AnimationGroup(
            FadeIn(mts[2]),
            FadeIn(mts[3]),
            lag_ratio=0.0,
            run_time=wt*0.1,
        ))
        self.play(AnimationGroup(
            mts[2].animate.next_to(
                mts[1], DOWN, buff=TENSOR_VGAP_SMALL,
            ).shift(OUT*TENSOR_EGAP_MEDIUM*0.5),
            mts[3].animate.next_to(
                mts[1], DOWN, buff=TENSOR_VGAP_SMALL,
            ).shift(IN*TENSOR_EGAP_MEDIUM*0.5),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show two shapes in graph
        # FIXME: better positioning for first shape
        self.play(AnimationGroup(
            mg.show_shape(
                t2s(t_m2.detach()[0]),
                index=8,
                direction=UP,
                buff=0.03,
            ),
            mg.show_shape(
                t2s(t_m3.detach()[0]),
                index=2,
                direction=LEFT,
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'prepare for bottlenecks application',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        mask = np.zeros(mg.ncards,dtype=bool)
        mask[2:5] = True
        self.play(AnimationGroup(
            mg.highlight(mask=mask),
            mts[1].tarnish(),
            mm_m1.lightup(),
            mm_m2.lightup(),
            mm_m3.lightup(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # align bottlenecks with second split
        self.play(AnimationGroup(
            *(mm.animate.align_to(mts[3], IN) for mm in [
                mm_m1, mm_m2, mm_m3,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply 1st bottleneck',
            skip_animations=False,
        )
        # ************************************************************
        # space in the mid
        gap = mts[4].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1, mts[1], mts[2], mts[3], mm_m1),
            VGroup(mm_m2, mm_m3, mm_cv2),
        )
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=gap)
        # new_center = mobs.target[0][-1].get_bottom()
        # new_center[2] = 0.0
        self.move_camera(
            # frame_center=new_center,
            zoom=0.9,
            added_anims=[
                MoveToTarget(mobs, run_time=wt),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # generate output
        mts[4].next_to(mm_m1, DOWN, buff=TENSOR_VGAP_SMALL)
        self.play(Succession(
            mm_m1.breath(
                lag_ratio=0.0,
                run_time=wt,
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
            index=3,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply 2nd bottleneck',
            skip_animations=False,
        )
        # ************************************************************
        # space in the mid
        gap = mts[5].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1, mts[1], mts[2], mts[3], mm_m1, mts[4], mm_m2),
            VGroup(mm_m3, mm_cv2),
        )
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=gap)
        # new_center = mobs.target[0][-1].get_bottom()
        # new_center[2] = 0.0
        self.move_camera(
            zoom=0.8,
            # frame_center=new_center,
            added_anims=[
                MoveToTarget(mobs, run_time=wt),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # generate output
        mts[5].next_to(mm_m2, DOWN, buff=TENSOR_VGAP_SMALL)
        self.play( Succession(
            mm_m2.breath(
                lag_ratio=0.0,
                run_time=wt,
            ),
            GrowFromCenter(
                mts[5],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m5.detach()[0]),
            index=4,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply 3rd bottleneck',
            skip_animations=False,
        )
        # ************************************************************
        # space in the mid
        gap = mts[6].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1, mts[1], mts[2], mts[3], mm_m1, mts[4], mm_m2, mts[5], mm_m3),
            VGroup(mm_cv2),
        )
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=gap)
        # new_center = mobs.target[0][-1].get_bottom()
        # new_center[2] = 0.0
        self.move_camera(
            zoom=0.7,           # NOTE: final zoom level
            # frame_center=new_center,
            added_anims=[
                MoveToTarget(mobs, run_time=wt),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # generate output
        mts[6].next_to(mm_m3, DOWN, buff=TENSOR_VGAP_SMALL)
        self.play(Succession(
            mm_m3.breath(
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
            t2s(t_m6.detach()[0]),
            index=5,
            direction=LEFT,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'prepare for concat',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[5]),
            mm_m1.tarnish(),
            mm_m2.tarnish(),
            mm_m3.tarnish(),
        ))

        # space in the mid
        gap = mts[7].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1, mts[1], mts[2], mts[3], mm_m1, mts[4], mm_m2, mts[5], mm_m3, mts[6]),
            VGroup(mm_cv2),
        )
        mobs.generate_target()
        mobs.target.arrange(DOWN, buff=gap)

        # NOTE: final mobs center here
        mobs.target.shift(UP*2.5)
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply concat',
            skip_animations=False,
        )
        # ************************************************************
        mts_copy = mts[2:7].copy()
        mts_copy.set_opacity(0.5)
        self.play(FadeIn(
            mts_copy,
            run_time=wt*0.1,
        ))

        # pending copies before concat
        self.play(mts_copy.animate(
            run_time=wt,
            rate_func=rate_functions.ease_in_out_expo,
        ).arrange(
            IN,
            buff=1.0,
        ).next_to(
            mm_cv2,
            UP,
            buff=TENSOR_VGAP_SMALL,
        ))
        # self.wait(wt)

        # 5 concat into 1
        self.play(mts_copy.animate(
            run_time=wt,
        ).arrange(
            IN,
            buff=0.0,
        ).next_to(
            mm_cv2,
            UP,
            buff=TENSOR_VGAP_SMALL,
        ))
        self.wait(wt)

        # replace
        mts[7].move_to(mts_copy)
        self.play(AnimationGroup(
            FadeOut(mts_copy),
            FadeIn(mts[7]),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_m7.detach()[0]),
            index=6,
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
            mg.highlight(mask=masks[6]),
            *(t.tarnish() for t in mts[2:7]),
            mm_cv2.lightup(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # generate final output
        mts[-1].next_to(
            mm_cv2,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )
        self.play(Succession(
            mm_cv2.breath(
                lag_ratio=0.0,
                run_time=wt,
            ),
            GrowFromCenter(
                mts[-1],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_o.detach()[0]),
            index=7,
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
            mm_m1.lightup(),
            mm_m2.lightup(),
            mm_m3.lightup(),
            *(mt.lightup() for mt in mts[:7]),
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
            mm_cv1, mm_m, mm_cv2,
            mts,
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
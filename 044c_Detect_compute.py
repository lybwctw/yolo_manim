# ************************************************************
# Detailed Compute loop for Detect (modified).
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

from torch.nn import Conv2d
from ultralytics.nn.modules import Conv
# from ultralytics.nn.modules import Detect

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

TENSOR_EGAP_MEDIUM = 1.0

INIT_SCALE = 0.8

################################################
#           input
#             |
#     |----------------|
#     b1              c1
#     b2              c2
#     b3              c3
#    split          sigmoid
#   softmax            |
#    concat
#     |
################################################

# INIT_CONFIG = {
#     'ch': 8,
#     'c2': 4,
#     'c3': 4,
#     'reg_max': 5,      # 4 probs for each direction (16 by default)
#     'nc': 3,           # 3 classes
# }

# FIXME: appearance issue for thin cubes' stroke

# TODO: add mid tensor shapes

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
        mc, mg = import_mobs('044b')
        module_config = mg.module_config

        # raw modules (manual)
        m_cv2 = [
            Conv(**Detect_2_b1_config(module_config)),    # 8, 8, 3, 1, 1
            Conv(**Detect_2_b2_config(module_config)),    # 8, 8, 3, 1, 1
            Conv2d(**Detect_2_b3_config(module_config)),    # 8, 24, 1, 1, 0, T
        ]
        m_cv3 = [
            Conv(**Detect_2_c1_config(module_config)),    # 8, 8, 3, 1, 1
            Conv(**Detect_2_c2_config(module_config)),    # 8, 8, 3, 1, 1
            Conv2d(**Detect_2_c3_config(module_config)),    # 8, 3, 1, 1, 0, T
        ]

        # raw tensors (manual)
        t_i = torch.randn(1, 8, 7, 9)
        tb_m1 = m_cv2[0](t_i)
        tb_m2 = m_cv2[1](tb_m1)
        tb_m3 = m_cv2[2](tb_m2)
        tb_m4, tb_m5, tb_m6, tb_m7 = torch.split(
            tb_m3, module_config['reg_max'], dim=1,
        )
        m_softmax = torch.nn.Softmax(dim=1)
        tb_m8, tb_m9, tb_m10, tb_m11 = (
            m_softmax(tb_m4),
            m_softmax(tb_m5),
            m_softmax(tb_m6),
            m_softmax(tb_m7),
        )
        tb_o = torch.cat(
            [tb_m8, tb_m9, tb_m10, tb_m11],
            dim=1,
        )
        tc_m1 = m_cv3[0](t_i)
        tc_m2 = m_cv3[1](tc_m1)
        tc_m3 = m_cv3[2](tc_m2)
        m_sigmoid = torch.nn.Sigmoid()
        tc_o = m_sigmoid(tc_m3)

        # module mobs for box prediction
        mm_b1 = UT_Conv(
            module_config=Detect_2_b1_config(module_config),
            init_scale=INIT_SCALE,
            opaque=True,
        )
        mm_b2 = UT_Conv(
            module_config=Detect_2_b2_config(module_config),
            init_scale=INIT_SCALE,
            opaque=True,
        )
        mm_b3 = UT_Conv(
            module_config=Detect_2_b3_config_fake(module_config),
            init_scale=INIT_SCALE,
            opaque=True,
            Conv2d=True,
        )
        mm_bs = VGroup(mm_b1, mm_b2, mm_b3).arrange(
            DOWN, 
            buff=TENSOR_VGAP_MINI,
        )

        # module mobs for cls prediction
        mm_c1 = UT_Conv(
            module_config=Detect_2_c1_config(module_config),
            init_scale=INIT_SCALE,
            opaque=True,
        )
        mm_c2 = UT_Conv(
            module_config=Detect_2_c2_config(module_config),
            init_scale=INIT_SCALE,
            opaque=True,
        )
        mm_c3 = UT_Conv(
            module_config=Detect_2_c3_config_fake(module_config),
            init_scale=INIT_SCALE,
            opaque=True,
            Conv2d=True,
        )
        mm_cs = VGroup(mm_c1, mm_c2, mm_c3).arrange(
            DOWN, 
            buff=TENSOR_VGAP_MINI,
        )
        mms = VGroup(mm_bs, mm_cs).arrange(
            RIGHT,
            buff=TENSOR_VGAP_MINI,
        )

        # tensor mobs
        mts = VGroup(
            FTensor3D(
                shape=t[0].shape,
                init_scale=INIT_SCALE,
                opaque=True,
            ) for t in [
                t_i,
                tb_m1, tb_m2, tb_m3, tb_m4, tb_m5, tb_m6, tb_m7,
                tb_m8, tb_m9, tb_m10, tb_m11, tb_o,
                tc_m1, tc_m2, tc_m3, tc_o,
            ]
        )

        # TODO: not verified yet
        increase_z_index_in_batch([
            mts[0], 
            mts[13], mts[14], mts[15], mts[16],
            mm_b1, mts[1], mm_b2, mts[2], mm_b3, mts[3],
            mts[7], mts[6], mts[5], mts[4],
            mts[11], mts[10], mts[9], mts[8],
            mts[12],
        ])

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(mc, mg)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show sub modules for box prediction',
            skip_animations=False,
        )
        # ************************************************************
        # highlight b1 in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[0],
            run_time=wt,
        ))
        # self.wait(wt)

        # show b1
        self.play(mm_b1.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight b2 in graph
        self.play(mg.highlight(
            mask=masks[1],
            run_time=wt,
        ))
        # self.wait(wt)

        # show b2
        self.play(mm_b2.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight b3 in graph
        self.play(mg.highlight(
            mask=masks[2],
            run_time=wt,
        ))
        # self.wait(wt)

        # show b2
        self.play(mm_b3.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight split
        self.play(mg.highlight(
            mask=masks[3],
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight Softmax
        self.play(mg.highlight(
            mask=masks[4],
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight Softmax
        self.play(mg.highlight(
            mask=masks[5],
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show sub modules for cls prediction',
            skip_animations=False,
        )
        # ************************************************************
        # highlight c1
        self.play(mg.highlight(
            mask=masks[6],
            run_time=wt,
        ))
        # self.wait(wt)

        # show c1
        self.play(mm_c1.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight c2 in graph
        self.play(mg.highlight(
            mask=masks[7],
            run_time=wt,
        ))
        # self.wait(wt)

        # show c2
        self.play(mm_c2.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight c3 in graph
        self.play(mg.highlight(
            mask=masks[8],
            run_time=wt,
        ))
        # self.wait(wt)

        # show c3
        self.play(mm_c3.create(
            ref='center',
            run_time=wt,
        ))
        self.wait(wt)

        # highlight split
        self.play(mg.highlight(
            mask=masks[9],
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
            VGroup(mm_b1, mm_c1),
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
            'prepare for box prediction',
            skip_animations=False,
        )
        # ************************************************************
        mask = np.zeros(mg.ncards, dtype=bool)
        mask[:6] = True

        # fade cls series
        self.play(AnimationGroup(
            mg.highlight(mask=mask),
            mm_c1.tarnish(),
            mm_c2.tarnish(),
            mm_c3.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # align input to box series
        self.play(mts[0].animate(
            run_time=wt,
        ).next_to(
            mm_b1,
            UP,
            buff=TENSOR_VGAP_SMALL,
        ))
        # self.wait(wt)

        # NOTE: new perspective
        # arrange mm_bs
        gap = mts[1].height + TENSOR_VGAP_MINI*2
        mm_bs.generate_target()
        mm_bs.target.arrange(
            DOWN,
            buff=gap,
        ).move_to(
            mm_bs,
            aligned_edge=UL,
        )
        self.move_camera(
            zoom=0.85,
            frame_center=1.5*DOWN,
            added_anims=[
                MoveToTarget(mm_bs),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply b1',
            skip_animations=False,
        )
        # ************************************************************
        mts[1].next_to(
            mm_b1,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(AnimationGroup(
            mm_b1.breath(
                lag_ratio=0.5,
                run_time=wt,
            ),
            mts[1].create(
                ref='top',
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply b2',
            skip_animations=False,
        )
        # ************************************************************
        mts[2].next_to(
            mm_b2,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(AnimationGroup(
            mm_b2.breath(
                lag_ratio=0.5,
                run_time=wt,
            ),
            mts[2].create(
                ref='top',
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply b3',
            skip_animations=False,
        )
        # ************************************************************
        mts[3].next_to(
            mm_b3,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(AnimationGroup(
            mm_b3.breath(
                lag_ratio=0.5,
                run_time=wt,
            ),
            mts[3].create(
                ref='top',
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply split',
            skip_animations=False,
        )
        # ************************************************************
        # NOTE: new perspective
        self.move_camera(
            zoom=0.7,
            frame_center=4.5*DOWN,
            run_time=wt,
        )
        self.wait(wt)

        # split animation
        # TODO: as template for other split animations
        mts_split = VGroup(mts[4], mts[5], mts[6], mts[7])
        mts_split.set_fill(opacity=0.1)
        mts[4].move_to(mts[3]).align_to(mts[3], OUT)
        mts[5].next_to(mts[4], IN, buff=0.0)
        mts[7].move_to(mts[3]).align_to(mts[3], IN)
        mts[6].next_to(mts[7], OUT, buff=0.0)

        # split module wiggles
        self.play(Wiggle(
            mg.cards_box[3],
            scale_value=1.2,
            run_time=wt,
        ))

        # write split targets
        self.play(AnimationGroup(
            Write(mts[4]),
            Write(mts[5]),
            Write(mts[6]),
            Write(mts[7]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # split animation
        mts_split.generate_target()
        mts_split.target.arrange(
            IN,
            buff=TENSOR_VGAP_MINI,
        ).next_to(
            mts[3],
            DOWN,
            buff=TENSOR_VGAP_MINI,
        ).set_fill(
            opacity=1.0,
        )
        self.play(AnimationGroup(
            Transform(mts[4], mts_split.target[0]),
            Transform(mts[5], mts_split.target[1]),
            Transform(mts[6], mts_split.target[2]),
            Transform(mts[7], mts_split.target[3]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply softmax in batch',
            skip_animations=False,
        )
        # ************************************************************
        # TODO: maybe a hint for softmax's dim?

        mts[8].next_to(mts[4], DOWN, buff=TENSOR_VGAP_MINI)
        mts[9].next_to(mts[5], DOWN, buff=TENSOR_VGAP_MINI)
        mts[10].next_to(mts[6], DOWN, buff=TENSOR_VGAP_MINI)
        mts[11].next_to(mts[7], DOWN, buff=TENSOR_VGAP_MINI)
        self.play(Succession(
            Wiggle(
                mg.cards_box[4],
                scale_value=1.2,
                run_time=wt,
            ),
            AnimationGroup(
                *(GrowFromCenter(
                    mto,
                    rate_func=rate_functions.ease_out_back,
                ) for mto in (mts[8], mts[9], mts[10], mts[11])),
                lag_ratio=0.5,
                run_time=wt,
            ),
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply concat',
            skip_animations=False,
        )
        # ************************************************************
        # prepare copies
        mts_copy = mts[8:12].copy()
        mts_copy.set_fill(opacity=0.1)

        # concat module card wiggles
        self.play(Wiggle(
            mg.cards_box[5],
            scale_value=1.2,
            run_time=wt,
        ))

        # show copy
        self.play(FadeIn(
            mts_copy,
            run_time=wt*0.1,
        ))

        # direct concat animation
        self.play(mts_copy.animate(
            run_time=wt,
        ).arrange(
            IN, buff=0.0,
        ).next_to(
            mts[8:12],
            DOWN,
            buff=TENSOR_VGAP_MINI,
        ))

        # replace multiple with single
        mts[12].move_to(mts_copy)
        self.play(AnimationGroup(
            *(Unwrite(mt) for mt in mts_copy),
            Write(mts[12]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'prepare for cls prediction',
            skip_animations=False,
        )
        # ************************************************************
        mask = np.zeros(mg.ncards, dtype=bool)
        mask[6:] = True

        series_box = VGroup(
            *mm_bs,
            *mts[1:13],
        )

        # TODO: align input to cls series
        self.play(mts[0].animate(
            run_time=wt,
        ).next_to(
            mm_c1,
            UP,
            buff=TENSOR_VGAP_SMALL,
        ))

        # NOTE: new perspective
        # fade box series and lightup cls series
        new_center = 2.5*DOWN
        new_center[0] = mm_c1.get_x()
        self.move_camera(
            phi=50*DEGREES,
            frame_center=new_center,
            added_anims=[
                AnimationGroup(
                    mg.highlight(mask=mask),
                    AnimationGroup(
                        *(m.tarnish() for m in series_box),
                        lag_ratio=0.0,
                    ),
                    mm_c1.lightup(),
                    mm_c2.lightup(),
                    mm_c3.lightup(),
                    lag_ratio=0.0,
                    run_time=wt,
                ),
            ],
            run_time=wt,
        )
        # self.wait(wt)

        # arrange mm_cs
        gap = mts[13].height + TENSOR_VGAP_MINI*2
        mm_cs.generate_target()
        mm_cs.target.arrange(
            DOWN,
            buff=gap,
        ).move_to(
            mm_cs,
            aligned_edge=UL,
        )
        self.play(
            MoveToTarget(mm_cs),
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply c1, c2, c3 fast',
            skip_animations=False,
        )
        # ************************************************************
        mts[13].next_to(
            mm_c1,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        mts[14].next_to(
            mm_c2,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        mts[15].next_to(
            mm_c3,
            DOWN,
            buff=TENSOR_VGAP_MINI,
        )
        self.play(AnimationGroup(
            mm_c1.breath(
                lag_ratio=0.5,
                run_time=wt,
            ),
            mts[13].create(
                ref='top',
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.play(AnimationGroup(
            mm_c2.breath(
                lag_ratio=0.5,
                run_time=wt,
            ),
            mts[14].create(
                ref='top',
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.play(AnimationGroup(
            mm_c3.breath(
                lag_ratio=0.5,
                run_time=wt,
            ),
            mts[15].create(
                ref='top',
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply sigmoid',
            skip_animations=False,
        )
        # ************************************************************
        mts[16].next_to(mts[15], DOWN, buff=TENSOR_VGAP_MINI)
        self.play(Succession(
            Wiggle(
                mg.cards_cls[-1],
                scale_value=1.2,
                run_time=wt,
            ),
            GrowFromCenter(
                mts[16],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ),
        ))
        self.wait(wt)
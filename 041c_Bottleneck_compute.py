# ************************************************************
# Detailed Compute loop for Bottleneck (shortcut=False).
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
        # load card and graph
        mc, mg = import_mobs('041b')
        module_config = mg.module_config

        # raw modules
        m_module = Bottleneck(**module_config)
        m_cv1 = m_module.cv1
        m_cv2 = m_module.cv2

        # raw tensor
        t_i = torch.randn(1, 8, 5, 6)
        t_m1 = m_cv1(t_i)
        t_o = m_cv2(t_m1)

        # module mobs (cv1 and cv2)
        mm_cv1 = UT_Conv(
            module_config=Bottleneck_2_cv1_config(module_config),
        )
        mm_cv2 = UT_Conv(
            module_config=Bottleneck_2_cv2_config(module_config),
        )
        VGroup(mm_cv1, mm_cv2).arrange(
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        # tensor mobs
        mts = VGroup(
            FTensor3D(
                shape=t[0].shape,
            ) for t in [
                t_i, t_m1, t_o,
            ]
        )

        increase_z_index_in_batch([
            mts[0],
            mm_cv1,
            mts[1],
            mm_cv2,
            mts[2],
        ])

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(mc, mg)
        self.wait(wt)
        
        # ************************************************************
        self.next_section(
            'tags on graph config',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, in previous script, when graph is in the center

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
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight cv2 in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[1],
            run_time=wt,
        ))
        # self.wait(wt)

        # show cv2
        self.play(mm_cv2.create(
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
            'show sample input',
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
            'output from cv1',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[0]),
            mm_cv2.ft_conv.tarnish(),
            mm_cv2.ft_bn.tarnish(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # make space in the mid
        gap = mts[1].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_cv1),
            mm_cv2,
        )
        mobs.generate_target()
        mobs.target.arrange(
            DOWN,
            buff=gap,
        )
        # point that should reside in ORIGIN
        target_center = mobs.target[0][1].get_bottom() + mobs.target[1].get_top() / 2
        mobs.target.shift(
            target_center[1] * DOWN,
            # mts[1].get_y()*DOWN,
        )
        self.play(MoveToTarget(mobs, run_time=wt))
        self.wait(wt)

        self.play(mobs.animate(
            run_time=wt,
        ).arrange(
            DOWN,
            buff=gap,
        ).align_to(
            mts[0],
            UP,
        ))
        # self.wait(wt)

        # m0 -[cv1]-> m1
        mts[1].next_to(
            mm_cv1,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )
        self.play(AnimationGroup(
            mts[1].create(
                ref='top',
                rate_func=smooth,
                run_time=wt*3,
            ),
            mm_cv1.breath(
                rate_func=smooth,
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            lag_ratio=0.1,
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
            'output from cv2',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[1]),
            mts[0].tarnish(),
            mm_cv1.ft_conv.tarnish(),
            mm_cv1.ft_bn.tarnish(),
            mm_cv2.ft_conv.lightup(),
            mm_cv2.ft_bn.lightup(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # m1 -[cv2]-> m2
        mts[2].next_to(
            mm_cv2,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )
        self.play(AnimationGroup(
            mts[2].create(
                ref='top',
                rate_func=smooth,
                run_time=wt*3,
            ),
            mm_cv2.breath(
                rate_func=smooth,
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            lag_ratio=0.1,
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_o.detach()[0]),
            index=2,
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
            mts[0].lightup(),
            mm_cv1.ft_conv.lightup(),
            mm_cv1.ft_bn.lightup(),
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
            mts[0], mm_cv1, mts[1], mm_cv2, mts[2],
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
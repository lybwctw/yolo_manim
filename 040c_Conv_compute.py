# ************************************************************
# Detailed Compute loop for Conv.
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
from modules.pt_Conv2d import *
from modules.pt_BatchNorm2d import *

from ultralytics.nn.modules import Conv

TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

# INIT_CONFIG = {
#     'c1': 4,
#     'c2': 5,
#     'k': 3,
#     's': 2,
#     'p': 1,
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
        mc, mg = import_mobs('040b')
        module_config = mg.module_config

        # raw modules
        m_module = Conv(**module_config)
        m_conv = m_module.conv
        m_bn = m_module.bn
        m_bn.eval()
        m_act = m_module.act

        # raw tensor
        t_i = torch.randn(1, 4, 5, 6)
        t_m1 = m_conv(t_i)
        t_m2 = m_bn(t_m1)
        t_o = m_act(t_m2)

        # module mobs (conv and bn)
        # TODO: use general func to generate sub config
        mm_conv = PT_Conv2d(
            module=m_conv,
            module_config=mg.config_conv,
            block_gap=0.5,
            bias_offset=0.5,
        )
        mm_bn = PT_BatchNorm2d(
            module=m_bn,
            module_config=mg.config_bn,
            mtensor_dir=RIGHT,
            mtensor_gap=0.5,
        )
        VGroup(mm_conv, mm_bn).arrange(
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )

        # tensor mobs
        mts = VGroup(
            MTensor3D(
                array=t.detach()[0],
                mode='cube',
                **SMALL_TENSOR_CONFIG,
            ) for t in [
                t_i, t_m1, t_m2, t_o,
            ]
        )

        # TODO: increate inside mob Conv
        increase_z_index_in_batch([
            mts[0],
            mm_conv.mt_weight,
            mts[1],
            mm_bn.mt_bias,
            mm_bn.mt_weight,
            mm_bn.mt_running_var,
            mm_bn.mt_running_mean,
            mts[2],
            mts[3],
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
        # highlight conv in graph
        masks = np.eye(mg.ncards,dtype=bool)
        self.play(mg.highlight(
            mask=masks[0],
            run_time=wt,
        ))
        # self.wait(wt)

        # show conv params (4d)
        self.play(mm_conv.create(
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight bn in graph
        self.play(mg.highlight(
            mask=masks[1],
            run_time=wt,
        ))

        # show bn params (4x1d)
        self.play(mm_bn.create(
            run_time=wt,
        ))
        # self.wait(wt)

        # highlight act in graph and back
        self.play(mg.highlight(
            mask=masks[2],
            run_time=wt,
        ))
        self.wait(wt)
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
            mm_conv,
            UP,
            TENSOR_VGAP_SMALL,
        )
        self.play(mts[0].create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        # self.wait(wt)

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
            'output from conv',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(
                mask=masks[0],
            ),
            *(mt.highlight(
                np.zeros(mm_bn.mt_bias.shape, dtype=bool)
            ) for mt in [
                mm_bn.mt_running_mean,
                mm_bn.mt_running_var,
                mm_bn.mt_weight,
                mm_bn.mt_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # make space in the mid
        gap = mts[1].height + TENSOR_VGAP_SMALL * 2
        mobs = VGroup(
            VGroup(mts[0], mm_conv),
            mm_bn,
        )
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

        # m0 -[Conv2d]-> m1
        mts[1].next_to(
            mm_conv,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )
        self.play(AnimationGroup(
            mm_conv.mt_weight.breath(
                style='whole',
                rate_func=smooth,           # sync with default
                lag_ratio=0.5,              # sync with default
            ),
            mts[1].create(
                style='layer',
                direction=IN,
                # rate_func=smooth,         # smooth by default
                # lag_ratio=1.0,            # 0.5 by default
            ),
            lag_ratio=0.1,
            run_time=wt*3,
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
            'output from bn',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[1]),
            *(mt.highlight() for mt in [
                mm_bn.mt_running_mean,
                mm_bn.mt_running_var,
                mm_bn.mt_weight,
                mm_bn.mt_bias,
            ]),
            mts[0].highlight(
                np.zeros(mts[0].shape, dtype=bool)
            ),
            mm_conv.mt_weight.highlight(
                np.zeros(mm_conv.mt_weight.shape, dtype=bool)
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # zoom out and new center
        self.move_camera(
            zoom=0.9,
            frame_center=mts[1].get_center(),
            run_time=wt,
        )
        # self.wait(wt)

        # m1 -[BatchNorm2d]-> m2
        mts[2].next_to(
            mm_bn,
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )
        self.play(AnimationGroup(
            mts[1].breath(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            *(mt.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ) for mt in [
                mm_bn.mt_running_mean,
                mm_bn.mt_running_var,
                mm_bn.mt_weight,
                mm_bn.mt_bias,
            ]),
            mts[2].create(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            lag_ratio=0.0
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
            'output from act',
            skip_animations=False,
        )
        # ************************************************************
        # highlight and fade
        self.play(AnimationGroup(
            mg.highlight(mask=masks[2]),
            mts[1].highlight(
                np.zeros(mts[1].shape, dtype=bool)
            ),
            *(mt.highlight(
                np.zeros(mm_bn.mt_bias.shape, dtype=bool)
            ) for mt in [
                mm_bn.mt_running_mean,
                mm_bn.mt_running_var,
                mm_bn.mt_weight,
                mm_bn.mt_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # zoom out and new center
        self.move_camera(
            zoom=0.75,
            frame_center=VGroup(mts[1],mm_bn).get_center(),
            run_time=wt,
        )
        # self.wait(wt)

        # m2 -[SiLU]-> m3
        mts[3].next_to(
            mts[2],
            DOWN,
            buff=TENSOR_VGAP_SMALL,
        )
        self.play(AnimationGroup(
            mts[2].breath(
                style='whole',
                run_time=wt,
            ),
            mts[3].create(
                style='whole',
                run_time=wt,
            ),
            lag_ratio=0.8,
        ))
        self.wait(wt)

        # show shape in graph
        self.play(mg.show_shape(
            t2s(t_o.detach()[0]),
            index=3,
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
            *(mt.highlight() for mt in [
                mts[0],
                mm_conv.mt_weight,
                mts[1],
                mm_bn.mt_running_mean,
                mm_bn.mt_running_var,
                mm_bn.mt_weight,
                mm_bn.mt_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))

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

        # remove mid tensors
        self.play(AnimationGroup(
            mts[1].uncreate(
                style='beam',
                direction=IN,
                run_time=wt,
            ),
            mts[2].uncreate(
                style='beam',
                direction=IN,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))

        # compact input / params / output
        mobs = VGroup(
            mts[0],
            mm_conv,
            mm_bn,
            mts[3],
        )
        self.move_camera(
            zoom=1.0,
            frame_center=ORIGIN,
            added_anims=[
                mobs.animate.arrange(
                    DOWN,
                    buff=TENSOR_VGAP_SMALL,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # export
        mobs = VGroup(
            tc_i, mc, tc_o,
            mts[0], mm_conv, mm_bn, mts[3],
            mg,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
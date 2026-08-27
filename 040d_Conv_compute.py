# ************************************************************
# Simplified compute loop for Conv.
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
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        (
            tc_i, mc, tc_o,
            mt_i, mm_conv, mm_bn, mt_o,
            mg,
        ) = import_mobs('040c')

        # existing mobs
        module_config = mg.module_config
        params_bn = VGroup(
            mm_bn.mt_running_mean,
            mm_bn.mt_running_var,
            mm_bn.mt_weight,
            mm_bn.mt_bias,
        )

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            tc_i, mc, tc_o, mg,
        )
        self.add(
            mt_i, mm_conv, mm_bn, mt_o,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'clean output',
            skip_animations=True,
        )
        # ************************************************************
        mt_o.save_state()
        self.play(AnimationGroup(
            mt_o.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            tc_o.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        mt_o.restore()      # reuse later

        # remove shapes in graph?

        # ************************************************************
        self.next_section(
            'tags on bn params',
            skip_animations=True,
        )
        # ************************************************************
        # name tag assets
        tag_running_mean = NameTag(
            ref=p2f(self, params_bn[0].get_corner(DL+IN)),
            text='running_mean',
            leader_direction=DR,
        )
        tag_running_var = NameTag(
            ref=p2f(self, params_bn[1].get_corner(DL+IN)),
            text='running_var',
            leader_direction=DR,
        )
        tag_weight = NameTag(
            ref=p2f(self, params_bn[2].get_corner(DL+IN)),
            text='weight',
            leader_direction=DR,
        )
        tag_bias = NameTag(
            ref=p2f(self, params_bn[3].get_corner(DL+IN)),
            text='bias',
            leader_direction=DR,
        )

        # show tags
        self.play(AnimationGroup(
            tag_running_mean.create(),
            tag_running_var.create(),
            tag_weight.create(),
            tag_bias.create(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # hide tags
        self.play(AnimationGroup(
            tag_running_mean.uncreate(),
            tag_running_var.uncreate(),
            tag_weight.uncreate(),
            tag_bias.uncreate(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'rearrange bn params',
            skip_animations=True,
        )
        # ************************************************************
        c = module_config['c2']
        vgs_conv = VGroup(mm_conv.mt_weight[i] for i in range(c))
        vgs_bn = VGroup(VGroup(
            mm_bn.mt_running_mean[i],
            mm_bn.mt_running_var[i],
            mm_bn.mt_weight[i],
            mm_bn.mt_bias[i],
        ) for i in range(c))

        # compact
        self.play(params_bn.animate(
            run_time=wt,
        ).arrange(
            RIGHT,
            buff=0.0,
        ).move_to(
            params_bn.get_center(),
        ))

        # rotate
        self.play(Rotate(
            params_bn,
            90*DEGREES,
            axis=DOWN,
            run_time=wt,
        ))

        # split
        self.play(AnimationGroup(
            *(vg_bn.animate.next_to(
                vg_conv,
                DOWN,
                buff=TENSOR_VGAP_SMALL,
            ) for vg_bn, vg_conv in zip(
                vgs_bn, vgs_conv
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # rotate to reverse order
        self.play(AnimationGroup(
            *(Rotate(
                vg,
                180*DEGREES,
                axis=RIGHT,
            ) for vg in vgs_bn),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'tags on bn again',
            skip_animations=True,
        )
        # ************************************************************
        # name tag assets
        tag_running_mean = NameTag(
            ref=p2f(self, vgs_bn[2][0].get_corner(DOWN)),
            text='running_mean',
            leader_direction=DR,
        )
        tag_running_var = NameTag(
            ref=p2f(self, vgs_bn[2][1].get_corner(DOWN)),
            text='running_var',
            leader_direction=DR,
        )
        tag_weight = NameTag(
            ref=p2f(self, vgs_bn[2][2].get_corner(DOWN)),
            text='weight',
            leader_direction=DR,
        )
        tag_bias = NameTag(
            ref=p2f(self, vgs_bn[2][3].get_corner(DOWN)),
            text='bias',
            leader_direction=DR,
        )

        # show tags
        self.play(AnimationGroup(
            tag_running_mean.create(),
            tag_running_var.create(),
            tag_weight.create(),
            tag_bias.create(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # hide tags
        self.play(AnimationGroup(
            tag_running_mean.uncreate(),
            tag_running_var.uncreate(),
            tag_weight.uncreate(),
            tag_bias.uncreate(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply conv and bn',
            skip_animations=True,
        )
        # ************************************************************
        # highlight and fade
        masks_graph = np.zeros((2,mg.ncards), dtype=bool)
        masks_graph[0, :2] = True
        masks_graph[1, 2] = True
        self.play(mg.highlight(
            mask=masks_graph[0],
            run_time=wt,
        ))
        # self.wait(wt)

        # loop
        self.play(AnimationGroup(
            mm_conv.mt_weight.breath(
                style='whole',
                rate_func=smooth,           # sync with default
                lag_ratio=0.5,              # sync with default
                run_time=wt*3,
            ),
            AnimationGroup(
                *(AnimationGroup(
                    *(cube.breath() for cube in beam),
                    lag_ratio=0.0,
                ) for beam in vgs_bn),
                rate_func=smooth,
                lag_ratio=0.5,
                run_time=wt*3,
            ),
            mt_o.create(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply act',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mg.highlight(
            mask=masks_graph[1],
            run_time=wt,
        ))
        # self.wait(wt)

        self.play(mt_o.translate(
            style='whole',
            run_time=wt*2,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean job',
            skip_animations=False,
        )
        # ************************************************************
        # lightup graph and output summary
        self.play(AnimationGroup(
            mg.highlight(),
            tc_o.expand_summary(t2s(mt_o.array)),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
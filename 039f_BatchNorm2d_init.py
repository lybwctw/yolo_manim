from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *

from modules.pt_Conv2d import *

import torch
import numpy as np

PARAM_HGAP_3D = 1.5

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load cards and input
        (
            card_i1,
            card_module,
            card_o1,
            mob_module,
        ) = import_mobs('039e')

        # raw module
        torch_module = mob_module.module
        module_config = mob_module.module_config
        mob_running_mean = mob_module.mt_running_mean
        mob_running_var = mob_module.mt_running_var
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show exact values of params',
            skip_animations=False,
        )
        # ***********************************************************#
        # FIXME: new perspective necessary??
        self.move_camera(
            **VIEW_INTRO,
            zoom=1.7,
            added_anims=[
                AnimationGroup(
                    *(mob.switch(
                        style='series',
                        direction=RIGHT,
                    ) for mob in [
                        mob_running_mean,
                        mob_running_var,
                        mob_weight,
                        mob_bias,
                    ]),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt*2,
        )
        self.wait(wt)

        # back
        self.play(AnimationGroup(
            *(mob.switch(
                style='series',
                direction=RIGHT,
            ) for mob in [
                mob_running_mean,
                mob_running_var,
                mob_weight,
                mob_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt*2,
        ))

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ***********************************************************#
        # FIXME: use module's uncreate?
        # remove module params
        self.play(AnimationGroup(
            *(mob.uncreate(
                style='series',
                direction=RIGHT,
                anim=Unwrite,
            ) for mob in [
                mob_running_mean,
                mob_running_var,
                mob_weight,
                mob_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # remove tensor cards
        self.play(AnimationGroup(
            detach_to_ref(card_i1, UP),
            detach_to_ref(card_o1, DOWN),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # shrink module card
        self.play(card_module.shrink_params(
            run_time=wt,
        ))
        self.wait(wt)
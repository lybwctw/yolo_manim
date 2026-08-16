from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *

from modules.pt_Conv2d import *

import torch

TENSOR_VGAP_3D = 2.0
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load cards and input
        (
            card_i1,
            card_module,
            card_o1,
            mob_i1,
            mob_module,
            mob_o1,
        ) = import_mobs('032h')

        # raw module and manim module
        mob_weight = mob_module.mt_weight
        torch_module = mob_module.module
        module_config = mob_module.module_config

        # raw tensors
        t_i1 = mob_i1.tensor[None,:]    # FIXME: manual new dim
        t_o1 = mob_o1.tensor[None,:]    # FIXME: manual new dim

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.add(mob_i1, mob_module, mob_o1)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'receptive field of output sample beam',
            skip_animations=True,
        )
        # ************************************************************
        mask_w = np.zeros(mob_weight.shape, dtype=bool)
        mask_o1 = np.zeros(mob_o1.shape, dtype=bool)
        mask_o1[:, 2, 3] = True
        mask_i1 = np.zeros(mob_i1.shape, dtype=bool)
        mask_i1[:, 1:4, 2:5] = True     # FIXME: manual

        # tarnish the whole weight
        self.play(mob_weight.highlight(
            mask=mask_w,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight sample beam in output
        self.play(mob_o1.highlight(
            mask=mask_o1,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight sample sublock in input
        self.play(mob_i1.highlight(
            mask=mask_i1,
            run_time=wt,
        ))
        self.wait(wt)

        # switch mode
        self.play(AnimationGroup(
            mob_weight.switch(
                style='beam',
                direction=IN,
                lag_ratio=0.0,
            ),
            mob_o1.switch(
                style='beam',
                direction=IN,
            ),
            mob_i1.switch(
                style='beam',
                direction=IN,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'changing sample receptive field',
            skip_animations=False,
        )
        # ************************************************************
        mob_i1.save_state()
        mob_o1.save_state()
        mob_weight.save_state()

        # focus on input / output
        self.move_camera(
            zoom=2.0,
            added_anims=[
                mob_weight.animate.fade(1.0),
                mob_i1.animate.next_to(
                    mob_weight,
                    UP,
                    buff=TENSOR_VGAP_3D*-0.5,
                ),
                mob_o1.animate.next_to(
                    mob_weight,
                    DOWN,
                    buff=TENSOR_VGAP_3D*-0.5,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)
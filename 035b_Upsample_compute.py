from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
import torch
import numpy as np

TENSOR_VGAP_3D = 1.0
TENSOR_HGAP_3D = 0.7
# TENSOR_EGAP_3D = 1.0

EMPTY_CONFIG = {
    'scale_factor': UNKNOWN,
    'mode': UNKNOWN,
    'align_corners': UNKNOWN,
}

INIT_CONFIG = {
    'scale_factor': 2.0,
    'mode': 'nearest',
    'align_corners': None,
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('034a')

        # raw module, no visible module
        module_config = INIT_CONFIG
        torch_module = torch.nn.Upsample(**module_config)

        # raw tensor
        t_i1 = torch.randn(1, 5, 3, 4)
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            TENSOR_VGAP_3D*UP,
            DOWN,
        )

        # output tensor mob
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            TENSOR_VGAP_3D*DOWN,
            UP,
        )

        # reposition input/output due to imbalance
        VGroup(mob_i1, mob_o1).center()

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'starting module card',
            skip_animations=True,
        )
        # ************************************************************
        # expand empty module card
        self.play(card_module.expand_params(
            params=EMPTY_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # update module card config
        self.play(card_module.update_params(
            module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=True,
        )
        # ************************************************************
        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        # self.wait(wt)

        # show input summary
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i1)
        self.play(attach_to_ref(
            card_i1,
            card_module,
            UP,
            run_time=wt,
        ))
        self.play(card_i1.expand_summary(
            t2s(t_i1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'first compute',
            skip_animations=True,
        )
        # ************************************************************
        c, h, w = mob_i1.shape
        masks_input = np.eye(h*w, dtype=bool).reshape(h*w,h,w)[:,None,:,:].repeat(c,1)
        masks_output = mob_o1.conv2d_masks(
            kh=int(module_config['scale_factor']),
            kw=int(module_config['scale_factor']),
            sh=int(module_config['scale_factor']),
            sw=int(module_config['scale_factor']),
        )
        blks_output = mob_o1.get_vgs(masks_output)

        # highlight first input beam
        self.play(mob_i1.highlight(
            mask=masks_input[0],
            run_time=wt,
        ))
        self.wait(wt)

        # generate first output block
        self.play(AnimationGroup(
            *(GrowFromCenter(
                mob,
                rate_func=rate_functions.ease_out_back,
            ) for mob in blks_output[0]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'the rest of compute loop',
            skip_animations=True,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input[1:],
                rate_func=smooth,
                run_time=wt*5,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in blk),
                    lag_ratio=0.0,
                ) for blk in blks_output[1:]),
                rate_func=smooth,
                run_time=wt*5,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # restore input
        self.play(mob_i1.highlight(
            run_time=wt,
        ))

        # show output summary
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1)
        self.play(attach_to_ref(
            card_o1,
            card_module,
            DOWN,
            run_time=wt,
        ))
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'switch to show exact value',
            skip_animations=True,
        )
        # ************************************************************
        vg = VGroup(mob_i1, mob_o1)
        vg.save_state()
        vg.generate_target()
        vg.target.arrange(
            RIGHT,
            buff=TENSOR_HGAP_3D,
        ).center()

        # new perspective
        self.move_camera(
            **VIEW_INTRO,
            zoom=1.7,
            added_anims=[
                MoveToTarget(vg),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # switch input/output
        self.play(AnimationGroup(
            mob_i1.switch(
                style='layer',
                direction=IN,
            ),
            mob_o1.switch(
                style='layer',
                direction=IN,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # loop by layers
        masks_input = np.tile(
            np.eye(mob_i1.shape[0],dtype=bool)[:,:,None,None],
            (1, 1, mob_i1.shape[1], mob_i1.shape[2]),
        )
        masks_output = np.tile(
            np.eye(mob_o1.shape[0],dtype=bool)[:,:,None,None],
            (1, 1, mob_o1.shape[1], mob_o1.shape[2]),
        )
        self.play(AnimationGroup(
            mob_i1.highlight_loop(masks=masks_input, rate_func=smooth),
            mob_o1.highlight_loop(masks=masks_output, rate_func=smooth),
            lag_ratio=0.0,
            run_time=wt*5,
        ))
        self.wait(wt)

        # loop back
        masks_input = np.tile(
            np.tri(mob_i1.shape[0],dtype=bool)[:,::-1][1:][:,:,None,None],
            (1, 1, mob_i1.shape[1], mob_i1.shape[2]),
        )
        masks_output = np.tile(
            np.tri(mob_o1.shape[0],dtype=bool)[:,::-1][1:][:,:,None,None],
            (1, 1, mob_o1.shape[1], mob_o1.shape[2]),
        )
        self.play(AnimationGroup(
            mob_i1.highlight_loop(masks=masks_input, rate_func=smooth),
            mob_o1.highlight_loop(masks=masks_output, rate_func=smooth),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # switch back
        self.play(AnimationGroup(
            mob_i1.switch(
                style='layer',
                direction=OUT,
            ),
            mob_o1.switch(
                style='layer',
                direction=OUT,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # original perspective
        self.move_camera(
            **VIEW_COMPUTE,
            zoom=1.0,
            added_anims=[
                Restore(vg),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean output',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_o1.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
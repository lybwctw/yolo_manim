from manim import *

from utils.mtensor import MTensor3D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_HGAP_3D = 1.0
TENSOR_VGAP_3D = 1.5
TENSOR_EGAP_3D = 1.0

CONFIG_0 = {
    'dim': 0,
}

CONFIG_1 = {
    'dim': 1,
}

CONFIG_2 ={
    'dim': 2,
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # cards
        cards = import_mobs('038c')
        (
            card_i1, card_module, card_o1
        ) = cards

        # raw tensors
        t_i1 = torch.randn(4,5,7)

        # tensor mobs
        mob_i1 = MTensor3D(
            array=t_i1,
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        )

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_i1, card_module, card_o1,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show input',
            skip_animations=False,
        )
        # ************************************************************
        # show input
        self.play(AnimationGroup(
            mob_i1.create(
                style='beam',
                direction=OUT,
            ),
            card_i1.expand_summary(
                t2s(t_i1),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'dim 0 compute loop',
            skip_animations=False,
        )
        # ************************************************************
        # new output
        module_config = CONFIG_0
        torch_module = torch.nn.Softmax(**module_config)
        t_o1 = torch_module(t_i1)
        mob_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        c, h, w = mob_i1.shape  # shared by output masks
        masks_input = np.eye(h*w,dtype=bool).reshape(h*w,h,w)[:,None,:,:].repeat(c,1)
        masks_output = np.eye(h*w,dtype=bool).reshape(h*w,h,w)[:,None,:,:].repeat(c,1)
        beams_output = mob_o1.get_vgs(masks_output)

        # update module config
        self.play(card_module.update_params(
            module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # loop
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input,
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(mob, rate_func=rate_functions.ease_out_back)
                      for mob in beam),
                    lag_ratio=0.0,
                ) for beam in beams_output),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # restore input
        self.play(mob_i1.highlight(
            run_time=wt,
        ))
        self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()),
            run_time=wt,
        ))
        self.wait(wt)

        # clean output
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

        # ************************************************************
        self.next_section(
            'dim 1 compute loop',
            skip_animations=False,
        )
        # ************************************************************
        # new output
        module_config = CONFIG_1
        torch_module = torch.nn.Softmax(**module_config)
        t_o1 = torch_module(t_i1)
        mob_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        c, h, w = mob_i1.shape  # shared by output masks
        masks_input = np.eye(c*w,dtype=bool).reshape(c*w,c,w)[:,:,None,:].repeat(h,2)
        masks_output = np.eye(c*w,dtype=bool).reshape(c*w,c,w)[:,:,None,:].repeat(h,2)
        beams_output = mob_o1.get_vgs(masks_output)

        # update module config
        self.play(card_module.update_params(
            module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # loop
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input,
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(mob, rate_func=rate_functions.ease_out_back)
                      for mob in beam),
                    lag_ratio=0.0,
                ) for beam in beams_output),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # restore input
        self.play(mob_i1.highlight(
            run_time=wt,
        ))
        self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()),
            run_time=wt,
        ))
        self.wait(wt)

        # clean output
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

        # ************************************************************
        self.next_section(
            'dim 2 compute loop',
            skip_animations=False,
        )
        # ************************************************************
        # new output
        module_config = CONFIG_2
        torch_module = torch.nn.Softmax(**module_config)
        t_o1 = torch_module(t_i1)
        mob_o1 = MTensor3D(
            array=t_o1,
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        c, h, w = mob_i1.shape  # shared by output masks
        masks_input = np.eye(c*h,dtype=bool).reshape(c*h,c,h)[:,:,:,None].repeat(w,3)
        masks_output = np.eye(c*h,dtype=bool).reshape(c*h,c,h)[:,:,:,None].repeat(w,3)
        beams_output = mob_o1.get_vgs(masks_output)

        # update module config
        self.play(card_module.update_params(
            module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # loop
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input,
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(mob, rate_func=rate_functions.ease_out_back)
                      for mob in beam),
                    lag_ratio=0.0,
                ) for beam in beams_output),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # restore input
        self.play(mob_i1.highlight(
            run_time=wt,
        ))
        self.wait(wt)

        # show output summary
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()),
            run_time=wt,
        ))
        self.wait(wt)

        # clean input/output
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=IN,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [mob_i1, mob_o1],
                [card_i1, card_o1],
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
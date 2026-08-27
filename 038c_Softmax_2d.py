from manim import *

from utils.mtensor import MTensor2D
from utils.general import *
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_2D = 1.5
TENSOR_EGAP_2D = 1.0
TENSOR_HGAP_2D = 1.0

INIT_CONFIG = {
    'dim': 0,
}

NEW_CONFIG = {
    'dim': 1,
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
        cards = import_mobs('038b')
        (
            card_i1, card_module, card_o1
        ) = cards

        # raw tensors
        t_i1 = torch.randn(5,7)
        module_config = INIT_CONFIG

        # tensor mobs
        mob_i1 = MTensor2D(
            array=t_i1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_2D,
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
                direction=RIGHT,
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
            'dim 0 compute loop, first colume',
            skip_animations=False,
        )
        # ************************************************************
        # new output
        torch_module = torch.nn.Softmax(**module_config)
        t_o1 = torch_module(t_i1)
        mob_o1 = MTensor2D(
            array=t_o1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_2D,
            UP,
        )

        masks_input = np.eye(mob_i1.shape[1],dtype=bool)[:,None,:].repeat(mob_i1.shape[0],1)
        masks_output = np.eye(mob_o1.shape[1],dtype=bool)[:,None,:].repeat(mob_o1.shape[0],1)
        beams_output = mob_o1.get_vgs(masks_output)

        # highlight first column of input
        self.play(mob_i1.highlight(
            mask=masks_input[0],
            run_time=wt,
        ))
        self.wait(wt)

        # generate first column of output
        self.play(AnimationGroup(
            *(GrowFromCenter(
                mob,
                rate_func=rate_functions.ease_out_back,
            ) for mob in beams_output[0]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'dim 0 compute loop, the rest',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input[1:],
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(mob, rate_func=rate_functions.ease_out_back)
                      for mob in beam),
                    lag_ratio=0.0,
                ) for beam in beams_output[1:]),
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
                direction=RIGHT,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'dim 1 compute loop, first row',
            skip_animations=False,
        )
        # ************************************************************
        # new output
        module_config = NEW_CONFIG
        torch_module = torch.nn.Softmax(**module_config)
        t_o1 = torch_module(t_i1)
        mob_o1 = MTensor2D(
            array=t_o1,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_2D,
            UP,
        )

        masks_input = np.eye(mob_i1.shape[0],dtype=bool)[:,:,None].repeat(mob_i1.shape[1],2)
        masks_output = np.eye(mob_o1.shape[0],dtype=bool)[:,:,None].repeat(mob_o1.shape[1],2)
        beams_output = mob_o1.get_vgs(masks_output)

        # update module config
        self.play(card_module.update_params(
            module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight first row of input
        self.play(mob_i1.highlight(
            mask=masks_input[0],
            run_time=wt,
        ))
        self.wait(wt)

        # generate first row of output
        self.play(AnimationGroup(
            *(GrowFromCenter(
                mob,
                rate_func=rate_functions.ease_out_back,
            ) for mob in beams_output[0]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'dim 1 compute loop, the rest',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input[1:],
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(mob, rate_func=rate_functions.ease_out_back)
                      for mob in beam),
                    lag_ratio=0.0,
                ) for beam in beams_output[1:]),
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

        # ************************************************************
        self.next_section(
            'clean input/output',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='beam',
                    direction=RIGHT,
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
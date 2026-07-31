from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor_3D
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
        # load mobs and torch module
        (
            card_i1,
            card_module,
            card_o1,
            mob_i1,
        ) = import_mobs('032f')

        # new module and mob
        module_config = {
            'in_channels': 3,
            'out_channels': 8,
            'kernel_size': 3,
            'stride': 1,
            'padding': 1,
            'bias': False,
            'dilation': 1,
            'groups': 1,
            'padding_mode': 'zeros',
        }
        torch_module = torch.nn.Conv2d(
            **module_config,
        )
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=module_config,
        )

        # new output and mob
        t_i1 = mob_i1.tensor[None,:]    # FIXME: manual new dim
        t_o1 = torch_module(t_i1)
        mob_o1 = MTensor_3D(
            array=t_o1.detach()[0],
            **SMALL_3D_CUBE_CONFIG,
        ).next_to(
            mob_module,
            DOWN,
            TENSOR_VGAP_3D,
        )

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.add(mob_i1)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show new module weights',
            skip_animations=True,
        )
        # ************************************************************
        # update with new params
        # NOTE: assert that only in_channels changes
        self.play(card_module.update_params(
            params={'out_channels': module_config['out_channels']},
            run_time=wt,
        ))
        card_module.add(card_module.line_mobs)    # FIXME

        # show new weights
        self.play(mob_module.mobs_weight.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={
                'lag_ratio': 0.1,
                'run_time': wt,
            },
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'pad before compute',
            skip_animations=True,
        )
        # ************************************************************
        self.play(mob_i1.pad(
            pad_width=(
                0,
                module_config['padding'],
                module_config['padding'],
            ),
            pad_value=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'fast layer compute loop',
            skip_animations=True,
        )
        # ************************************************************
        mob_i1.prepare_for_highlight()
        mob_module.mobs_weight.prepare_for_highlight()

        masks_weight = [ ]
        for blk_idx in range(mob_o1.shape[0]):
            mask = np.zeros(mob_module.mobs_weight.shape, dtype=bool)
            mask[blk_idx] = True
            masks_weight.append(mask)

        o1_layers = [mob_o1[i] for i in range(mob_o1.shape[0])]
        self.play(AnimationGroup(
            mob_module.mobs_weight.highlight_loop(
                masks=masks_weight,
                back=False,
                rate_func=smooth,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in layer),
                    lag_ratio=0.0,
                ) for layer in o1_layers),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # unfade module blocks
        self.play(mob_module.mobs_weight.highlight(
            run_time=wt,
        ))

        # unpad input tensor
        self.play(mob_i1.unpad(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'output summary',
            skip_animations=True,
        )
        # ************************************************************
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'shapes on input/weights/output',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # show shapes
        # self.play(AnimationGroup(
        #     ShowShape3D(
        #         scene=self,
        #         mob=mob_module.mobs_weight,
        #         facing='right',
        #         aargs={'lag_ratio': 0.5},
        #     ),
        #     ShowShape3D(
        #         scene=self,
        #         mob=mob_i1,
        #         facing='right',
        #         aargs={'lag_ratio': 0.5},
        #     ),
        #     ShowShape3D(
        #         scene=self,
        #         mob=mob_o1,
        #         facing='right',
        #         aargs={'lag_ratio': 0.5},
        #     ),
        #     run_time=wt*4,
        # ))
        # self.wait(wt)

        # # hide shapes
        # self.play(AnimationGroup(
        #     *(HideShape3D(
        #         mob=mob,
        #         aargs={'lag_ratio': 0.5},
        #     ) for mob in [
        #         mob_i1,
        #         mob_module.mobs_weight,
        #         mob_o1,
        #     ]),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'highlight sample output beam and input block',
            skip_animations=False,
        )
        # ************************************************************
        mob_i1.prepare_for_highlight()
        mob_o1.prepare_for_highlight()

        mask_o = np.zeros(mob_o1.shape, dtype=bool)
        mask_o[:, 1, 2] = True
        mask_i = np.zeros(mob_i1.shape, dtype=bool)
        mask_i[:, 0:3, 1:4] = True

        # highlight sample beam in output
        self.play(mob_o1.highlight(
            mask=mask_o,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight receptive field in input
        self.play(mob_i1.highlight(
            mask=mask_i,
            run_time=wt,
        ))
        self.wait(wt)

        # highlight back
        self.play(AnimationGroup(
            mob_i1.highlight(),
            mob_o1.highlight(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'switch mode and highlight again',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            mob_i1.switch_mode(
                style='beam',
                direction=IN,
            ),
            mob_o1.switch_mode(
                style='beam',
                direction=IN,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        mob_i1.prepare_for_highlight()
        mob_o1.prepare_for_highlight()

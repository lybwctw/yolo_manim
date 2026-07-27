from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor_3D
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
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
        card_module, mob_module, _ = import_mobs('032a')
        torch_module = mob_module.module
        module_config = mob_module.module_config

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '(6,4,7) -[Conv2d]- (5,4,7)',
            skip_animations=False,
        )
        # ************************************************************
        # raw tensor
        t_i1 = torch.randn(1, 6, 4, 7)
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor_3D(
            array=t_i1.detach()[0],
            **SMALL_3D_CUBE_CONFIG,
        ).next_to(
            mob_module,
            UP,
            TENSOR_VGAP_3D,
        )

        # output tensor mob
        mob_o1 = MTensor_3D(
            array=t_o1.detach()[0],
            **SMALL_3D_CUBE_CONFIG,
        ).next_to(
            mob_module,
            DOWN,
            TENSOR_VGAP_3D,
        )

        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'run_time': wt},
        ))
        self.wait(wt)

        # # show input summary
        # card_i1 = InfoCard('in_1').hide_to_corner(UP)
        # self.add_fixed_in_frame_mobjects(card_i1)
        # self.play(attach_to_ref(
        #     card_i1,
        #     card_module,
        #     UP,
        #     run_time=wt,
        # ))
        # self.play(card_i1.expand_summary(
        #     t2s(t_i1.detach()[0]),
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # FIXME: show compute output
        # self.play(mob_o1.create(
        #     style='beam',
        #     direction=OUT,
        #     anim=GrowFromCenter,
        #     aargs={'rate_func': rate_functions.ease_out_back},
        #     gargs={'run_time': wt},
        # ))
        # self.wait(wt)

        # --------------  compute output ----------------
        # pad
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

        # TODO: switch mode to show exact pad value

        layers_output = []
        mob_i1.prepare_for_highlight()
        # for i in range(mob_o1.shape[0]):

        # first weights block
        self.play(mob_module.mobs_weight.highlight_block(
            direction=RIGHT,
            n=0,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # first input subblock
        self.play(mob_i1.highlight(
            mob_i1.highlight_loop_conv2d_mask(
                kernel_size=module_config['kernel_size'],
                stride=module_config['stride'],
            )[0],

        ))

        # first output cube
        self.play(GrowFromCenter(
            mob_o1[0][0],
            rate_func=rate_functions.ease_out_back,
            run_time=wt,
        ))
        self.wait(wt)

        # # generate first output layer
        # self.play(AnimationGroup(
        #     mob_i1.highlight_loop_conv2d(
        #         kernel_size=mob_module.module_config['kernel_size'],
        #         stride=mob_module.module_config['stride'],
        #         back=False,
        #         rate_func=smooth,
        #     ),
        #     Succession(
        #         *(GrowFromCenter(mob, rate_func=rate_functions.ease_out_back)
        #         for mob in mob_o1[i]),
        #         rate_func=smooth,
        #     ),
        #     lag_ratio=0.0,
        #     run_time=5.0,
        # ))

        # # fade current output layer, use highlight args
        # if i != mob_o1.shape[0]-1:
        #     layer = mob_o1[i].save_state()
        #     self.play(AnimationGroup(
        #         *(mob.animate.set_fill(
        #             opacity=0.0,
        #         ).set_stroke(
        #             width=1.0,
        #             opacity=0.05,
        #         ) for mob in layer),
        #         lag_ratio=0.0,
        #         run_time=wt,
        #     ))
        #     # self.play(layer.animate(
        #     #     run_time=wt,
        #     # ).fade(0.9))
        #     layers_output.append(layer)
        # self.wait(wt)

        # -----------------------------------------------

        # # show output summary
        # card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        # self.add_fixed_in_frame_mobjects(card_o1)
        # self.play(attach_to_ref(
        #     card_o1,
        #     card_module,
        #     DOWN,
        #     run_time=wt,
        # ))
        # self.play(card_o1.expand_summary(
        #     t2s(t_o1.detach()[0]),
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'shape relationships',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # shape of module weights
        # self.play(ShowShape3D(
        #     scene=self,
        #     mob=mob_module.mobs_weight,
        #     facing='right',
        #     aargs={
        #         'lag_ratio': 0.5,
        #         'run_time': wt*4,
        #     },
        # ))
        # self.wait(wt)

        # # shape of input/output tensor
        # self.play(AnimationGroup(
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
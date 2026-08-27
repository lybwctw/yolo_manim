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

FONT_SIZE_FORMULA = 24
FORMULA_V_OFFSET = 2.5
FORMULA_V_OFFSET_FOCUS = 3.0
FORMULA_H_OFFSET_FOCUS = 2.2
SUB_BUFF = 0.1

TENSOR_VGAP_3D = 2.0
TENSOR_VGAP_3D_FOCUS = 0.7
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load mobs and torch module
        card_module, mob_module = import_mobs('039b')
        torch_module = mob_module.module
        mob_running_mean = mob_module.mt_running_mean
        mob_running_var = mob_module.mt_running_var
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias
        module_config = mob_module.module_config

        # raw tensor
        t_i1 = torch.randn(1, 6, 3, 4)
        torch_module.eval()             # important
        t_o1 = torch_module(t_i1)

        # input tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_weight,
            UP,
            TENSOR_VGAP_3D,
        )

        # output tensor mob
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='card',
            **SMALL_TENSOR_CONFIG,
        ).next_to(
            mob_module,
            DOWN,
            TENSOR_VGAP_3D,
        )

        # FIXME: make this method of MTensor
        # increate z_index of module mobs
        n = len(mob_i1.mobs)
        for tmob in [mob_running_mean, mob_running_var, mob_weight, mob_bias]:
            for mob in tmob.mobs:
                mob.z_index = mob.z_index + n
                mob.set_z_index(mob.z_index)

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(card_module)
        self.add(mob_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show input',
            skip_animations=True,
        )
        # ************************************************************
        # show input tensor
        self.play(mob_i1.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        self.wait(wt)

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
            'formula and named tags again',
            skip_animations=True,
        )
        # ************************************************************
        # assets
        formula = MathTex(
            r"y = \frac{x-\mu}{\sqrt{\sigma^2+\epsilon}} \cdot \gamma + \beta",
            font_size=FONT_SIZE_FORMULA,
        ).shift(UP*FORMULA_V_OFFSET)
        tag_running_mean = NameTag(
            ref=p2f(self, mob_running_mean[-1].get_corner(DL+IN)),
            text='μ',
            leader_direction=DR,
        )
        tag_running_var = NameTag(
            ref=p2f(self, mob_running_var[-1].get_corner(DL+IN)),
            text='σ²',
            leader_direction=DR,
        )
        tag_weight = NameTag(
            ref=p2f(self, mob_weight[-1].get_corner(DL+IN)),
            text='γ',
            leader_direction=DR,
        )
        tag_bias = NameTag(
            ref=p2f(self, mob_bias[-1].get_corner(DL+IN)),
            text='β',
            leader_direction=DR,
        )

        # show formula
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(wt)

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
            'focus and switch',
            skip_animations=True,
        )
        # ************************************************************
        # mob_i1.save_state()
        # mob_o1.save_state()
        formula.save_state()

        # focus
        mob_o1.next_to(
            mob_module,
            DOWN,
            buff=TENSOR_VGAP_3D_FOCUS,
        )
        mob_i1.generate_target()
        mob_i1.target.next_to(
            mob_module,
            UP,
            buff=TENSOR_VGAP_3D_FOCUS,
        )
        formula.generate_target()
        formula.target.center().shift(FORMULA_V_OFFSET_FOCUS*UP)
        self.move_camera(
            zoom=1.8,
            added_anims=[
                MoveToTarget(mob_i1),
                MoveToTarget(formula),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # switch mode
        self.play(AnimationGroup(
            mob_i1.switch(
                style='beam',
                direction=IN,
                run_time=wt*3,
            ),
            mob_running_mean.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_running_var.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_weight.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_bias.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute for the first in first layer of output',
            skip_animations=True,
        )
        # ************************************************************
        c, h, w = mob_i1.shape
        mask_input = np.tile(
            np.eye(c,dtype=bool)[:,:,None,None],
            (1, 1, h, w),
        )[0]
        mask_param = np.eye(mob_bias.shape[0],dtype=bool)[0]

        # focus on first input layer and first params
        self.play(AnimationGroup(
            mob_i1.highlight(mask_input),
            mob_running_mean.highlight(mask_param),
            mob_running_var.highlight(mask_param),
            mob_weight.highlight(mask_param),
            mob_bias.highlight(mask_param),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # focus on first in first input layer
        c, h, w = mob_i1.shape
        masks_input = np.eye(c*h*w,dtype=bool).reshape(c*h*w,c,h,w)[:h*w]
        self.play(mob_i1.highlight(
            mask=masks_input[0],
            run_time=wt,
        ))
        self.wait(wt)

        # prepare substitutions
        sub1 = MathTex(
            rf"= \frac{{({t_i1[0][0,0,0]:+.2f})-({mob_running_mean.array[0]:+.2f})}}"
            rf"{{\sqrt{{({mob_running_var.array[0]:+.2f})+10^{{-5}}}}}}"
            rf"\cdot ({mob_weight.array[0]:+.2f}) + ({mob_bias.array[0]:+.2f})",
            font_size=FONT_SIZE_FORMULA,
        )
        sub2 = MathTex(
            rf"= {t_o1[0][0,0,0]:+.2f}",
            font_size=FONT_SIZE_FORMULA,
        )

        # reposition formula
        self.play(formula.animate(
            run_time=wt,
        ).shift(LEFT*FORMULA_H_OFFSET_FOCUS))

        # show substitutions
        sub1.next_to(formula, RIGHT, buff=SUB_BUFF)
        offset = formula[0][1].get_y() - sub1[0][0].get_y()
        sub1.shift(UP*offset)
        sub2.next_to(sub1, RIGHT, buff=SUB_BUFF)
        offset = formula[0][1].get_y() - sub2[0][0].get_y()
        sub2.shift(UP*offset)
        self.add_fixed_in_frame_mobjects(sub1)
        self.play(Write(sub1, run_time=wt))
        self.add_fixed_in_frame_mobjects(sub2)
        self.play(Write(sub2, run_time=wt))
        self.wait(wt)

        # show first output in first layer
        self.play(GrowFromCenter(
            mob_o1[0,0,0],
            rate_func=rate_functions.ease_out_back,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute loop for the rest in first layer of output',
            skip_animations=True,
        )
        # ************************************************************
        c, h, w = mob_i1.shape
        masks_input = np.eye(c*h*w,dtype=bool).reshape(c*h*w,c,h,w)[:h*w]
        for idx, (i, j) in enumerate(np.ndindex(h, w)):
            # skip the first
            if idx == 0:
                continue

            # highlight current input
            self.play(mob_i1.highlight(
                mask=masks_input[idx],
                run_time=wt,
            ))

            # new sub and result
            sub1_new = MathTex(
                rf"= \frac{{({t_i1[0][0,i,j]:+.2f})-({mob_running_mean.array[0]:+.2f})}}"
                rf"{{\sqrt{{({mob_running_var.array[0]:+.2f})+10^{{-5}}}}}}"
                rf"\cdot ({mob_weight.array[0]:+.2f}) + ({mob_bias.array[0]:+.2f})",
                font_size=FONT_SIZE_FORMULA,
            )
            sub2_new = MathTex(
                rf"= {t_o1[0][0,i,j]:+.2f}",
                font_size=FONT_SIZE_FORMULA,
            )
            sub1_new.shift(sub1[0][0].get_center() - sub1_new[0][0].get_center())
            sub2_new.shift(sub2[0][0].get_center() - sub2_new[0][0].get_center())
            self.play(AnimationGroup(
                Transform(sub1, sub1_new),
                Transform(sub2, sub2_new),
                lag_ratio=0.0,
                run_time=wt,
            ))

            # generate current output
            self.play(GrowFromCenter(
                mob_o1[0,i,j],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ))
            # self.wait(wt)

        # ************************************************************
        self.next_section(
            'finish first layer computation',
            skip_animations=True,
        )
        # ************************************************************
        # highlight first layer of input
        c, h, w = mob_i1.shape
        mask_input = np.tile(
            np.eye(c,dtype=bool)[:,:,None,None],
            (1, 1, h, w),
        )[0]
        self.play(mob_i1.highlight(
            mask_input,
            run_time=wt,
        ))

        # remove subs and reposition formula
        self.play(Succession(
            Unwrite(sub2),
            Unwrite(sub1),
            formula.animate.set_x(0),
            run_time=wt*3,
        ))
        self.wait(wt)

        # switch mode
        self.play(AnimationGroup(
            mob_i1.switch(
                style='layer',
                direction=IN,
                run_time=wt*3,
            ),
            mob_running_mean.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_running_var.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_weight.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_bias.switch(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            AnimationGroup(
                *(mob.switch() for mob in mob_o1[0]),
                lag_ratio=0.0,
                run_time=wt,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # manual switch other layers of output
        for mob in mob_o1[1:]:
            mob.switch_instant()
        mob_o1.mode = 'cube'

        # focus back
        mob_i1.generate_target()
        mob_i1.target.next_to(
            mob_module,
            UP,
            buff=TENSOR_VGAP_3D,
        )
        mob_o1_layer = mob_o1[0]
        mob_o1_layer.generate_target()
        orig_z = mob_o1_layer.get_z()
        mob_o1_layer.target.next_to(
            mob_module,
            DOWN,
            buff=TENSOR_VGAP_3D,
        ).set_z(orig_z)
        self.move_camera(
            zoom=1.0,
            added_anims=[
                MoveToTarget(mob_i1),
                MoveToTarget(mob_o1_layer),
                Restore(formula),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # NOTE: reposition output hidden layers
        mob_o1[1:].next_to(
            mob_o1_layer,
            IN,
            buff=0.0,
        )

        # ************************************************************
        self.next_section(
            'compute the rest layers of output',
            skip_animations=False,
        )
        # ************************************************************
        c, h, w = mob_i1.shape
        masks_input = np.tile(
            np.eye(c,dtype=bool)[:,:,None,None],
            (1, 1, h, w),
        )
        masks_param = np.eye(mob_bias.shape[0],dtype=bool)
        masks_output = np.tile(
            np.eye(c,dtype=bool)[:,:,None,None],
            (1, 1, h, w),
        )
        layers_output = mob_o1.get_vgs(masks_output)

        # loop
        self.play(AnimationGroup(
            mob_i1.highlight_loop(
                masks=masks_input[1:],
                rate_func=smooth,
                run_time=wt*3,
            ),
            mob_running_mean.highlight_loop(
                masks=masks_param[1:],
                rate_func=smooth,
                run_time=wt*3,
            ),
            mob_running_var.highlight_loop(
                masks=masks_param[1:],
                rate_func=smooth,
                run_time=wt*3,
            ),
            mob_weight.highlight_loop(
                masks=masks_param[1:],
                rate_func=smooth,
                run_time=wt*3,
            ),
            mob_bias.highlight_loop(
                masks=masks_param[1:],
                rate_func=smooth,
                run_time=wt*3,
            ),
            Succession(
                *(AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in layer),
                    lag_ratio=0.0,
                ) for layer in layers_output[1:]),
                rate_func=smooth,
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # highlight back input and params
        self.play(AnimationGroup(
            mob_i1.highlight(),
            mob_running_mean.highlight(),
            mob_running_var.highlight(),
            mob_weight.highlight(),
            mob_bias.highlight(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

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
        # self.wait(wt)

        # remove formula
        self.play(Unwrite(
            formula,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        # remove input/output
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
            mob_module,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
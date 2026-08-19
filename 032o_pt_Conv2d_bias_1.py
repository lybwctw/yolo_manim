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

TENSOR_VGAP_3D = 1.0            # smaller than previous
# TENSOR_HGAP_3D = 1.0
# TENSOR_EGAP_3D = 1.0
BIAS_GAP_BIG = 2.0
BIAS_GAP_SMALL = 0.8

NEW_CONFIG = {
    'in_channels': 4,
    'out_channels': 5,
    'kernel_size': 3,
    'stride': 1,
    'padding': 1,
    'bias': True,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

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
        ) = import_mobs('032n')

        # raw module and manim module
        module_config = NEW_CONFIG
        torch_module = torch.nn.Conv2d(**module_config)
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=module_config,
            block_gap=0.5,
            bias_offset=BIAS_GAP_BIG,
        ).center()
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # new raw tensor
        t_i1 = torch.randn(1, 4, 6, 7)
        t_o2 = torch_module(t_i1)
        t_o1 = t_o2 - torch_module.bias[None, :, None, None]

        # new output tensor mob
        mob_i1 = MTensor3D(
            array=t_i1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        )
        mob_o1 = MTensor3D(
            array=t_o1.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        )
        mob_o2 = MTensor3D(
            array=t_o2.detach()[0],
            mode='cube',
            **SMALL_TENSOR_CONFIG,
        )

        # show initial mobs
        self.set_camera_orientation(**VIEW_COMPUTE)
        self.add_fixed_in_frame_mobjects(
            card_i1,
            card_module,
            card_o1,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show new module (weight+bias) and card',
            skip_animations=True,
        )
        # ************************************************************
        # new module params
        # NOTE: assert that only padding/bias changes
        self.play(card_module.update_params(
            params={
                'padding': module_config['padding'],
                'bias': module_config['bias'],
            },
            run_time=wt,
        ))

        # show new module
        self.play(AnimationGroup(
            mob_module.create(
                wargs={'run_time': wt},
                bargs={'run_time': wt},
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show name tags on weight and bias
        ref_weight = mob_weight[-1].get_corner(UR+OUT)
        ref_bias = mob_bias[-1].get_corner(UR+OUT)
        tag_weight = NameTag(
            ref=p2f(self, ref_weight),
            text='weight',
            leader_direction=UR,
        )
        tag_bias = NameTag(
            ref=p2f(self, ref_bias),
            text='bias',
            leader_direction=UR,
        )
        self.play(AnimationGroup(
            tag_weight.create(),
            tag_bias.create(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show shapes on weight and bias',
            skip_animations=True,
        )
        # ************************************************************
        # show shapes on weight and bias
        self.play(AnimationGroup(
            ShowShape3D(
                scene=self,
                mob=mob_weight,
                view='compute',
                lag_ratio=0.5,
            ),
            ShowShape3D(
                scene=self,
                mob=mob_bias,
                view='compute',
                lag_ratio=0.5,
            ),
            lag_ratio=0.0,
            run_time=wt*5,
        ))
        self.wait(wt)

        # out_channels matching
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                card_module.value_objs['out_channels'],
                mob_weight.shape_texts[0],
                mob_bias.shape_texts[0],
            ]),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean and prepare for compute',
            skip_animations=True,
        )
        # ************************************************************
        # hide shapes for weight
        self.play(AnimationGroup(
            HideShape3D(
                mob_weight,
                lag_ratio=0.0,
            ),
            HideShape3D(
                mob_bias,
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # hide tags
        self.play(AnimationGroup(
            tag_weight.uncreate(),
            tag_bias.uncreate(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # make weight and bias closer
        mobs = VGroup(mob_weight, mob_bias)
        self.play(mobs.animate(
            run_time=wt,
        ).arrange(
            DOWN,
            BIAS_GAP_SMALL,       # 0.8
        ))
        self.wait(wt)

        # reposition input and output
        mob_i1.next_to(
            mob_module,
            UP,
            TENSOR_VGAP_3D,
        )
        mob_o1.next_to(
            mob_module,
            DOWN,
            TENSOR_VGAP_3D,
        )

        # show input and summary
        self.play(AnimationGroup(
            mob_i1.create(
                style='beam',
                direction=OUT,
            ),
            card_i1.expand_summary(
                t2s(t_o1.detach()[0]),
            ),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'weight compute step, breath style',
            skip_animations=True,
        )
        # ************************************************************
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

        # loop
        self.play(AnimationGroup(
            mob_weight.breath(
                style='whole',
                rate_func=smooth,           # sync with default
                lag_ratio=0.5,              # sync with default
            ),
            mob_o1.create(
                style='layer',
                direction=IN,
                # rate_func=smooth,         # smooth by default
                # lag_ratio=1.0,            # 0.5 by default
            ),
            lag_ratio=0.1,
            run_time=wt*3,
        ))
        self.wait(wt)

        # unpad
        self.play(mob_i1.unpad(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'rearrange bias',
            skip_animations=True,
        )
        # ************************************************************
        orig_center = mob_bias.get_center()
        self.play(mob_bias.mobs.animate(
            run_time=wt,
        ).arrange(
            RIGHT,
            buff=0.0,
        ).move_to(
            orig_center,
        ))
        self.play(mob_bias.animate(
            run_time=wt,
        ).rotate(
            90*DEGREES,
            axis=UP,
        ).move_to(
            orig_center,
        ))
        self.wait(wt)

        # swap bias and mid output
        mob_bias.generate_target()
        mob_o1.generate_target()
        mob_o1.target.next_to(
            mob_weight,
            DOWN,
            TENSOR_VGAP_3D,
        )
        mob_bias.target.next_to(
            mob_o1.target,
            DOWN,
            TENSOR_VGAP_3D,
        )
        self.play(AnimationGroup(
            MoveToTarget(mob_bias),
            MoveToTarget(mob_o1),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'first bias compute',
            skip_animations=True,
        )
        # ************************************************************
        # focus on mid output
        self.move_camera(
            frame_center=mob_o1.get_center(),
            run_time=wt,
        )
        self.wait(wt)

        # prepare masks
        c, h, w = mob_o1.shape
        masks_o1 = np.tile(
            np.eye(c, dtype=bool)[:, :, None, None],
            (1, 1, h, w),
        )
        masks_bias = np.eye(mob_bias.shape[0], dtype=bool)
        layers_o2 = mob_o2.get_layers(IN)

        # first mid output layer and first bias
        self.play(AnimationGroup(
            mob_o1.highlight(
                mask=masks_o1[0],
            ),
            mob_bias.highlight(
                mask=masks_bias[0],
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # first final output layer
        mob_o2.next_to(
            mob_bias,
            DOWN,
            TENSOR_VGAP_3D,
        )
        self.play(Succession(
            mob_bias[0].breath(),
            AnimationGroup(
                *(GrowFromCenter(
                    mob,
                    rate_func=rate_functions.ease_out_back,
                ) for mob in layers_o2[0]),
                lag_ratio=0.0,
            ),
            run_time=wt*2,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'remaining bias compute',
            skip_animations=True,
        )
        # ************************************************************
        # TODO: mtensor occlude issue
        # TODO: increase z_index of mtensor in batch

        for idx in range(1, mob_bias.shape[0]):
            # fade previous layer of output
            self.play(AnimationGroup(
                *(mob.tarnish() for mob in layers_o2[idx-1]),
                lag_ratio=0.0,
                run_time=wt,
            ))

            # highlight current layer of mid output
            self.play(AnimationGroup(
                mob_o1.highlight(
                    mask=masks_o1[idx],
                ),
                mob_bias.highlight(
                    mask=masks_bias[idx],
                ),
                lag_ratio=0.0,
                run_time=wt,
            ))

            # compute current layer of final output
            self.play(Succession(
                mob_bias[idx].breath(),
                AnimationGroup(
                    *(GrowFromCenter(
                        mob,
                        rate_func=rate_functions.ease_out_back,
                    ) for mob in layers_o2[idx]),
                    lag_ratio=0.0,
                ),
                run_time=wt,
            ))

        # restore o1 / bias / o2
        self.wait(wt)
        self.play(AnimationGroup(
            mob_o1.highlight(),
            mob_bias.highlight(),
            AnimationGroup(
                *(mob.lightup() for mob in mob_o2[:-1]),
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # final output summary
        self.play(card_o1.expand_summary(
            t2s(t_o2.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean mid output and rearrange',
            skip_animations=True,
        )
        # ************************************************************
        # clean mid output
        self.play(mob_o1.uncreate(
            style='beam',
            direction=IN,
            anim=Unwrite,
            run_time=wt,
        ))

        # reposition bias and final output
        mobs = VGroup(mob_bias, mob_o2)
        self.move_camera(
            frame_center=ORIGIN,
            added_anims=[
                mobs.animate(
                    run_time=wt,
                ).next_to(
                    mob_weight,
                    DOWN,
                    BIAS_GAP_SMALL,
                ),
            ],
            run_time=wt,
        )

        # back to original view of bias
        orig_center = mob_bias.get_center()
        b, c, h, w = mob_weight.shape
        masks_weight = np.tile(
            np.eye(b, dtype=bool)[:, :, None, None, None],
            (1, c, h, w),
        )
        self.play(mob_bias.animate(
            run_time=wt,
        ).rotate(
            -90*DEGREES,
            axis=UP,
        ).move_to(
            orig_center,
        ))

        # more gap on input output by the way
        self.play(AnimationGroup(
            *(mb.animate.next_to(mw, DOWN, buff=BIAS_GAP_SMALL)
            for mb, mw in zip(
                mob_bias.mobs,
                mob_weight.get_vgs(masks_weight),
            )),
            mob_i1.animate.next_to(
                mob_module,
                UP,
                1.5,
            ),
            mob_o2.animate.next_to(
                mob_module,
                DOWN,
                1.5,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        # ************************************************************
        self.next_section(
            'clean final output',
            skip_animations=True,
        )
        # ************************************************************
        mob_o2.save_state()
        self.play(AnimationGroup(
            mob_o2.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        mob_o2.restore()

        # ************************************************************
        self.next_section(
            'simplified layer compute loop, breath style',
            skip_animations=False,
        )
        # ************************************************************
        # apply weight
        self.play(AnimationGroup(
            mob_weight.breath(
                style='whole',
                rate_func=smooth,       # sync with default
                lag_ratio=0.5,          # sync with default
            ),
            mob_o2.create(
                style='layer',
                direction=IN,
                # rate_func=smooth,     # smooth by default
                # lag_ratio=1.0,        # 0.5 by default
            ),
            lag_ratio=0.1,
            run_time=wt*3,
        ))

        # apply bias
        self.play(AnimationGroup(
            mob_bias.breath(
                style='series',
                direction=RIGHT,
            ),
            mob_o2.translate(
                style='layer',
                direction=IN,
            ),
            lag_ratio=0.1,
            run_time=wt*5,
        ))

        # output summary
        self.play(card_o1.expand_summary(
            t2s(t_o2.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # clean output and summary
        mob_o2.save_state()
        self.play(AnimationGroup(
            mob_o2.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        mob_o2.restore()

        # ************************************************************
        self.next_section(
            'even simpler, breath style',
            skip_animations=False,
        )
        # ************************************************************
        # apply weight and bias
        self.play(AnimationGroup(
            mob_weight.breath(
                style='whole',
                rate_func=smooth,       # sync with default
                lag_ratio=0.5,          # sync with default
                run_time=wt*3,
            ),
            mob_bias.breath(
                style='series',
                direction=RIGHT,
                run_time=wt*3,
            ),
            mob_o2.create(
                style='layer',
                direction=IN,
                # rate_func=smooth,     # smooth by default
                # lag_ratio=1.0,        # 0.5 by default
                run_time=wt*3,
            ),
            lag_ratio=0.0,
        ))

        # output summary
        self.play(card_o1.expand_summary(
            t2s(t_o2.detach()[0]),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean module and output',
            skip_animations=False,
        )
        # ************************************************************
        # clean output and summary
        self.play(AnimationGroup(
            mob_o2.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
            ),
            card_o1.shrink_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # clean module weight and bias
        self.play(AnimationGroup(
            mob_weight.uncreate(
                style='beam',
                direction=IN,
                anim=Unwrite,
                run_time=wt,
            ),
            mob_bias.uncreate(
                style='series',
                direction=RIGHT,
                anim=Unwrite,
                run_time=wt,
            ),
            lag_ratio=0.0,
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
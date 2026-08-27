from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *
from utils.name_tag import *

from modules.pt_BatchNorm2d import *

import torch

EMPTY_CONFIG = {
    'num_features': UNKNOWN,
    'eps': UNKNOWN,
    'momentum': UNKNOWN,
    'affine': UNKNOWN,
    'track_running_stats': UNKNOWN,
}

INIT_CONFIG = {
    'num_features': 6,
    'eps': 1e-5,
    'momentum': 0.1,
    'affine': True,
    'track_running_stats': True,
}

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('039a')

        # raw module with random init
        torch_module = torch.nn.BatchNorm2d(**INIT_CONFIG)
        with torch.no_grad():
            torch_module.running_mean.copy_(torch.randn_like(torch_module.running_mean))
            torch_module.running_var.copy_(torch.rand_like(torch_module.running_var) + 0.5)
            torch_module.weight.copy_(torch.randn_like(torch_module.weight))
            torch_module.bias.copy_(torch.randn_like(torch_module.bias))

        # mob module
        mob_module = PT_BatchNorm2d(
            module=torch_module,
            module_config=INIT_CONFIG,
            mtensor_dir=RIGHT,
            mtensor_gap=1.5,        # closer after introduction
        )
        mob_running_mean = mob_module.mt_running_mean
        mob_running_var = mob_module.mt_running_var
        mob_weight = mob_module.mt_weight
        mob_bias = mob_module.mt_bias

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_INTRO,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'starting module card',
            skip_animations=False,
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
            INIT_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # show module params, 4x1d
        self.play(mob_module.create(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'name tag for each param',
            skip_animations=False,
        )
        # ************************************************************
        # name tag assets
        tag_running_mean = NameTag(
            ref=p2f(self, mob_running_mean[0].get_corner(UR+OUT)),
            text='running_mean(μ)',
            leader_direction=UR,
        )
        tag_running_var = NameTag(
            ref=p2f(self, mob_running_var[0].get_corner(UR+OUT)),
            text='running_var(σ²)',
            leader_direction=UR,
        )
        tag_weight = NameTag(
            ref=p2f(self, mob_weight[0].get_corner(UR+OUT)),
            text='weight(γ)',
            leader_direction=UR,
        )
        tag_bias = NameTag(
            ref=p2f(self, mob_bias[0].get_corner(UR+OUT)),
            text='bias(β)',
            leader_direction=UR,
        )
        self.play(AnimationGroup(
            tag_running_mean.create(),
            tag_running_var.create(),
            tag_weight.create(),
            tag_bias.create(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'shape matching',
            skip_animations=False,
        )
        # ************************************************************
        # show shapes
        self.play(AnimationGroup(
            *(ShowShape3D(
                scene=self,
                mob=mob,
                view='intro',
            ) for mob in [
                mob_running_mean,
                mob_running_var,
                mob_weight,
                mob_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # shape matching to num_features
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                card_module.value_objs['num_features'],
                mob_running_mean.shape_texts[0],
                mob_running_var.shape_texts[0],
                mob_weight.shape_texts[0],
                mob_bias.shape_texts[0],
            ]),
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean and into compute view',
            skip_animations=False,
        )
        # ************************************************************
        # hide shapes
        self.play(AnimationGroup(
            *(HideShape3D(
                mob=mob,
            ) for mob in [
                mob_running_mean,
                mob_running_var,
                mob_weight,
                mob_bias,
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

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

        # new view and make params closer
        mobs = VGroup(
            mob_running_mean,
            mob_running_var,
            mob_weight,
            mob_bias,
        )
        self.move_camera(
            **VIEW_COMPUTE,
            added_anims=[
                mobs.animate.arrange(
                    RIGHT,
                    buff=0.5,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # export
        mobs = VGroup(card_module, mob_module)
        export_mobs(__file__, mobs)
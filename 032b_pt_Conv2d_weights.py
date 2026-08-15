from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *
from utils.name_tag import *

from modules.pt_Conv2d import *

import torch

EMPTY_CONFIG = {
    'in_channels': UNKNOWN,
    'out_channels': UNKNOWN,
    'kernel_size': UNKNOWN,
    'stride': UNKNOWN,
    'padding': UNKNOWN,
    'bias': UNKNOWN,
    'dilation': UNKNOWN,
    'groups': UNKNOWN,
    'padding_mode': UNKNOWN,
}

INIT_CONFIG = {
    'in_channels': 6,
    'out_channels': 5,
    'kernel_size': 3,
    'stride': 1,
    'padding': 1,
    'bias': False,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('032a')

        # raw module and manim module
        torch_module = torch.nn.Conv2d(**INIT_CONFIG)
        mob_module = PT_Conv2d(
            module=torch_module,
            module_config=INIT_CONFIG,
            block_gap=0.5,
            bias_offset=0.5,
        )

        # ************************************************************
        self.next_section(
            'empty module card',
            skip_animations=True,
        )
        # ************************************************************
        # show initial mobs
        self.set_camera_orientation(
            **VIEW_INTRO,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # expand empty module card
        self.play(card_module.expand_params(
            params=EMPTY_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'init with concrete module',
            skip_animations=True,
        )
        # ************************************************************
        # update module card config
        self.play(card_module.update_params(
            INIT_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # show module weight
        self.play(mob_module.create(
            run_time=wt,
        ))
        self.wait(wt)

        # show name tag
        ref = mob_module.mt_weight[-1].get_corner(UR+OUT)
        tag_weight = NameTag(
            ref=p2f(self, ref),
            text='weight',
            leader_direction=UR,
        )
        self.play(tag_weight.create(run_time=wt))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'shape matching between weight and config',
            skip_animations=False,
        )
        # ************************************************************
        # show shape of weight
        self.play(ShowShape3D(
            scene=self,
            mob=mob_module.mt_weight,
            view='intro',
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # in_channels matching
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                card_module.value_objs['in_channels'],
                mob_module.mt_weight.shape_texts[1],
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # out_channels matching
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                card_module.value_objs['out_channels'],
                mob_module.mt_weight.shape_texts[0],
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # out_channels matching
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                card_module.value_objs['kernel_size'],
                mob_module.mt_weight.shape_texts[2],
                mob_module.mt_weight.shape_texts[3],
            ]),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean and into compute view',
            skip_animations=False,
        )
        # ************************************************************
        # hide shapes for weight
        self.play(HideShape3D(
            mob_module.mt_weight,
            lag_ratio=0.0,
            run_time=wt,
        ))

        # hide tag
        self.play(tag_weight.uncreate(
            run_time=wt,
        ))
        self.wait(wt)

        # new view
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )
        self.wait(wt)

        # export
        mobs = VGroup(card_module, mob_module)
        export_mobs(__file__, mobs)
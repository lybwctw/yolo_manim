from manim import *

from utils.constants import *
from utils.general import import_mobs, random_path
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.image_pad import ImagePad
from utils.explainer import Explainer
from utils.anchor_point import COLOR_MAP, DIRECTION_SERIES
from utils.show_shape import ShowShape, HideShape

import random

COMPUTE_IDX = 190
N_COMPUTE_SAMPLES = 5
PCELLS_BUFF = 0.1

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        # NOTE: import from 2d scene failed.
        self.set_camera_orientation(
            phi=0*DEGREES,
            theta=-90*DEGREES,
        )

        background = ImagePad(padded=True).set_opacity(0.1)
        e32 = Explainer.from_file(
            background=background,
            version=32,
        )
        s32 = Group(background, e32)

        self.add(s32)
        self.wait(wt)
        
        self.play(e32.show_anchor_points(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show probcells for sample anchor point',
            skip_animations=True,
        )
        # ************************************************************
        sap, oaps = e32.random_ap(COMPUTE_IDX)

        self.play(
            sap.mob.animate.set_opacity(1.0),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.1)
                for ap in oaps),
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=wt,
        )
        self.wait(0.5)

        # show pcells
        self.play(sap.show_pcells(
            box_config={},
            lag_ratio = 0.5,
            run_time = wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'stack probcells in 3d',
            skip_animations=True,
        )
        # ************************************************************
        self.move_camera(
            phi=75*DEGREES,
            theta=-60*DEGREES,
            run_time=1.0,
        )
        self.wait(wt)

        # FIXME: occlusion issue.

        self.play(sap.arrange_pcells(
            lag_ratio=0.5,
            run_time=wt*10,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through several samples',
            skip_animations=True,
        )
        # ************************************************************
        sample_idxs = random_path(
            n=N_COMPUTE_SAMPLES,
            step=2,
            shape=e32.shape,
            start_idx=COMPUTE_IDX,
        )
        pcells = sap.pcells

        for idx in sample_idxs:
            sap, oaps = e32.random_ap(idx)
            pcells_new = sap.create_pcells(
                box_config={},
                arranged=True,
            )
            self.play(
                AnimationGroup(
                    *(Transform(
                        series,
                        new_series,
                    ) for series, new_series in zip(
                        pcells.values(),
                        pcells_new.values()
                    )),
                    lag_ratio=0.0,
                ),
                sap.mob.animate.set_opacity(1.0),
                AnimationGroup(
                    *(ap.mob.animate.set_opacity(0.1)
                    for ap in oaps),
                    lag_ratio=0.0,
                ),
                lag_ratio=0.0,
                run_time=wt,
            )
            sap.pcells = pcells
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'replace pcells with 64-layer DFL tensor',
            skip_animations=False,
        )
        # ************************************************************
        layer_center = background.get_center()
        layer_width = background.width
        layer_height = background.height
        layer_buff = PCELLS_BUFF    # share buff with pcells

        # remove pcells
        self.play(sap.hide_pcells(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # remove anchor points
        self.play(e32.hide_anchor_points(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # create unexpanded raw layers
        tensor_64 = LayersFake(
            n=64,
            width=layer_width,
            height=layer_height,
            width_nominal=20,
            height_nominal=20,
            buff=0.04,
            rect_config={
                'fill_color': BLACK,
                'fill_opacity': 0.0,
            },
        ).move_to(layer_center)
        self.play(Write(
            tensor_64,
            run_time=wt,
        ))

        # expand layers
        tensor_64.generate_target()
        tensor_64.target.rects.arrange(
            direction=IN,
            buff=layer_buff,
        )
        for i, layer in enumerate(tensor_64.target.rects):
            color = COLOR_MAP[DIRECTION_SERIES[i//16]]
            layer.set_style(
                fill_color=BLACK,
                fill_opacity=0.5,
                stroke_width=0.8,
                stroke_color=color,
                stroke_opacity=1.0,
            )
        self.play(MoveToTarget(
            tensor_64,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'DFL tensor in 2d perspective',
            skip_animations=False,
        )
        # ************************************************************
        # change perspective and rearrange layers
        tensor_64.generate_target()
        tensor_64.target.rects.scale(0.3)
        layer_buff = -tensor_64.target.rects[0].width + 0.02
        tensor_64.target.rects.arrange(
            direction=UR,
            buff=layer_buff,    # native arrange issue
        )
        self.move_camera(
            phi=0*DEGREES,
            theta=-90*DEGREES,
            added_anims=[
                MoveToTarget(
                    tensor_64,
                ),
                background.animate.set_opacity(
                    0.0,
                )
            ],
            run_time=wt,
        )
        self.wait(wt)

        # show shape of layers
        self.play(ShowShape(
            tensor_64,
            text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            aargs={'run_time': wt},
        ))
        self.wait(wt)
        self.play(HideShape(
            tensor_64,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'replace 64-layer tensor with 8-layer substitute',
            skip_animations=False,
        )
        # ************************************************************
        tensor_sub = LayersFake(
            n=8,                       # variable?
            ref=tensor_64,
            expanded=True,
            buff=0.08,
            width_nominal=20,
            height_nominal=20,
            depth_nominal=64,
        ).move_to(tensor_64)

        self.wait(wt)
        self.play(Unwrite(
            tensor_64,
            run_time=wt,
        ))
        self.play(Write(
            tensor_sub,
            run_time=0.5,
            lag_ratio=wt,
        ))
        self.wait(wt)

        self.play(ShowShape(
            tensor_sub,
            text_config=MEDIUM_SHAPE_TEXT_CONFIG,
            aargs={'run_time': wt},
        ))
        self.wait(wt)
        self.play(HideShape(
            tensor_sub,
            aargs={'run_time': wt},
        ))
        self.wait(wt)
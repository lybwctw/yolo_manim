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
N_COMPUTE_SAMPLES = 3
PCELLS_BUFF = 0.1

class MainScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES)

        # ************************************************************
        self.next_section(
            'init background + explainer from 021',
            skip_animations=False,
        )
        # ************************************************************
        # NOTE: import from 2d scene failed.
        # s32 = import_mobs('021')
        # background, e32 = s32

        background = ImagePad(padded=True).set_opacity(0.1)
        e32 = Explainer.from_file(
            background=background,
            version=32,
        )
        s32 = Group(background, e32)

        self.add(s32)
        self.wait()
        
        self.play(e32.show_anchor_points(
            lag_ratio=0.0,
            run_time=0.3,
        ))
        self.wait(0.3)

        # ************************************************************
        self.next_section(
            'show probcells on specific anchor point',
            skip_animations=False,
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
            run_time=0.5,
        )
        self.wait(0.5)

        for direction in DIRECTION_SERIES:
            self.play(sap.show_pcells_direction(
                direction=direction,
                label_config={
                    'font_size': 10,
                    'color': WHITE,
                },
                box_config={},
                lag_ratio=0.5,
                run_time=0.5,
            ))
            self.wait(0.2)

        self.wait(0.5)

        # show WHITE stroke before stacking
        self.play(AnimationGroup(
            *(pc.mob_box.animate.set_stroke(
                # color=WHITE,
                opacity=0.8,
                width=0.8,
            ) for pc in sap.pcells),
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(0.2)

        # ************************************************************
        self.next_section(
            'stack probcells in 3d',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            phi=75*DEGREES,
            theta=-60*DEGREES,
            run_time=1.0,
        )
        self.wait(0.5)

        # # FIXME: occlusion issue.
        # sap.pcells[:32].set_z_index(3)
        # background.set_z_index(2)
        # sap.pcells[32:].set_z_index(1)
        # self.wait(1.0)

        self.play(sap.arrange_pcells(
            lag_ratio=0.5,
            run_time=3.0,
        ))
        self.wait(1.0)

        # ************************************************************
        self.next_section(
            'loop through several samples with aligned pcells',
            skip_animations=False,
        )
        # ************************************************************
        # h, w = e32.shape
        # row, col = divmod(COMPUTE_IDX, w)
        # sample_idxs = []
        # for _ in range(N_COMPUTE_SAMPLES):
        #     dr, dc = random.choice([
        #         (-2, -2), (-2, 0), (-2, 2),
        #         (0, -2),           (0, 2),
        #         (2, -2),  (2, 0),  (2, 2),
        #     ])
        #     row = min(max(row + dr, 0), h - 1)
        #     col = min(max(col + dc, 0), w - 1)
        #     sample_idxs.append(row*w + col)
        
        sample_idxs = random_path(
            n=N_COMPUTE_SAMPLES,
            step=2,
            shape=e32.shape,
            start_idx=COMPUTE_IDX,
        )
        pcells = sap.pcells

        for idx in sample_idxs:
            sap, oaps = e32.random_ap(idx)
            pcells_new = sap.create_pcells_arranged(
                label_config={
                    'font_size': 10,
                    'color': WHITE,
                },
                box_config={
                    # 'stroke_color': WHITE,
                    'stroke_opacity': 0.8,
                    'stroke_width': 0.8,
                },
                buff=PCELLS_BUFF,
            )
            self.play(
                Transform(
                    pcells,
                    pcells_new,
                ),
                sap.mob.animate.set_opacity(1.0),
                AnimationGroup(
                    *(ap.mob.animate.set_opacity(0.1)
                    for ap in oaps),
                    lag_ratio=0.0,
                ),
                lag_ratio=0.0,
                run_time=0.16,
            )
            sap.pcells = pcells

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

        self.play(Unwrite(
            pcells,
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(0.2)

        self.play(e32.hide_anchor_points(
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(0.2)

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

        self.play(Write(tensor_64))
        # self.wait()

        # manually expand layers
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
        self.play(MoveToTarget(tensor_64))
        self.wait()

        # ************************************************************
        self.next_section(
            'DFL tensor in 2d perspective',
            skip_animations=False,
        )
        # ************************************************************
        # change perspective and adjust arrange of layers
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
        )
        self.wait()

        self.play(ShowShape(
            tensor_64,
            text_config=SMALL_SHAPE_TEXT_CONFIG,
        ))
        self.wait()
        self.play(HideShape(
            tensor_64,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'replace 64-layer tensor with 8-layer substitute',
            skip_animations=False,
        )
        # ************************************************************
        tensor_sub = LayersFake(
            n=16,                       # variable?
            ref=tensor_64,
            expanded=True,
            buff=0.08,
            width_nominal=20,
            height_nominal=20,
            depth_nominal=64,
        ).move_to(tensor_64)

        self.wait()
        self.play(Unwrite(
            tensor_64,
            run_time=0.5,
        ))
        self.play(Write(
            tensor_sub,
            run_time=0.5,
            lag_ratio=0.5,
        ))
        self.wait()

        self.play(ShowShape(
            tensor_sub,
            text_config=SMALL_SHAPE_TEXT_CONFIG,
        ))
        self.wait()
        self.play(HideShape(
            tensor_sub,
        ))
        self.wait()
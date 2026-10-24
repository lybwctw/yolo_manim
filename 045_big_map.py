# ************************************************************
# Big map for yolov8n for 3 classes.
# ************************************************************
from manim import *

from utils.yolo_annotation import YoloAnnotation
from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.ftensor import *
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *
import torch
import numpy as np

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 5.0

TENSOR_EGAP = 2.0

UNIT_BUFF = 0.7

DEFAULT_TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
    'color': WHITE,
}

DEFAULT_CODE_CONFIG = {
    'language': 'yaml',
    'formatter_style': 'vim',
    'background_config': {
        "fill_color": "#1E1E2E",
        "fill_opacity": 1,
        "stroke_color": "#45475A",
        "stroke_width": 1.5,
        "corner_radius": 0.12,
    },
    'paragraph_config': {
        "font": "JetBrains Mono",
        "font_size": 20,
        "line_spacing": 0.4,
    },
    'tab_width': 2,
}


wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('044h')
        (
            mt_input, mm_modules,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        ) = mobs
        mt_outputs = VGroup(
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )

        cam_args = {
            **VIEW_INTRO,
            # 'focal_distance': 20,
            # 'zoom': 1.0,
        }
        self.set_camera_orientation(
            **cam_args,
        )
        self.add(
            mm_modules, mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert preprocess and postprocess',
            skip_animations=False,
        )
        # ************************************************************
        input_raw = mt_input.copy()
        input_raw.stretch_to_fit_height(mt_input.height*540/640)
        input_raw.stretch_to_fit_width(mt_input.height*960/640)
        input_raw.next_to(mt_input, LEFT, buff=UNIT_BUFF)

        output_raw = Rectangle(
            width=0.2,
            height=2.0,
            stroke_width=input_raw.mob.stroke_width,
            stroke_color=WHITE,
            stroke_opacity=1.0,
            fill_color=GRAY,
            fill_opacity=1.0,
        ).next_to(
            mt_outputs,
            RIGHT,
            buff=UNIT_BUFF,
        )

        output_final = Rectangle(
            width=0.2,
            height=0.6,
            stroke_width=input_raw.mob.stroke_width,
            stroke_color=WHITE,
            stroke_opacity=1.0,
            fill_color=GRAY,
            fill_opacity=1.0,
        ).next_to(
            output_raw,
            RIGHT,
            buff=UNIT_BUFF*2,
        )

        self.play(AnimationGroup(
            Write(input_raw),
            Write(output_raw),
            Write(output_final),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce intuition assets',
            skip_animations=False,
        )
        # ************************************************************
        # raw image
        IT_image_raw = ImageMobject(
            PATH_IMAGE_640,
        ).scale_to_fit_width(
            input_raw.width,
        ).next_to(
            input_raw,
            OUT,
            buff=TENSOR_EGAP,
        )
        IT_image_raw.shade_in_3d = True

        # padded image
        IT_image_padded = ImageMobject(
            PATH_IMAGE_640_PAD,
        ).scale_to_fit_width(
            mt_input.width,
        ).next_to(
            mt_input,
            OUT,
            buff=TENSOR_EGAP,
        )
        IT_image_raw.shade_in_3d = True

        # partial outputs
        IT_b1 = IT_image_padded.copy().set_opacity(
            0.3).scale(0.5).move_to(mt_22_box)
        IT_b2 = IT_b1.copy().move_to(mt_23_box)
        IT_b3 = IT_b1.copy().move_to(mt_24_box)
        IT_c1 = IT_b1.copy().move_to(mt_22_cls)
        IT_c2 = IT_b1.copy().move_to(mt_23_cls)
        IT_c3 = IT_b1.copy().move_to(mt_24_cls)
        IT_out_mids = Group(
            IT_b1, IT_b2, IT_b3,
            IT_c1, IT_c2, IT_c3,
        )

        # unfiltered output
        IT_output = IT_b1.copy().move_to(output_raw)

        # final output: background + annotation
        IT_final = ImageMobject(PATH_IMAGE_640).fade(0.6).move_to(output_final)
        IT_final.shade_in_3d = True
        annotation = YoloAnnotation(
            background=IT_final,
            annotation=PATH_LABEL,
        )
        IT_final = Group(
            IT_final,
            annotation,
        ).scale_to_fit_width(
            input_raw.width
        )

        IT_mobs = Group(
            IT_image_raw,
            IT_image_padded,
            IT_b1, IT_b2, IT_b3,
            IT_c1, IT_c2, IT_c3,
            IT_output,
            IT_final,
        ).shift(UP*2.5)

        # show intuition space
        self.move_camera(
            phi=0*DEGREES,
            theta=-90*DEGREES,
            frame_center=ORIGIN,
            focal_distance=100,
            added_anims=[
                AnimationGroup(
                    FadeIn(
                        IT_image_raw,
                        run_time=wt,
                    ),
                    FadeIn(
                        IT_image_padded,
                        run_time=wt,
                    ),
                    FadeIn(
                        IT_out_mids,
                        run_time=wt,
                    ),
                    FadeIn(
                        IT_output,
                        run_time=wt,
                    ),
                    FadeIn(
                        IT_final,
                        run_time=wt,
                    ),
                    lag_ratio=0.0,
                ),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'unknown things in intuition view',
            skip_animations=False,
        )
        # ************************************************************
        unknown_text = Text(
            '?????????',
            **DEFAULT_TEXT_CONFIG,
        ).move_to(
            mm_modules,
        ).shift(
            UP*2.5,
        )
        self.play(Write(
            unknown_text,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce code view assets',
            skip_animations=False,
        )
        # ************************************************************
        codes = VGroup(
            Code(
                code_file=file,
                **DEFAULT_CODE_CONFIG,
            ).scale_to_fit_height(
                2.0
            ) for file in [
                r"assets\cfg\yolov3.yaml",
                r"assets\cfg\yolov5.yaml",
                r"assets\cfg\yolov8.yaml",
                r"assets\cfg\yolo11.yaml",
                r"assets\cfg\yolo26.yaml",
            ]
        ).arrange(RIGHT).move_to(
            mm_modules,
        ).shift(
            DOWN*2.5,
        )
        self.play(Write(codes, run_time=wt*3))
        self.wait(wt)
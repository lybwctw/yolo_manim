# ************************************************************
# Big map for yolov8n for 3 classes.
# ************************************************************
from manim import *

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

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('045h')
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

        self.set_camera_orientation(
            **VIEW_INTRO,
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
            skip_animations=True,
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

        self.move_camera(
            zoom=1.0,
            run_time=wt,
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
            'prepare intuition assets',
            skip_animations=False,
        )
        # ************************************************************
        # push in tensor space things
        tmobs = VGroup(
            input_raw,
            mt_input, mm_modules, mt_outputs,
            output_raw, output_final,
        )
        self.play(tmobs.animate(
            run_time=wt,
        ).shift(
            IN*TENSOR_EGAP*0.5 + LEFT*0.8,
        ))
        self.wait(wt)

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
            0.3).scale(0.5).next_to(
            mt_22_box, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())
        IT_b2 = IT_b1.copy().next_to(
            mt_23_box, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())
        IT_b3 = IT_b1.copy().next_to(
            mt_24_box, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())
        IT_c1 = IT_b1.copy().next_to(
            mt_22_cls, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())
        IT_c2 = IT_b1.copy().next_to(
            mt_23_cls, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())
        IT_c3 = IT_b1.copy().next_to(
            mt_24_cls, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())
        IT_out_mids = Group(
            IT_b1, IT_b2, IT_b3,
            IT_c1, IT_c2, IT_c3,
        )

        # unfiltered output
        IT_output = IT_b1.copy().next_to(
            output_raw, OUT, buff=TENSOR_EGAP,
        ).set_z(IT_image_padded.get_z())

        # FIXME: final output
        IT_final = ImageMobject(
            PATH_IMAGE_640,
        ).scale_to_fit_width(
            input_raw.width,
        ).next_to(
            output_final,
            OUT,
            buff=TENSOR_EGAP,
        )
        IT_final.shade_in_3d = True

        # show intuition space
        self.play(AnimationGroup(
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
        ))
        self.wait(wt)
from manim import *

from utils.explainer_bbox import ExplainerBbox
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.constants import *

import torch

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=True,
        )
        # ************************************************************
        background = ImagePad(padded=True)
        background.scale(1.3).set_opacity(0.2)
        self.add(background)
        # self.play(background.animate.set_opacity(0.2))
        self.wait()

        # TODO, make distance loading a function
        data_dist = torch.load(
            'assets/tensors/_dist_box.pt',
            weights_only=True,
            map_location='cpu',
            )  # (1, 4, 8400)
        data_dist = data_dist[0,:,8000:].transpose(0,1).reshape(20,20,4).numpy()

        explainer_bbox = ExplainerBbox(background, data_dist)
        self.add(explainer_bbox)

        # ************************************************************
        self.next_section(
            'anchor points capture thinking',
            skip_animations=True,
        )
        # ************************************************************
        # show grid and anchor points
        self.play(explainer_bbox.create_grid(lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(explainer_bbox.create_anchor_points(lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(explainer_bbox.remove_grid(lag_ratio=0, run_time=0.5))
        self.wait()

        # anchor points capture
        self.play(explainer_bbox.to_rects(lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(explainer_bbox.to_dots(lag_ratio=0, run_time=0.5))
        self.wait()

        # show and fade annotation, VGroup of SingleAnnotation
        annotation = YoloAnnotation(
            background=background.image,
            annotation=PATH_LABEL_640,
        ).annotation.set_z_index(1) # annotation should on top
        self.play(Write(annotation, lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                *(anno.label.animate.set_opacity(opacity=0) for anno in annotation),
                lag_ratio=0, run_time=0.5,
            ),
            AnimationGroup(
                *(anno.bbox.animate.set_fill(opacity=0) for anno in annotation),
                lag_ratio=0, run_time=0.5,
            ),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'inside anchor points capture',
            skip_animations=False,
        )
        # ************************************************************
        explainer_bbox.save_state()
        in_aps, out_aps = explainer_bbox.collect_in_out_aps(annotation)
        
        # highlight inside anchor points
        self.play(AnimationGroup(
            AnimationGroup(
                *(ap.animate.set_pattern(opacity=0.4,color=PURE_YELLOW) for ap in in_aps),
                lag_ratio=0, run_time=0.5,
            ),
            AnimationGroup(
                *(ap.animate.set_pattern(opacity=0.3,color=WHITE) for ap in out_aps),
                lag_ratio=0, run_time=0.5,
            ),
        ))
        self.wait()

        # inside anchor points capture
        self.play(AnimationGroup(
            *(ap.to_rect() for ap in in_aps),
            lag_ratio=0, run_time=0.5,
        ))
        self.wait()

        # restore
        self.play(AnimationGroup(
            explainer_bbox.animate(run_time=0.5).restore(),
            Unwrite(annotation, lag_ratio=0, run_time=0.5),
        ))
        self.wait()

        # # ************************************************************
        # self.next_section(
        #     'sample, from distance to position',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # focus on sample anchor point
        
        # # distance to position

        # # digit counterpart

        # # loop through several samples

        # # ************************************************************
        # self.next_section(
        #     'global, from distance to position',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # # sync, distance generation

        # # sync, position generation

        # # to thunbnail
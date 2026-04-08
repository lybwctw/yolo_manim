from manim import *

from utils.explainer_bbox import ExplainerBbox
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.constants import *

from utils.anchor_point import AnchorPoint

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

        # TODO, make distance tensor loading a function
        data_dist = torch.load(
            'assets/tensors/_dist_box.pt',
            weights_only=True,
            map_location='cpu',
            )  # (1, 4, 8400)
        data_dist = data_dist[0,:,8000:].transpose(0,1).reshape(20,20,4).numpy()

        explainer_bbox = ExplainerBbox(
            background=background,
            data=data_dist,
            sf_nominal=32,
        )

        # if add background to ExplainerBbox
        # then it can not be restored as a whole
        explainer_system = Group(explainer_bbox, background)
        self.add(explainer_system)
        self.wait()

        # ************************************************************
        self.next_section(
            'anchor points capture thinking',
            skip_animations=True,
        )
        # ************************************************************
        # show grid and anchor points
        self.play(explainer_bbox.show_grid(lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(explainer_bbox.show_anchor_points(lag_ratio=0, run_time=0.5))
        self.wait()
        self.play(explainer_bbox.hide_grid(lag_ratio=0, run_time=0.5))
        self.wait()

        # anchor points capture
        self.play(explainer_bbox.to_rects(
            gargs={'lag_ratio':0, 'run_time':0.5,}
        ))
        self.wait()
        self.play(explainer_bbox.to_dots(
            gargs={'lag_ratio':0, 'run_time':0.5,}
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'inside anchor points capture',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME, show and fade annotation, VGroup of SingleAnnotation
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

        # highlight inside anchor points
        explainer_bbox.save_state()
        in_aps, out_aps = explainer_bbox.collect_in_out_aps(annotation)
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

        # fade out and remove annotation
        self.play(AnimationGroup(
            *(anno.bbox.animate.set_opacity(opacity=0) for anno in annotation),
            lag_ratio=0, run_time=0.5,
        ))
        self.remove(annotation)
        self.wait()

        # inside anchor points capture
        self.play(AnimationGroup(
            *(ap.to_rect() for ap in in_aps),
            lag_ratio=0, run_time=0.5,
        ))
        self.wait()

        # restore to anchor point array
        self.play(explainer_bbox.animate(run_time=0.5).restore())
        self.wait()

        # ************************************************************
        self.next_section(
            'sample, from distance to position',
            skip_animations=False,
        )
        # ************************************************************
        # focus on sample anchor point
        sample_ap, other_aps = explainer_bbox.collect_focus_ap(189)
        self.play(AnimationGroup(
            sample_ap.animate(run_time=0.5).set_pattern(opacity=1.0),
            AnimationGroup(
                *(ap.animate.set_pattern(opacity=0.3) for ap in other_aps),
                lag_ratio=0, run_time=0.5,
            )
        ))
        self.wait()
        
        # distance representation
        self.play(sample_ap.to_rect(run_time=0.5))
        self.wait()
        self.play(sample_ap.show_arrows(lag_ratio=0.1, run_time=0.5))
        self.wait()
        self.play(sample_ap.show_distance_abs(lag_ratio=0.1, run_time=0.5))
        self.wait()
        self.play(AnimationGroup(
            sample_ap.arrows.animate(run_time=0.5).set_opacity(0.3),
            sample_ap.show_divide(run_time=0.5),
        ))
        self.wait()

        self.play(AnimationGroup(
            sample_ap.arrows.animate(run_time=0.5).set_opacity(1.0),
            sample_ap.abs_to_rela(
                aargs={'run_time':0.3,},
                gargs={'lag_ratio':0.1, 'run_time':0.5,},
            ),
        ))
        self.wait()

        # distance to position computation
        self.play(explainer_system.animate(run_time=0.5).shift(LEFT*3).scale(0.8))
        self.wait()

        # loop through several samples

        # # restore
        # self.play(explainer_bbox.animate(run_time=0.5).restore())
        # self.wait()

        # # # ************************************************************
        # # self.next_section(
        # #     'global, from distance to position',
        # #     skip_animations=False,
        # # )
        # # # ************************************************************
        # # # sync, distance generation

        # # # sync, position generation

        # # # to thunbnail
    
from manim import *

from utils.constants import *
from utils.arrow_comment import ArrowComment
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import YoloAnnotation
from utils.explainer_bbox import ExplainerBbox

import torch

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
        )
        # ************************************************************
        background = ImagePad(padded=True)
        background.scale(1.3).set_opacity(0.2)
        self.add(background)
        self.wait()

        # TODO, make distance tensor loading a function
        data_dist = torch.load(
            'assets/tensors/_dist_box.pt',
            weights_only=True,
            map_location='cpu',
            )  # (1, 4, 8400)
        data_dist = data_dist[0,:,8000:].transpose(0,1).reshape(20,20,4).numpy()
        data_cls = torch.load(
            'assets/tensors/_norm_cls.pt',
            weights_only=True,
            map_location='cpu',
            )  # (1, 3, 8400)
        data_cls = data_cls[0,:,8000:].transpose(0,1).reshape(20,20,3).numpy()
        # data_cls = np.random.uniform(0.5,1,(20,20,3))

        explainer = ExplainerBbox(
            background=background,
            data=data_dist,
            # data_cls=data_cls,
            data_cls=np.random.uniform(0.1,0.9,(20,20,3)),  # random for introduction
            sf_nominal=32,
        )

        explainer_bg = Group(explainer, background)
        self.add(explainer_bg)
        self.wait(0.3)

        # ************************************************************
        self.next_section(
            'class prob thinking for each ANCHOR POINT TARGET',
            skip_animations=False,
        )
        # ************************************************************
        # start with anchor points
        self.play(explainer.show_anchor_points(lag_ratio=0))
        self.wait()
        self.play(AnimationGroup(
            *(ap.animate.set_pattern(opacity=0.1)
              for ap in explainer.anchor_points),
              lag_ratio=0,
              run_time=1.0,
        ))
        self.wait(0.5)

        # generate random pbars
        self.play(explainer.show_pbars())
        self.wait()

        # FIXME! no valid class capture for 20x20 feature map
        # from random pbars to ideal pbars
        self.play(explainer.to_probs(data_cls))
        self.wait()

        
        # ************************************************************
        self.next_section(
            'generate tensor_probs',
            skip_animations=False,
        )
        # ************************************************************
        tensor_probs = explainer.create_probs_tensor().shift(RIGHT*2)
        self.play(explainer_bg.animate.shift(LEFT*3))
        self.wait()
        self.play(Write(tensor_probs, lag_ratio=0.02, run_time=2.0))
        self.wait()
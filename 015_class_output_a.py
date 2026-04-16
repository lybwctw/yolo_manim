from manim import *

from utils.constants import *
from utils.arrow_comment import ArrowComment
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.yolo_annotation import YoloAnnotation
from utils.explainer_bbox import ExplainerBbox
from utils.general import tensor_to_line_matrix, save_everything
from utils.layers_fake import LayersFake

import torch

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=True,
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
            skip_animations=True,
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
        # show tensor probs in the right
        # TODO, loop through each pbars, rate_functions.there_and_back
        self.play(explainer_bg.animate.scale(0.8).shift(LEFT*3))
        tensor_probs = explainer.create_probs_tensor().shift(RIGHT*6)
        self.wait()
        self.play(Write(tensor_probs, lag_ratio=0.02, run_time=2.0))
        self.wait()

        # scale and rearrange into up-down
        manager = Group(explainer_bg, tensor_probs)
        manager.generate_target()
        manager.target.scale(0.6).arrange(DOWN,buff=0.45).shift(LEFT*2)
        manager.target[1].align_to(manager.target[0][0].background, LEFT)   # adjustment
        self.play(MoveToTarget(manager, run_time=1.0))
        self.wait(0.5)

        #  transform probs into reshaped 2d version
        tensor_probs_2d = tensor_probs.copy()
        self.add(tensor_probs)  # TODO, fadein animation?
        line_matrix = explainer.create_line_matrix(n=3).scale(0.07).shift(RIGHT*3.5)
        self.play(tensor_to_line_matrix(
            tensor=tensor_probs_2d,
            lmatrix=line_matrix,
            targs={},
            gargs={'lag_ratio':0.02, 'run_time':0.1,},
            ggargs={'lag_ratio':0.05, 'run_time':2.1,},
        ))
        self.wait(0.3)

        # ************************************************************
        self.next_section(
            'simplify tensor_probs/tensor_probs_2d' \
            'into lf_output_32_cls/lf_output_32_cls_2d',
            skip_animations=False,
        )
        # ************************************************************
        # create lf_output_32_cls
        lf_output_32_cls = LayersFake(
            n=3,
            ref=tensor_probs,
            width_nominal=20,
            height_nominal=20,
            buff=0.05,
            expanded=True,
        ).move_to(tensor_probs).scale(0.95)

        # create lf_output_32_cls_2d
        lf_output_32_cls_2d = LayersFake(
            n=1,
            ref=tensor_probs_2d,
            width_nominal=3,
            height_nominal=400,
            expanded=True,
        ).move_to(tensor_probs_2d)

        # simplify tensor_probs/tensor_probs_2d
        self.play(AnimationGroup(
            Unwrite(tensor_probs, lag_ratio=0, run_time=1.0),
            Write(lf_output_32_cls, run_time=1.0),
            Unwrite(tensor_probs_2d, lag_ratio=0, run_time=1.0),
            Write(lf_output_32_cls_2d, run_time=1.0)
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'simplify explainer_dist and explainer_xyxy ' \
            'into 4x4 mini version',
            skip_animations=False,
        )
        # ************************************************************
        # clean explainer
        self.play(explainer.hide_pbars(
            aargs={},
            gargs={},
            ggargs={'lag_ratio':0, 'run_time':1.0},
        ))
        self.wait(0.5)
        self.play(explainer.hide_anchor_points(
            lag_ratio=0, run_time=0.5,
        ))
        self.wait(0.5)
        self.remove(explainer)

        # create mini version of explainer
        explainer = ExplainerBbox(
            background=background,
            data=np.load(MINI_32_DIST_PATH),
            data_cls=np.load(MINI_32_PROB_PATH),
            sf_nominal=32,
        )
        explainer_bg = Group(explainer, background)

        # dim anchor points, show pbars
        self.play(AnimationGroup(
            explainer.show_anchor_points(
                lag_ratio=0, run_time=0.5,
            )
        ))
        self.wait(0.5)
        self.play(AnimationGroup(
            *(ap.animate.set_pattern(opacity=0.1)
              for ap in explainer.anchor_points),
              lag_ratio=0,
              run_time=1.0,
        ))
        
        self.play(explainer.show_pbars(
            aargs={},
            gargs={},
            ggargs={},
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'save for next scene which go back to big map',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            explainer_bg,
            lf_output_32_cls,
            lf_output_32_cls_2d,
        )
        save_everything(S015_EVERYTHING, everything)
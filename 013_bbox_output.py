from manim import *

from utils.explainer_bbox import ExplainerBbox
from utils.yolo_annotation import YoloAnnotation
from utils.image_pad import ImagePad
from utils.constants import *
from utils.line_matrix import LineMatrix
from utils.anchor_point import AnchorPoint
from utils.general import tensor_to_line_matrix, save_everything
from utils.layers_fake import LayersFake

import torch

import random

SHORT_DURATION=0.1

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init',
            skip_animations=False,
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

        # explainer for distance tensor
        explainer_dist = ExplainerBbox(
            background=background,
            data=data_dist,
            sf_nominal=32,
        )

        explainer_dist_bg = Group(explainer_dist, background)
        self.add(explainer_dist_bg)
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'anchor points capture thinking',
            skip_animations=False,
        )
        # ************************************************************
        # show grid and anchor points
        self.play(explainer_dist.show_grid(lag_ratio=0, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)
        self.play(explainer_dist.show_anchor_points(lag_ratio=0, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)
        self.play(explainer_dist.hide_grid(lag_ratio=0, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)

        # anchor points capture
        self.play(explainer_dist.to_rects(
            gargs={'lag_ratio':0, 'run_time':SHORT_DURATION,}
        ))
        self.wait(SHORT_DURATION)
        self.play(explainer_dist.to_dots(
            gargs={'lag_ratio':0, 'run_time':SHORT_DURATION,}
        ))
        self.wait(SHORT_DURATION)

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
        self.play(Write(annotation, lag_ratio=0, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)
        self.play(AnimationGroup(
            AnimationGroup(
                *(anno.label.animate.set_opacity(opacity=0) for anno in annotation),
                lag_ratio=0, run_time=SHORT_DURATION,
            ),
            AnimationGroup(
                *(anno.bbox.animate.set_fill(opacity=0) for anno in annotation),
                lag_ratio=0, run_time=SHORT_DURATION,
            ),
        ))
        self.wait(SHORT_DURATION)

        # highlight inside anchor points
        explainer_dist.save_state()
        in_aps, out_aps = explainer_dist.collect_in_out_aps(annotation)
        self.play(AnimationGroup(
            AnimationGroup(
                *(ap.animate.set_pattern(opacity=1.0,color=PURE_YELLOW) for ap in in_aps),
                lag_ratio=0, run_time=SHORT_DURATION,
            ),
            AnimationGroup(
                *(ap.animate.set_pattern(opacity=0.3,color=WHITE) for ap in out_aps),
                lag_ratio=0, run_time=SHORT_DURATION,
            ),
        ))
        self.wait(SHORT_DURATION)

        # fade out and remove annotation
        self.play(AnimationGroup(
            *(anno.bbox.animate.set_opacity(opacity=0) for anno in annotation),
            lag_ratio=0, run_time=SHORT_DURATION,
        ))
        self.remove(annotation)
        self.wait(SHORT_DURATION)

        # inside anchor points capture
        # TODO, make target rect transparent?
        self.play(AnimationGroup(
            *(ap.to_rect() for ap in in_aps),
            lag_ratio=0, run_time=SHORT_DURATION,
        ))
        self.wait(SHORT_DURATION)

        # restore to anchor point array
        self.play(explainer_dist.animate(run_time=SHORT_DURATION).restore())
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'sample, from distance to position thinking',
            skip_animations=False,
        )
        # ************************************************************
        # focus on sample anchor point
        sample_idx = 189
        sample_ap, other_aps = explainer_dist.collect_focus_ap(sample_idx)
        self.play(AnimationGroup(
            sample_ap.animate(run_time=SHORT_DURATION).set_pattern(opacity=1.0),
            AnimationGroup(
                *(ap.animate.set_pattern(opacity=0.3) for ap in other_aps),
                lag_ratio=0, run_time=SHORT_DURATION,
            )
        ))
        self.wait(SHORT_DURATION)
        
        # from distance to position, thinking
        self.play(sample_ap.show_arrows(lag_ratio=0.1, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)
        self.play(sample_ap.to_rect(run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)
        self.play(sample_ap.to_dot(run_time=SHORT_DURATION),)
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'sample, from absolute distance to relative distance',
            skip_animations=False,
        )
        # ************************************************************
        # from distance to position, details
        self.play(sample_ap.show_distance_abs(lag_ratio=0.1, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)
        self.play(AnimationGroup(
            sample_ap.arrows.animate(run_time=SHORT_DURATION).set_opacity(0.3),
            sample_ap.show_divide(run_time=SHORT_DURATION),
        ))
        self.wait(SHORT_DURATION)
        self.play(AnimationGroup(
            sample_ap.arrows.animate(run_time=SHORT_DURATION).set_opacity(1.0),
            sample_ap.abs_to_rela(
                aargs={'run_time':0.3,},
                gargs={'lag_ratio':0.1, 'run_time':SHORT_DURATION,},
            ),
        ))
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'sample, detailed computation from distance to position',
            skip_animations=False,
        )
        # ************************************************************
        # make room for equations
        self.play(explainer_dist_bg.animate(run_time=SHORT_DURATION).shift(LEFT*2).scale(0.9))
        self.wait(SHORT_DURATION)

        # create equations for sample
        sample_eq = sample_ap.create_decode_equations(
            buff=0.3,
        ).shift(RIGHT*3)
        self.play(Create(sample_eq))
        self.wait(SHORT_DURATION)

        # show point from x1y1
        self.play(explainer_dist.show_point_from_xy(
            sample_idx,
            direction=UL,
            pargs={'run_time':SHORT_DURATION, 'time_width':2},
            targs={},
            gargs={'lag_ratio':SHORT_DURATION,},
        ))
        self.wait(SHORT_DURATION)
        self.play(explainer_dist.hide_xy_txts(run_time=SHORT_DURATION))

        # show point from x2y2
        self.play(explainer_dist.show_point_from_xy(
            sample_idx,
            direction=DR,
            pargs={'run_time':1, 'time_width':2},
            targs={},
            gargs={'lag_ratio':SHORT_DURATION,},
        ))
        self.wait(SHORT_DURATION)
        self.play(explainer_dist.hide_xy_txts(run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)

        # to rect
        self.play(AnimationGroup(
            sample_ap.hide_distance(run_time=SHORT_DURATION, lag_ratio=0),
            sample_ap.to_rect(run_time=SHORT_DURATION),
        ))
        self.wait(SHORT_DURATION)

        # clean
        self.play(AnimationGroup(
            sample_ap.hide_arrows(run_time=SHORT_DURATION),
            sample_ap.to_dot(run_time=SHORT_DURATION),
            Uncreate(sample_eq, run_time=SHORT_DURATION),
        ))
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'loop, from distance to position',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, more natural way of looping
        k=1         # TODO, proper loop number
        idxs = random.sample(
            range(data_dist.shape[0]*data_dist.shape[1]),
            k=k,
        )
        for idx in idxs:
            # highlight one target point
            sample_ap, other_aps = explainer_dist.collect_focus_ap(idx)
            self.play(AnimationGroup(
                sample_ap.animate(run_time=SHORT_DURATION).set_pattern(opacity=1.0),
                AnimationGroup(
                    *(ap.animate.set_pattern(opacity=0.3) for ap in other_aps),
                    lag_ratio=0, run_time=SHORT_DURATION,
                )
            ))
            self.wait(SHORT_DURATION)

            # show arrows
            self.play(sample_ap.show_arrows(lag_ratio=0.0, run_time=SHORT_DURATION))
            self.wait(SHORT_DURATION)

            # show equations
            sample_eq = sample_ap.create_decode_equations(
                buff=0.3,
            ).shift(RIGHT*3)
            self.play(Create(sample_eq, run_time=SHORT_DURATION))
            self.wait(SHORT_DURATION)

            # to rect
            self.play(sample_ap.to_rect(run_time=SHORT_DURATION))
            self.wait(SHORT_DURATION)

            # restore
            self.play(AnimationGroup(
                sample_ap.hide_arrows(run_time=SHORT_DURATION),
                sample_ap.to_dot(run_time=SHORT_DURATION),
                Uncreate(sample_eq, run_time=SHORT_DURATION),
            ))
            self.wait(SHORT_DURATION)
        
        # make all aps opacity 1.0
        self.play(AnimationGroup(
            *(ap.animate.set_pattern(opacity=1.0)
            for ap in explainer_dist.anchor_points),
            lag_ratio=0.0,
            run_time=SHORT_DURATION,
        ))
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'global, generate distance tensor',
            skip_animations=False,
        )
        # ************************************************************
        # sync distance generation
        self.play(explainer_dist_bg.animate(run_time=SHORT_DURATION).scale(0.8).shift(LEFT*.5))
        self.wait(SHORT_DURATION)

        tensor_dist = explainer_dist.create_distance_tensor(font_size=8)
        tensor_dist.center().shift(RIGHT*3)
        self.play(AnimationGroup(
            explainer_dist.show_arrows(
                arrow_config={'stroke_width':1, 'tip_length':0.03,},
                gargs={'run_time':SHORT_DURATION, 'lag_ratio':0.02},
            ),
            Write(tensor_dist, run_time=SHORT_DURATION, lag_ratio=0.02),
        ))  # TODO, 3 seconds looks good
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'global, generate xyxy tensor',
            skip_animations=False,
        )
        # ************************************************************
        # scale and make room in the bottom
        sync_bbox = Group(explainer_dist_bg, tensor_dist)
        sync_bbox.generate_target()
        sync_bbox.target.scale(0.7).arrange(DOWN,buff=0.5).shift(LEFT*3)
        sync_bbox.target[1].align_to(sync_bbox.target[0][0].background, LEFT)
        self.play(MoveToTarget(sync_bbox, run_time=SHORT_DURATION))
        self.wait(SHORT_DURATION)

        # make copy of distance
        explainer_xyxy_bg = explainer_dist_bg.copy()
        self.add(explainer_xyxy_bg)
        self.play(explainer_xyxy_bg.animate(run_time=1.0).shift(RIGHT*5.5))
        self.wait(SHORT_DURATION)

        explainer_xyxy = explainer_xyxy_bg[0]

        # sync position generation
        tensor_xyxy = explainer_xyxy.create_xyxy_tensor(font_size=6)
        tensor_xyxy.align_to(tensor_dist, UP)
        self.play(AnimationGroup(
            explainer_xyxy.to_rects(
                rect_config={'width':0.5,},
                aargs={},
                gargs={'lag_ratio':0.01, 'run_time': SHORT_DURATION},
            ),
            explainer_xyxy.hide_arrows(
                aargs={},
                gargs={'lag_ratio':0.01, 'run_time': SHORT_DURATION},
            ),
            Write(tensor_xyxy, run_time=SHORT_DURATION, lag_ratio=0.01),
        ))  # TODO, 3 seconds looks good
        self.wait(SHORT_DURATION)

        # # TODO, generate comment labels for layers of tensors

        # ************************************************************
        self.next_section(
            'reshape xyxy tensor to 2d',
            skip_animations=False,
        )
        # ************************************************************
        # make room for reshaped xyxy tensor
        self.play(AnimationGroup(
            explainer_dist_bg.animate(run_time=SHORT_DURATION).shift(LEFT*1),
            tensor_dist.animate(run_time=SHORT_DURATION).shift(LEFT*1),
            explainer_xyxy_bg.animate(run_time=SHORT_DURATION).shift(LEFT*2),
            tensor_xyxy.animate(run_time=SHORT_DURATION).shift(LEFT*2),
        ))
        self.wait(SHORT_DURATION)

        # transform xyxy into reshaped 2d version
        tensor_xyxy_2d = tensor_xyxy.copy()     # make a copy as target 2d tensor
        self.add(tensor_xyxy_2d)
        line_matrix = explainer_xyxy.create_line_matrix().scale(0.07).shift(RIGHT*4.3)
        self.play(tensor_to_line_matrix(
            tensor=tensor_xyxy_2d,
            lmatrix=line_matrix,
            targs={},
            gargs={'lag_ratio':0.02, 'run_time':0.1,},
            ggargs={'lag_ratio':0.05, 'run_time':SHORT_DURATION,},
        ))
        self.wait(SHORT_DURATION)

        # ************************************************************
        self.next_section(
            'simplify tensor_dist/tensor_xyxy/tensor_xyxy_2d' \
            'into lf_output_32_dist/lf_output_32_xyxy/lf_output_32_xyxy_2d',
            skip_animations=False,
        )
        # ************************************************************
        # create lf_output_32_dist
        lf_output_32_dist = LayersFake(
            n=4,
            ref=tensor_dist,
            width_nominal=20,
            height_nominal=20,
            buff=0.05,
            expanded=True,
        ).move_to(tensor_dist).scale(0.95)

        # create lf_output_32_xyxy
        lf_output_32_xyxy = lf_output_32_dist.copy()
        lf_output_32_xyxy.move_to(tensor_xyxy)

        # create lf_output_32_xyxy_2d
        lf_output_32_xyxy_2d = LayersFake(
            n=1,
            ref=tensor_xyxy_2d,
            width_nominal=4,
            height_nominal=400,
            expanded=True,
        ).move_to(tensor_xyxy_2d)

        # simplify tensor_dist/tensor_xyxy/tensor_xyxy_2d
        self.play(AnimationGroup(
            Unwrite(tensor_dist, lag_ratio=0, run_time=1.0),
            Write(lf_output_32_dist, run_time=1.0),
            Unwrite(tensor_xyxy, lag_ratio=0, run_time=1.0),
            Write(lf_output_32_xyxy, run_time=1.0),
            Unwrite(tensor_xyxy_2d, lag_ratio=0, run_time=1.0),
            Write(lf_output_32_xyxy_2d, run_time=1.0),
        ))
        self.wait(0.3)


        # ************************************************************
        self.next_section(
            'simplify explainer_dist and explainer_xyxy ' \
            'into 4x4 mini version',
            skip_animations=False,
        )
        # ************************************************************
        # clean explainer_dist and explainer_xyxy
        self.play(AnimationGroup(
            explainer_dist.hide_arrows(
                aargs={},
                gargs={'lag_ratio':0, 'run_time':0.5},
            ),
            explainer_xyxy.to_dots(
                aargs={},
                gargs={'lag_ratio':0, 'run_time':0.5},
            ),
        ))
        self.wait(0.3)
        self.play(AnimationGroup(
            explainer_dist.hide_anchor_points(
                lag_ratio=0, run_time=0.5,
            ),
            explainer_xyxy.hide_anchor_points(
                lag_ratio=0, run_time=0.5,
            ),
        ))
        self.wait(0.3)
        self.remove(explainer_dist, explainer_xyxy)
        
        # create mini version explainer_dist and explainer_xyxy
        explainer_dist = ExplainerBbox(
            background=background,
            data=np.load(MINI_32_PATH),
            sf_nominal=32,
        )
        explainer_xyxy = ExplainerBbox(
            background=explainer_xyxy_bg[1],
            data=np.load(MINI_32_PATH),
            sf_nominal=32,
        )
        explainer_dist_bg = Group(explainer_dist, background)
        explainer_xyxy_bg = Group(explainer_xyxy, explainer_xyxy_bg[1])

        # show content for explainer_dist and explainer_xyxy
        self.play(AnimationGroup(
            explainer_dist.show_anchor_points(
                lag_ratio=0, run_time=0.5,
            ),
            explainer_xyxy.show_anchor_points(
                lag_ratio=0, run_time=0.5,
            ),
        ))
        self.wait(0.5)
        self.play(AnimationGroup(
            explainer_dist.show_arrows(
                arrow_config={'stroke_width':2, 'tip_length':0.06,},
                aargs={},
                gargs={'lag_ratio':0, 'run_time':0.5},
            ),
            explainer_xyxy.to_rects(
                rect_config={'width':1,},
                aargs={},
                gargs={'lag_ratio':0, 'run_time':0.5},
            ),
        ))
        self.wait(0.5)

        # # ************************************************************
        # self.next_section(
        #     'generate explainer_xyxy_2d from explainer_xyxy',
        #     skip_animations=False,
        # )
        # # ************************************************************

        # ************************************************************
        self.next_section(
            'save for next scene which go back to big map',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            explainer_dist_bg,
            explainer_xyxy_bg,
            lf_output_32_dist,
            lf_output_32_xyxy,
            lf_output_32_xyxy_2d,
        )
        save_everything(S013_EVERYTHING, everything)
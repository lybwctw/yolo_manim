from manim import *

from utils.constants import *
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.general import load_everything
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.layers_fake import LayersFake
from utils.explainer import Explainer
from utils.multi_arrow import MultiArrow
from utils.general import save_everything

class MainScene(Scene):
    def construct(self) -> None:
        # TODO, shift in through video editting
        # ************************************************************
        self.next_section(
            'init all mobs from start',
            skip_animations=False,
        )
        # ************************************************************
        background = ImagePad(padded=True).scale(0.4).set_opacity(0.2)
        explainer = Explainer(
            background=background,
            data=np.load(MINI_32_DIST_PATH),
            data_cls=np.load(MINI_32_PROB_PATH),
            sf_nominal=32,
        )

        # bbox output flowchart
        system_dist = Group(explainer, background)
        system_xyxy = system_dist.copy()
        system_xyxy_2d = system_xyxy.copy()
        tensor_32_dist = LayersFake(
            n=4,
            ref=system_dist[1],
            width_nominal=20,
            height_nominal=20,
            buff=0.05,
            expanded=True,
        ).scale(0.92)
        tensor_32_xyxy = tensor_32_dist.copy()
        tensor_32_xyxy_2d = LayersFake(
            n=1,
            width=0.5,
            height=2.0,
            width_nominal=4,
            height_nominal=400,
            expanded=True,
        )

        # class output flowchart
        system_probs = system_dist.copy()
        system_probs_2d = system_probs.copy()
        tensor_32_probs = LayersFake(
            n=3,
            ref=system_probs[1],
            width_nominal=20,
            height_nominal=20,
            buff=0.05,
            expanded=True,
        ).scale(0.92)
        tensor_32_probs_2d = LayersFake(
            n=1,
            width=0.3,
            height=2.0,
            width_nominal=3,
            height_nominal=400,
            expanded=True,
        )

        # acb -> ac for bbox
        acb_ab = ArrowComment(False, RIGHT, '?')
        acb_bc = ArrowComment(False, RIGHT, '?')
        acb_game = ArrowComment(False, RIGHT, '?')      # stand out
        acb_12 = ArrowComment(False, RIGHT, '?')
        acb_23 = ArrowComment(False, RIGHT, '?')
        acb_post = ArrowComment(False, RIGHT, '?')      # stand out

        # acc -> ac for bbox
        acc_ab = ArrowComment(False, RIGHT, '?')
        acc_game = ArrowComment(False, RIGHT, '?')      # stand out
        acc_12 = ArrowComment(False, RIGHT, '?')
        acc_post = ArrowComment(False, RIGHT, '?')      # stand out

        # for reference
        acb_all = VGroup(
            acb_ab, acb_bc,
            acb_game, acb_12, acb_23, acb_post,
        ).scale(0.4)
        acc_all = VGroup(
            acc_ab,
            acc_game, acc_12, acc_post,
        ).scale(0.4)
        
        # ************************************************************
        self.next_section(
            'start with bbox output flowchart',
            skip_animations=False,
        )
        # ************************************************************
        manager_bbox = Group(
            *[VMobject(), system_dist, acb_ab, system_xyxy, acb_bc, system_xyxy_2d, VMobject()],
            *[acb_game, tensor_32_dist, acb_12, tensor_32_xyxy, acb_23, tensor_32_xyxy_2d, acb_post],
        ).arrange_in_grid(
            rows=3,
            cols=7,
            buff=0.3,
        )
        manager_cls = Group(
            *[VMobject(), system_probs, acc_ab, system_probs_2d, VMobject()],
            *[acc_game, tensor_32_probs, acc_12, tensor_32_probs_2d, acc_post],
        ).arrange_in_grid(
            rows=3,
            cols=5,
            buff=0.3,
        ).shift(DOWN*10)    # hide for now

        # start with manager_bbox
        self.add(manager_bbox)
        self.wait()
        
        # bbox: show anchor points for each system
        self.play(AnimationGroup(
            system_dist[0].show_anchor_points(lag_ratio=0),
            system_xyxy[0].show_anchor_points(lag_ratio=0),
            system_xyxy_2d[0].show_anchor_points(lag_ratio=0),
        ))
        self.wait()

        # bbox: show target for each system
        self.play(AnimationGroup(
            system_dist[0].show_arrows(aargs={'lag_ratio':0}, gargs={'run_time':1}),
            system_xyxy[0].to_rects(
                rect_config={'width':1, 'color':GRAY},
                aargs={'lag_ratio':0},
                gargs={'run_time':1},
            ),
            system_xyxy_2d[0].to_rects(
                rect_config={'width':1, 'color':GRAY},
                aargs={'lag_ratio':0},
                gargs={'run_time':1},
            ),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'shift in class output flowchart',
            skip_animations=False,
        )
        # ************************************************************
        self.add(manager_cls)
        self.play(AnimationGroup(
            manager_bbox.animate.scale(0.63).shift(UP*2),
            manager_cls.animate.scale(0.63).shift(UP*8.5),
        ))
        self.wait()

        # class: show anchor points
        self.play(AnimationGroup(
            system_probs[0].show_anchor_points(lag_ratio=0),
            system_probs_2d[0].show_anchor_points(lag_ratio=0),
        ))

        # class: show target for each system
        self.play(AnimationGroup(
            system_probs[0].show_pbars(
                aargs={},
                gargs={},
                ggargs={},
            ),
            system_probs_2d[0].show_pbars(
                aargs={},
                gargs={},
                ggargs={},
            ),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'show shapes of all tensors',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, font size issue on shape texts
        # bbox: show shapes of each tensor
        acb_all.save_state()
        acc_all.save_state()
        system_dist.save_state()
        system_xyxy.save_state()
        system_xyxy_2d.save_state()
        system_probs.save_state()
        system_probs_2d.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                acb_all.animate.fade(0.8),
                acc_all.animate.fade(0.8),
                system_dist.animate.fade(0.8),
                system_xyxy.animate.fade(0.8),
                system_xyxy_2d.animate.fade(0.8),
                system_probs.animate.fade(0.8),
                system_probs_2d.animate.fade(0.8),
            ),
            AnimationGroup(
                tensor_32_dist.show_passing_flash(),
                tensor_32_xyxy.show_passing_flash(),
                tensor_32_xyxy_2d.show_passing_flash(),
                tensor_32_probs.show_passing_flash(),
                tensor_32_probs_2d.show_passing_flash(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # bbox: hide shapes
        # restore fails for system objects due to color interpolation issue
        self.play(AnimationGroup(
            AnimationGroup(
                tensor_32_dist.unwrite_shape_texts(),
                tensor_32_xyxy.unwrite_shape_texts(),
                tensor_32_xyxy_2d.unwrite_shape_texts(),
                tensor_32_probs.unwrite_shape_texts(),
                tensor_32_probs_2d.unwrite_shape_texts(),
            ),
            AnimationGroup(
                acb_all.animate.restore(),
                acc_all.animate.restore(),
                Transform(system_dist, system_dist.saved_state),
                Transform(system_xyxy, system_xyxy.saved_state),
                Transform(system_xyxy_2d, system_xyxy_2d.saved_state),
                Transform(system_probs, system_probs.saved_state),
                Transform(system_probs_2d, system_probs_2d.saved_state),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'merge bbox line and class flowchart',
            skip_animations=False,
        )
        # ************************************************************
        iview_bbox = Group(
            *[system_dist, acb_ab, system_xyxy, acb_bc, system_xyxy_2d],
        )
        tview_bbox = VGroup(
            *[acb_game, tensor_32_dist, acb_12, tensor_32_xyxy, acb_23, tensor_32_xyxy_2d, acb_post],
        )
        iview_cls = Group(
            *[system_probs, acc_ab, system_probs_2d],
        )
        tview_cls = VGroup(
            *[acc_game, tensor_32_probs, acc_12, tensor_32_probs_2d, acc_post],
        )

        # rearrange intuition view and tensor view
        self.play(AnimationGroup(
            tview_bbox.animate.shift(DOWN*2),
            iview_cls.animate.shift(UP*2),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'the merged output in both views',
            skip_animations=False,
        )
        # ************************************************************
        marrow_in = MultiArrow(
            one_to_many=True,
            p1=acb_game.get_right(),
            p2=acc_game.get_right(),
        )
        marrow_out = MultiArrow(
            one_to_many=False,
            p1=acb_post.get_left()+LEFT*0,
            p2=acc_post.get_left()+LEFT*0,
            ratio_input=0.2,
            ratio_brace=0.4,
            ratio_output=0.2,
        )

        # merge input arrows
        self.play(AnimationGroup(
            AnimationGroup(
                Unwrite(acb_game),
                Unwrite(acc_game),
            ),
            Write(marrow_in),
            lag_ratio=0.5,
        ))
        self.wait()

        # merge output arrows
        self.play(AnimationGroup(
            AnimationGroup(
                Unwrite(acb_post),
                Unwrite(acc_post),
            ),
            Write(marrow_out),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'tensor view, merge 2d tensors',
            skip_animations=False,
        )
        # ************************************************************
        tensor_32_xyxy_2d_copy = tensor_32_xyxy_2d.copy()
        tensor_32_probs_2d_copy = tensor_32_probs_2d.copy()
        self.play(AnimationGroup(
            FadeIn(tensor_32_xyxy_2d_copy),
            FadeIn(tensor_32_probs_2d_copy),
            run_time=0.3,
        ))
        self.wait(0.3)

        tensor_32_xyxy_2d_copy.generate_target()
        tensor_32_xyxy_2d_copy.target.next_to(marrow_out, RIGHT, buff=0.5)      # manual adjusted
        tensor_32_probs_2d_copy.generate_target()
        tensor_32_probs_2d_copy.target.next_to(tensor_32_xyxy_2d_copy.target, RIGHT, buff=0)
        tensor_copy = VGroup(
            tensor_32_xyxy_2d_copy,
            tensor_32_probs_2d_copy,
        )
        self.play(AnimationGroup(
            MoveToTarget(tensor_32_xyxy_2d_copy),
            MoveToTarget(tensor_32_probs_2d_copy),
        ))
        self.wait()

        # replace with a single tensor
        tensor_merged_2d = LayersFake(
            n=1,
            ref=tensor_copy,
            expanded=True,
            width_nominal=7,
            height_nominal=400,
        ).move_to(tensor_copy)
        self.play(AnimationGroup(
            FadeOut(tensor_copy),
            FadeIn(tensor_merged_2d),       # simply add?
        ))
        self.wait()

        # show shape of the merged 2d
        marrow_out.save_state()
        self.play(AnimationGroup(
            marrow_out.animate.fade(0.8),
            tensor_merged_2d.show_passing_flash(),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            tensor_merged_2d.unwrite_shape_texts(),
            marrow_out.animate.restore(),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'intuition view, merge outputs',
            skip_animations=False,
        )
        # ************************************************************
        # used in post-process part, scale back later
        scale_factor = 1.1

        # make a copy of marrow_out in intuition view
        # marrow_out_iview = marrow_out.copy()
        # self.add(marrow_out_iview)
        # self.play(
        #     marrow_out_iview\
        #     .animate(run_time=1.0)\
        #     .align_to(system_xyxy_2d, UP)\
        #     .shift(system_xyxy_2d.height/2*DOWN),
        # )
        # self.wait()

        # use new marrow instead of copy
        marrow_out_iview = MultiArrow(
            one_to_many=False,
            p1=system_xyxy_2d.get_right()+RIGHT*.2,
            p2=system_probs_2d.get_right()+RIGHT*.2,
            ratio_input=0.1,
            ratio_brace=0.4,
            ratio_output=0.1,
        )
        self.play(Write(marrow_out_iview))
        self.wait()

        # system_merged as a copy of system_xyxy_2d
        system_merged = system_xyxy_2d.copy()
        self.play(FadeIn(system_merged, run_time=0.3))
        self.play(
            system_merged\
            .animate(run_time=1.0)\
            .scale(scale_factor)\
            .next_to(marrow_out_iview, RIGHT, buff=0.26)
        )
        self.wait()

        # generate fake labels for each bbox
        self.play(system_merged[0].show_multi_labels(
            width_ratio=0.3,
            height_ratio=0.2,
            label_config={
                'fill_opacity': 0.9,
                'stroke_opacity': 0.0,
            },
            aargs={
                'lag_ratio': 0.1,
            },
            gargs={
                'lag_ratio': 0.2,
                'run_time': 1.0,
            }
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            "save everything, used by 019",
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            *iview_bbox, *iview_cls, *tview_bbox, *tview_cls,
            marrow_in, marrow_out, marrow_out_iview,
            system_merged, tensor_merged_2d,
        )
        save_everything(S017_EVERYTHING_BM, everything)

        # ************************************************************
        self.next_section("""
            focus on system_merged and tensor_merged_2d,
            used by 018.
            """,
            skip_animations=False,
        )
        # ************************************************************
        # manual init position for scene 018
        self.play(AnimationGroup(
            system_merged[1].animate(run_time=1.0).center().scale(4.0).to_edge(LEFT,buff=1.0),  # manual adjust background scale factor
            Unwrite(system_merged[0], lag_ratio=0, run_time=0.3),
            Unwrite(tensor_merged_2d, lag_ratio=0, run_time=0.3),
            FadeOut(iview_bbox, lag_ratio=0, run_time=0.3),
            FadeOut(iview_cls, lag_ratio=0, run_time=0.3),
            Unwrite(tview_bbox, lag_ratio=0, run_time=0.3),
            Unwrite(tview_cls, lag_ratio=0, run_time=0.3),
            Unwrite(marrow_in, lag_ratio=0, run_time=0.3),
            Unwrite(marrow_out, lag_ratio=0, run_time=0.3),
            Unwrite(marrow_out_iview, lag_ratio=0, run_time=0.3),
        ))
        self.wait()
        everything = Group(
            system_merged[1],
        )
        save_everything(S017_EVERYTHING_PP, everything)
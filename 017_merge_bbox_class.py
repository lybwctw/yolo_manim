from manim import *

from utils.constants import *
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.general import load_everything
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.layers_fake import LayersFake
from utils.explainer_bbox import ExplainerBbox
from utils.multi_arrow import MultiArrow

class MainScene(Scene):
    def construct(self) -> None:
        # TODO, shift in through video editting
        # ************************************************************
        self.next_section(
            'init all from start',
            skip_animations=True,
        )
        # ************************************************************
        background = ImagePad(padded=True).scale(0.4).set_opacity(0.2)
        explainer = ExplainerBbox(
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
            skip_animations=True,
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
            skip_animations=True,
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
            skip_animations=True,
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
            skip_animations=True,
        )
        # ************************************************************
        iview_bbox = Group(
            *[system_dist, acb_ab, system_xyxy, acb_bc, system_xyxy_2d],
        )
        tview_bbox = Group(
            *[acb_game, tensor_32_dist, acb_12, tensor_32_xyxy, acb_23, tensor_32_xyxy_2d, acb_post],
        )
        iview_cls = Group(
            *[system_probs, acc_ab, system_probs_2d],
        )
        tviwe_cls = Group(
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
            skip_animations=True,
        )
        # ************************************************************
        marrow_in = MultiArrow(
            one_to_many=True,
            p1=acb_game.get_right(),
            p2=acc_game.get_right(),
        )
        marrow_out = MultiArrow(
            one_to_many=False,
            p1=acb_post.get_left()+LEFT*0,     # manual adjust
            p2=acc_post.get_left()+LEFT*0,     # manual adjust
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
            skip_animations=True,
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
        tensor_32_xyxy_2d_copy.target.next_to(marrow_out, RIGHT, buff=0.3)
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
            skip_animations=True,
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

        # NOTE, played after 018_post_process!!!!!!!!!!!!!!!!!!
        # NOTE, played after 018_post_process!!!!!!!!!!!!!!!!!!
        # NOTE, played after 018_post_process!!!!!!!!!!!!!!!!!!

        # ************************************************************
        self.next_section("""
            Prepare before get into details of post-process.
            """,
            skip_animations=True,
        )
        # ************************************************************
        # shift left the big map 
        mobs = Group(*self.get_top_level_mobjects())
        self.play(mobs.animate.shift(LEFT*10.))
        self.wait()

        gap_postprocess = 0.2

        # ************************************************************
        self.next_section("""
            [1] max class selection
            (6400,7) -> (6400,6) [xyxy, conf, cls]
            split if [multi_label] option is on: (6400,7) -> (6400*3,6)
            """,
            skip_animations=True,
        )
        # ************************************************************
        # generate a copy of system_merged for post-process flowchart
        ac_a = acb_ab.copy().next_to(system_merged, RIGHT, buff=gap_postprocess)
        self.play(Write(ac_a))
        system_after_max = system_merged.copy()
        self.play(system_after_max.animate.next_to(ac_a, RIGHT, buff=gap_postprocess))
        # TODO: show comment on ac_a
        self.play(system_after_max[0].keep_max_label(
            aargs={},
            gargs={},
            ggargs={},
        ))
        self.wait()

        # generate a copy of tensor_merged_2d for post-process flowchart
        ac_1 = ac_a.copy().next_to(tensor_merged_2d, RIGHT, buff=gap_postprocess)\
            .align_to(ac_a, LEFT)
        self.play(Write(ac_1))
        tensor_after_max = tensor_merged_2d.copy()
        self.play(tensor_after_max.animate.next_to(ac_1, RIGHT, buff=gap_postprocess)\
            .set_x(system_after_max.get_x()))
        # TODO: show comment on ac_1
        self.play(tensor_after_max.animate.stretch_to_fit_width(
            tensor_merged_2d.width * 0.8
        ))
        tensor_after_max.width_nominal = 6      # xyxy, conf, cls
        self.wait()

        # show shapes of the new tensors after max class selection
        ac_1.save_state()
        marrow_out.save_state()     # marrow_out already changed, save again for later restore
        self.play(AnimationGroup(
            AnimationGroup(
                marrow_out.animate.fade(0.8),
                ac_1.animate.fade(0.8),
            ),
            AnimationGroup(
                tensor_merged_2d.show_passing_flash(),
                tensor_after_max.show_passing_flash(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                tensor_merged_2d.unwrite_shape_texts(),
                tensor_after_max.unwrite_shape_texts(),
            ),
            AnimationGroup(
                marrow_out.animate.restore(),
                ac_1.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section("""
            [2] filter use [conf] option: (6400,6) -> (k,6) [xyxy, conf, cls]
            classes filter if [classes] option is specified
            """,
            skip_animations=True,
        )
        # ************************************************************
        # generate a copy of system_after_max for post-process flowchart
        ac_b = ac_a.copy().next_to(system_after_max, RIGHT, buff=gap_postprocess)
        self.play(Write(ac_b))
        system_after_conf = system_after_max.copy()
        self.play(system_after_conf.animate.next_to(ac_b, RIGHT, buff=gap_postprocess))
        # TODO: show comment on ac_b
        # TODO: use hardcoded removal
        self.play(system_after_conf[0].keep_ratio(
            ratio=0.8,
            aargs={},
            gargs={},
        ))
        self.wait()

        # generate a copy of tensor_after_max for post-process flowchart
        ac_2 = ac_b.copy().next_to(tensor_after_max, RIGHT, buff=gap_postprocess)\
            .align_to(ac_b, LEFT)
        self.play(Write(ac_2))
        tensor_after_conf = tensor_after_max.copy()
        self.play(tensor_after_conf.animate.next_to(ac_2, RIGHT, buff=gap_postprocess)\
            .set_x(system_after_conf.get_x()))
        # TODO: show comment on ac_2
        self.play(tensor_after_conf.animate.stretch_to_fit_height(
            tensor_after_max.height * 0.6
        ))
        tensor_after_conf.height_nominal = 'k'      # xyxy, conf, cls
        self.wait()

        # show shapes of the new tensors after confidence filtering
        ac_2.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                marrow_out.animate.fade(0.8),
                ac_1.animate.fade(0.8),
                ac_2.animate.fade(0.8),
            ),
            AnimationGroup(
                tensor_merged_2d.show_passing_flash(),
                tensor_after_max.show_passing_flash(),
                tensor_after_conf.show_passing_flash(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                tensor_merged_2d.unwrite_shape_texts(),
                tensor_after_max.unwrite_shape_texts(),
                tensor_after_conf.unwrite_shape_texts(),
            ),
            AnimationGroup(
                marrow_out.animate.restore(),
                ac_1.animate.restore(),
                ac_2.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section("""
            [3] NMS filter using [iou] option: (k,6) -> (m,6) [xyxy, conf, cls]
            class agnostic NMS if [agnostic_nms] option is on
            [4-skipped] filter using [max_det] option
            """,
            skip_animations=True,
        )
        # ************************************************************
        # generate a copy of system_after_conf for post-process flowchart
        ac_c = ac_b.copy().next_to(system_after_conf, RIGHT, buff=gap_postprocess)
        self.play(Write(ac_c))
        system_after_nms = system_after_conf.copy()
        self.play(system_after_nms.animate.next_to(ac_c, RIGHT, buff=gap_postprocess))
        # TODO: show comment on ac_c
        # TODO: use hardcoded removal
        self.play(system_after_nms[0].keep_ratio(
            ratio=0.6,
            aargs={},
            gargs={},
        ))
        self.wait()

        # generate a copy of tensor_after_conf for post-process flowchart
        ac_3 = ac_c.copy().next_to(tensor_after_conf, RIGHT, buff=gap_postprocess)\
            .align_to(ac_c, LEFT)
        self.play(Write(ac_3))
        tensor_after_nms = tensor_after_conf.copy()
        self.play(tensor_after_nms.animate.next_to(ac_3, RIGHT, buff=gap_postprocess)\
            .set_x(system_after_nms.get_x()))
        # TODO: show comment on ac_3
        self.play(tensor_after_nms.animate.stretch_to_fit_height(
            tensor_after_conf.height * 0.6
        ))
        tensor_after_nms.height_nominal = 'm'      # xyxy, conf, cls
        self.wait()

        # show shapes of the new tensors after NMS filtering
        ac_3.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                marrow_out.animate.fade(0.8),
                ac_1.animate.fade(0.8),
                ac_2.animate.fade(0.8),
                ac_3.animate.fade(0.8),
            ),
            AnimationGroup(
                tensor_merged_2d.show_passing_flash(),
                tensor_after_max.show_passing_flash(),
                tensor_after_conf.show_passing_flash(),
                tensor_after_nms.show_passing_flash(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                tensor_merged_2d.unwrite_shape_texts(),
                tensor_after_max.unwrite_shape_texts(),
                tensor_after_conf.unwrite_shape_texts(),
                tensor_after_nms.unwrite_shape_texts(),
            ),
            AnimationGroup(
                marrow_out.animate.restore(),
                ac_1.animate.restore(),
                ac_2.animate.restore(),
                ac_3.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section("""
            [5] scale back to original image size: (m,6) -> (n,6)
                maybe convert to desired output format (e.g. xywh)
            """,
            skip_animations=True,
        )
        # ************************************************************
        # TODO, adjust naming
        # generate a copy of system_after_nms for post-process flowchart

        ac_d = ac_c.copy().next_to(system_after_nms, RIGHT, buff=gap_postprocess)
        self.play(Write(ac_d))
        # system_after_maxdet = system_after_nms.copy()
        system_scale_back = system_after_nms.copy()        # TODO
        self.play(system_scale_back.animate.next_to(ac_d, RIGHT, buff=gap_postprocess))
        self.play(system_scale_back[1].hide_paddings(
            updown=True,        # manual
            width_nominal=640,
            height_nominal=360,
            aargs={},
            gargs={},
        ))
        
        # TODO, scale up system as a whole, ugly alignment
        system_scale_back.generate_target()
        system_scale_back.target.scale(
            1.5,
            about_point=system_scale_back.target[1].get_center(),
        )
        y_to_align = system_scale_back.target[1].get_y()
        system_scale_back.target.next_to(
            ac_d,
            RIGHT,
            buff=gap_postprocess,
        )
        system_scale_back.target.set_y(y_to_align)
        self.play(MoveToTarget(
            system_scale_back,
            run_time=1.0,
        ))
        self.wait(0.3)

        # clip into the shrinked background image
        self.play(system_scale_back[0].clip_to_background(
            aargs={},
            gargs={},
        ))
        self.wait()
        # TODO: show comment on ac_d

        # generate a copy of tensor_after_nms for post-process flowchart
        ac_4 = ac_d.copy().next_to(tensor_after_nms, RIGHT, buff=gap_postprocess)\
            .align_to(ac_d, LEFT)
        self.play(Write(ac_4))
        tensor_scale_back = tensor_after_nms.copy()
        self.play(tensor_scale_back.animate.next_to(ac_4, RIGHT, buff=gap_postprocess)\
            .set_x(system_scale_back.get_x()))
        # TODO: show comment on ac_4
        self.play(tensor_scale_back.animate.stretch_to_fit_height(
            tensor_after_nms.height * 0.8
        ))
        tensor_scale_back.height_nominal = 'n'      # xywh, conf, cls
        self.wait()

        # show shapes of the new tensors after max_det filtering
        ac_4.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                marrow_out.animate.fade(0.8),
                ac_1.animate.fade(0.8),
                ac_2.animate.fade(0.8),
                ac_3.animate.fade(0.8),
                ac_4.animate.fade(0.8),
            ),
            AnimationGroup(
                tensor_merged_2d.show_passing_flash(),
                tensor_after_max.show_passing_flash(),
                tensor_after_conf.show_passing_flash(),
                tensor_after_nms.show_passing_flash(),
                tensor_scale_back.show_passing_flash(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            AnimationGroup(
                tensor_merged_2d.unwrite_shape_texts(),
                tensor_after_max.unwrite_shape_texts(),
                tensor_after_conf.unwrite_shape_texts(),
                tensor_after_nms.unwrite_shape_texts(),
                tensor_scale_back.unwrite_shape_texts(),
            ),
            AnimationGroup(
                marrow_out.animate.restore(),
                ac_1.animate.restore(),
                ac_2.animate.restore(),
                ac_3.animate.restore(),
                ac_4.animate.restore(),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'back to output big map',
            skip_animations=True,
        )
        # ************************************************************
        # scale down the big map
        mobs = Group(*self.get_top_level_mobjects())
        self.play(mobs.animate.scale(0.7).center())
        self.wait()

        # show shapes for all tensors in the big map
        ac_all = VGroup(
            acc_all, acb_all,
            ac_a, ac_b, ac_c, ac_d,
            ac_1, ac_2, ac_3, ac_4,
            marrow_in, marrow_out, marrow_out_iview,
        )
        ac_all.save_state()

        # TODO, setup font size and gap for shape texts
        # TODO, also shape text z_index
        self.play(
            ac_all.animate.fade(0.8),
            run_time=1.0,
        )
        self.play(AnimationGroup(
            tensor_32_dist.show_passing_flash(),
            tensor_32_xyxy.show_passing_flash(),
            tensor_32_xyxy_2d.show_passing_flash(),
            tensor_32_probs.show_passing_flash(),
            tensor_32_probs_2d.show_passing_flash(),
            tensor_merged_2d.show_passing_flash(),
            tensor_after_max.show_passing_flash(),
            tensor_after_conf.show_passing_flash(),
            tensor_after_nms.show_passing_flash(),
            tensor_scale_back.show_passing_flash(),
            lag_ratio=0.1,
        ))
        self.wait()

        self.play(AnimationGroup(
            tensor_32_dist.unwrite_shape_texts(),
            tensor_32_xyxy.unwrite_shape_texts(),
            tensor_32_xyxy_2d.unwrite_shape_texts(),
            tensor_32_probs.unwrite_shape_texts(),
            tensor_32_probs_2d.unwrite_shape_texts(),
            tensor_merged_2d.unwrite_shape_texts(),
            tensor_after_max.unwrite_shape_texts(),
            tensor_after_conf.unwrite_shape_texts(),
            tensor_after_nms.unwrite_shape_texts(),
            tensor_scale_back.unwrite_shape_texts(),
            lag_ratio=0.1,
        ))
        self.play(
            ac_all.animate.restore(),
            run_time=1.0,
        )
        self.wait()

        # ************************************************************
        self.next_section("""
            split output procedure into 2 stages:
            post-process and post-post-process
            """,
            skip_animations=True,
        )
        # ************************************************************
        # TODO, make state saving clear
        system_all = Group(
            system_dist, system_xyxy, system_xyxy_2d,
            system_probs, system_probs_2d,
            system_merged, system_after_max, system_after_conf, system_after_nms, system_scale_back,
        ).save_state()
        tensor_all = VGroup(
            tensor_32_dist, tensor_32_xyxy, tensor_32_xyxy_2d,
            tensor_32_probs, tensor_32_probs_2d,
            tensor_merged_2d, tensor_after_max, tensor_after_conf, tensor_after_nms, tensor_scale_back,
        ).save_state()
        ac_all.save_state()
        for system, tensor in zip(system_all, tensor_all):
            system.save_state()
            tensor.save_state()

        # fade all
        self.play(AnimationGroup(
            ac_all.animate.fade(0.8),
            system_all.animate.fade(0.8),
            tensor_all.animate.fade(0.8),
            lag_ratio=0.1,
        ))
        self.wait(.3)

        # show init system/tensors
        self.play(AnimationGroup(
            Transform(system_dist, system_dist.saved_state.scale(1.2)),
            Transform(system_probs, system_probs.saved_state.scale(1.2)),
            Transform(tensor_32_dist, tensor_32_dist.saved_state.scale(1.2)),
            Transform(tensor_32_probs, tensor_32_probs.saved_state.scale(1.2)),
            lag_ratio=0,
        ))
        self.wait(1)

        # from init systems/tensors to decoded system/tensor
        # TODO, make it faster
        self.play(AnimationGroup(
            AnimationGroup(
                AnimationGroup(
                    Transform(system_xyxy, system_xyxy.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                    Transform(system_xyxy_2d, system_xyxy_2d.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                    Transform(system_merged, system_merged.saved_state.scale(1.2)),
                    lag_ratio=0.3,
                    run_time=1.0,
                ),
                AnimationGroup(
                    Transform(system_probs_2d, system_probs_2d.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),   
                    lag_ratio=0.5,
                    run_time=0.8,
                ),
                lag_ratio=0,
            ),
            AnimationGroup(
                AnimationGroup(
                    Transform(tensor_32_xyxy, tensor_32_xyxy.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                    Transform(tensor_32_xyxy_2d, tensor_32_xyxy_2d.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                    Transform(tensor_merged_2d, tensor_merged_2d.saved_state.scale(1.2)),
                    lag_ratio=0.3,
                    run_time=1.0,
                ),
                AnimationGroup(
                    Transform(tensor_32_probs_2d, tensor_32_probs_2d.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),   
                    lag_ratio=0.5,
                    run_time=0.8,
                ),
                lag_ratio=0,
            ),
            lag_ratio=0,
        ))
        self.wait()

        # from decoded system/tensor to postprocessed system/tensor
        self.play(AnimationGroup(
            AnimationGroup(
                Transform(system_after_max, system_after_max.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                Transform(system_after_conf, system_after_conf.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                Transform(system_after_nms, system_after_nms.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                Transform(system_scale_back, system_scale_back.saved_state.scale(1.2)),
                lag_ratio=0.2,
                run_time=0.8,
            ),
            AnimationGroup(
                Transform(tensor_after_max, tensor_after_max.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                Transform(tensor_after_conf, tensor_after_conf.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                Transform(tensor_after_nms, tensor_after_nms.saved_state.scale(1.2), rate_func=rate_functions.there_and_back_with_pause),
                Transform(tensor_scale_back, tensor_scale_back.saved_state.scale(1.2)),
                lag_ratio=0.2,
                run_time=0.8,
            ),
        ))
        self.wait()

        # NOTE: video editing point!!!!!!!!!!!!!!!!!!

        # ************************************************************
        self.next_section(
            'simplify the details in post-process stage',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, more natural transform from current acs to new acs?
        ac_cd = ArrowComment(False, RIGHT, 'decode').scale(0.3).shift(UP*10)
        ac_de = ArrowComment(False, RIGHT, 'post-process').scale(0.3).shift(UP*10)
        ac_game = ArrowComment(False, RIGHT, 'model').scale(0.3).shift(LEFT*10) # TODO, stand out
        ac_34 = ArrowComment(False, RIGHT, 'decode').scale(0.3).shift(DOWN*10)
        ac_45 = ArrowComment(False, RIGHT, 'post-process').scale(0.3).shift(DOWN*10)
        manager = Group(
            *[VMobject(), system_dist, system_probs, ac_cd, system_merged, ac_de, system_scale_back],
            *[ac_game, tensor_32_dist, tensor_32_probs, ac_34, tensor_merged_2d, ac_45, tensor_scale_back],
        )
        other_systems = Group(
            *(system for system in system_all if system not in 
            [system_dist, system_probs, system_merged, system_scale_back])
        )
        other_tensors = Group(
            *(tensor for tensor in tensor_all if tensor not in 
            [tensor_32_dist, tensor_32_probs, tensor_merged_2d, tensor_scale_back])
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=2,
            cols=7,
            buff=0.5,
        ).center()
        # stretch up the final tensor for better visual after rearrangement
        manager.target[13].stretch_to_fit_height(
            tensor_merged_2d.height * 0.6,
        )   
        self.play(AnimationGroup(
            FadeOut(other_systems),
            FadeOut(other_tensors),
            Unwrite(ac_all),
            MoveToTarget(manager),
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'bigger map: from input to output',
            skip_animations=False,
        )
        # ************************************************************
        ac_ab = ArrowComment(False, RIGHT, 'preprocess').scale(0.3).shift(LEFT*10)
        ac_12 = ArrowComment(False, RIGHT, 'preprocess').scale(0.3).shift(LEFT*10)
        image_raw = system_scale_back[1].copy().set_x(0).shift(LEFT*10)
        image_pad = system_merged[1].copy().set_x(0).shift(LEFT*10)
        tensor_raw = LayersFake(
            n=3,
            ref=image_raw,
            expanded=True,
            width_nominal=image_raw.width_nominal,
            height_nominal=image_raw.height_nominal,
            buff=0.05,              # TODO, natural buff?
        ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?
        tensor_pad = LayersFake(
            n=3,
            ref=image_pad,
            expanded=True,
            width_nominal=image_pad.width_nominal,
            height_nominal=image_pad.height_nominal,
            buff=0.05,              # TODO, natural buff?
        ).scale(1.0).shift(LEFT*10) # TODO, scale up a little bit?

        manager = Group(
            *[image_raw, ac_ab, image_pad, VMobject(), system_dist, system_probs, ac_cd, system_merged, ac_de, system_scale_back],
            *[tensor_raw, ac_12, tensor_pad, ac_game, tensor_32_dist, tensor_32_probs, ac_34, tensor_merged_2d, ac_45, tensor_scale_back],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=2,
            cols=10,
            # buff=0.5,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # TODO, pop out comments from acs

        # ************************************************************
        self.next_section(
            'more on output design',
            skip_animations=True,
        )
        # ************************************************************
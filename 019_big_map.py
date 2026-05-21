from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.general import import_mobs, export_mobs

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs according to 017',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs(S017_EVERYTHING_BM)
        (
            s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, marrow_out_iview, s32_merged_2d,
            s32_prob, acc_12, s32_prob_2d,
            marrow_in_tview,
            t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d, marrow_out_tview, t32_merged_2d,
            t32_prob, acc_12, t32_prob_2d,
        ) = mobs

        # for reference
        acb_all = VGroup(
            acb_ab, acb_bc,
            acb_game, acb_12, acb_23, acb_post,
        )
        acc_all = VGroup(
            acc_ab,
            acc_game, acc_12, acc_post,
        )
        
        self.add(everything)
        self.wait()

        # ************************************************************
        self.next_section("""
            Prepare before get into details of post-process.
            """,
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
            skip_animations=False,
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
        image_raw = system_scale_back[1].copy().set_opacity(1.0).set_x(0).shift(LEFT*10)
        image_pad = system_merged[1].copy().set_opacity(1.0).set_x(0).shift(LEFT*10)
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
        # TODO, maybe show shapes again?

        # ************************************************************
        self.next_section(
            'save everything for multi-layers output big map',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME, redundancy between manager and everything
        everything = Group(
            *[image_raw, ac_ab, image_pad, VMobject(), system_dist, system_probs, ac_cd, system_merged, ac_de, system_scale_back],
            *[tensor_raw, ac_12, tensor_pad, ac_game, tensor_32_dist, tensor_32_probs, ac_34, tensor_merged_2d, ac_45, tensor_scale_back],
        )
        save_everything(S019_EVERYTHING, everything)
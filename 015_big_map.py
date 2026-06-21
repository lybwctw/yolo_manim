from manim import *

from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.layers_fake import LayersFake
from utils.explainer import Explainer
from utils.multi_arrow import MultiArrow
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs
from utils.constants import *

MERGED_SCALE_FACTOR = 1.1

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # NOTE, shift in box flowchart by video editting
        # ************************************************************
        self.next_section(
            'init mobs from 013 and 014',
            skip_animations=True,
        )
        # ************************************************************
        # load 013(box) mobs and 014(cls) mobs
        mobs_box = import_mobs('013')
        mobs_cls = import_mobs('014').shift(DOWN*10)

        (
            _,           s32_offset, aci_7, s32_xyxy, aci_8, s32_xyxy_2d,
            _,           acm_5,      _,     acm_6,    _,     acm_7,
            ac_game_box, t32_offset, act_7, t32_xyxy, act_8, t32_xyxy_2d,
        ) = mobs_box
        (
            _,           s32_prob, aci_9, s32_prob_2d,
            _,           acm_8,    _,     acm_9,
            ac_game_cls, t32_prob, act_9, t32_prob_2d,
        ) = mobs_cls

        # for reference
        mobs_box_s = Group(
            s32_offset, aci_7, s32_xyxy, aci_8, s32_xyxy_2d,
        )
        mobs_box_t = Group(
            ac_game_box, t32_offset, act_7, t32_xyxy, act_8, t32_xyxy_2d,
        )
        mobs_cls_s = Group(
            s32_prob, aci_9, s32_prob_2d,
        )
        mobs_cls_t = Group(
            ac_game_cls, t32_prob, act_9, t32_prob_2d,
        )
        ac_all = VGroup(
            aci_7, aci_8, aci_9,
            act_7, act_8, act_9,
            ac_game_box, ac_game_cls,
        )

        # start with box mobs
        self.add(mobs_box)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'insert cls mobs and merge',
            skip_animations=True,
        )
        # ************************************************************
        # shift in 014 mobs
        mobs = Group(
            mobs_box,
            mobs_cls,
        )
        mobs.generate_target()
        mobs.target.arrange(
            DOWN,
            buff=0.7,
        ).scale(0.6).center()
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # remove up-down arrows
        ac_remove = VGroup(
            acm_5, acm_6, acm_7, acm_8, acm_9,
        )
        self.play(Unwrite(
            ac_remove,
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # scale up and adjust position
        self.play(AnimationGroup(
            mobs_box_s.animate.scale(1.3),
            mobs_box_t.animate.scale(1.3).shift(UP*0.3),
            mobs_cls_s.animate.scale(1.3).shift(DOWN*0.3),
            mobs_cls_t.animate.scale(1.3),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # merge intuition(system) view and tensor view of box/cls
        self.play(AnimationGroup(
            mobs_box_t.animate.shift(DOWN*2),
            mobs_cls_s.animate.shift(UP*2),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'merge input and output arrows in tensor view',
            skip_animations=True,
        )
        # ************************************************************
        mat_1 = MultiArrow(
            one_to_many=True,
            p1=ac_game_box.get_right(),
            p2=ac_game_cls.get_right(),
        )
        # replace input arrows with a single marrow
        self.play(AnimationGroup(
            AnimationGroup(
                Unwrite(ac_game_box),
                Unwrite(ac_game_cls),
            ),
            Write(mat_1),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # update quick reference
        ac_all.remove(ac_game_box, ac_game_cls)
        ac_all.add(mat_1)

        # show shapes of tensor before continue
        ac_all.save_state()
        self.play(ac_all.animate(
            run_time=wt,
        ).fade(0.8))
        self.play(AnimationGroup(
            ShowShape(t32_offset, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_xyxy, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_xyxy_2d, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_prob, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            ShowShape(t32_prob_2d, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # hide shapes
        self.play(AnimationGroup(
            HideShape(t32_offset),
            HideShape(t32_xyxy),
            HideShape(t32_xyxy_2d),
            HideShape(t32_prob),
            HideShape(t32_prob_2d),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.play(ac_all.animate(
            run_time=wt,
        ).restore())
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'tensor view: generate merged 2d tensor',
            skip_animations=False,
        )
        # ************************************************************
        # ajust positioning of all mobs
        mobs = Group(*self.get_top_level_mobjects())
        self.play(mobs.animate(
            run_time=wt,
        ).shift(LEFT*1.0))
        self.wait(wt)

        # show marrow before merged tensor
        mat_2 = MultiArrow(
            one_to_many=False,
            p1=t32_xyxy_2d.get_right()+RIGHT*0.5,
            p2=t32_prob_2d.get_right()+RIGHT*0.5,
            ratio_input=0.2,
            ratio_brace=0.4,
            ratio_output=0.2,
        )
        ac_all.add(mat_2)
        self.play(Write(
            mat_2,
            run_time=wt,
        ))
        self.wait(wt)

        # create copy of 2d tensors
        t32_xyxy_2d_copy = t32_xyxy_2d.copy()
        t32_prob_2d_copy = t32_prob_2d.copy()
        self.play(AnimationGroup(
            FadeIn(t32_xyxy_2d_copy),
            FadeIn(t32_prob_2d_copy),
            run_time=wt,
        ))

        # move copy to target position
        t32_xyxy_2d_copy.generate_target()
        t32_xyxy_2d_copy.target.next_to(mat_2, RIGHT, buff=0.5)
        t32_prob_2d_copy.generate_target()
        t32_prob_2d_copy.target.next_to(t32_xyxy_2d_copy.target, RIGHT, buff=0)
        t32_combined = VGroup(
            t32_xyxy_2d_copy,
            t32_prob_2d_copy,
        )
        self.play(AnimationGroup(
            MoveToTarget(t32_xyxy_2d_copy),
            MoveToTarget(t32_prob_2d_copy),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # replace copies with a single tensor
        t32_merged_2d = LayersFake(
            n=1,
            ref=t32_combined,
            width_nominal=7,
            height_nominal=400,
            expanded=True,
        ).move_to(t32_combined)
        self.play(AnimationGroup(
            FadeOut(t32_combined),
            FadeIn(t32_merged_2d),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show shape of the just merged
        mat_2.save_state()
        self.play(AnimationGroup(
            mat_2.animate.fade(0.8),
            ShowShape(t32_merged_2d, text_config=MEDIUM_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)
        self.play(AnimationGroup(
            HideShape(t32_merged_2d),
            mat_2.animate.restore(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'intuition view, create merge system',
            skip_animations=False,
        )
        # ************************************************************
        # use new merge marrow instead of copy
        mas_2 = MultiArrow(
            one_to_many=False,
            p1=s32_xyxy_2d.get_right()+RIGHT*.2,
            p2=s32_prob_2d.get_right()+RIGHT*.2,
            ratio_input=0.10,
            ratio_brace=0.4,
            ratio_output=0.1,
        )
        ac_all.add(mas_2)
        self.play(Write(
            mas_2,
            run_time=wt,
        ))
        self.wait(wt)

        # merged system as a copy of s32_xyxy_2d
        s32_merged_2d = s32_xyxy_2d.copy()
        self.play(FadeIn(
            s32_merged_2d,
            run_time=wt,
        ))
        self.play((
            s32_merged_2d.animate(
                run_time=wt,
            ).scale(
                MERGED_SCALE_FACTOR,
            ).next_to(
                mas_2,
                RIGHT,
                buff=0.26,
            )
        ))
        self.wait(wt)

        # generate fake labels for each box in merged
        self.play(s32_merged_2d[-1].show_multi_labels(
            include_text=False,
            box_config={
                'width': 0.1,
                'height': 0.05,
                'fill_opacity': 1.0,
            },
            aargs={
                'lag_ratio': 0.1,
            },
            gargs={
                'lag_ratio': 0.2,
                'run_time': wt,
            }
        ))
        self.wait()

        # # ************************************************************
        # self.next_section(
        #     "save everything, used by 019",
        #     skip_animations=False,
        # )
        # # ************************************************************
        # mobs = Group(
        #     s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, marrow_out_iview, s32_merged_2d,
        #     s32_prob, acc_ab, s32_prob_2d,
        #     marrow_in_tview,
        #     t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d, marrow_out_tview, t32_merged_2d,
        #     t32_prob, acc_12, t32_prob_2d,
        # )
        # export_mobs(__file__, mobs)
from manim import *

from utils.constants import *
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import YoloAnnotation
from utils.layers_fake import LayersFake
from utils.explainer import Explainer
from utils.multi_arrow import MultiArrow
from utils.show_shape import ShowShape, HideShape
from utils.general import export_mobs

MERGED_SCALE_FACTOR = 1.1

# FIXME: update order issue of system
class MainScene(Scene):
    def construct(self) -> None:
        # NOTE, shift in box flowchart by video editting
        # ************************************************************
        self.next_section(
            'init all mobs from start',
            skip_animations=False,
        )
        # ************************************************************
        background = ImagePad(padded=True).scale(0.4).set_opacity(0.2)
        e32_dist = Explainer.from_random(       # explainer of stride 32 for distance(box)
            background=background,
            reg_max=4,
            dist_range=(0.5, 1),
            prob_range=(0, 1),
            shape=(4, 4),
            sf_pcell=0.5,
        )

        s32_dist = Group(background, e32_dist)  # system of stride 32 for distance(box)
        s32_xyxy = s32_dist.copy()              # system of stride 32 for xyxy(box)
        s32_xyxy_2d = s32_xyxy.copy()           # system of stride 32 for 2d xyxy(box)
        t32_dist = LayersFake(                  # tensor of stride 32 for distance(box)
            n=4,
            ref=s32_dist[0],
            width_nominal=20,
            height_nominal=20,
            buff=0.05,
            expanded=True,
        ).scale(0.92)
        t32_xyxy = t32_dist.copy()              # tensor of stride 32 for xyxy(box)
        t32_xyxy_2d = LayersFake(               # tensor of stride 32 for 2d xyxy(box)
            n=1,
            width=0.5,
            height=2.0,
            width_nominal=4,
            height_nominal=400,
            expanded=True,
        )

        s32_prob = s32_dist.copy()              # system of stride 32 for prob(cls)
        s32_prob_2d = s32_prob.copy()           # system of stride 32 for 2d prob(cls)
        t32_prob = LayersFake(                  # tensor of stride 32 for prob(cls)
            n=3,
            ref=s32_prob[0],
            width_nominal=20,
            height_nominal=20,
            buff=0.05,
            expanded=True,
        ).scale(0.92)
        t32_prob_2d = LayersFake(               # tensor of stride 32 for 2d prob(cls)
            n=1,
            width=0.4,
            height=2.0,
            width_nominal=3,
            height_nominal=400,
            expanded=True,
        )

        # acb -> arrowcomment for box
        acb_ab = ArrowComment(False, RIGHT, '?')
        acb_bc = ArrowComment(False, RIGHT, '?')
        acb_game = ArrowComment(False, RIGHT, '?')      # TODO: stand out
        acb_12 = ArrowComment(False, RIGHT, '?')
        acb_23 = ArrowComment(False, RIGHT, '?')
        acb_post = ArrowComment(False, RIGHT, '?')      # TODO: stand out

        # acc -> arrowcomment for cls
        acc_ab = ArrowComment(False, RIGHT, '?')
        acc_game = ArrowComment(False, RIGHT, '?')      # TODO: stand out
        acc_12 = ArrowComment(False, RIGHT, '?')
        acc_post = ArrowComment(False, RIGHT, '?')      # TODO: stand out

        # reference
        ac_all = VGroup(
                      acb_ab, acb_bc,
            acb_game, acb_12, acb_23, acb_post,
                      acc_ab,
            acc_game, acc_12, acc_post,
        ).scale(0.4)    # all arrow with comments

        iv32_box = Group(
            *[Mobject(), s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, VMobject()],
        )   # intuition view of stride 32 box
        tv32_box = Group(
            *[acb_game,  t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d, acb_post],
        )   # tensor view of stride 32 box
        iv32_cls = Group(
            *[Mobject(), s32_prob, acc_ab, s32_prob_2d, Mobject()],
        )   # intuition view of stride 32 cls
        tv32_cls = Group(
            *[acc_game,  t32_prob, acc_12, t32_prob_2d, acc_post],
        )   # tensor view of stride 32 cls
        flowchart_box = Group(
            *iv32_box,
            *tv32_box,
        ).arrange_in_grid(rows=3, cols=7, buff=0.3,)
        flowchart_cls = Group(
            *iv32_cls,
            *tv32_cls,
        ).arrange_in_grid(rows=3, cols=5, buff=0.3,).shift(DOWN*10)
        
        # ************************************************************
        self.next_section(
            'show box prediction flowchart',
            skip_animations=False,
        )
        # ************************************************************
        self.add(flowchart_box)
        self.wait()
        
        # box: show anchor points for each system
        self.play(AnimationGroup(
            s32_dist[-1].show_anchor_points(lag_ratio=0),
            s32_xyxy[-1].show_anchor_points(lag_ratio=0),
            s32_xyxy_2d[-1].show_anchor_points(lag_ratio=0),
        ))
        self.wait()

        # box: show target for each system
        self.play(AnimationGroup(
            s32_dist[-1].show_arrows(
                aargs={'lag_ratio':0},
                gargs={'run_time':1},
            ),
            s32_xyxy[-1].to_rects(
                rect_config={
                    'stroke_width':1,
                    'stroke_color':GRAY,
                },
                aargs={'lag_ratio':0},
                gargs={'run_time':1},
            ),
            s32_xyxy_2d[-1].to_rects(
                rect_config={
                    'stroke_width':1,
                    'stroke_color':GRAY,
                },
                aargs={'lag_ratio':0},
                gargs={'run_time':1},
            ),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'shift in class prediction flowchart',
            skip_animations=False,
        )
        # ************************************************************
        self.add(flowchart_cls)
        self.play(AnimationGroup(
            flowchart_box.animate.scale(0.63).shift(UP*1.9),
            flowchart_cls.animate.scale(0.63).shift(UP*8.5),
        ))
        self.wait()

        # show anchor points
        self.play(AnimationGroup(
            s32_prob[-1].show_anchor_points(lag_ratio=0),
            s32_prob_2d[-1].show_anchor_points(lag_ratio=0),
        ))

        # hide anchor points and show pbars
        self.play(AnimationGroup(
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.0)
                  for ap in s32_prob[-1].anchor_points),
                lag_ratio=0.0,
                run_time=1.0,
            ),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.0)
                  for ap in s32_prob_2d[-1].anchor_points),
                lag_ratio=0.0,
                run_time=1.0,
            ),
            s32_prob[-1].show_pbars(
                aargs={},
                gargs={},
                ggargs={},
            ),
            s32_prob_2d[-1].show_pbars(
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
        ac_all.save_state()
        iv32_box.save_state()
        iv32_cls.save_state()
        self.play(AnimationGroup(
            AnimationGroup(
                ac_all.animate.fade(0.8),
                iv32_box.animate.fade(0.8),
                iv32_cls.animate.fade(0.8),
            ),
            AnimationGroup(
                ShowShape(t32_dist, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_xyxy, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_xyxy_2d, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_prob, text_config=SMALL_SHAPE_TEXT_CONFIG),
                ShowShape(t32_prob_2d, text_config=SMALL_SHAPE_TEXT_CONFIG),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # FIXME: restore fails for system objects due to color interpolation issue
        self.play(AnimationGroup(
            AnimationGroup(
                HideShape(t32_dist),
                HideShape(t32_xyxy),
                HideShape(t32_xyxy_2d),
                HideShape(t32_prob),
                HideShape(t32_prob_2d),
            ),
            AnimationGroup(
                ac_all.animate.restore(),
                Transform(iv32_box, iv32_box.saved_state),
                Transform(iv32_cls, iv32_cls.saved_state),
            ),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'merge box+cls intuition view and tensor view',
            skip_animations=False,
        )
        # ************************************************************
        # # swap box intuition view and cls tensor view manually
        # self.play(AnimationGroup(
        #     tview_box.animate.shift(DOWN*2),
        #     iview_cls.animate.shift(UP*2),
        # ))
        self.play(Swap(tv32_box, iv32_cls))
        self.wait()

        # ************************************************************
        self.next_section(
            'merge input and output arrows in tensor view',
            skip_animations=False,
        )
        # ************************************************************
        marrow_in_tview = MultiArrow(
            one_to_many=True,
            p1=acb_game.get_right(),
            p2=acc_game.get_right(),
        )
        marrow_out_tview = MultiArrow(
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
            Write(marrow_in_tview),
            lag_ratio=0.5,
        ))

        # merge output arrows
        self.play(AnimationGroup(
            AnimationGroup(
                Unwrite(acb_post),
                Unwrite(acc_post),
            ),
            Write(marrow_out_tview),
            lag_ratio=0.5,
        ))
        self.wait()

        # update reference group
        ac_all.remove(acb_game, acb_post, acc_game, acc_post)
        ac_all.add(marrow_in_tview, marrow_out_tview)
        # TODO: iv32, tv32, flowchart..

        # ************************************************************
        self.next_section(
            'tensor view: create merged 2d tensor',
            skip_animations=False,
        )
        # ************************************************************
        t32_xyxy_2d_copy = t32_xyxy_2d.copy()
        t32_prob_2d_copy = t32_prob_2d.copy()
        self.play(AnimationGroup(
            FadeIn(t32_xyxy_2d_copy),
            FadeIn(t32_prob_2d_copy),
            run_time=0.3,
        ))
        self.wait(0.3)

        t32_xyxy_2d_copy.generate_target()
        t32_xyxy_2d_copy.target.next_to(marrow_out_tview, RIGHT, buff=0.5)
        t32_prob_2d_copy.generate_target()
        t32_prob_2d_copy.target.next_to(t32_xyxy_2d_copy.target, RIGHT, buff=0)
        t32_combined = VGroup(
            t32_xyxy_2d_copy,
            t32_prob_2d_copy,
        )
        self.play(AnimationGroup(
            MoveToTarget(t32_xyxy_2d_copy),
            MoveToTarget(t32_prob_2d_copy),
        ))
        self.wait()

        # replace with a single tensor
        t32_merged_2d = LayersFake(
            n=1,
            ref=t32_combined,
            expanded=True,
            width_nominal=7,
            height_nominal=400,
        ).move_to(t32_combined)
        self.play(AnimationGroup(
            FadeOut(t32_combined),
            FadeIn(t32_merged_2d),       # or simply add?
        ))
        self.wait()

        # show shape of the just merged
        marrow_out_tview.save_state()
        self.play(AnimationGroup(
            marrow_out_tview.animate.fade(0.8),
            ShowShape(t32_merged_2d, text_config=SMALL_SHAPE_TEXT_CONFIG),
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(AnimationGroup(
            HideShape(t32_merged_2d),
            marrow_out_tview.animate.restore(),
            lag_ratio=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'intuition view, create merge system',
            skip_animations=False,
        )
        # ************************************************************

        # use new marrow instead of copy
        marrow_out_iview = MultiArrow(
            one_to_many=False,
            p1=s32_xyxy_2d.get_right()+RIGHT*.2,
            p2=s32_prob_2d.get_right()+RIGHT*.2,
            ratio_input=0.1,
            ratio_brace=0.4,
            ratio_output=0.1,
        )
        self.play(Write(marrow_out_iview))
        self.wait()

        # system_merged as a copy of system_xyxy_2d
        s32_merged_2d = s32_xyxy_2d.copy()
        self.play(FadeIn(s32_merged_2d, run_time=0.3))
        self.play((
            s32_merged_2d
            .animate(run_time=1.0)
            .scale(MERGED_SCALE_FACTOR)
            .next_to(marrow_out_iview, RIGHT, buff=0.26)
        ))
        self.wait()

        # generate fake labels for each bbox
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
        mobs = Group(
            s32_dist, acb_ab, s32_xyxy, acb_bc, s32_xyxy_2d, marrow_out_iview, s32_merged_2d,
            s32_prob, acc_ab, s32_prob_2d,
            marrow_in_tview,
            t32_dist, acb_12, t32_xyxy, acb_23, t32_xyxy_2d, marrow_out_tview, t32_merged_2d,
            t32_prob, acc_12, t32_prob_2d,
        )
        export_mobs(__file__, mobs)
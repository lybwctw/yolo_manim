from manim import *

from utils.constants import *
from utils.general import load_everything
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.image_pad import ImagePad

FAST_RT = 0.1

CONF_THRESH = 0.7
IOU_THRESH = 0.05

# TODO: multi-label option
# TODO: nms-ignore option
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'start with xyxyccc format',
            skip_animations=True,
        )
        # ************************************************************
        # FIXME: use background from 017 for better continuity
        background = ImagePad(padded=True).scale(1.0).set_opacity(0.2)
        # FIXME: use random 10x10 for now
        explainer = Explainer.from_file(
            background=background,
            version='mini',
            sf_nominal=64,
        )
        system = Group(background, explainer)
        self.add(system)
        self.wait(FAST_RT)

        self.play(explainer.show_anchor_points(
            run_time=FAST_RT,
        ))
        self.wait(FAST_RT)

        self.play(explainer.to_rects(
            gargs={'run_time': FAST_RT},
        ))
        self.wait(FAST_RT)

        self.play(explainer.show_multi_labels(
            label_config={'font_size': 8},
            gargs={'run_time': FAST_RT},
        ))
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply take max',
            skip_animations=True,
        )
        # ************************************************************
        explainer.apply_max_select(
            scene=self,
            run_time_ratio=FAST_RT,
        )
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply conf filter',
            skip_animations=True,
        )
        # ************************************************************
        explainer.apply_conf_filter(
            self,
            conf_thresh=CONF_THRESH,
            run_time_ratio=1.0,
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'apply class split',
            skip_animations=True,
        )
        # ************************************************************
        # nothing for now

        # ************************************************************
        self.next_section(
            'sort each class',
            skip_animations=True,
        )
        # ************************************************************
        # nothing for now

        # ************************************************************
        self.next_section(
            'NMS each class',
            skip_animations=False,
        )
        # ************************************************************
        # change perspective
        BG_GAP = 3.0
        self.move_camera(
            phi=45*DEGREES,
            theta=-180*DEGREES,
            gamma=-90*DEGREES,
            run_time=0.5,
            added_anims=[
                system.animate.shift(IN*BG_GAP),
            ],
        )
        self.wait(0.5)

        # show background for kept predictions
        target_bg = Rectangle(
            width=background.width,
            height=background.height,
            stroke_width=2.6,
            stroke_color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.0,
            # shade_in_3d=True,
        ).move_to(background, aligned_edge=UL)
        self.play(Write(target_bg))
        self.play(target_bg.animate(
            run_time=0.5,
        ).shift(OUT*BG_GAP*2))
        self.wait(0.5)

        # apply NMS for each class
        for cls in range(3):
            explainer.apply_nms_filter(
                self,
                cls=cls,
                iou_thresh=IOU_THRESH,
                offset=BG_GAP*2,
                run_time_ratio=FAST_RT,
            )
            self.wait(0.3)
        
        # back to 2d perspective
        self.play(Unwrite(
            target_bg,
            run_time=0.5,
        ))
        self.move_camera(
            phi=0*DEGREES,
            theta=-90*DEGREES,
            gamma=0*DEGREES,
            run_time=0.5,
            added_anims=[
                system.animate.shift(OUT*BG_GAP),
            ],
        )
        self.wait(0.5)
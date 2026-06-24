from manim import *

from utils.general import import_mobs
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.image_pad import ImagePad
from utils.constants import *

CONF_THRESH = 0.5
IOU_THRESH = 0.05

# TODO: multi-label option
# TODO: nms-ignore option
wt = SHORT_DURATION     # wait time
qt = 0.1                # quick time
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'start with xyxyccc',
            skip_animations=False,
        )
        # ************************************************************
        background = ImagePad(padded=True)
        background.scale(0.9)

        explainer = Explainer.from_file(
            background=background,
            version=80,
            sf_nominal=80,
        )
        # explainer = Explainer.from_random(
        #     background=background,
        #     shape=(10,10),
        #     n_distrib=4,
        #     offsets_range=(0,2),
        #     prob_range=(0,1),
        #     sf_nominal=64,
        #     dot_config={},
        #     rect_config={},
        # )
        system = Group(background, explainer)

        # instroduce background and explainer
        self.add(system)
        self.wait(wt)

        # fade background
        self.play(background.animate(
            run_time=wt,
        ).set_opacity(0.2))
        self.wait(wt)

        # show anchor points
        self.play(explainer.show_anchor_points(
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(wt)

        self.play(explainer.show_rect_labels(
            rect_config={
                'stroke_opacity': 0.5,
                'stroke_color': WHITE,
            },
            include_text=True,
            label_txt_config={},
            label_bg_config={
                'fill_opacity': 0.7,
            },
            aargs={},
            gargs={'lag_ratio': 1.0, 'run_time': 0.5},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply take max',
            skip_animations=False,
        )
        # ************************************************************
        explainer.apply_max_select(
            scene=self,
            run_time_ratio=qt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply conf filter',
            skip_animations=False,
        )
        # ************************************************************
        explainer.apply_conf_filter(
            scene=self,
            conf_thresh=CONF_THRESH,
            run_time_ratio=1.0,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply class split',
            skip_animations=False,
        )
        # ************************************************************
        # nothing for now

        # ************************************************************
        self.next_section(
            'sort each class',
            skip_animations=False,
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
        BG_GAP = 2.5
        self.move_camera(
            phi=45*DEGREES,
            theta=-180*DEGREES,
            gamma=-90*DEGREES,
            run_time=wt,
            added_anims=[
                system.animate.shift(IN*BG_GAP),
            ],
        )
        self.wait(wt)

        # show background for kept predictions
        target_bg = Rectangle(
            width=background.width,
            height=background.height,
            stroke_width=2.6,
            stroke_color=WHITE,
            fill_color=BLACK,
            fill_opacity=0.0,
            # shade_in_3d=True,
        ).move_to(
            background,
            aligned_edge=UL,
        )
        self.play(Write(
            target_bg,
            run_time=wt,
        ))
        self.play(target_bg.animate(
            run_time=wt,
        ).shift(OUT*BG_GAP*2))
        self.wait(wt)

        # apply NMS for each class
        for cls in range(3):    # FIXME
            explainer.apply_nms_filter(
                self,
                cls=cls,
                iou_thresh=IOU_THRESH,
                offset=BG_GAP*2,
                run_time_ratio=qt,
            )
            self.wait(wt)
        
        # back to 2d perspective
        self.play(Unwrite(
            target_bg,
            run_time=wt,
        ))
        self.move_camera(
            phi=0*DEGREES,
            theta=-90*DEGREES,
            gamma=0*DEGREES,
            run_time=wt,
            added_anims=[
                system.animate.shift(OUT*BG_GAP),
            ],
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply scale back steps',
            skip_animations=False,
        )
        # ************************************************************
        # shrink -> scale -> clip
        explainer.apply_scale_back(
            scene=self,
            scale_factor=1.2,
            run_time_ratio=1.0,
        )
        self.wait(wt)

        # TODO: insert class name before conf?
from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.image_pad import ImagePad
from utils.value_2d import Value2D

TENSOR_GAP = 3.5

CONF_THRESH = 0.5
IOU_THRESH = 0.05

# TODO: multi-label option
# TODO: nms-ignore option
wt = SHORT_DURATION     # wait time
qt = 0.1                # quick time
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'start with xyxyccc',
            skip_animations=True,
        )
        # ************************************************************
        background = ImagePad(padded=True)
        background.scale(0.9)

        explainer = Explainer.from_file(
            background=background,
            version=80,
            sf_nominal=80,
        )

        tensor_raw = Value2D.from_ref(
            ref=explainer,
            decimal_config={
                'font': 'JetBrains Mono',
                'font_size': 8,
            },
            cell_width=0.42,
            cell_height=0.11,
        )

        self.wait()
        self.play(Write(
            tensor_raw,
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply take max',
            skip_animations=True,
        )
        # ************************************************************
        tensor_cmax = tensor_raw.into_take_max(
            scene=self,
            offset=RIGHT*TENSOR_GAP,
            run_time_ratio=qt*5,
        )
        self.wait(wt)

        # replace the old with new
        self.play(Uncreate(
            tensor_raw,
            run_time=wt,
        ))
        self.play(tensor_cmax.animate(
            run_time=wt,
        ).set_x(0.0))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply conf filter',
            skip_animations=True,
        )
        # ************************************************************
        tensor_conf = tensor_cmax.into_filter_conf(
            scene=self,
            conf_thresh=CONF_THRESH,
            offset=RIGHT*TENSOR_GAP,
            run_time_ratio=qt*5,
        )
        self.wait(wt)

        # replace the old with new
        self.play(Uncreate(
            tensor_cmax,
            run_time=wt,
        ))
        self.play(tensor_conf.animate(
            run_time=wt,
        ).set_x(0.0))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'apply class split',
            skip_animations=True,
        )
        # ************************************************************
        tensors_split = tensor_conf.into_splitted(
            scene=self,
            offset=RIGHT*TENSOR_GAP,
            buff=0.3,
            run_time_ratio=qt*5,
        )
        self.wait(wt)

        # TODO: make sure all classes survived?

        # replace the old with multiple news
        self.play(Uncreate(
            tensor_conf,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(t.animate.set_x(0.0) for t in tensors_split),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'sort each class',
            skip_animations=True,
        )
        # ************************************************************
        tensors_sort = []
        for tensor in tensors_split:
            tensor_sorted = tensor.into_sort(
                scene=self,
                offset=RIGHT*TENSOR_GAP,
                run_time_ratio=qt,
            )
            tensors_sort.append(tensor_sorted)
            self.wait(wt)
        self.wait(wt)
        
        # replace the multiple olds with multiple news
        self.play(AnimationGroup(
            *(Uncreate(t, lag_ratio=0.0) for t in tensors_split),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(t.animate.set_x(0.0) for t in tensors_sort),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'NMS each class',
            skip_animations=True,
        )
        # ************************************************************
        self.wait(1.0)
        tensors_nms = []
        for t in tensors_sort:
            t_nms = t.into_filter_nms(
                scene=self,
                iou_thresh=IOU_THRESH,
                offset=RIGHT*TENSOR_GAP,
                run_time_ratio=qt*0.85,     # faster
            )
            tensors_nms.append(t_nms)
            self.wait(0.5)
        
        # replace the multiple olds with multiple news
        self.play(AnimationGroup(
            *(Uncreate(t, lag_ratio=0.0) for t in tensors_sort),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(t.animate.set_x(0.0) for t in tensors_nms),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # ************************************************************
        self.next_section(
            'concat nms result into a single one',
            skip_animations=False,
        )
        # ************************************************************
        tensor_nms = Value2D.from_tensors(
            tensor_list=tensors_nms,
        )
        self.play(ApplyMethod(
            tensor_nms.arrange_matrix,
            ORIGIN,     # NOTE: use screen center as new center
            rate_func=rate_functions.ease_out_back,
            run_time=wt,
        ))
        self.wait(wt)

        # FIXME: temp export for convenience
        export_mobs(__file__, tensor_nms)

        # # ************************************************************
        # self.next_section(
        #     'apply scale back steps',
        #     skip_animations=False,
        # )
        # # shrink -> scale -> clip
        # # ************************************************************
        # # scale up tensor a bit
        # self.wait(wt)
        # self.play(tensor_nms.animate.scale(1.5))
        # self.wait(wt)
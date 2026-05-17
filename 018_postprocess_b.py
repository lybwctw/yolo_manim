from manim import *

from utils.constants import *
from utils.general import load_everything
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.explainer import Explainer
from utils.show_shape import ShowShape, HideShape
from utils.image_pad import ImagePad
from utils.tensor_2d import Tensor2D

TENSOR_GAP = 3
FAST_RT = 0.1

CONF_THRESH = 0.7
IOU_THRESH = 0.2

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'start with xyxyccc format',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME: use background from 017 for better continuity
        background = ImagePad(padded=True).scale(1.0).set_opacity(0.2)
        # FIXME: use random 10x10 for now
        explainer = Explainer.from_file(
            background=background,
            version='mini',
            sf_nominal=64,
        )   # for reference

        # tensor starts with xyxyccc
        tensor_raw = Tensor2D.from_ref(
            ref=explainer,
            decimal_config={
                'font': 'JetBrains Mono',
                'font_size': 6,
            },
            cell_width=0.25,
            cell_height=0.07,
        )
        self.play(Write(
            tensor_raw,
            lag_ratio=0.3,
            run_time=FAST_RT,
        ))
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply take max',
            skip_animations=False,
        )
        # ************************************************************
        tensor_cmax = tensor_raw.into_take_max(
            scene=self,
            offset=RIGHT*TENSOR_GAP,
            run_time_ratio=FAST_RT,
        )
        self.wait(FAST_RT)

        # replace the old with new
        self.play(Uncreate(
            tensor_raw,
            run_time=FAST_RT,
        ))
        self.play(tensor_cmax.animate(
            run_time=FAST_RT,
        ).shift(LEFT*TENSOR_GAP))
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply conf filter',
            skip_animations=False,
        )
        # ************************************************************
        tensor_conf = tensor_cmax.into_filter_conf(
            scene=self,
            conf_thresh=CONF_THRESH,
            offset=RIGHT*TENSOR_GAP,
            run_time_ratio=FAST_RT,
        )
        self.wait(FAST_RT)

        # replace the old with new
        self.play(Uncreate(
            tensor_cmax,
            run_time=FAST_RT,
        ))
        self.play(tensor_conf.animate(
            run_time=FAST_RT,
        ).shift(LEFT*TENSOR_GAP).scale(1.5))
        self.wait(FAST_RT)

        # ************************************************************
        self.next_section(
            'apply class split',
            skip_animations=False,
        )
        # ************************************************************
        tensors_split = tensor_conf.into_splitted(
            scene=self,
            offset=RIGHT*TENSOR_GAP,
            buff=0.3,
            run_time_ratio=FAST_RT,
        )
        tensors_split = VGroup(*tensors_split)
        self.wait(FAST_RT)

        # TODO: make sure all classes survived?

        # replace the old with multiple news
        self.play(Uncreate(
            tensor_conf,
            run_time=FAST_RT,
        ))
        self.play(tensors_split.animate(
            run_time=FAST_RT,
        ).shift(LEFT*TENSOR_GAP))
        self.wait(1.0)

        # ************************************************************
        self.next_section(
            'sort each class',
            skip_animations=False,
        )
        # ************************************************************
        tensors_sort = []
        for t in tensors_split:
            t_s = t.into_sort(
                scene=self,
                offset=RIGHT*TENSOR_GAP,
                run_time_ratio=1.0,
            )
            tensors_sort.append(t_s)
            self.wait(0.5)
        self.wait()
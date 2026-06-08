import sys
sys.path.append('..')

from manim import *
import numpy as np

from utils.show_shape import ShowShape
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.ylabel import YLabel
from utils.constants import *

DEFAULT_LABEL_TXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 12,
    'color': WHITE,
}
DEFAULT_LABEL_BG_CONFIG = {
    'stroke_color': GRAY,       # overridden
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'fill_color': GRAY,         # overridden
    'fill_opacity': 1.0,
}
DEFAULT_BOX_CONFIG = {
    'width': 2.0,
    'height': 1.0,
    'stroke_color': GRAY,       # overridden
    'stroke_width': 2,
    'stroke_opacity': 1.0,
    'fill_color': BLACK,        # overridden
    'fill_opacity': 0.0,
}

class SingleAnnotation(VMobject):
    """
    Example
    -------
    from manim import *
    class Demo(Scene):
        def construct(self):
            sano = SingleAnnotation(text='test')
            self.add(sano)
            self.wait()
    """
    def __init__(
        self,
        text: str = 'None',
        label_txt_config: dict = {},
        label_bg_config: dict = {},
        box_config: dict = {},
    ):
        super().__init__()
        self.text = text

        label_txt_config = {**DEFAULT_LABEL_TXT_CONFIG, **label_txt_config}
        label_bg_config = {**DEFAULT_LABEL_BG_CONFIG, **label_bg_config}
        box_config = {**DEFAULT_BOX_CONFIG, **box_config}

        box = Rectangle(
            **box_config,
        )
        label = YLabel(
            text=text,
            label_txt_config=label_txt_config,
            label_bg_config=label_bg_config,
        ).move_to(
            box.get_corner(UL),
            aligned_edge=DL,
        )

        self.box = box
        self.label = label
        self.add(self.box, self.label)


class YoloAnnotation(VMobject):
    """
    Example
    -------
    from manim import *
    from utils.image_raw import ImageRaw

    class Demo(Scene):
        def construct(self):
            background = ImageRaw()
            self.add(background)
            self.wait()
            annotation = YoloAnnotation(
                background=background,
            )
            self.play(Write(annotation))
            self.wait()
    """
    def __init__(
        self,
        background: ImageRaw | ImagePad | None = None,
        annotation: str | np.ndarray = PATH_LABEL,
        label_txt_config: dict = {},
        label_bg_config: dict = {},
        box_config: dict = {},
        name_map: dict = KK_NAME_MAP,
        color_map: dict = KK_COLOR_MAP,
    ):
        super().__init__()

        self.name_map = name_map    # idx -> name
        self.color_map = color_map  # idx -> color

        # background as reference
        self.background = background

        # setup raw data
        if isinstance(annotation, str):
            self.data = np.loadtxt(annotation).astype(np.float32)
        else:
            self.data = annotation

        _cls = self.data[:, 0].astype(np.int32).tolist()
        _xywh = self.data[:, 1:5].astype(np.float32).tolist()
        _width = self.background.width
        _height = self.background.height
        _origin = self.background.get_corner(UL)

        # setup annotation mobs
        mobs = VGroup()
        for cls, xywh in zip(_cls, _xywh):
            cx, cy, w, h = xywh
            cls_name = self.name_map[cls]
            cls_color = self.color_map[cls]

            label_txt_config = {
                **DEFAULT_LABEL_TXT_CONFIG,
                **label_txt_config,
            }
            label_bg_config = {
                **DEFAULT_LABEL_BG_CONFIG,
                **label_bg_config,
                'stroke_color': cls_color,
                'fill_color': cls_color,
            }
            box_config = {
                **DEFAULT_BOX_CONFIG,
                'width': self.background.width * w,
                'height': self.background.height * h,
                'fill_color': cls_color,
                'stroke_color': cls_color,
            }

            sano = SingleAnnotation(
                text=cls_name,
                label_txt_config=label_txt_config,
                label_bg_config=label_bg_config,
                box_config=box_config,
            )

            _center = _origin + _width*cx*RIGHT + _height*cy*DOWN
            _offset = _center - sano.box.get_center()
            sano.shift(_offset)
            mobs.add(sano)
        self.mobs = mobs

        # self.add(self.background)
        self.add(self.mobs)

#     @property
#     def xywh_abs(self):
#         """
#         Example
#         -------
#         annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
#         value = annotation.xywh_abs
#         """
#         scale = np.array([
#             self.background.width_nominal,
#             self.background.height_nominal,
#             self.background.width_nominal,
#             self.background.height_nominal,
#         ])
#         return self.xywh * scale

#     @property
#     def xyxy(self):
#         """
#         Example
#         -------
#         annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
#         value = annotation.xyxy
#         """
#         cx, cy, w, h = self.xywh.T
#         x1 = cx - w / 2
#         y1 = cy - h / 2
#         x2 = cx + w / 2
#         y2 = cy + h / 2
#         return np.stack([x1, y1, x2, y2], axis=1)

#     @property
#     def xyxy_abs(self):
#         """
#         Example
#         -------
#         annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
#         value = annotation.xyxy_abs
#         """
#         cx, cy, w, h = self.xywh.T
#         x1 = (cx - w / 2) * self.background.width_nominal
#         y1 = (cy - h / 2) * self.background.height_nominal
#         x2 = (cx + w / 2) * self.background.width_nominal
#         y2 = (cy + h / 2) * self.background.height_nominal

#         return np.stack([x1, y1, x2, y2], axis=1)

class Demo(Scene):
    def construct(self):
        background = ImageRaw()
        self.add(background)
        self.wait()
        annotation = YoloAnnotation(
            background=background,
        )
        self.play(Write(annotation))
        self.wait()

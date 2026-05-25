"""Usage
-----
Example inside a scene outside ``utils/``::

    from utils.image_pad import ImagePad
    from utils.yolo_annotation import YoloAnnotation

    background = ImagePad(path='../assets/images/sample_640_360.jpg', padded=False)
    annotation = YoloAnnotation(background=background, annotation='../assets/images/labels.txt')
    anno_with_bg = Group(background, annotation)
    self.add(background)
    self.play(Write(annotation))
    self.play(anno_with_bg.animate.scale(1.5).shift(LEFT*2))
    self.play(annotation.show_passing_flash())
"""

import sys
sys.path.append('..')

from manim import *
import numpy as np

from utils.show_shape import ShowShape
from utils.image_raw import ImageRaw
from utils.image_pad import ImagePad
from utils.constants import *

ANNO_BBOX_CONFIG = {
    'stroke_width': 3,
    'stroke_color': GRAY,
    'fill_color': GRAY,
    'fill_opacity': 0.1,
}

ANNO_LABEL_CONFIG = {
    'font_size': 20,
    'color': WHITE,
    'font': 'JetBrains Mono',
}

ANNO_LABEL_BG_CONFIG = {
    'color': GRAY,
    'opacity': 1.0,
    'buff': 0.03,
    'stroke_width': 3,
    # 'stroke_color': GRAY,
    'stroke_opacity': 1.0,
}

def bg_get_point(bg, cx, cy):
    # cx, cy in normalized [0,1]
    base = bg.get_corner(UL)
    point = base + bg.width*cx*RIGHT + bg.height*cy*DOWN
    return point

class SingleAnnotation(VMobject):
    def __init__(
        self,
        text: str = 'test',
        label_config: dict = {},
        label_bg_config: dict = {},
        bbox_config: dict = {},     # width, height
    ):
        """
        Example
        -------
        annotation = SingleAnnotation({"bbox": [0, 0, 1, 1], "cls": 0})
        """
        super().__init__()
        self.text = text
        self.label_config = {**ANNO_LABEL_CONFIG, **label_config}
        self.label_bg_config = {**ANNO_LABEL_BG_CONFIG, **label_bg_config}
        self.bbox_config = {**ANNO_BBOX_CONFIG, **bbox_config}

        bbox = Rectangle(
            **self.bbox_config,
        )

        label = Text(
            text=self.text,
            **self.label_config,
        ).add_background_rectangle(
            **self.label_bg_config,
        ).move_to(
            bbox.get_corner(UL),
            aligned_edge=DL,
        )

        # BackgroundRectangle Fix, Write/Create animtion issue
        new_bg = Rectangle(
            stroke_width=0,
            width=label.background_rectangle.width,
            height=label.background_rectangle.height,
        ).set_style(
            **label.background_rectangle.get_style(simple=True),
        ).move_to(label.background_rectangle)
        label.remove(label.background_rectangle)
        label.background_rectangle = new_bg
        label.add_to_back(label.background_rectangle)

        self.bbox = bbox
        self.label = label
        self.add(self.bbox, self.label)


class YoloAnnotation(VMobject):
    def __init__(
        self,
        background: str | ImageRaw | ImagePad | None = None,
        annotation: str | np.ndarray = PATH_LABEL,
        name_map: dict = KK_NAME_MAP,
        color_map: dict = KK_COLOR_MAP,
    ):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        """
        super().__init__()

        if isinstance(background, (str, type(None))):
            background = ImageRaw(background or PATH_IMAGE_640)

        self.background = background
        self.name_map = name_map
        self.color_map = color_map

        if isinstance(annotation, str):
            self.data = np.loadtxt(annotation).astype(np.float32)
        else:
            self.data = annotation

        # setup annotation as a vgroup of mobs
        annotation = VGroup()
        for cls, xywh in zip(self.cls.tolist(), self.xywh.tolist()):
            cx, cy, w, h = xywh
            name = self.name_map[cls]
            color = self.color_map[cls]

            label_config = {
                'font_size': 10,
            }
            label_bg_config = {
                'color': color,
            }
            bbox_config = {
                'width': self.background.width * w,
                'height': self.background.height * h,
                'fill_color': color,
                'stroke_color': color,
            }

            anno = SingleAnnotation(
                text=name,
                label_config=label_config,
                label_bg_config=label_bg_config,
                bbox_config=bbox_config,
            )
            anno.shift(
                bg_get_point(self.background,cx,cy) - anno.bbox.get_center()
            )
            annotation.add(anno)
        self.annotation = annotation

        # store reference to background without add
        # self.add(self.background)
        self.add(self.annotation)

    def show_passing_flash(
        self,
    ):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        self.play(annotation.show_passing_flash())
        """
        return self.background.show_passing_flash()

    def unwrite_shape_texts(
        self,
    ):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        result = annotation.unwrite_shape_texts()
        """
        return self.background.unwrite_shape_texts()

    def hide_text(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        self.play(annotation.hide_text())
        """
        pass

    def unhide_text(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        result = annotation.unhide_text()
        """
        pass

    @property
    def labels(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.labels
        """
        res = VGroup()
        for anno in self.annotation:
            res.add(anno.label)
        return res

    @property
    def bboxes(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.bboxes
        """
        res = VGroup()
        for anno in self.annotation:
            res.add(anno.bbox)
        return res

    @property
    def cls(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.cls
        """
        return self.data[:, 0].astype(np.int32)

    @property
    def xywh(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.xywh
        """
        return self.data[:, 1:5]

    @property
    def xywh_abs(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.xywh_abs
        """
        scale = np.array([
            self.background.width_nominal,
            self.background.height_nominal,
            self.background.width_nominal,
            self.background.height_nominal,
        ])
        return self.xywh * scale

    @property
    def xyxy(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.xyxy
        """
        cx, cy, w, h = self.xywh.T
        x1 = cx - w / 2
        y1 = cy - h / 2
        x2 = cx + w / 2
        y2 = cy + h / 2
        return np.stack([x1, y1, x2, y2], axis=1)

    @property
    def xyxy_abs(self):
        """
        Example
        -------
        annotation = YoloAnnotation(background=background, annotation="assets/images/labels.txt")
        value = annotation.xyxy_abs
        """
        cx, cy, w, h = self.xywh.T
        x1 = (cx - w / 2) * self.background.width_nominal
        y1 = (cy - h / 2) * self.background.height_nominal
        x2 = (cx + w / 2) * self.background.width_nominal
        y2 = (cy + h / 2) * self.background.height_nominal

        return np.stack([x1, y1, x2, y2], axis=1)


# FIXME: copy of ImageRepad, expediency
class AnnotationRepad(Mobject, ShowShape):
    def __init__(
        self,
        annotation,
        padded=False,
    ):
        """
        Example
        -------
        annotation_repad = AnnotationRepad(annotation)
        """
        super().__init__()
        self.scale_factor = 1.0
        self.annotation = annotation    # ImageAnnotation
        self._w = annotation._w
        self._h = annotation._h
        self.padded = padded
        self.natural_pad = False  # natural means w>h

        if self.padded:
            width, height = self.annotation.width, self.annotation.height
            if self._w > self._h:
                self.natural_pad = True
                t_width, t_height = width, (width - height) / 2
                p1 = Rectangle(
                    width=t_width,
                    height=t_height,
                    stroke_width=0,
                    fill_color=GRAY,  # FIXME, using exact 114,114,114
                    fill_opacity=0.2,
                ).next_to(self.annotation, DOWN, buff=0)
                p2 = p1.copy().next_to(self.annotation, UP, buff=0)
            else:
                self.natural_pad = False
                t_width, t_height = (height - width) / 2, height
                p1 = Rectangle(
                    width=t_width,
                    height=t_height,
                    stroke_width=0,
                    fill_color=GRAY,  # FIXME, using exact 114,114,114
                    fill_opacity=0.2,
                ).next_to(self.annotation, LEFT, buff=0)
                p2 = p1.copy().next_to(self.annotation, RIGHT, buff=0)
            self.paddings = VGroup(p1, p2)
            self.add(self.paddings)
        else:
            self.paddings = None

        self.add(annotation)

    def get_shape_path(self):
        """
        Example
        -------
        annotation_repad = AnnotationRepad(annotation)
        result = annotation_repad.get_shape_path()
        """
        path = VMobject()
        if self.natural_pad:
            path.set_points_as_corners([
                self.paddings[0].get_corner(LEFT + DOWN),
                self.paddings[1].get_corner(LEFT + UP),
                self.paddings[1].get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
        else:
            path.set_points_as_corners([
                self.paddings[0].get_corner(LEFT + DOWN),
                self.paddings[0].get_corner(LEFT + UP),
                self.paddings[1].get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
        return path

    def get_shape_text(self):
        """
        Example
        -------
        annotation_repad = AnnotationRepad(annotation)
        result = annotation_repad.get_shape_text()
        """
        if self.natural_pad:
            text_h = Text(str(self._h), font_size=20).next_to(self.annotation, LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.paddings[1], UP)
        else:
            text_h = Text(str(self._h), font_size=20).next_to(self.paddings[0], LEFT)
            text_w = Text(str(self._w), font_size=20).next_to(self.annotation, UP)
        text = VGroup(text_h, text_w)
        return text

    def show_paddings(self):
        """
        Example
        -------
        annotation_repad = AnnotationRepad(annotation)
        self.play(annotation_repad.show_paddings())
        """
        if self.padded:
            return None

        width, height = self.annotation.width, self.annotation.height
        if self._w > self._h:
            self.natural_pad = True
            t_width, t_height = width, (width - height) / 2
            p1 = Rectangle(
                width=t_width,
                height=0,
                stroke_width=0,
                fill_color=GRAY,  # FIXME, using exact 114,114,114
            ).next_to(self.annotation, DOWN, buff=0)
            p2 = p1.copy().next_to(self.annotation, UP, buff=0)
            p1_res = Rectangle(
                width=t_width,
                height=t_height,
                stroke_width=0,
                fill_color=GRAY,
                fill_opacity=0.2,       # faded annotation as annotation
            ).next_to(p1, DOWN, buff=0)
            p2_res = p1_res.copy().next_to(p2, UP, buff=0)

            self.paddings = VGroup(p1, p2)
            self.add(self.paddings)
            self.padded = True
            self._h = self._w
            return AnimationGroup(
                Transform(p1, p1_res),
                Transform(p2, p2_res),
            )
        else:
            self.natural_pad = False
            t_width, t_height = (height - width) / 2, height
            p1 = Rectangle(
                width=0,
                height=t_height,
                stroke_width=0,
                fill_color=GRAY,  # FIXME, using exact 114,114,114
            ).next_to(self.annotation, LEFT, buff=0)
            p2 = p1.copy().next_to(self.annotation, RIGHT, buff=0)
            p1_res = Rectangle(
                width=t_width,
                height=t_height,
                stroke_width=0,
                fill_color=GRAY,
                fill_opacity=0.2,
            ).next_to(p1, LEFT, buff=0)
            p2_res = p1_res.copy().next_to(p2, RIGHT, buff=0)

            self.paddings = VGroup(p1, p2)
            self.add(self.paddings)
            self.padded = True
            self._w = self._h
            return AnimationGroup(
                Transform(p1, p1_res),
                Transform(p2, p2_res),
            )

class Demo(Scene):
    def construct(self):
        path = '../assets/images/sample_640_360.jpg'
        background = ImagePad(
            path=path,
            padded=False,
        )
        annotation = YoloAnnotation(
            background=background,
            annotation='../assets/images/labels.txt',
        )

        anno_with_bg = Group(background, annotation)

        self.add(background)
        self.wait()
        self.play(Write(annotation))
        self.wait()

        self.play(anno_with_bg.animate.scale(1.5).shift(LEFT*2))
        self.play(annotation.show_passing_flash())
        self.play(annotation.unwrite_shape_texts())
        self.wait()

        self.play(background.show_natural_paddings())
        self.wait()

        self.play(anno_with_bg.animate.shift(RIGHT).scale(0.8))
        self.wait()

        self.play(annotation.show_passing_flash())
        self.wait()

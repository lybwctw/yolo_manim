from manim import *
from utils.show_shape import ShowShape
import numpy as np
from .constants import (
    KK_NAME_MAP,
    KK_COLOR_MAP,
    PATH_IMAGE_640,
    PATH_LABEL_640,
)

class ImageAnnotation(Mobject, ShowShape):
    def __init__(
        self,
        image=None,    # background image object, or path?
        label=None,    # label path
        name_map=None, # class name map
        color_map=None, # class color map
        transparent=False,
        width_nominal=300,
        height_nominal=200,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.scale_factor = 1.0
        self._w = width_nominal
        self._h = height_nominal

        # setup name map if not yet
        if name_map:
            self.name_map = name_map
        else:
            self.name_map = {0: '0', 1: '1', 2: '2'}   # FIXME, if not 3 classes

        # setup color map if not yet
        if color_map:
            self.color_map = color_map
        else:
            self.color_map = {0: RED, 1: GREEN, 2: BLUE}    # FIXME, if not 3 classes

        # setup image object if not yet
        if isinstance(image, ImageMobject):
            self.image = image
        elif isinstance(image, str):
            image = ImageMobject(image)
            image.set_opacity(1.0)
            self.image = image
        else:
            raise ValueError('invalid image arg for ImageAnnotation')
        if transparent:
            self.image.set_opacity(0.3)
        self.add(self.image)

        # setup raw label data if not yet
        # FIXME, rename label naming, confused with labels
        if isinstance(label, np.ndarray):
            self.label = label
        elif isinstance(label, str):
            self.label = np.loadtxt(label)
        else:
            raise ValueError('invalid label arg for ImageAnnotation')

        # setup cls and xywh according to label
        self.cls = self.label[:,0].astype(int).tolist()
        self.xywh = self.label[:, 1:5]

        # setup vmobject for labels
        self.labels = []
        self.mobs = VGroup()
        for _cls, _xywh in zip(self.cls, self.xywh):
            _cls = int(_cls)
            _name = self.name_map[_cls]
            _color = self.color_map[_cls]
            _x, _y, _w, _h = _xywh

            # create text and bbox
            text = Text(
                _name,
                font_size=8,
                color=WHITE,
                font='JetBrains Mono',
            ).add_background_rectangle(
                color=_color,
                opacity=1.0,
                buff=0.03,
                stroke_width=3,
                stroke_color=_color,
                stroke_opacity=1.0,
            )
            bbox = Rectangle(
                stroke_width=3,
                stroke_color=_color,
                fill_color=_color,
                fill_opacity=0.1,
            )

            # move bbox to target position
            ref_tl = self.image.get_corner(UL)
            width = _w * self.image.width
            height = _h * self.image.height
            shift_cx = _x * self.image.width * RIGHT
            shift_cy = _y * self.image.height * DOWN
            (
                bbox
                .stretch_to_fit_width(width)
                .stretch_to_fit_height(height)
                .move_to(ref_tl)
                .shift(shift_cx + shift_cy)
            )

            # align text to bbox
            text.align_to(bbox, LEFT+DOWN).shift(UP * bbox.height)
            # text.add_updater(
            #     lambda m: m.align_to(bbox, LEFT+DOWN).shift(UP * bbox.height)
            # )
            
            # add to labels and mobs
            self.labels.append(
                {
                    'text': text,
                    'bbox': bbox,
                }
            )
            self.mobs.add(text, bbox)
        self.add(self.mobs)

    def hide_text(self):
        anims = []
        for label in self.labels:
            text = label['text']
            anim = text.animate.set_opacity(0.0)
            anims.append(anim)
        return AnimationGroup(*anims)

    def unhide_text(self):
        anims = []
        for label in self.labels:
            text = label['text']
            anim = text.animate.set_opacity(1.0)
            anims.append(anim)
        return AnimationGroup(*anims)

    def get_shape_path(self):
        path = VMobject()
        path.set_points_as_corners([
            self.image.get_corner(LEFT + DOWN),
            self.image.get_corner(LEFT + UP),
            self.image.get_corner(RIGHT + UP),
        ]).set_stroke(color=BLUE)
        return path

    def get_shape_text(self):
        text_h = Text(str(self._h), font_size=20).next_to(self.image, LEFT)
        text_w = Text(str(self._w), font_size=20).next_to(self.image, UP)
        text = VGroup(text_h, text_w)
        return text

    def scale(self, scale_factor, **kwargs):
        self.scale_factor *= scale_factor
        return super().scale(scale_factor, **kwargs)

    def scale_back(self):
        self.scale(1 / self.scale_factor)
        return self

class Demo(Scene):
    def construct(self) -> None:
        anno = ImageAnnotation(
            image=PATH_IMAGE_640,
            label=PATH_LABEL_640,
            name_map=KK_NAME_MAP,
            color_map=KK_COLOR_MAP,
        )
        self.add(anno)
        self.wait()
        self.play(anno.animate.scale(0.8).shift(2*RIGHT))
        self.wait()
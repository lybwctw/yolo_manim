from manim import *
import numpy as np

class ImageAnnotation(Mobject):
    def __init__(
        self,
        image=None,    # background image object, or path?
        label=None,    # label path
        text='???',     # label text
        label_height=0.22,
        label_padding=0.08,
        label_color=LOGO_WHITE,
        label_bg=GRAY_E,
        label_stroke_width=3,
        bbox_stroke_width=3,
        **kwargs,
    ):
        super().__init__(**kwargs)
        # setup image object if not yet
        if isinstance(image, ImageMobject):
            self.image = image
        elif isinstance(image, str):
            self.image = ImageMobject(image)
        else:
            raise ValueError('invalid image arg for ImageAnnotation')
        self.add(self.image)

        # setup raw label data if not yet
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
            _x, _y, _w, _h = _xywh

            # create text and bbox
            text = Text(
                str(_cls),
                font_size=13,
                color=WHITE,
                font='JetBrains Mono',
            ).add_background_rectangle(
                color=GREEN,
                buff=0.1,
            )
            bbox = Rectangle(
                stroke_width=3,
                stroke_color=WHITE,
                fill_color=YELLOW,
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

class Demo(Scene):
    def construct(self) -> None:
        anno = ImageAnnotation(
            image='assets/images/sample_1280_720.jpg',
            label='assets/images/labels.txt',
        )
        self.add(anno)
        self.wait()
        self.play(anno.animate.scale(0.8).shift(2*RIGHT))
        self.wait()
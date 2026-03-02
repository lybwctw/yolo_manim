from manim import *
import numpy as np

class ImageAnnotation(VMobject):
    def __init__(
        self,
        image=None,    # background image object, or path?
        label=None,    # label path
        xywh=None,      # [x, y, w, h]
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
        

        if xywh is None:
            x, y, w, h = 0.5, 0.5, 0.5, 0.5
        else:
            x, y, w, h = [float(t) for t in xywh]
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        
        # get core args for source
        if self.image is None:
            ref_tl = np.array([-config.frame_width / 2, config.frame_height / 2, 0.0])
            width = self.w * config.frame_width
            height = self.h * config.frame_height
            center_x = self.x * config.frame_width * RIGHT
            center_y = self.y * config.frame_height * DOWN
        else:
            ref_tl = self.image.get_corner(UL)
            width = self.w * self.image.width
            height = self.h * self.image.height
            center_x = self.x * self.image.width * RIGHT
            center_y = self.y * self.image.height * DOWN

        # share same stroke color with the label
        self.bbox = Rectangle(
            stroke_width=bbox_stroke_width,
            stroke_color=label_bg,
            fill_color=label_bg,
            fill_opacity=0.2,
        )
        
        (
            self.bbox
            .stretch_to_fit_width(width)
            .stretch_to_fit_height(height)
            .move_to(ref_tl)
            .shift(center_x + center_y)
        )

        self.text = Text(
            text,
            font_size=13,
            color=label_color,
            font='JetBrains Mono'
        )

        self.label_bg = Rectangle(
            height=label_height,
            width=self.text.width + 2 * label_padding,
            fill_color=label_bg,
            fill_opacity=1.0,
            stroke_width=label_stroke_width,
            stroke_color=label_bg,
        )
        self.text.move_to(self.label_bg)
        self.label = VGroup(self.label_bg, self.text)

        # always align label to bbox
        self.label.align_to(self.bbox, LEFT + DOWN).shift(UP * self.bbox.height)
        self.label.add_updater(
            lambda m: m.align_to(self.bbox, LEFT + DOWN).shift(UP * self.bbox.height)
        )

        self.add(self.bbox, self.label)

class Demo(Scene):
    def construct(self) -> None:
        class_map = {0: 'kunkun', 1: 'coke', 2: 'pepsi'}
        color_map = {0: YELLOW, 1: PURE_RED, 2: PURE_BLUE}
        image_path = r'assets\images\sample_1280_720.jpg'
        label_path = r'assets\images\labels.txt'

        sq = ImageMobject(image_path)
        data = np.loadtxt(label_path)
        cls = data[:,0].astype(int).tolist()
        xywh = data[:, 1:5]
        annos = VGroup(
            SingleAnnotation(
                source=sq,
                xywh=t,
                text=class_map[c],
                label_bg=color_map[c],
                label_color=BLACK,
            ) for c, t in zip(cls, xywh)
        )

        self.add(sq, annos)
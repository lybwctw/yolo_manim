from manim import *

class YoloAnnotation(VGroup):
    def __init__(
        self,
        source=None,
        xywh=None,
        text='NULL',
        label_height=0.22,
        label_padding=0.08,
        label_color=LOGO_WHITE,
        label_bg=GRAY_E,
        label_stroke_width=3,
        bbox_stroke_width=3,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.source = source
        if xywh is None:
            x, y, w, h = 0.5, 0.5, 0.5, 0.5
        else:
            x, y, w, h = [float(t) for t in xywh]
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # share same stroke color with the label
        self.bbox = Rectangle(
            stroke_width=bbox_stroke_width,
            stroke_color=label_bg,
            fill_color=label_bg,
            fill_opacity=0.2,
        )

        def align_to_source(mob):
            if self.source is None:
                ref_tl = np.array([-config.frame_width/2, config.frame_height/2, 0.0])
                width = self.w * config.frame_width
                height = self.h * config.frame_height
                center_x = self.x * config.frame_width * RIGHT
                center_y = self.y * config.frame_height * DOWN
            else:
                ref_tl = self.source.get_corner(UL)
                width = self.w * self.source.width
                height = self.h * self.source.height
                center_x = self.x * self.source.width * RIGHT
                center_y = self.y * self.source.height * DOWN
            (
                mob
                .stretch_to_fit_width(width)
                .stretch_to_fit_height(height)
                .move_to(ref_tl)
                .shift(center_x + center_y)
            )
        align_to_source(self.bbox)

        # --- Label text ---
        self.text = Text(
            text,
            font_size=13,
            color=label_color,
            font='JetBrains Mono'
        )

        # --- Label background ---
        self.label_bg = Rectangle(
            height=label_height,
            width=self.text.width + 2 * label_padding,
            fill_color=label_bg,
            fill_opacity=1.0,
            stroke_width=label_stroke_width,
            stroke_color=label_bg,
        )

        # Center text inside label
        self.text.move_to(self.label_bg)

        self.label = VGroup(self.label_bg, self.text)

        # always align label to bbox
        self.label.align_to(self.bbox, LEFT + DOWN).shift(UP * self.bbox.height)
        self.label.add_updater(
            lambda m: m.align_to(self.bbox, LEFT+DOWN).shift(UP * self.bbox.height)
        )

        self.add(self.bbox, self.label)
        # self.bbox.add_updater(align_to_source)

class Demo(Scene):
    def construct(self):
        sq = Square()
        self.add(sq)
        self.wait()
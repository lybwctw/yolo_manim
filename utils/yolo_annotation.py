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
        class_map = {0: 'kunkun', 1: 'coke', 2: 'pepsi'}
        color_map = {0: YELLOW, 1: PURE_RED, 2: PURE_BLUE}
        image_path = r'D:\deeplearning\ultralytics-8.3.163\runs\detect\predict25\005_frames\005_1.jpg'
        label_path = r'D:\deeplearning\ultralytics-8.3.163\runs\detect\predict25\labels\005_1.txt'

        sq = ImageMobject(image_path)
        data = np.loadtxt(label_path)
        cls = data[:,0].astype(int).tolist()
        xywh = data[:, 1:5]
        annos = VGroup(
            YoloAnnotation(
                source=sq,
                xywh=t,
                text=class_map[c],
                label_bg=color_map[c],
                label_color=BLACK,
            ) for c, t in zip(cls, xywh)
        )

        self.add(sq, annos)
        self.play(sq.animate.shift(RIGHT*2))
        annos.suspend_updating(recursive=True)
        self.wait()
        self.play(sq.animate.shift(LEFT*2))
        self.wait()

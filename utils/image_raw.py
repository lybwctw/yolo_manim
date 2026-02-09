from manim import *

class ImageRaw(VGroup):
    def __init__(
        self,
        path,
        width_nominal=None,
        height_nominal=None,
    ):
        super().__init__()
        self.w = width_nominal if width_nominal else 640
        self.h = height_nominal if height_nominal else 360
        rect = Rectangle(
            fill_color=GREEN_E,
            fill_opacity=0.8,
            stroke_width=0.0,
        )
        rect.stretch_to_fit_width(3.2)
        rect.stretch_to_fit_height(1.8)
        self.rect = rect
        self.add(self.rect)
        self.shape_texts = VGroup()

    def show_passing_flash(self):
        path = VMobject()
        path.set_points_as_corners([
            self.get_corner(LEFT+DOWN),
            self.get_corner(LEFT+UP),
            self.get_corner(RIGHT+UP),
        ]).set_stroke(color=BLUE)
        text_h = Text(str(self.h),font_size=20).next_to(self,LEFT)
        text_w = Text(str(self.w),font_size=20).next_to(self,UP)
        self.shape_texts = VGroup(text_h, text_w)
        anim = AnimationGroup(
            ShowPassingFlash(
                path,
                run_time=2.,
                time_width=2.,
            ),
            AnimationGroup(
                *(Write(text) for text in self.shape_texts),
                lag_ratio=0.8,
            )
        )

        return anim

    def unwrite_shape_texts(self):
        anim = AnimationGroup(
            *(Unwrite(text) for text in self.shape_texts),
            lag_ratio=0.3,
        )
        return anim

class ImagePad(VGroup):
    def __init__(self, image_raw, wh=640):
        super().__init__()
        self.image_raw = image_raw
        self.add(image_raw)
        pad_updown = image_raw.w > image_raw.h
        self.pad_updown = pad_updown
        self.pad1 = VMobject()
        self.pad2 = VMobject()
        if pad_updown:
            _height = (image_raw.width - image_raw.height) / 2
            pad1 = Rectangle(
                height=_height,
                width=image_raw.width,
                fill_color=GRAY,
                fill_opacity=1.0,
                stroke_width=0,
            ).next_to(image_raw, UP, buff=0.)
            pad2 = pad1.copy().next_to(image_raw, DOWN, buff=0.)
        else:
            _width = (image_raw.height - image_raw.width) / 2
            pad1 = Rectangle(
                width=_width,
                height=image_raw.height,
                fill_color=GRAY,
                fill_opacity=1.0,
                stroke_width=0,
            ).next_to(image_raw, LEFT, buff=0.)
            pad2 = pad1.copy().next_to(image_raw, RIGHT, buff=0.)
        self.w = self.h = wh
        # self.add(pad1, pad2)
        self.pad1 = pad1
        self.pad2 = pad2

    def show_padding(self):
        anims = AnimationGroup(
            Write(self.pad1),
            Write(self.pad2),
        )
        # self.add(self.pad1, self.pad2)
        return anims

    def show_passing_flash(self):
        path = VMobject()
        if self.pad_updown:
            path.set_points_as_corners([
                self.pad2.get_corner(LEFT+DOWN),
                self.pad1.get_corner(LEFT+UP),
                self.pad1.get_corner(RIGHT+UP),
            ]).set_stroke(color=BLUE)
            text_h = Text(str(self.h), font_size=20).next_to(self.image_raw, LEFT)
            text_w = Text(str(self.w), font_size=20).next_to(self.pad1, UP)
        else:
            path.set_points_as_corners([
                self.pad1.get_corner(LEFT + DOWN),
                self.pad1.get_corner(LEFT + UP),
                self.pad2.get_corner(RIGHT + UP),
            ]).set_stroke(color=BLUE)
            text_h = Text(str(self.h), font_size=20).next_to(self.pad1, LEFT)
            text_w = Text(str(self.w), font_size=20).next_to(self.image_raw, UP)

        self.shape_texts = VGroup(text_h, text_w)
        anim = AnimationGroup(
            ShowPassingFlash(
                path,
                run_time=2.,
                time_width=2.,
            ),
            AnimationGroup(
                *(Write(text) for text in self.shape_texts),
                lag_ratio=0.8,
            )
        )

        return anim

    def unwrite_shape_texts(self):
        anim = AnimationGroup(
            *(Unwrite(text) for text in self.shape_texts),
            lag_ratio=0.3,
        )
        return anim

class Demo(Scene):
    def construct(self):
        imgraw = ImageRaw(None)
        imgpad = ImagePad(imgraw)
        self.add(imgpad)
        self.play(imgpad.show_padding())
        self.play(imgpad.show_passing_flash())
        self.wait()
        self.play(imgpad.unwrite_shape_texts())
        self.wait()
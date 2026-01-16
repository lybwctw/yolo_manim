from manim import *
from manim.utils.rate_functions import there_and_back_with_pause

FONT = 'JetBrains Mono'

import cv2
import numpy as np

def resize_and_pad(img, target=640, pad_value=114):
    h, w = img.shape[:2]

    # 1. scale so that max(h, w) == target
    scale = target / max(h, w)
    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # 2. compute padding
    pad_w = target - new_w
    pad_h = target - new_h

    left   = pad_w // 2
    right  = pad_w - left
    top    = pad_h // 2
    bottom = pad_h - top

    padded = cv2.copyMakeBorder(
        resized,
        top, bottom, left, right,
        borderType=cv2.BORDER_CONSTANT,
        value=(pad_value, pad_value, pad_value)
    )

    return padded, scale, (left, top)

class ImageRaw(Mobject):
    def __init__(self, path):
        super().__init__()
        image = cv2.imread(path)[...,::-1]
        self._setup(image)

    def _setup(self, image):
        self.image = ImageMobject(image)
        self.shape = self.image.get_pixel_array().shape
        self.coords = VGroup()
        self.add(self.image)

    def show_axes(self):
        ax_width, ax_height = self.image.width*1.1, self.image.height*1.1
        self.axes = Axes(
            x_range=[0, ax_width, 1.],
            y_range=[0, ax_height, 1.],
            x_length = ax_width,
            y_length = ax_height,
            axis_config={
                'include_tip': True,
                'include_ticks': False,
                'tip_width': 0.2,
                'tip_height': 0.2,
                'scaling': LinearBase(scale_factor=self.shape[0]/self.image.height),
            },
            ul_origin=True,
        )
        self.axes.shift(self.image.get_corner(UL) - self.axes.get_origin())
        self.add(self.axes)
        return Write(self.axes, lag_ratio=0.)

    def show_shape(self):
        line1 = Line(self.image.get_corner(UL), self.image.get_corner(DL))
        line2 = Line(self.image.get_corner(UL), self.image.get_corner(UR))
        text1 = Text(str(self.shape[0])).scale(0.5).next_to(line1, LEFT)
        text2 = Text(str(self.shape[1])).scale(0.5).next_to(line2, UP)
        return AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(line1, time_width=1.8),
                Write(text1),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                ShowPassingFlash(line2, time_width=1.8),
                Write(text2),
                lag_ratio=0.5,
            ),
        )

    def show_coords(self, x, y):
        # dot -> dashed -> passingflash -> length -> coords
        point = self.axes.c2p(x, y)
        dot = Dot(point).scale(0.5)
        dash1 = self.axes.get_line_from_axis_to_point(0, point)
        dash2 = self.axes.get_line_from_axis_to_point(1, point)
        dash1.invert()
        dash2.invert()
        path1 = Line(self.axes.c2p(x, 0), self.axes.get_origin())
        path2 = Line(self.axes.c2p(0, y), self.axes.get_origin())
        _width = Text(str(x), font=FONT).scale(0.3).next_to(path1, UP)
        _height = Text(str(y), font=FONT).scale(0.3).next_to(path2, LEFT)
        # for later reference
        self._dashes = VGroup(dash1, dash2)
        self._coords = Text('('+str(x)+','+str(y)+')', font=FONT).scale(0.3).next_to(
            self.axes.c2p(x,y), direction=RIGHT,
        )
        self._xy = VGroup(_width, _height).save_state()

        return Succession(
            Create(dot),
            AnimationGroup(
                Write(dash1, run_time=0.5),
                Write(dash2, run_time=0.5),
            ),
            AnimationGroup(
                AnimationGroup(
                    ShowPassingFlash(path1, time_width=1.),
                    Write(_width),
                    lag_ratio=0.5,
                ),
                AnimationGroup(
                    ShowPassingFlash(path2, time_width=1.),
                    Write(_height),
                    lag_ratio=0.5,
                ),
            ),
        )
    def clean_dashes(self):
        return AnimationGroup(
                *(Unwrite(d) for d in self._dashes),
                run_time=0.5,
        )

    def show_frame(self, x1, y1, x2, y2):
        path1, path2 = VMobject(), VMobject()
        path1.set_points_as_corners([
            self.axes.c2p(x1,y1),
            self.axes.c2p(x2,y1),
            self.axes.c2p(x2,y2),
        ])
        path2.set_points_as_corners([
            self.axes.c2p(x1, y1),
            self.axes.c2p(x1, y2),
            self.axes.c2p(x2, y2),
        ])
        _width = Text(str(x2-x1), font=FONT).scale(0.3).next_to(path1, UP)
        _height = Text(str(y2-y1), font=FONT).scale(0.3).next_to(path2, LEFT)
        self._wh = VGroup(_width, _height)
        return AnimationGroup(
            AnimationGroup(
                ShowPassingFlash(path1, time_width=3.),
                Write(_width),
                lag_ratio=0.5,
            ),
            AnimationGroup(
                ShowPassingFlash(path2, time_width=3.),
                Write(_height),
                lag_ratio=0.5,
            ),
        )
class ImagePadded(ImageRaw):
    def __init__(self, path):
        Mobject.__init__(self)
        image = cv2.imread(path)[...,::-1]
        rpad, _, _ = resize_and_pad(image)
        self._setup(rpad)

class Demo(Scene):
    def construct(self) -> None:
        img1 = ImageRaw(r'assets/images/sample_1280_720.jpg')
        img2 = ImagePadded(r'assets/images/sample_1280_720.jpg')
        Group(img1, img2).scale(.5).arrange()
        self.add(img1, img2)

# class Demo(Scene):
#     def construct(self) -> None:
#         img = ImageRaw(r'assets/images/sample_1280_720.jpg').scale(0.6).shift(LEFT*2)
#         self.add(img)
#         # self.wait()
#         # self.play(img.show_shape())
#         # self.wait()
#         self.play(img.show_axes())
#         # self.wait()
#         x1, y1 = (200, 200) 
#         x2, y2 = (888, 555)
#         w, h = x2-x1, y2-y1
#         cx, cy = int((x1+x2)//2), int((y1+y2)//2)
#         self.play(img.image.animate.set_opacity(0.3))
#         self.play(img.show_coords(cx, cy))
#         # self.wait()
#         self.play(TransformMatchingShapes(img._xy, img._coords))
#         self.play(img.clean_dashes())
#         self.play(img.show_frame(x1,y1,x2,y2))
#         self.wait()
#
#         vg = VGroup(img._coords, img._wh)
#         target = Text(' '.join([str(cx), str(cy), str(w), str(h)]), font=FONT).scale(0.3).shift(RIGHT*2)
#         self.play(TransformMatchingShapes(vg, target))
#         self.wait()
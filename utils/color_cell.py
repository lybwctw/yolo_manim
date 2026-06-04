from typing import Self
from manim import *

import cv2

def load_central_cells(
    path,
    rows,
    cols,
    target_height,
):
    """
    Load central pixels and convert into cells vmobjects
    """
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    r0 = (h - rows) // 2
    c0 = (w - cols) // 2
    ps = img[r0:r0+rows, c0:c0+cols]

    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            r, g, b = ps[i, j]
            cells.add(ColorCell(r, g, b))
    cells.arrange_in_grid(
        rows=rows,
        cols=cols,
        buff=0,
    ).scale_to_fit_height(target_height)

    return cells

class ColorCell(VMobject):
    def __init__(self, r, g, b, **kwargs):
        """
        Example
        -------
        cell = ColorCell(1, 2, 3)
        """
        super().__init__(**kwargs)
        self.r = r
        self.g = g
        self.b = b
        self._color = rgb_to_color([int(r), int(g), int(b)])
        rect = Square(
            side_length=1,
            fill_color=self._color,
            fill_opacity=1.0,
            stroke_color=BLACK,
            stroke_width=2,
            stroke_opacity=1.0,
        )
        self.rect = rect
        self.add(self.rect)

    def write_digit(self, target='r'):
        """
        Example
        -------
        cell = ColorCell(1, 2, 3)
        result = cell.write_digit()
        """
        if target=='r':
            digit = self.r
            zidx = 6
        elif target=='g':
            digit = self.g
            zidx = 4
        elif target=='b':
            digit = self.b
            zidx = 2
        else:
            digit = 0
            zidx = 0

        text = Text(
            str(digit),
            font_size=13,
            font='JetBrains Mono',
        ).move_to(self).set_z_index(zidx)
        self.text = text
        self.add(text)

        anims = AnimationGroup(
            Write(text),
            self.rect.animate.set_fill(color=BLACK, opacity=0.8),
        )
        return anims
    def unwrite_digit(self, target):
        """
        Example
        -------
        cell = ColorCell(1, 2, 3)
        result = cell.unwrite_digit(target='r')
        """
        if target=='r':
            tcolor = rgb_to_color((self.r, 0, 0))
        elif target=='g':
            tcolor = rgb_to_color((0, self.g, 0))
        elif target=='b':
            tcolor = rgb_to_color((0, 0, self.b))
        else:
            tcolor = BLACK

        anims = AnimationGroup(
            Unwrite(self.text),
            self.rect.animate.\
                set_fill(tcolor,opacity=0.7).\
                set_stroke(BLACK,opacity=1.0)
        )
        return anims

class Demo(Scene):
    def construct(self) -> None:
        cell = ColorCell(1,2,3)
        self.add(cell)
        self.wait()

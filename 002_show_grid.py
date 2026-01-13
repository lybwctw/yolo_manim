from manim import *
import numpy as np
from PIL import Image
from manim.utils.rate_functions import ease_in_out_cubic

from color_cell import ColorCell


def load_center_pixels(path, rows=16, cols=30):
    """
    Load an image and return the center (rows x cols) RGB pixels
    as a NumPy array of shape (rows, cols, 3).
    """
    img = Image.open(path).convert("RGB")
    arr = np.array(img)  # (H, W, 3)

    H, W, _ = arr.shape
    r0 = (H - rows) // 2 - 6
    c0 = (W - cols) // 2

    return arr[r0:r0 + rows, c0:c0 + cols]


class ImageToPixels(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
        )

        # Background reference image
        image = ImageMobject("assets/images/pixels.png")
        image.scale_to_fit_height(config.frame_height)
        self.add(image)

        # Load real RGB data from resized.jpg
        pixels = load_center_pixels(
            "assets/images/resized.jpg",
            rows=16,
            cols=30,
        )

        f_rows, f_cols = 14, 26
        fpixels = load_center_pixels(
            "assets/images/resized.jpg",
            rows=f_rows,
            cols=f_cols,
        )

        # Build ColorCell grid
        cells = VGroup()
        for i in range(16):
            for j in range(30):
                r, g, b = pixels[i, j]
                cells.add(ColorCell(r, g, b, size=0.5))
        fcells = VGroup()
        for i in range(f_rows):
            for j in range(f_cols):
                r, g, b = fpixels[i, j]
                fcells.add(ColorCell(r, g, b, size=0.5))

        cells.arrange_in_grid(
            rows=16,
            cols=30,
            buff=0,
        )
        fcells.arrange_in_grid(
            rows=f_rows,
            cols=f_cols,
            buff=0,
        )
        cells.scale_to_fit_height(config.frame_height)
        fcells.scale_to_fit_height(config.frame_height*f_rows/16)
        cells.shuffle()
        fcells.shuffle()
        for i, cell in enumerate(fcells):
            cell.cards[0].set_z_index(cell.cards[0].z_index+999-i)
            cell.nums[0].set_z_index(cell.nums[0].z_index+999-i)

        self.play(Write(cells))
        self.remove(image)
        self.add(fcells)
        self.play(FadeOut(cells))
        # self.wait()

        # Expand into RGB numbers
        self.play(
            AnimationGroup(
                *[c.extend_show() for c in fcells],
                lag_ratio=0.05,
                run_time=3,
                rate_func=ease_in_out_cubic,
            )
        )

        # self.wait()

        for i, cell in enumerate(fcells):
            cell.cards[0].set_z_index(cell.cards[0].z_index+4*i)
            cell.nums[0].set_z_index(cell.nums[0].z_index+4*i)

        # shrink RGB numbers
        self.play(
            AnimationGroup(
                *[c.shrink() for c in fcells],
                lag_ratio=0.05,
                run_time=3,
                rate_func=smooth,
            )
        )

        # self.wait()
        self.play(AnimationGroup(
            FadeIn(image),
            FadeOut(fcells),
            lag_ratio=0.3,
        ))


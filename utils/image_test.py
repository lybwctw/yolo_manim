from manim import *
import numpy as np
from PIL import Image


class ImageGrid3D(ThreeDScene):
    def construct(self):
        # --------------------------------
        # Camera
        # --------------------------------
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-85 * DEGREES,
            zoom=1.2,
        )

        # --------------------------------
        # Parameters
        # --------------------------------
        GRID_W = 20
        GRID_H = 20
        CELL_SIZE = 0.2
        BG_COLOR = np.array([114,114,114])  # padding color

        # --------------------------------
        # Load image
        # --------------------------------
        img = Image.open("assets/images/sample.jpg").convert("RGB")
        img_w, img_h = img.size

        # --------------------------------
        # Aspect-ratio preserving resize
        # --------------------------------
        scale = min(GRID_W / img_w, GRID_H / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        img_resized = img.resize((new_w, new_h), Image.BILINEAR)
        img_np = np.array(img_resized)

        # --------------------------------
        # Padding (letterbox)
        # --------------------------------
        canvas = np.ones((GRID_H, GRID_W, 3)) * BG_COLOR

        y0 = (GRID_H - new_h) // 2
        x0 = (GRID_W - new_w) // 2

        canvas[y0:y0 + new_h, x0:x0 + new_w] = img_np
        canvas = canvas / 255.0

        # --------------------------------
        # Build grid of colored squares
        # --------------------------------
        grid = VGroup()

        for i in range(GRID_H):
            for j in range(GRID_W):
                r, g, b = canvas[i, j]

                pixel_color = rgb_to_color([r, g, b])

                cell = Square(
                    side_length=CELL_SIZE,
                    fill_color=pixel_color,
                    fill_opacity=1.,
                    stroke_width=0,
                    stroke_opacity=0.,
                )

                # Position in 3D
                cell.move_to([
                    (j - GRID_W / 2) * CELL_SIZE,
                    (GRID_H / 2 - i) * CELL_SIZE,
                    0,
                ])

                grid.add(cell)

        self.add(grid)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(6)

from manim import *

class ImageFromArray(MovingCameraScene):
    def construct(self):
        # FIXME, replace with kk image instead
        image = ImageMobject(r'assets/images/sample_640_360.jpg')
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        orig_height = image.height
        # self.add(image.scale_to_fit_height(config.frame_height))
        self.add(image)
        self.wait()
        self.play(image.animate.scale_to_fit_height(360/2).shift(DOWN*3))
        # image.scale_to_fit_height(360/2).shift(DOWN*3)
        self.wait()

        # to be used as 004_image_zoom_out.py
        self.play(image.animate.shift(UP*3).scale_to_fit_height(orig_height))
        # image.shift(UP*3).scale_to_fit_height(orig_height)
        self.wait()
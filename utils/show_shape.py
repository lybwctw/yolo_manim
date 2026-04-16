from manim import *

# TODO, implement this as a Animation
# TODO, font size and buff as configuration arg
class ShowShape:
    def __init__(self):
        self.shape_texts = VGroup()

    def show_passing_flash(self):
        path = self.get_shape_path()
        texts = self.get_shape_text()
        self.shape_texts = texts
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
            lag_ratio=0.2,
        )
        return anim

    def get_shape_path(self):
        pass

    def get_shape_text(self):
        pass
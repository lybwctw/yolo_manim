from manim import *
from utils.explainer import Explainer
from utils.image_pad import ImagePad

class Demo(ThreeDScene):
    def construct(self):
        background = ImagePad(padded=True).scale(1.0).set_opacity(0.2)
        explainer = Explainer.from_random(
            background=background,
            dist_range=(0, 2),
            prob_range=(0, 1),
            shape=(10,10),
            sf_nominal=32,
        )
        system = Group(background, explainer)

        self.add(system)
        self.wait()

        self.play(explainer.show_anchor_points())
        self.wait()

        # self.play(explainer.to_dots())
        # self.wait()

        # self.play(explainer.show_arrows())
        # self.wait()

        self.play(explainer.to_rects())
        self.wait()

        # self.play(explainer.hide_arrows())
        # self.wait()

        self.play(explainer.show_multi_labels(
            label_config={'font_size': 8},
        ))
        self.wait()

        self.play(explainer.apply_max_select())
        self.wait()

        self.move_camera(
            phi=90*DEGREES,
            theta=-180*DEGREES,
            gamma=-90*DEGREES,
            run_time=1.0,
            added_anims=[
                system.animate.shift(IN*5),
            ],
        )
        self.wait()

        for ap in explainer.anchor_points:
            ap.save_state()

        self.play(AnimationGroup(
            *(ap.animate(
                rate_func=rate_functions.ease_out_back,
                ).shift(OUT*10*ap.conf)
                for ap in explainer.anchor_points),
            run_time=5.0,
            lag_ratio=0.5,
            rate_func=rate_functions.ease_in_out_quart,
        ))
        self.wait()

        self.play(AnimationGroup(
            *(ap.animate(
                rate_func=rate_functions.ease_in_out_quart,
                ).restore()
                for ap in explainer.anchor_points),
            run_time=1.0,
            lag_ratio=0.0,
        ))
        self.wait()

        self.move_camera(
            phi=0*DEGREES,
            theta=-90*DEGREES,
            gamma=0*DEGREES,
            run_time=1.0,
            added_anims=[
                system.animate.shift(OUT*5),
            ],
        )
        self.wait()
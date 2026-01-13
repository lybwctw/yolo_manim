from manim import *
from typing_extensions import runtime

from rgb_display import RGBDisplay
from slider import *

# TODO: intersection -> down\up <- numbers
# concat from both sides to build number/color connection

class RGB(Scene):
    def construct(self) -> None:
        circle_r = Circle(
            stroke_opacity=0.0,
            fill_color=ManimColor('#FF0000'),
            fill_opacity=1.0
        ).shift(LEFT/2)
        circle_g = Circle(
            stroke_opacity=0.0,
            fill_color=ManimColor('#00FF00'),
            fill_opacity=1.0
        ).shift(RIGHT/2)
        circle_b = Circle(
            stroke_opacity=0.0,
            fill_color=ManimColor('#0000FF'),
            fill_opacity=1.0
        ).shift(DOWN*3**.5/2)

        rg = Intersection(
            circle_r, circle_g,
            color=ManimColor('#FFFF00'),
            stroke_opacity=0.0,
            fill_opacity=1.0,
        )
        rb = Intersection(
            circle_r, circle_b,
            color=ManimColor('#FF00FF'),
            stroke_opacity=0.0,
            fill_opacity=1.0,
        )
        gb = Intersection(
            circle_g, circle_b,
            color=ManimColor('#00FFFF'),
            stroke_opacity=0.0,
            fill_opacity=1.0,
        )

        rgb = Intersection(
            circle_r, circle_g, circle_b,
            color=ManimColor('#FFFFFF'),
            stroke_opacity=0.0,
            fill_opacity=1.0,
        )

        palette = VGroup(circle_r, circle_b, circle_g,
                         rg, rb, gb,
                         rgb)

        r_tracker = ValueTracker(value=255)
        g_tracker = ValueTracker(value=255)
        b_tracker = ValueTracker(value=255)

        _hfstr = '{:02X}'
        circle_r.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#'+_hfstr.format(round(r_tracker.get_value()))+'0000'
            ))
        )
        circle_g.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#' + '00' + _hfstr.format(round(g_tracker.get_value())) + '00'
            ))
        )
        circle_b.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#' + '0000' + _hfstr.format(round(b_tracker.get_value()))
            ))
        )

        rg.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#' + \
                _hfstr.format(round(r_tracker.get_value())) + \
                _hfstr.format(round(g_tracker.get_value())) + \
                '00'
            ))
        )
        rb.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#' + \
                _hfstr.format(round(r_tracker.get_value())) + \
                '00' + \
                _hfstr.format(round(b_tracker.get_value()))
                ))
        )
        gb.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#' + \
                '00' + \
                _hfstr.format(round(g_tracker.get_value())) + \
                _hfstr.format(round(b_tracker.get_value()))
            ))
        )

        rgb.add_updater(
            lambda c: c.set_fill(color=ManimColor(
                '#' + \
                _hfstr.format(round(r_tracker.get_value())) + \
                _hfstr.format(round(g_tracker.get_value())) + \
                _hfstr.format(round(b_tracker.get_value()))
            ))
        )



        r_slider = Slider(r_tracker, "R", color=rgb_to_color((255,0,0)))
        g_slider = Slider(g_tracker, "G", color=rgb_to_color((0,255,0)))
        b_slider = Slider(b_tracker, "B", color=rgb_to_color((0,0,255)))
        sliders = VGroup(r_slider, g_slider, b_slider)
        sliders.arrange(DOWN, buff=0.6)

        # VGroup(palette, rgb_big, sliders).arrange()
        # self.add(palette, rgb_big, sliders)
        VGroup(palette, sliders).arrange()
        self.add(palette, sliders)

        self.play(
            AnimationGroup(
                r_tracker.animate.set_value(0),
                g_tracker.animate.set_value(0),
                b_tracker.animate.set_value(0),
            ),
            runtime=2,
        )
        self.wait()

        for _ in range(5):
            r, g, b = [np.random.randint(0,256) for _ in range(3)]
            # r, g, b = random_color().to_int_rgb()
            self.play(
                AnimationGroup(
                    r_tracker.animate.set_value(r),
                    g_tracker.animate.set_value(g),
                    b_tracker.animate.set_value(b),
                )
            )
            self.wait(0.2)

        rgb_display = RGBDisplay(rgb.copy().shift(RIGHT*2).scale(2),
            r_tracker, g_tracker, b_tracker).move_to(sliders)

        self.wait()
        self.play(ReplacementTransform(sliders, rgb_display))
        for _ in range(5):
            r, g, b = [np.random.randint(0,256) for _ in range(3)]
            # r, g, b = random_color().to_int_rgb()
            self.play(
                AnimationGroup(
                    r_tracker.animate.set_value(r),
                    g_tracker.animate.set_value(g),
                    b_tracker.animate.set_value(b),
                )
            )
            self.wait(0.2)

        self.wait()
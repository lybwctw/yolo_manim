from manim import *
from utils.slider import Slider
from utils.constants import *

N_SAMPLES_S1 = 3    # n + 3 in total
N_SAMPLES_S2 = 3
N_SAMPLES_S3 = 3

DEFAULT_TEXT_CONFIG = {
    'font_size': 24,
    'font': "JetBrains Mono",
}

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        r_tracker = ValueTracker(value=255)
        g_tracker = ValueTracker(value=255)
        b_tracker = ValueTracker(value=255)

        circle_r = Circle(
            stroke_opacity=0.0,
            stroke_width=0,
            fill_color=ManimColor('#FF0000'),
            fill_opacity=1.0
        ).shift(UP * 3 ** .5 / 2 * 2)
        circle_g = Circle(
            stroke_opacity=0.0,
            stroke_width=0,
            fill_color=ManimColor('#00FF00'),
            fill_opacity=1.0
        ).shift(LEFT / 2 * 2)
        circle_b = Circle(
            stroke_opacity=0.0,
            stroke_width=0,
            fill_color=ManimColor('#0000FF'),
            fill_opacity=1.0
        ).shift(RIGHT / 2 * 2)

        circle_r.add_updater(
            lambda c: c.set_fill(
                color=rgb_to_color((
                    int(r_tracker.get_value()),
                    0,
                    0,
                ))
            )
        )
        circle_g.add_updater(
            lambda c: c.set_fill(
                color=rgb_to_color((
                    0,
                    int(g_tracker.get_value()),
                    0,
                ))
            )
        )
        circle_b.add_updater(
            lambda c: c.set_fill(
                color=rgb_to_color((
                    0,
                    0,
                    int(b_tracker.get_value()),
                ))
            )
        )

        rg = always_redraw(
            lambda: Intersection(
                circle_r, circle_g,
                color=rgb_to_color((
                    int(r_tracker.get_value()),
                    int(g_tracker.get_value()),
                    0,
                )),
                stroke_opacity=0.0,
                fill_opacity=1.0,
            ).set_z_index(1)
        )
        rb = always_redraw(
            lambda: Intersection(
                circle_r, circle_b,
                color=rgb_to_color((
                    int(r_tracker.get_value()),
                    0,
                    int(b_tracker.get_value()),
                )),
                stroke_opacity=0.0,
                fill_opacity=1.0,
            ).set_z_index(1)
        )
        gb = always_redraw(
            lambda: Intersection(
                circle_g, circle_b,
                color=rgb_to_color((
                    0,
                    int(g_tracker.get_value()),
                    int(b_tracker.get_value()),
                )),
                stroke_opacity=0.0,
                fill_opacity=1.0,
            ).set_z_index(1)
        )

        rgb = always_redraw(
            lambda: Intersection(
                circle_r, circle_g, circle_b,
                color=rgb_to_color((
                    int(r_tracker.get_value()),
                    int(g_tracker.get_value()),
                    int(b_tracker.get_value()),
                )),
                stroke_opacity=0.0,
                fill_opacity=1.0,
            ).set_z_index(2)
        )

        palette = VGroup(circle_r, circle_b, circle_g,
                         rg, rb, gb,
                         rgb)

        r_slider = Slider(r_tracker, "R", color=rgb_to_color((255, 0, 0)))
        g_slider = Slider(g_tracker, "G", color=rgb_to_color((0, 255, 0)))
        b_slider = Slider(b_tracker, "B", color=rgb_to_color((0, 0, 255)))
        sliders = VGroup(r_slider, g_slider, b_slider)
        sliders.arrange(DOWN, buff=0.6)

        VGroup(sliders, palette).arrange(buff=1.0).center()
        palette.shift(UP*0.5)   # adjust palette position

        # ************************************************************
        self.next_section(
            'show sliders and palette',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            Write(sliders, lag_ratio=0),
            Succession(
                FadeIn(
                    palette, run_time=0.3,
                ),
                AnimationGroup(
                    circle_r.animate.shift(DOWN * 3 ** .5 / 2),
                    circle_g.animate.shift(RIGHT / 2),
                    circle_b.animate.shift(LEFT / 2),
                ),
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'random digit-color mapping',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, show (0,0,0) and those common ones before random
        random_colors = [
            (np.random.randint(0,256) for _ in range(3))
                for _ in range(N_SAMPLES_S1)
        ]
        random_colors = [[0, 0, 0], [128, 128, 128]] +\
                        random_colors +\
                        [[255,255,255]]
        
        for colors in random_colors:
            # r, g, b = [np.random.randint(0,256) for _ in range(3)]
            r, g, b = colors
            self.play(AnimationGroup(
                r_tracker.animate.set_value(r),
                g_tracker.animate.set_value(g),
                b_tracker.animate.set_value(b),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'combine numbers and color',
            skip_animations=False,
        )
        # ************************************************************
        # FIXME, problem when copy from sliders
        # orig_text = VGroup(
        #     slider.value_text.copy().clear_updaters()
        #     for slider in sliders
        # )
        orig_text = VGroup(
            Text(
                f'{int(r_tracker.get_value())}',
                **DEFAULT_TEXT_CONFIG,
            ).move_to(sliders[0].value_text),
            Text(
                f'{int(g_tracker.get_value())}',
                **DEFAULT_TEXT_CONFIG,
            ).move_to(sliders[1].value_text),
            Text(
                f'{int(b_tracker.get_value())}',
                **DEFAULT_TEXT_CONFIG,
            ).move_to(sliders[2].value_text),
        )
        orig_color = rgb.copy()

        self.add(orig_text, orig_color)
        self.wait()

        _text = (f'({int(r_tracker.get_value())},'
                 f'{int(g_tracker.get_value())},'
                 f'{int(b_tracker.get_value())})')
        res_text = Text(
            _text,
            **DEFAULT_TEXT_CONFIG,
        )
        res_color = orig_color.copy().center().shift(DOWN*.3)
        res_text.next_to(res_color, UP)

        self.play(AnimationGroup(
            TransformMatchingShapes(
                orig_text,
                res_text,
            ),
            Transform(
                orig_color,
                res_color,
            ),
            sliders.animate.shift(LEFT*1.5),
            palette.animate.shift(RIGHT*1.5),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop again',
            skip_animations=False,
        )
        # ************************************************************
        new_text = always_redraw(
            lambda: Text(
                (f'({int(r_tracker.get_value())},'
                 f'{int(g_tracker.get_value())},'
                 f'{int(b_tracker.get_value())})'),
                 **DEFAULT_TEXT_CONFIG,
            ).next_to(res_color, UP)
        )
        self.add(new_text)
        self.remove(res_text)

        random_colors = [
            (np.random.randint(0,256) for _ in range(3))
                for _ in range(N_SAMPLES_S2)
        ]
        random_colors = [[0, 0, 0], [128, 128, 128]] + random_colors
        
        for colors in random_colors:
            r, g, b = colors
            _color = rgb_to_color((r, g, b))
            self.play(AnimationGroup(
                r_tracker.animate.set_value(r),
                g_tracker.animate.set_value(g),
                b_tracker.animate.set_value(b),
                res_color.animate.set_color(_color),
                lag_ratio=0.0,
                run_time=wt,
            ))
            # res_text = new_text
            self.wait(wt)

        self.wait(wt)

        # ************************************************************
        self.next_section(
            'color background with central numbers',
            skip_animations=False,
        )
        # ************************************************************
        new_text.clear_updaters().set_z_index(1)
        bg_color = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            color=rgb_to_color((
                int(r_tracker.get_value()),
                int(g_tracker.get_value()),
                int(b_tracker.get_value()),
            )),
            fill_opacity=1.0,
        ).center()

        self.play(AnimationGroup(
            Transform(res_color, bg_color),
            new_text.animate.center(),
            sliders.animate.shift(LEFT*10),
            palette.animate.shift(RIGHT*10),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop again',
            skip_animations=False,
        )
        # ************************************************************
        # setup bg_color and new_text again to auto update
        self.remove(orig_color, res_color, new_text)
        bg_color = always_redraw(
            lambda: Rectangle(
                width=config.frame_width,
                height=config.frame_height,
                color=rgb_to_color((
                    int(r_tracker.get_value()),
                    int(g_tracker.get_value()),
                    int(b_tracker.get_value()),
                )),
                fill_opacity=1.0,
            ).center()
        )

        new_text = always_redraw(
            lambda: Text(
                (f'({int(r_tracker.get_value())},'
                 f'{int(g_tracker.get_value())},'
                 f'{int(b_tracker.get_value())})'),
                font_size=24,
                font='JetBrains Mono',
            ).center()
        )
        self.add(bg_color, new_text)

        random_colors = [
            (np.random.randint(0,256) for _ in range(3))
                for _ in range(N_SAMPLES_S2)
        ]
        random_colors = [[0, 0, 0], [128, 128, 128]] +\
                        random_colors +\
                        [[0, 0, 0]]
        for colors in random_colors:
            r, g, b = colors
            self.play(AnimationGroup(
                r_tracker.animate.set_value(r),
                g_tracker.animate.set_value(g),
                b_tracker.animate.set_value(b),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'fadeout everything',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            FadeOut(bg_color),
            Unwrite(
                new_text,
                lag_ratio=0.0,
            ),
            run_time=wt,
        ))
        self.wait(wt)
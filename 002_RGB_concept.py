from manim import *
from utils.slider import Slider

class MainScene(Scene):
    def construct(self) -> None:
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
            skip_animations=True,
        )
        # ************************************************************
        self.play(
            AnimationGroup(
                Write(sliders, lag_ratio=0),
                # Write(palette, lag_ratio=0.3),
                Succession(
                    FadeIn(
                        palette, run_time=0.3,
                    ),
                    AnimationGroup(
                        circle_r.animate.shift(DOWN * 3 ** .5 / 2),
                        circle_g.animate.shift(RIGHT / 2),
                        circle_b.animate.shift(LEFT / 2),
                    ),
                )
            )
        )
        self.wait()

        # ************************************************************
        self.next_section(
            'random digit-color mapping',
            skip_animations=True,
        )
        # ************************************************************
        # TODO, show (0,0,0) and those common ones before random
        for _ in range(3):
            r, g, b = [np.random.randint(0,256) for _ in range(3)]
            self.play(
                AnimationGroup(
                    r_tracker.animate.set_value(r),
                    g_tracker.animate.set_value(g),
                    b_tracker.animate.set_value(b),
                )
            )
            self.wait(0.3)
        self.wait()

        # ************************************************************
        self.next_section(
            'combine digit and color',
            skip_animations=True,
        )
        # ************************************************************
        # FIXME, problem when copy from sliders
        orig_text = VGroup(
            Text(
                f'{int(r_tracker.get_value())}',
                font_size=24,
                font="JetBrains Mono",
            ).move_to(sliders[0].value_text),
            Text(
                f'{int(g_tracker.get_value())}',
                font_size=24,
                font="JetBrains Mono",
            ).move_to(sliders[1].value_text),
            Text(
                f'{int(b_tracker.get_value())}',
                font_size=24,
                font="JetBrains Mono",
            ).move_to(sliders[2].value_text),
        )
        orig_color = rgb.copy()

        self.add(orig_text, orig_color)

        _text = (f'({int(r_tracker.get_value())},'
                 f'{int(g_tracker.get_value())},'
                 f'{int(b_tracker.get_value())})')
        res_text = Text(
            _text,
            font_size=24,
            font='JetBrains Mono',
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
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'random color several times',
            skip_animations=True,
        )
        # ************************************************************
        new_text = always_redraw(
            lambda: Text(
                (f'({int(r_tracker.get_value())},'
                 f'{int(g_tracker.get_value())},'
                 f'{int(b_tracker.get_value())})'),
                font_size=24,
                font='JetBrains Mono',
            ).next_to(res_color, UP)
        )
        self.add(new_text)
        self.remove(res_text)
        for _ in range(5):
            r, g, b = [np.random.randint(0,256) for _ in range(3)]
            _color = rgb_to_color((r, g, b))
            self.play(AnimationGroup(
                r_tracker.animate.set_value(r),
                g_tracker.animate.set_value(g),
                b_tracker.animate.set_value(b),
                res_color.animate.set_color(_color),
            ))
            # res_text = new_text
            self.wait(0.5)

        self.wait()

        # ************************************************************
        self.next_section(
            'color background with central digits',
            skip_animations=True,
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

        self.play(
            Transform(res_color, bg_color),
            new_text.animate.center(),
            sliders.animate.shift(LEFT*10),
            palette.animate.shift(RIGHT*10),
        )

        # ************************************************************
        self.next_section(
            'switching random color',
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

        for _ in range(3):
            r, g, b = [np.random.randint(0,256) for _ in range(3)]
            self.play(AnimationGroup(
                r_tracker.animate.set_value(r),
                g_tracker.animate.set_value(g),
                b_tracker.animate.set_value(b),
            ))
            self.wait(0.5)

        self.wait()

        # ************************************************************
        self.next_section(
            'fadeout everything for the next scene',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            FadeOut(bg_color),
            Unwrite(new_text),
        ))
        self.wait()
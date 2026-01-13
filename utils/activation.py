from manim import *

class Sample(Scene):
    def construct(self) -> None:
        ax = Axes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            x_length=6,
            y_length=6,
            axis_config={
                'include_numbers': True,
                'tip_width': 0.2,
                'tip_height': 0.2,
                'font_size': 18,
                'tick_size': 0.05,
                'decimal_number_config': {
                    'num_decimal_places': 0,
                    'color': GRAY,
                },
            },
        )
        graph = ax.plot(
            lambda x: np.exp(x)/(1+np.exp(x)),
            # lambda x: x*np.exp(x)/(1+np.exp(x)),
            # lambda x: 0 if x < 0 else x,
            # lambda x: np.tanh(x)*.99,
            use_smoothing=False,
            color=MAROON,
        )

        x_tracker = ValueTracker(0.0)
        dot_label = always_redraw(
            lambda: VGroup(
                Dot(
                    ax.i2gp(x=x_tracker.get_value(), graph=graph),
                    radius=0.05,
                ),
                ax.get_graph_label(
                    graph=graph,
                    x_val=x_tracker.get_value(),
                    label=Text(
                        '('+','.join(f'{x:.2f}' for x in ax.i2gc(x=x_tracker.get_value(), graph=graph))+')',
                        font_size=16,
                        font='JetBrains Mono',
                        weight=NORMAL,
                    ),
                    direction=UL,
                    buff=0.20,
                    color=LOGO_WHITE,
                ).shift(
                    float(x_tracker.get_value()<0) * x_tracker.get_value() * LEFT * 0.20
                ),
                ax.get_lines_to_point(
                    ax.i2gp(x=x_tracker.get_value(), graph=graph),
                    line_func=Line,
                    color=GRAY,
                    line_config={
                        'stroke_opacity': 0.3,
                    },
                ),
            )
        )

        asym = DashedLine(
            ax.c2p(-5,1),
            ax.c2p(5,1),
            stroke_width=2,
            color=GRAY,
            stroke_opacity=0.5,
        )

        act_name = Text(
            'Sigmoid',
            font_size=28,
            font='JetBrains Mono',
            weight=NORMAL,
        ).align_to(ax, UL).shift(RIGHT*.2)
        # self.wait()

        # self.wait()
        # self.play(AnimationGroup(
        #     ax.animate.set_opacity(0.3),
        #     asym.animate.set_opacity(0.3),
        # ))

        act_plot = VGroup(
            ax,
            graph,
            asym,
            # dot_label,
            act_name,
        )
        # self.wait()
        # self.play(Write(dot_label))
        # self.wait()
        # self.play(x_tracker.animate.set_value(-4.5), run_time=2)
        # self.wait()
        # self.play(x_tracker.animate.set_value(4), run_time=3)
        # self.wait()

        formula = MathTex(
            r"= \frac{1}{1 + e^{-x}}",
            font_size=32,
        ).next_to(act_name, DOWN).align_to(act_name, LEFT)
        # self.play(act_plot.animate.move_to(LEFT*2))

        self.play(AnimationGroup(
            Write(ax),
            Write(graph),
            Write(asym),
            Write(act_name),
            Write(formula),
            lag_ratio=0.25,
        ))
        self.wait()
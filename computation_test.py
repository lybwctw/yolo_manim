from manim import *

DEFAULT_TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
}

class Computation(VGroup):
    def __init__(
        self,
        formatter: str = "",
        values: list = [],
        colors=None,
        **text_config,
    ):
        super().__init__()

        if colors is None:
            colors = [None] * len(values)
        elif not isinstance(colors, (list, tuple)):
            colors = [colors] * len(values)

        colored_values = []

        for value, color in zip(values, colors):
            value = str(value)

            if color is not None:
                value = (
                    f'<span foreground="{ManimColor(color).to_hex()}">'
                    f"{value}"
                    f"</span>"
                )

            colored_values.append(value)

        text = formatter.format(*colored_values)

        text_config = {**DEFAULT_TEXT_CONFIG, **text_config}
        self.computation = MarkupText(
            text,
            **text_config,
        )

        self.add(self.computation)


class ComputationExample(Scene):
    def construct(self):

        # --------------------------------------------------
        # Basic arithmetic
        # --------------------------------------------------

        comp1 = Computation(
            formatter="{} + {} = {}",
            values=[3, 4, 7],
            colors=[BLUE, GREEN, YELLOW],
        )

        # --------------------------------------------------
        # DFL expectation
        # --------------------------------------------------

        comp2 = Computation(
            formatter="{} × {} + {} × {} = {}",
            values=[
                "0.2", "1",
                "0.8", "2",
                "1.8",
            ],
            colors=[
                BLUE, BLUE,
                GREEN, GREEN,
                YELLOW,
            ],
        )

        # --------------------------------------------------
        # Tensor reshape
        # --------------------------------------------------

        comp3 = Computation(
            formatter="{} → {} → {}",
            values=[
                "(80,80,64)",
                "(80,80,4,16)",
                "(80,80,4)",
            ],
            colors=[
                BLUE,
                GREEN,
                YELLOW,
            ],
        )

        # --------------------------------------------------
        # Same color for all values
        # --------------------------------------------------

        comp4 = Computation(
            formatter="softmax({}) = {}",
            values=[
                "[2.1, 0.3, 1.4]",
                "[0.59, 0.10, 0.31]",
            ],
            colors=BLUE,
        )

        VGroup(
            comp1,
            comp2,
            comp3,
            comp4,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.8,
        )

        self.play(
            LaggedStart(
                *[Write(comp) for comp in [comp1, comp2, comp3, comp4]],
                lag_ratio=0.3,
            )
        )

        self.wait()
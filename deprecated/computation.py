from manim import *

TEXT_CONFIG = {
    'color': GRAY,
    'font_size': 15,
    'font': 'JetBrains Mono',
}

class Computation(VGroup):
    def __init__(
        self,
        formatter: str = '',
        values: list | None = None,
        **text_config,
    ):
        """
        Example
        -------
        computation = Computation(formatter="{:.2f}", values=[1.0])
        """
        super().__init__()
        self.formatter = formatter
        self.values = values

        text = self.formatter.format(*values)
        computation = MarkupText(
            text,
            **{**TEXT_CONFIG, **(text_config or {})},
        )
        self.computation = computation
        self.add(self.computation)

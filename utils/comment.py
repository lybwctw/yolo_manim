import sys
sys.path.append('..')

from manim import *

DEFAULT_TEXT_CONFIG = {
    "font": "JetBrains Mono",
    "font_size": 32,
}

# TODO: replace comptuation with text
class Comment(VGroup):
    """Comment text with colored fields.
    """
    def __init__(
        self,
        formatter: str,
        values: list | None = None,
        colors=None,
        **config,
    ):
        super().__init__()

        text_config = {**DEFAULT_TEXT_CONFIG, **config}

        values = values or []
        if colors is None:
            colors = [None] * len(values)
        elif not isinstance(colors, (list, tuple)):
            colors = [colors] * len(values)
        elif len(colors) < len(values):
            colors = list(colors) + [None] * (len(values) - len(colors))

        from string import Formatter

        fmt = Formatter()
        rendered = ''
        auto_index = 0
        for literal_text, field_name, format_spec, conversion in fmt.parse(formatter):
            rendered += literal_text
            if field_name is None:
                continue

            if field_name == '':
                index = auto_index
                auto_index += 1
            elif field_name.isdigit():
                index = int(field_name)
            else:
                raise ValueError(
                    f'Unsupported field name in text formatter: {field_name}'
                )

            if index >= len(values):
                raise ValueError(
                    'Formatter expects more values than provided for text.'
                )

            value = values[index]
            if conversion is not None:
                if conversion == 's':
                    value = str(value)
                elif conversion == 'r':
                    value = repr(value)
                elif conversion == 'a':
                    value = ascii(value)
                else:
                    raise ValueError(
                        f'Unsupported conversion in text formatter: {conversion}'
                    )

            field_text = fmt.format_field(value, format_spec)
            if colors[index] is not None:
                field_text = (
                    f'<span foreground="{ManimColor(colors[index]).to_hex()}">'
                    f'{field_text}'
                    f'</span>'
                )
            rendered += field_text

        self.text = MarkupText(rendered, **text_config)
        self.add(self.text)


class Demo(Scene):
    def construct(self):
        # comp = Comment(
        #     formatter='{}+{}={}',
        #     values=[3, 4, 7],
        #     colors=[BLUE, PURE_GREEN, YELLOW],
        #     font_size=36,
        #     color=GRAY,
        # )

        # self.play(Create(comp))
        # self.wait()
        class_mapping = Comment(
            formatter=(
                '{:<6s}->0\n'
                '{:<6s}->1\n'
                '{:<6s}->2\n'
            ),
            values=['kunkun', 'coke', 'pepsi'],
            colors=[GREEN, RED, BLUE],
            font_size=36,
            color=GRAY,
        )
        self.play(Create(class_mapping))
        self.wait()
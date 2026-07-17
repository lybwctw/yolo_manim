from manim import *

DEFAULT_TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
}

class AlignedText(VMobject):
    def __init__(
        self,
        text: str = '???',
        text_config: dict = {},
    ):
        super().__init__()
        self.text = text

        text_config = {**DEFAULT_TEXT_CONFIG, **text_config}
        mob = Text(
            ':' + self.text + ':',
            **text_config,
        )
        mob[0].set_opacity(0)
        mob[-1].set_opacity(0)

        self.mob = mob

        self.add(self.mob)

class Demo(Scene):
    def construct(self):
        mob = AlignedText('for test')
        rect = BackgroundRectangle(mob, fill_color=GREEN)

        self.add(rect)
        self.play(Create(mob, run_time=0.3))
        self.wait()
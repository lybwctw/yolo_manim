from manim import *

class YLabel(VMobject):
    """
    Example
    -------
    from manim import *
    class Demo(Scene):
        def construct(self):
            label = YLabel(
                text='test',
                label_txt_config={
                    'font': 'JetBrains Mono',
                    'font_size': 30,
                },
                label_bg_config={
                    'stroke_color': GREEN,
                    'stroke_width': 0,
                    'stroke_opacity': 0.0,
                    'fill_color': GREEN,
                    'fill_opacity': 1.0,
                },
            )
            self.play(Write(label))
            self.wait()
    """
    def __init__(
        self,
        text: str = 'None',
        label_txt_config: dict | None = None,
        label_bg_config: dict | None = None,
    ):
        super().__init__()
        self.text = text

        label_txt = Text(
            text=text,
            **label_txt_config,
        )

        # auto width/height if not provided
        label_bg_config = {
            'width': label_txt.width * 1.1,
            'height': label_txt.height * 1.3,
            **label_bg_config,
        }

        label_bg = Rectangle(
            **label_bg_config,
        )

        self.label_txt = label_txt
        self.label_bg = label_bg
        self.add(self.label_bg)
        self.add(self.label_txt)
    
class Demo(Scene):
    def construct(self):
        label = YLabel(
            text='test',
            label_txt_config={
                'font': 'JetBrains Mono',
                'font_size': 30,
            },
            label_bg_config={
                'stroke_color': GREEN,
                'stroke_width': 0,
                'stroke_opacity': 0.0,
                'fill_color': GREEN,
                'fill_opacity': 1.0,
            },
        )
        self.play(Write(label))
        self.wait()
from manim import *

LABEL_BG_RATIO_W = 1.1
LABEL_BG_RATIO_H = 1.3

class YLabel(VMobject):
    def __init__(
        self,
        include_text: bool = True,  # False for mini explainer
        text: str = 'None',
        label_txt_config: dict = {},
        label_bg_config: dict = {},
    ):
        super().__init__()
        self.text = text

        # remember config
        self.label_txt_config = label_txt_config
        self.label_bg_config = label_bg_config

        if include_text:
            label_txt = Text(
                text=text,
                **label_txt_config,
            )
            self.label_txt = label_txt
            # auto width/height if not provided
            label_bg_config = {
                'width': label_txt.width * LABEL_BG_RATIO_W,
                'height': label_txt.height * LABEL_BG_RATIO_H,
                **label_bg_config,
            }
        else:
            label_bg_config = {
                **label_bg_config,
            }

        label_bg = Rectangle(
            **label_bg_config,
        )
        self.label_bg = label_bg

        self.add(self.label_bg)
        
        if include_text:
            self.add(self.label_txt)

    def update_text(
        self,
        text: str = 'new',
        **aargs,
    ) -> Animation:
        """Update text, keep down left corner aligned.
        """
        self.text = text
        label_txt_config = {
            **self.label_txt_config,
            **{'font_size': self.label_txt.font_size},
        }
        label_txt = Text(
            text=text,
            **label_txt_config,
        )
        label_bg_config = {
            'width': label_txt.width * LABEL_BG_RATIO_W,
            'height': label_txt.height * LABEL_BG_RATIO_H,
            **self.label_bg_config,
        }
        label_bg = Rectangle(
            **label_bg_config,
        )

        vg = VGroup(label_bg, label_txt)
        vg.move_to(self.label_bg.get_corner(DL), aligned_edge=DL)

        return AnimationGroup(
            Transform(self.label_bg, label_bg),
            Transform(self.label_txt, label_txt),
            **aargs,
        )

    
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
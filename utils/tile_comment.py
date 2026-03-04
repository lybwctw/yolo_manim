from manim import *

class TileComment(VMobject):
    def __init__(self, text='None'):
        super().__init__()
        self.text = Text(
            text=text,
            font_size=73,
            color=BLACK,
            font='Source Han Sans SC'
        ).add_background_rectangle(
            color=WHITE,
            opacity=1.0,
            buff=0.1,
            stroke_width=0,
        )
        self.add(self.text)

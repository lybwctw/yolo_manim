from manim import *

DEFAULT_TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
    # 'disable_ligatures': True,
}

class AlignedText(VMobject):
    def __init__(
        self,
        text: str = 'None',
        **text_config,
    ):
        super().__init__()
        self.text = text

        text_config = {**DEFAULT_TEXT_CONFIG, **text_config}
        mob = Text(
            'o' + self.text + 'o',
            **text_config,
        )
        mob[0].set_opacity(0)
        mob[-1].set_opacity(0)

        self.mob = mob

        self.add(self.mob)
    
    def get_width(
        self,
    ) -> float:
        """Width based on colon.
        """
        return self.width

    def get_height(
        self,
    ) -> float:
        """Height based on colon.
        """
        return self.mob[0].height
    
    def colon_width(
        self,
    ) -> float:
        return self.mob[0].width
    
    def get_font_size(
        self,
    ) -> float:
        return self.mob.font_size
    
    def attach_offset(
        self,
        ref: np.ndarray,
    ):
        offset = ref - self.mob[0].get_corner(LEFT)
        return offset
    
    def attach_to_point(
        self,
        ref: np.ndarray,
    ):
        """Align 1st colon's center to point.
        """
        # offset = ref - self.mob[0].get_corner(LEFT)
        offset = self.attach_offset(ref)
        self.shift(offset)

    def tarnish(
        self,
        opacity: float = 0.5,
    ) -> Animation:
        return self.mob[1:-1].animate.set_opacity(opacity)

    def lightup(
        self,
    ) -> Animation:
        return self.mob[1:-1].animate.set_opacity(1.0)
    

class Demo(Scene):
    def construct(self):
        mob = AlignedText('for test')

        rect = Rectangle(
            width=mob.get_width(),
            height=mob.get_height()*2,
            fill_color=GREEN,
            fill_opacity=1.0,
            stroke_width=0,
        ).move_to(mob)

        self.add(rect)
        self.play(Create(mob, run_time=0.3))
        self.wait()

        self.play(rect.animate.stretch_to_fit_width(5))
        self.wait()
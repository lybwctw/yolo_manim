from manim import *

DEFAULT_TEXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 32,
    'disable_ligatures': True,
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
    
    # def get_center(
    #     self,
    # ) -> np.ndarray:
    #     """Center based on colon.
    #     """
    #     return np.array([
    #         self.get_x(),
    #         self.mob[0].get_y(),
    #         0,
    #     ])
    
    # def offset_to_corner(
    #     self,
    #     corner,
    #     buff_w: float = 0.0,
    #     buff_h: float = 0.0,
    # ) -> np.ndarray:
    #     tpos = corner + buff_w*RIGHT + buff_h*DOWN
    #     spos = self.mob[0].get_corner(UL)
    #     offset = tpos - spos
    #     return offset
    
    # def align_to_corner(
    #     self,
    #     corner,
    #     buff_w: float = 0.0,
    #     buff_h: float = 0.0,
    # ):
    #     offset = self.offset_to_corner(
    #         corner,
    #         buff_w,
    #         buff_h,
    #     )
    #     self.shift(offset)
    
    # def concat_to_atext(
    #     self,
    #     ref,
    #     closer: bool = False,       # ignore the first colon?
    # ):
    #     self.next_to(ref, RIGHT, buff=0.0)
    #     if closer:
    #         self.shift(self.mob[0].get_width() * LEFT)
    #     tbot = ref.mob[0].get_bottom()[1]
    #     sbot = self.mob[0].get_bottom()[1]
    #     offset = (tbot - sbot) * UP
    #     self.shift(offset)

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
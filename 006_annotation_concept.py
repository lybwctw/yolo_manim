from manim import *

from utils.constants import S005_EVERYTHING
from utils.general import load_everything


class MainScene(Scene):
    def construct(self) -> None:
        (
            _, annotation, _, _, _,
        ) = load_everything(S005_EVERYTHING)
        self.add(annotation)
        self.wait()
        self.play(annotation.hide_text())
        self.wait()
        self.play(annotation.unhide_text())
        self.wait()
        self.play(annotation.show_passing_flash())
        self.wait()
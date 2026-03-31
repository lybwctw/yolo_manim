from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground

class MainScene(Scene):
    def construct(self) -> None:
        (
            x,
        ) = load_everything(??)

        # capture little object?

        # save for next scene
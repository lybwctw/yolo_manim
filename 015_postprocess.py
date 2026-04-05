from manim import *

from utils.constants import *
from utils.general import load_everything, save_everything, scale_manager_target
from utils.arrow_comment import ArrowComment
from utils.yolo_annotation import ImageAnnotation, AnnotationRepad
from utils.repad_background import RepadBackground

class MainScene(Scene):
    def construct(self) -> None:
        (
            x,
        ) = load_everything(??)

        # classic: conf + nms

        # freedom during postprocess, multi-label?

        # nms issue

        # digit view: from decoded to repad

        # save for next scene
from manim import *

image_path = None
label_path = None

class MainScene(Scene):
    def construct(self) -> None:
        image = ImageRaw(image_path)
        annotation = ImageAnnotation(image, label_path)
        aqmark_down = ArrowQmark(DOWN)
        aqmark_up = ArrowQmark(UP)
        aqmark_right = ArrowQmark(RIGHT)

        manager = LayoutManager(image, aqmark, annotation)

        self.add(image)
        self.wait()
        self.add(annotation)
        self.wait()
        # TODO: realtime detection loop until demo image/annotation

        self.play(manager.expand(RIGHT))
        self.wait()
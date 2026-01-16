from manim import *

image_path = None
label_path = None

class MainScene(Scene):
    def construct(self) -> None:
        image = ImageRaw(image_path)
        annotation = ImageAnnotation(image, label_path)
        aqmark_1 = ArrowQmark(DOWN)
        aqmark_2 = ArrowQmark(UP)
        aqmark_main = ArrowQmark(RIGHT)
        dtile_1 = DigitTile()
        dtile_2 = DigitTile()

        manager = LayoutManager([image, aqmark_main, annotation])

        self.add(image)
        self.wait()
        self.add(annotation)
        self.wait()
        # TODO: realtime detection loop until demo image/annotation

        self.play(manager.expand(RIGHT))
        self.wait()

        self.play(manager.expand([
            [image, None, annotation],
            [aqmark_1, None, aqmark_2],
            [dtile_1, aqmark_main, dtile_2],
        ]))

         
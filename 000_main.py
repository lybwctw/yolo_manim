from manim import *
from utils.yolo_annotation import YoloAnnotation
from utils.image_raw import ImageRaw
from utils.image_annotation import ImageAnnotation
from utils.arrow_qmark import ArrowQmark
from utils.digit_tile import DigitTile

image_path = None
label_path = None

class MainScene(Scene):
    def construct(self) -> None:
        manager = VGroup()

        image = ImageRaw(image_path).scale(2.)
        annotation = ImageAnnotation(image, label_path)
        aq1 = ArrowQmark(DOWN, LEFT).scale(.6).shift(LEFT*10)
        aq2 = ArrowQmark(UP, RIGHT).scale(.6).shift(RIGHT*10)
        aq3 = ArrowQmark(RIGHT, UP).scale(.6).shift(UP*.5)
        dt1 = DigitTile('一堆\n数字').shift(DOWN*10)
        dt2 = DigitTile('一堆\n数字').shift(DOWN*10)

        manager.add(
            *[image, aq3, annotation]
        )

        self.add(manager)
        self.wait()

        manager.save_state()
        manager.generate_target()
        manager.target[0].scale(.5)
        manager.target[2].scale(.5)
        manager.target.arrange()
        self.play(MoveToTarget(manager))
        self.wait()
        # self.play(manager.animate.restore())
        # self.wait()

        self.play(AnimationGroup(
            *(manager[i].animate(rate_func=there_and_back).scale(1.1) for i in range(3)),
            lag_ratio=0.2,
            run_time=1.8,
        ))

        # manager.generate_target()
        # manager[1] = VMobject()
        # manager.add(
        #     *[aq1, VMobject(), aq2],
        #     *[dt1, aq3, dt2],
        # )
        # manager.generate_target()
        # manager.target.arrange_in_grid(
        #     rols=3, cols=3,
        # )
        # manager.target.center()
        # self.play(MoveToTarget(manager))
        # self.wait()
        #
        # self.play(manager.animate.scale(0.5))
        # self.wait()

        # self.play(TransformMatchingShapes(manager, manager.target))
        # self.wait()

        # self.play(manager.animate.arrange())
        # self.wait()
        # TODO: realtime detection loop until demo image/annotation

        # self.play(manager.expand(RIGHT))
        # self.wait()
        #
        # self.play(manager.expand([
        #     [image, None, annotation],
        #     [aqmark_1, None, aqmark_2],
        #     [dtile_1, aqmark_main, dtile_2],
        # ]))
        #

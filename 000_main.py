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
        # ------------------------------------------------------------
        self.next_section(
            'init assets',
            skip_animations=True,
        )
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

        # ------------------------------------------------------------
        self.next_section(
            'create centered image and annotation',
            skip_animations=True,
        )
        # TODO, difference between add to manager and add to screen?
        # self.play(Write(image))
        # self.play(Write(annotation))
        self.add(manager)
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'expand into image -> annotation',
            skip_animations=True,
        )
        manager.save_state()
        manager.generate_target()
        manager.target[0].scale(.5)
        manager.target[2].scale(.5)
        manager.target.arrange()
        self.play(MoveToTarget(manager))
        self.wait()

        # # scale-highlight one by one
        # self.play(AnimationGroup(
        #     *(manager[i].animate(
        #       rate_func=there_and_back,
        #     ).scale(1.1) for i in range(3)),
        #     lag_ratio=0.3,
        #     run_time=0.6,
        # ))

        # ------------------------------------------------------------
        self.next_section(
            'introduce digital game idea, the big map',
            skip_animations=True,
        )
        manager[1] = VMobject()
        manager.add(
            *[aq1, VMobject(), aq2],
            *[dt1, aq3, dt2],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rols=3, cols=3,
        )
        manager.target.center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'maybe, realtime detection loop until demo image/annotation',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'focus on raw image input',
            skip_animations=False,
        )
        manager.save_state()
        manager.generate_target()
        manager.target.arrange_in_grid(rows=3, cols=3, buff=6.)
        manager.target.shift(-manager.target[0].get_center())
        manager.target[0].scale(2.)
        self.play(MoveToTarget(manager))
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'maybe, highlight width and height',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '001_image_zoom, explain the concept of RGB',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'reverse back from focused image to the big map',
            skip_animations=False,
        )
        self.play(manager.animate.restore())
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'tranfrom dt1 ->  (digit tile to ',
            skip_animations=False,
        )
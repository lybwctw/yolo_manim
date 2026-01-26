from manim import *
from utils.yolo_annotation import YoloAnnotation
from utils.image_raw import ImageRaw
from utils.image_annotation import ImageAnnotation
from utils.arrow_qmark import ArrowQmark
from utils.digit_tile import DigitTile
from utils.digit_layer_fake import DigitLayerFake

image_path = None
label_path = None

class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        # TODO 1-1. introduce object detection problem
        # ************************************************************
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

        # ------------------------------------------------------------
        # # scale-highlight one by one
        # self.play(AnimationGroup(
        #     *(manager[i].animate(
        #       rate_func=there_and_back,
        #     ).scale(1.1) for i in range(3)),
        #     lag_ratio=0.3,
        #     run_time=0.6,
        # ))

        # ************************************************************
        # TODO 1-2. convert one problem into three
        # ------------------------------------------------------------
        # ImageRaw                  Annotation
        #    ->                         ->
        # DigitTile       =>        DigitTile
        # ************************************************************
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

        # ************************************************************
        # TODO 1-3. digitalize image input
        # ------------------------------------------------------------
        # ImageRaw                  Annotation
        #    |                          |
        # DigitLayerFake    =>      DigitTile
        # ************************************************************
        self.next_section(
            'focus on raw image input',
            skip_animations=True,
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
            skip_animations=True,
        )
        self.play(manager.animate.restore())
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'tranfrom dt1 (digit tile) -> dlf1 (fake digit layer)',
            skip_animations=False,
        )
        dlf1 = DigitLayerFake(
            n=3,
            width=image.width,
            height=image.height,
            buff=0.1,
        ).move_to(dt1)
        self.play(
            Transform(dt1, dlf1),
        )
        self.wait()

        # ************************************************************
        # TODO 1-4. digitalize annotation output
        # ------------------------------------------------------------
        # ImageRaw                  Annotation
        #    |                          |
        # DigitLayerFake    =>      DigitLayerFake
        # ************************************************************
        self.next_section(
            'focus on annotation',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 1-5. two preferences of modern AI
        # ------------------------------------------------------------
        #
        # ************************************************************

        # ************************************************************
        # TODO 1-6. redigitalize image input
        # ------------------------------------------------------------
        # IR   ->  IR                Ann  ->  Ann
        #  |        |                 |        |
        # DLF  ->  DLF  ->  DLF  =>  DLF  ->  DLF
        # ------------------------------------------------------------
        # IR                         Ann
        #      ->                ->
        #          DLF  =>  DLF
        # ************************************************************

        # ************************************************************
        # TODO 1-7. redigitalize annotation output
        #      reference of YOLO versions, including YOLO26
        # ------------------------------------------------------------
        # IR                                              Ann
        #      ->                                     ->
        #          DLF   =>  DLF*2  ->  DLF  ->  DLF
        # ************************************************************

        # ************************************************************
        # TODO 1-8. multi-layer annotation output
        # ------------------------------------------------------------
        # IR                                                      Ann
        #      ->           DLF*2  ->  DLF                    ->
        #          DLF  =>  DLF*2  ->  DLF  ->  DLF  ->  DLF
        #                   DLF*2  ->  DLF
        # ************************************************************

        # ************************************************************
        # FIXME 1-9. [visual thinking] VS [digital thinking]
        # ------------------------------------------------------------
        # IR  -> IR                                   Ann -> Ann
        #  |      |            DLF*2 -> DLF            |      |
        # DLF -> DLF -> DLF => DLF*2 -> DLF -> DLF -> DLF -> DLF
        #                      DLF*2 -> DLF
        # ------------------------------------------------------------
        # IR                                           Ann
        #      <pre>           DLF*2           <post>
        #             DLF  =>  DLF*2  ->  DLF
        #                      DLF*2
        # ************************************************************

        # ************************************************************
        # TODO 2-1. [tensor] [model/network] [module]
        # ------------------------------------------------------------
        #                                                     MC*2
        # MC    =>     MC    =>     MC    =>     MC    =>     MC*2
        #                                                     MC*2
        # ------------------------------------------------------------
        #                                                     MC*2
        # MC => mod => MC => mod => MC => mod => MC => mod => MC*2
        #                                                     MC*2
        # ************************************************************

        # ************************************************************
        # TODO 2-2. add / split / concat (multiple..)
        # ------------------------------------------------------------
        # MC
        #     -[add/sub/mul/div]->  MC
        # MC
        # ------------------------------------------------------------
        # MC                               MC
        #     -[concat]->  MC  -[split]->
        # MC                               MC
        # ************************************************************

        # ************************************************************
        # TODO 2-3. conv2d
        # ------------------------------------------------------------
        # MC  =[conv2d]=>  MC
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # TODO 2-4. MaxPool2d
        # ------------------------------------------------------------
        # MC  -[conv2d]->  MC
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # TODO 2-5. Upsample
        # ------------------------------------------------------------
        # MC  -[Upsample]->  MC
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # TODO 2-6. activation functions
        # ------------------------------------------------------------
        # MC  -[ReLU/SiLU/tanh/sigmoid/...]->  MC
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # TODO 2-7. Softmax
        # ------------------------------------------------------------
        # MC  -[Softmax]->  MC
        # ************************************************************

        # ************************************************************
        # TODO 2-8. Linear
        # ------------------------------------------------------------
        # MC  =[Linear]=>  MC
        # ************************************************************

        # ************************************************************
        # TODO 2-9. BatchNorm2d
        # ------------------------------------------------------------
        # MC  =[BatchNorm2d]=>  MC
        # ************************************************************

        # ************************************************************
        # TODO 3-1. Conv/CBS
        # ------------------------------------------------------------
        # MC  =[Conv/CBS]=>  MC
        # ************************************************************

        # ************************************************************
        # TODO 3-2. Bottleneck
        # ------------------------------------------------------------
        # MC  =[Bottleneck]=>  MC
        # ************************************************************

        # ************************************************************
        # TODO 3-3. C2f
        # ------------------------------------------------------------
        # MC  =[C2f]=>  MC
        # ************************************************************

        # ************************************************************
        # TODO 3-4. SPPF
        # ------------------------------------------------------------
        # MC  =[SPPF]=>  MC
        # ************************************************************

        # ************************************************************
        # TODO 3-5. Detect
        # ------------------------------------------------------------
        # MC               MC*2
        # MC  =[Detect]=>  MC*2
        # MC               MC*2
        # ************************************************************

        # ************************************************************
        # TODO 4-1. YOLOv8n network/model
        # ------------------------------------------------------------
        #                   MC*2
        # MC  =[YOLOv8n]=>  MC*2
        #                   MC*2
        # ------------------------------------------------------------
        # MC [Conv] [Conv] [C2f] ... [Detect] MC
        # ************************************************************

        # ************************************************************
        # TODO 4-2. preprocess -> inference(decode) -> postprocess
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # TODO 4-3. YOLOv8n inference
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # FIXME 4-4. insight into tensor, module, network/model
        # ------------------------------------------------------------
        # ************************************************************


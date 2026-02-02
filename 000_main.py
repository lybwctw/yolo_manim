from manim import *
from utils.yolo_annotation import YoloAnnotation
from utils.image_raw import ImageRaw
from utils.image_annotation import ImageAnnotation
from utils.arrow_qmark import ArrowQmark
from utils.digit_tile import DigitTile
from utils.digit_layer_fake import MDigitLayerFake, DigitLayerFake

image_path = None
label_path = None

# FIXME, ALOT OF examples to explain
class MainScene(Scene):
    def construct(self) -> None:
        # ************************************************************
        # TODO 1-1. introduce object detection problem
        # ------------------------------------------------------------
        # ImageRaw       ...>        annotation_final
        # ************************************************************
        self.next_section(
            'init assets',
            skip_animations=True,
        )
        manager = VGroup()
        image_raw = ImageRaw(image_path).scale(2.)
        annotation_final = ImageAnnotation(image_raw, label_path)
        aq1 = ArrowQmark(DOWN, LEFT).scale(.6).shift(LEFT*10)
        aq2 = ArrowQmark(UP, RIGHT).scale(.6).shift(RIGHT*10)
        aq3 = ArrowQmark(RIGHT, UP).scale(.6).shift(UP*.5)
        dt_input = DigitTile('一堆\n数字').shift(DOWN*10)
        dt_output = DigitTile('一堆\n数字').shift(DOWN*10)
        manager.add(
            *[image_raw, aq3, annotation_final]
        )

        # ------------------------------------------------------------
        self.next_section(
            'create centered image_raw and annotation_final',
            skip_animations=True,
        )
        # self.play(Write(image_raw))
        # self.play(Write(annotation_final))
        self.add(manager)
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'expand into image_raw -> annotation_final',
            skip_animations=True,
        )
        # manager.save_state()
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
        # ImageRaw                  annotation_final
        #    ->                         ->
        # DigitTile       ...>        DigitTile
        # ************************************************************
        self.next_section(
            'introduce digital game idea, the big map',
            skip_animations=True,
        )
        manager[1] = VMobject()
        manager.add(
            *[aq1, VMobject(), aq2],
            *[dt_input, aq3, dt_output],
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
            'maybe, realtime detection loop until demo image_raw/annotation_final',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 1-3. digitalize image_raw input
        # ------------------------------------------------------------
        # ImageRaw                   annotation_final
        #    |                           |
        # MDigitLayerFake    ...>      DigitTile
        # ************************************************************
        self.next_section(
            'focus on raw image_raw input',
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
            'reverse back from focused image_raw to the big map',
            skip_animations=True,
        )
        self.play(manager.animate.restore())
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'tranfrom mdlf_input_raw from dt to mdlf',
            skip_animations=False,
        )
        mdlf_input_raw = MDigitLayerFake(
            n=3,
            width=image_raw.width,
            height=image_raw.height,
            width_nominal=640,
            height_nominal=360,
            buff=0.1,
        ).move_to(dt_input)
        self.play(
            ReplacementTransform(dt_input, mdlf_input_raw),
        )
        self.wait()
        self.play(
            mdlf_input_raw.show_passing_flash(),
        )
        self.play(
            mdlf_input_raw.unwrite_shape_texts(),
        )
        self.wait()

        # ************************************************************
        # TODO 1-4. digitalize annotation_final output
        # ------------------------------------------------------------
        # ImageRaw                     annotation_final
        #    |                           |
        # MDigitLayerFake    ...>      DigitLayerFake
        # ************************************************************
        self.next_section(
            'focus on annotation_final',
            skip_animations=False,
        )
        manager.save_state()
        manager.generate_target()
        manager.target.arrange_in_grid(rows=3, cols=3, buff=6.)
        manager.target.shift(-manager.target[2].get_center())
        manager.target[2].scale(2.)
        self.play(MoveToTarget(manager))
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            '002_annotation_zoom, explain the concept of annotation_final',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'reverse back from focused annotation_final to the big map',
            skip_animations=False,
        )
        self.play(manager.animate.restore())
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'tranfrom dlf_output_final from dt to dlf',
            skip_animations=False,
        )
        dlf_output_final = DigitLayerFake(
            width=1.,
            height=1.5,
            width_nominal=5,
            height_nominal=8,
        ).move_to(dt_output)
        self.play(
            Transform(dt_output, dlf_output_final),
        )
        self.wait()
        self.play(
            dlf_output_final.show_passing_flash(),
        )
        self.play(
            dlf_output_final.unwrite_shape_texts(),
        )
        self.wait()

        # ************************************************************
        # TODO 1-5. two preferences of modern AI
        # ------------------------------------------------------------
        #
        # ************************************************************
        self.next_section(
            'the changing shapes of current input & output',
            skip_animations=False,
        )

        self.next_section(
            'the magnitude of current input & output',
            skip_animations=False,
        )

        self.next_section(
            'try fixing current design of input & output',
            skip_animations=False,
        )

        # ************************************************************
        # TODO 1-6. redesign image_raw input
        # ------------------------------------------------------------
        #  IR   ->   IR                   Ann  ->  Ann
        #  |         |                     |        |
        # MDLF  ->  MDLF  ->  MDLF  ...>  DLF  ->  DLF
        # ------------------------------------------------------------
        #  IR                                      Ann
        #          <prep>                    <post>
        #                     MDLF  ...>  DLF
        # ************************************************************
        image_repad = VMobject()
        mdlf_input_repad = VMobject()
        mdlf_input_norm = VMobject()
        annotation_repad = VMobject()
        dlf_output_repad = VMobject()
        
        self.next_section(
            'focus on image_raw and mdlf_input_raw',
            skip_animations=False,
        )

        self.next_section(
            'resize image_raw',
            skip_animations=False,
        )

        self.next_section(
            'resize mdlf_input_raw',
            skip_animations=False,
        )

        self.next_section(
            'pad image_raw',
            skip_animations=False,
        )

        self.next_section(
            'pad mdlf_input_raw',
            skip_animations=False,
        )

        self.next_section(
            'normalize mdlf_input_raw',
            skip_animations=False,
        )

        self.next_section(
            'simplify into preprocessing step',
            skip_animations=False,
        )

        self.next_section(
            'reverse back to the big map',
            skip_animations=False,
        )

        self.next_section(
            'introduce postprocess on dlf_output_final',
            skip_animations=False,
        )

        self.next_section(
            'fix shape and small mag after preprocessing',
            skip_animations=False,
        )

        # ************************************************************
        # TODO 1-7. redigitalize annotation_final output
        #      reference of YOLO versions, including YOLO26
        # ------------------------------------------------------------
        #  IR   ->   IR                               Ann  ->  Ann  ->  Ann
        #  |         |                                 |        |        |
        # MDLF  ->  MDLF  ->  MDLF  ...>  MDLF*2  ->  DLF  ->  DLF  ->  DLF
        # ------------------------------------------------------------
        #  IR                                                           Ann
        #          <prep>                                     <post>
        #                     MDLF  ...>  MDLF*2  ->  DLF
        # ************************************************************
        mdlf_output_32_box = VMobject()
        mdlf_output_32_cls = VMobject()
        dlf_output_32_decode = VMobject()
        annotation_32_decode = VMobject()

        self.next_section(
            'focus on annotation_repad and dlf_output_repad',
            skip_animations=False,
        )

        self.next_section(
            'focus on annotation_repad',
            skip_animations=False,
        )

        # ************************************************************
        # TODO 1-8. multi-layer annotation_final output
        # FIXME, explicitly contain the step of concat on 32/16/8?
        # ------------------------------------------------------------
        #  IR   ->   IR                                        Ann  ->  Ann
        #  |         |                     MDLF*2  ->  DLF      |        |
        # MDLF  ->  MDLF  ->  MDLF  ...>  MDLF*2  ->  DLF  ->  DLF  ->  DLF
        #                                MDLF*2  ->  DLF
        # ------------------------------------------------------------
        #  IR                                                           Ann
        #          <prep>                  MDLF*2  ->  DLF    <post>
        #                     MDLF  ...>  MDLF*2  ->  DLF
        #                                MDLF*2  ->  DLF
        # ************************************************************
        mdlf_output_16_box = VMobject()
        mdlf_output_16_cls = VMobject()
        dlf_output_16_decode = VMobject()
        annotation_16_decode = VMobject()

        mdlf_output_8_box = VMobject()
        mdlf_output_8_cls = VMobject()
        dlf_output_8_decode = VMobject()
        annotation_8_decode = VMobject()

        self.next_section(
            '',
            skip_animations=False,
        )

        # ************************************************************
        # FIXME 1-9. [visual thinking] VS [digital thinking]
        # ------------------------------------------------------------

        # ************************************************************
        # TODO 2-1. [tensor] [model/network] [module/layer] [parameter]
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


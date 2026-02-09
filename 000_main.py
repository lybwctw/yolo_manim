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
            'focus on image_raw input',
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
        # flash RGB background
        self.next_section(
            '001_rgb_input, explain the concept of RGB',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'back to the big map',
            skip_animations=True,
        )
        self.play(manager.animate.restore())
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'transform mdlf_input_raw from dt to mdlf',
            skip_animations=True,
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
            skip_animations=True,
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
            '002_annotation_output, concept of label output',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'back to the big map',
            skip_animations=True,
        )
        self.play(manager.animate.restore())
        self.wait()

        # ------------------------------------------------------------
        self.next_section(
            'transform dlf_output_final from dt to dlf',
            skip_animations=True,
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
        #   1. fix-shape
        #   2. small-mag
        # ------------------------------------------------------------
        #
        # ************************************************************
        self.next_section(
            'the changing shapes of current input & output',
            skip_animations=True,
        )

        self.next_section(
            'the magnitude of current input & output',
            skip_animations=True,
        )

        self.next_section(
            'try fixing current design of input & output',
            skip_animations=True,
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
        manager.save_state()
        manager.generate_target()
        manager.target.arrange_in_grid(rols=3,cols=3,col_widths=[10.,10.,10.])
        manager.target.shift(-manager.target[3].get_center())
        self.play(MoveToTarget(manager))
        self.wait()

        self.next_section(
            'int-view: append image_resize',
            skip_animations=True,
        )

        self.next_section(
            'data-view: append mdlf_input_resize',
            skip_animations=True,
        )

        self.next_section(
            'int-view: pad image_resize into image_repad',
            skip_animations=True,
        )

        self.next_section(
            'data-view: pad mdlf_input_resize into mdlf_input_repad',
            skip_animations=True,
        )

        self.next_section(
            'data-view: append mdlf_input_norm',
            skip_animations=True,
        )

        self.next_section(
            'the concept of preprocessing',
            skip_animations=True,
        )

        self.next_section(
            'int-view: prepend annotation_repad',
            skip_animations=True,
        )

        self.next_section(
            'data-view: prepend dlf_output_repad',
            skip_animations=True,
        )

        self.next_section(
            'changing raw input, good input, bad output',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 1-7. redesign output
        #      reference of YOLO versions, including YOLO26
        # ------------------------------------------------------------
        #  IR   ->   IR                    Ann*2  ->  Ann  ->  Ann  ->  Ann
        #  |         |                       |         |        |        |
        # MDLF  ->  MDLF  ->  MDLF  ...>  MDLF*2  ->  DLF  ->  DLF  ->  DLF
        # ------------------------------------------------------------
        #  IR                                                           Ann
        #          <prep>                                     <post>
        #                     MDLF  ...>  MDLF*2  ->  DLF
        # ************************************************************
        mdlf_output_32_box = VMobject()
        mdlf_output_32_cls = VMobject()
        dlf_output_32_decode = VMobject()
        annotation_32_box = VMobject()
        annotation_32_cls = VMobject()
        annotation_32_decode = VMobject()

        # ------------------------------------------------------------
        self.next_section(
            'focus on annotation_repad and dlf_output_repad',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'focus on annotation_repad, the filter thinking',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '003_DFL_output, explain the output design of YOLO',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '004_DFL_decode, explain the decode of model output',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'both-view: prepend 32_box, 32_cls, 32_decode',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '005_postprocess, best class -> conf -> iou -> max_det',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 1-8. multi-layer annotation_final output
        # FIXME, explicitly contain the step of concat on 32/16/8?
        # ------------------------------------------------------------
        #  IR   ->   IR                    ...                 Ann  ->  Ann
        #  |         |                     MDLF*2  ->           |        |
        # MDLF  ->  MDLF  ->  MDLF  ...>  MDLF*2  ->  DLF  ->  DLF  ->  DLF
        #                                MDLF*2  ->
        # ------------------------------------------------------------
        #  IR                                                           Ann
        #          <prep>                  MDLF*2  ->         <post>
        #                     MDLF  ...>  MDLF*2  ->  DLF
        #                                MDLF*2  ->
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
            '006_DFL_output_m, multi-layer output',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '007_DFL_decode_m, multi-layer decode',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            '008_postprocess, multi-layer postprocess',
            skip_animations=True,
        )

        # ************************************************************
        # FIXME 1-9. recap, focus on the most important part
        # ------------------------------------------------------------
        #  IR                                                           Ann
        #          <prep>                  MDLF*2  ->         <post>
        #                     MDLF  ...>  MDLF*2  ->  DLF
        #                                MDLF*2  ->
        # ------------------------------------------------------------
        #                                  MDLF*2  ->
        #                     MDLF  ...>  MDLF*2  ->  DLF
        #                                MDLF*2  ->
        # ************************************************************
        self.next_section(
            'recap on the details of inference',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'recap on the simplified version of inference',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'focus on the most important part',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-1. tensor, module, parameter, model
        # ************************************************************

        self.next_section(
            'tensor, 1d/2d/3d/4d, dim/shape/value',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'module/layer/block/function',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'parameters in module',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'model/network',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-2. operations
        # ************************************************************
        self.next_section(
            'add operation',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'sub, mul, div',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'split',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'concat',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-3. conv2d
        # ------------------------------------------------------------
        # MC  =[conv2d]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on conv2d',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'conv2d on 2d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'params, FLOPs, as comments by default',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option1: kernel size',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option2: stride',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option3: padding',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option4: bias',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option5: in_channels, conv2d on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option6: out_channels',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'quick reference on other options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with pytorch, init',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'extension: conv1d, 1d input -> 2d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'extension: conv3d, 3d input -> 4d input',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-4. Linear
        # ------------------------------------------------------------
        # MC  =[Linear]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on linear',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'linear on 1d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option1: in_features',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option2: out_features',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option2: bias',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'linear on 2d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'linear on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'linear vs 1x1 conv2d',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-5. MaxPool2d
        # ------------------------------------------------------------
        # MC  -[conv2d]->  MC
        # ************************************************************
        self.next_section(
            'prologue on maxpool2d',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'maxpool2d on 2d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option1: kernel size',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option2: stride',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option3: padding',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'maxpool2d on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'quick reference on other options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with pytorch',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'extension: avgpool, minpool',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'extension: conv1d, 1d input -> 2d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'extension: conv3d, 3d input -> 4d input',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-6. Upsample
        # ------------------------------------------------------------
        # MC  -[Upsample]->  MC
        # ************************************************************
        self.next_section(
            'prologue on upsample',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'upsample on 2d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'option1: scale_factor',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'maxpool2d on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'quick reference on other options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with pytorch',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-7. activation functions
        # ------------------------------------------------------------
        # MC  -[ReLU/SiLU/tanh/sigmoid/.../Softmax]->  MC
        # ************************************************************
        self.next_section(
            'prologue on activation functions',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'ReLU on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'SiLU on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'tanh on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'sigmoid on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'quick reference on other options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'Softmax on 1d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'Softmax on 2d input, dim',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'Softmax on 3d input, dim',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-8. BatchNorm2d
        # ------------------------------------------------------------
        # MC  =[BatchNorm2d]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on BatchNorm2d',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'batchnorm2d on 3d input',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with pytorch, init',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 2-9. PyTorch assets, version related
        # ************************************************************

        # ************************************************************
        # TODO 3-1. Conv/CBS
        # ------------------------------------------------------------
        # MC  =[Conv/CBS]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on Conv/CBS',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'components',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with ultralytics',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'showcase',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 3-2. Bottleneck
        # ------------------------------------------------------------
        # MC  =[Bottleneck]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on Bottleneck',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'components',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with ultralytics',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'showcase',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 3-3. C2f
        # ------------------------------------------------------------
        # MC  =[C2f]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on C2f',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'components',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with ultralytics',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'showcase',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 3-4. SPPF
        # ------------------------------------------------------------
        # MC  =[SPPF]=>  MC
        # ************************************************************
        self.next_section(
            'prologue on SPPF',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'components',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with ultralytics',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'showcase',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 3-5. Detect
        # ------------------------------------------------------------
        # MC               MC*2
        # MC  =[Detect]=>  MC*2
        # MC               MC*2
        # ************************************************************
        self.next_section(
            'prologue on Detect head',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'components',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'options',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'interacting with ultralytics',
            skip_animations=True,
        )

        # ------------------------------------------------------------
        self.next_section(
            'showcase',
            skip_animations=True,
        )

        # ************************************************************
        # TODO 3-6. Ultralytics module assets, version related
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
        # TODO 4-3. interacting with Ultralytics: YOLOv8n inference
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # TODO 4-4. Ultralytics model assets, version related
        # ------------------------------------------------------------
        # ************************************************************

        # ************************************************************
        # FIXME 4-5. insight into tensor, module, network/model
        # ------------------------------------------------------------
        # ************************************************************


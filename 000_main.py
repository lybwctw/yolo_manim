from manim import *

from utils.yolo_annotation import YoloAnnotation


# Entry point of whole project
# also learning of git
# TODO
# start with one frame
# pretend to run video detection
# stop at good example for demo

class ImageFromArray(MovingCameraScene):
    def construct(self):
        ##############################################################################################
        self.next_section('the start of animation', skip_animations=False)
        class_map = {0: 'kunkun', 1: 'coke', 2: 'pepsi'}
        color_map = {0: YELLOW, 1: PURE_RED, 2: PURE_BLUE}
        # FIXME, replace source image with >3 targets (3 classes)
        image_path = r'assets/images/sample_640_360.jpg'
        label_path = r'assets/images/labels.txt'

        image = ImageMobject(image_path)
        image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        image.set_z_index(1)
        image.scale_to_fit_height(3)

        data = np.loadtxt(label_path)
        cls = data[:,0].astype(int).tolist()
        xywh = data[:, 1:5]
        annos = VGroup(
            YoloAnnotation(
                source=image,
                xywh=t,
                text=class_map[c],
                label_bg=color_map[c],
                label_color=BLACK,
            ) for c, t in zip(cls, xywh)
        ).set_z_index(2)

        ##############################################################################################
        self.next_section('show image with annotations', skip_animations=False)
        self.play(FadeIn(image))
        self.wait()

        # show annotation
        # TODO, kunkun should be on top
        self.play(Write(annos))
        self.wait()

        ##############################################################################################
        self.next_section('create ? on arrow', skip_animations=False)
        arrow = Arrow(start=LEFT, end=RIGHT)
        qmark = Text('?', font='JetBrains Mono').next_to(arrow, UP)
        qmark_on_arrow = VGroup(arrow, qmark)

        ##############################################################################################
        self.next_section('split image, arrow, annotation', skip_animations=False)
        annos_bg = image.copy().set_opacity(0.2).set_z_index(0)
        annos.suspend_updating()
        # annos.source = annos_bg
        annos_vg = Group(annos_bg, annos)
        # FIXME, arrange would not align input and output along the button
        self.play(Group(image, qmark_on_arrow, annos_vg).animate.arrange())
        self.wait()

        ##############################################################################################
        self.next_section('shift out arrow and annotation', skip_animations=False)
        self.play(AnimationGroup(
            image.animate.center(),
            annos_vg.animate.shift(RIGHT*10),
            qmark_on_arrow.animate.shift(RIGHT*10),
        ))
        self.wait()

        ##############################################################################################
        # color -> values
        #   001_image_zoom
        #   002_show_grid
        #   003_a_RGB
        #   003_b_RGB

        ##############################################################################################
        self.next_section('shift in arrow and annotation', skip_animations=False)
        self.play(Group(image, qmark_on_arrow, annos_vg).animate.arrange())
        self.wait()

        ##############################################################################################
        self.next_section('transform input image into grid', skip_animations=False)
        layers_vg = VGroup(
            Rectangle(
                fill_color=BLACK,
                fill_opacity=0.8,
                height=image.height,
                width=image.width,
                stroke_width=2,
                grid_xstep=0.08,
                grid_ystep=0.08,
                grid_stroke_width=1,
            ).set_z_index(3 - i) for i in range(3)
        ).move_to(image)
        self.play(AnimationGroup(
            FadeOut(image),
            FadeIn(layers_vg),
        ))
        self.wait()

        ##############################################################################################
        # TODO, bit of overshot thus more vibrant?
        self.next_section('transform grid into rgb layers', skip_animations=False)
        self.play(AnimationGroup(
            layers_vg[0].animate.set_fill(color=RED, opacity=0.5).shift((DOWN + LEFT) * .1),
            layers_vg[1].animate.set_fill(color=GREEN, opacity=0.5),
            layers_vg[2].animate.set_fill(color=BLUE, opacity=0.5).shift((UP + RIGHT) * .1),
        ))
        self.wait()

        ##############################################################################################
        self.next_section('shift out input+arrow towards left', skip_animations=False)
        self.play(AnimationGroup(
            annos_vg.animate.center(),
            layers_vg.animate.shift(LEFT * 10),
            qmark_on_arrow.animate.shift(LEFT * 10),
        ))
        self.wait()

        ##############################################################################################
        # self.next_section('show axis', skip_animations=False)
        # # 00? explanation of annotation
        # sq = Square()
        # self.play(Create(sq))
        # self.wait()

        ##############################################################################################
        self.next_section('shift in input+arrow', skip_animations=False)
        self.play(Group(layers_vg, qmark_on_arrow, annos_vg).animate.arrange())
        self.wait()
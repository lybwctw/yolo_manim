from manim import *
from utils.explainer import Explainer
from utils.image_pad import ImagePad

class Demo(ThreeDScene):
    def construct(self):
        background = ImagePad(padded=True).scale(1.0).set_opacity(0.2)
        explainer = Explainer.from_file(
            background=background,
            version=32,
        )
        system = Group(background, explainer)

        self.add(system)
        self.wait()

        self.play(explainer.show_anchor_points())
        self.wait()

        self.play(explainer.to_rects())
        self.wait()

        # self.play(explainer.show_multi_labels(
        #     label_config={'font_size': 8},
        # ))
        # self.wait()

        # explainer.apply_max_select(
        #     self,
        #     run_time_ratio=0.1,
        # )
        # self.wait()

        # # explainer.apply_conf_filter(
        # #     self,
        # #     conf_thresh=0.9,
        # #     run_time_ratio=0.1,
        # # )
        # # self.wait()

        # # # explainer.show_3d_aps(
        # # #     self,
        # # #     run_time_ratio=0.5,
        # # # )
        # # # self.wait()

        # # # change view point
        # # GAP = 3.0
        # # self.move_camera(
        # #     phi=45*DEGREES,
        # #     theta=-180*DEGREES,
        # #     gamma=-90*DEGREES,
        # #     run_time=0.5,
        # #     added_anims=[
        # #         system.animate.shift(IN*GAP),
        # #     ],
        # # )
        # # self.wait(0.5)

        # # # show target background
        # # target_bg = Rectangle(
        # #     width=background.width,
        # #     height=background.height,
        # #     stroke_width=3,
        # #     stroke_color=WHITE,
        # #     fill_color=BLACK,
        # #     fill_opacity=0.0,
        # #     # shade_in_3d=True,
        # # ).move_to(background, aligned_edge=UL)
        # # # target_bg.set_z_index(1)
        # # self.play(Write(target_bg))
        # # self.play(target_bg.animate(
        # #     run_time=0.5,
        # # ).shift(OUT*GAP*2))
        # # self.wait()

        # # for cls in range(3):
        # #     explainer.apply_nms_filter(
        # #         self,
        # #         cls=cls,
        # #         iou_thresh=0.05,
        # #         offset=GAP*2,
        # #         run_time_ratio=0.5,
        # #     )
        # #     self.wait(0.5)
        # # # explainer.apply_nms_filter(
        # # #     self,
        # # #     cls=-1,
        # # #     iou_thresh=0.05,
        # # #     offset=GAP*2,
        # # #     run_time_ratio=0.5,
        # # # )
        # # # self.wait(0.5)

        # # # change view back
        # # self.play(Unwrite(target_bg))
        # # self.wait(0.5)
        # # self.move_camera(
        # #     phi=0*DEGREES,
        # #     theta=-90*DEGREES,
        # #     gamma=0*DEGREES,
        # #     run_time=0.5,
        # #     added_anims=[
        # #         system.animate.shift(OUT*GAP),
        # #     ],
        # # )
        # # self.wait(0.5)
from manim import *
from utils.constants import *
from utils.general import load_everything, scale_manager_target, save_everything
from utils.image_annotation import ImageAnnotation
from utils.arrow_comment import ArrowComment
from utils.layers_fake import LayersFake
from utils.tile_comment import TileComment
from utils.image_repad import ImageRaw

class MainScene(Scene):
    def construct(self) -> None:
        # the loaded image_raw is of type ImageMobject instead of ImageRaw
        (
            _image_raw_ref,
        ) = load_everything(S004_EVERYTHING)
        image_raw = ImageRaw(PATH_IMAGE_640)
        image_raw.scale_to_fit_width(_image_raw_ref.width).move_to(_image_raw_ref)
        annotation_final = ImageAnnotation(
            image=PATH_IMAGE_640,
            label=PATH_LABEL_640,
            name_map=KK_NAME_MAP,
            color_map=KK_COLOR_MAP,
            transparent=True,
            width_nominal=960,
            height_nominal=540,
        ).scale_to_fit_width(image_raw.width)
        tile_output = TileComment('一堆数字').scale(0.8)

        ac_a1 = ArrowComment(True, DOWN, '?')
        ac_z9 = ArrowComment(True, DOWN, '?')
        ac_game = ArrowComment(False, RIGHT, '?')

        lf_image_raw = LayersFake(
            3,
            width=image_raw.width,
            height=image_raw.height,
            width_nominal=960,
            height_nominal=540,
        ).scale(0.9)   # to be fully covered by image_raw


        everything = Group(
            image_raw,
            annotation_final,
            ac_a1, ac_z9,
            ac_game,
        )

        # ************************************************************
        self.next_section(
            'starting image_raw',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[lf_image_raw, ac_a1, image_raw],
        )
        self.add(manager)
        self.wait()

        # ************************************************************
        self.next_section(
            'generate lf_image_raw from image_raw and show shapes',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[lf_image_raw, ac_a1, image_raw],
        )
        manager.generate_target()
        scale_manager_target(
            manager,
            everything,
            scale=0.7,
        )
        manager.target.arrange_in_grid(
            rows=3,
            cols=1,
            flow_order='ru',
            buff=0.35
        )

        # generate lf_image_raw from image_raw
        self.play(MoveToTarget(manager))
        self.wait()
        self.play(lf_image_raw.expand())
        self.wait()

        # show shapes of lf_image_raw and image_raw
        self.play(AnimationGroup(
            image_raw.show_passing_flash(),
            lf_image_raw.show_passing_flash(),
            ac_a1.animate.set_opacity(0.1),
        ))
        self.wait()

        # TODO, fast switching of image_raw and lf_image_raw
        # cool frames, throw slow motion
        # frames from a clip, frames from another clip, ...
        # back to the first one finally

        # unwrite shape texts
        self.play(Succession(
            AnimationGroup(
                image_raw.unwrite_shape_texts(),
                lf_image_raw.unwrite_shape_texts(),
            ),
            ac_a1.animate.set_opacity(1.0),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'shift in annotation_final and tile_output',
            skip_animations=False,
        )
        # ************************************************************
        # prepare those will be shift in
        annotation_final.shift(RIGHT*10)
        ac_z9.shift(RIGHT*10)
        ac_game.shift(RIGHT*10)
        tile_output.shift(RIGHT*10)

        manager = Group(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[lf_image_raw, ac_game, tile_output],
        )
        manager.generate_target()
        scale_manager_target(
            manager,
            everything,
            scale=0.8,
        )
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'focus on annotation_final',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[lf_image_raw, ac_game, tile_output],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        manager.target.shift(-manager.target[2].get_center())
        manager.target[2].scale(2.0)
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene, explain annotation concept',
            skip_animations=False,
        )
        # ************************************************************
        save_everything(S005_EVERYTHING, everything)
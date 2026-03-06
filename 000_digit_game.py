from manim import *
from utils.constants import *
from utils.image_repad import ImageRaw, ImageRepad
from utils.tile_comment import TileComment
from utils.arrow_comment import ArrowComment
from utils.image_annotation import ImageAnnotation
from utils.general import save_everything, load_everything, scale_manager_target

class MainScene(Scene):
    def construct(self) -> None:
        image_raw = ImageRaw(PATH_IMAGE_640)
        tile_input = TileComment('一堆数字')
        annotation_final = ImageAnnotation(
            image=PATH_IMAGE_640,
            label=PATH_LABEL_640,
            name_map=KK_NAME_MAP,
            color_map=KK_COLOR_MAP,
        ).scale_to_fit_width(image_raw.width)
        tile_output = TileComment('一堆数字')

        ac_a1 = ArrowComment(True, DOWN, '?')
        ac_z9 = ArrowComment(True, DOWN, '?')
        ac_game = ArrowComment(False, RIGHT, '?')

        everything = Group(
            image_raw, tile_input,
            annotation_final, tile_output,
            ac_a1, ac_z9,
            ac_game,
        )
        # ************************************************************
        self.next_section(
            'overlapped image_raw and annotation_final',
            skip_animations=False,
        )
        # ************************************************************
        image_raw.center()
        annotation_final.center()
        ac_game.center()

        manager = Group(
            *[image_raw, ac_game, annotation_final],
        ).center()

        self.add(manager)
        self.wait()

        # ************************************************************
        self.next_section(
            'split image_raw and annotation_final',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[image_raw, ac_game, annotation_final],
        )
        manager.generate_target()
        scale_manager_target(
            manager,
            everything,
            scale=0.6,
        )
        manager.target.arrange_in_grid(
            rows=1,
            cols=3,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'introduce tile_input and tile_output',
            skip_animations=False,
        )
        # ************************************************************
        ac_a1.move_to(image_raw)
        ac_z9.move_to(annotation_final)
        tile_input.move_to(image_raw)
        tile_output.move_to(annotation_final)
        manager = Group(
            *[tile_input, ac_game, tile_output],
            *[ac_a1, VMobject(), ac_z9],
            *[image_raw, VMobject(), annotation_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            flow_order='ru',
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'focus on image_raw, save scale factor',
            skip_animations=False,
        )
        # ************************************************************
        manager = Group(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[tile_input, ac_game, tile_output],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            buff=10.0,
        )
        manager.target.shift(-manager.target[0].get_center())
        manager.target[0].scale(2.0)
        self.play(MoveToTarget(manager))
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene, explain RGB color space',
            skip_animations=False,
        )
        # ************************************************************
        save_everything(S000_EVERYTHING, everything)
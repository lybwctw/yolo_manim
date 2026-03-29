from manim import *
from utils.constants import *
from utils.arrow_comment import ArrowComment
from utils.general import load_everything, save_everything
from utils.layers_fake import LayersFake

class MainScene(Scene):
    def construct(self) -> None:
        # load from s005 and s006
        (
            annotation_old,
            cmap,
            table_xywh,
        ) = load_everything(S006_EVERYTHING)
        (
            image_raw,
            annotation_final,
            ac_a1, ac_z9,
            lf_image_raw, ac_game, tile_output,
        ) = load_everything(S005_EVERYTHING)

        manager = Group(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[lf_image_raw, ac_game, tile_output],
        )
        annotation_final.align_to(annotation_old.image, UL)    # FIXME, not robust
        self.add(manager, cmap, table_xywh)
        self.wait()

        manager.generate_target()
        manager.target[2].scale(0.5)
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        manager.target[7].shift(RIGHT*.4)   # FIXME, adjust ac_game in previous scene
        self.play(AnimationGroup(
            MoveToTarget(manager),
            Unwrite(cmap, lag_ratio=0, run_time=0.6,),
            Unwrite(table_xywh, lag_ratio=0, run_time=0.6,),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'introduce lf_output_final',
            skip_animations=False,
        )
        # ************************************************************
        lf_output_final = LayersFake(
            1,
            width=1.0,
            height=0.8,
            width_nominal=5,
            height_nominal='n',
        ).scale(1.0)
        lf_output_final.shift(RIGHT*10+DOWN*1.5)

        manager = Group(
            *[image_raw, VMobject(), annotation_final],
            *[ac_a1, VMobject(), ac_z9],
            *[lf_image_raw, ac_game, lf_output_final],
        )
        manager.generate_target()
        manager.target.arrange_in_grid(
            rows=3,
            cols=3,
            # buff=1.0,
        ).center()
        manager.target[7].shift(RIGHT*.4)   # adjust ac_game

        self.play(AnimationGroup(
            MoveToTarget(manager),
            tile_output.animate.shift(DOWN*10),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'show input shapes and output shapes',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            ac_a1.animate.set_opacity(0.1),
            ac_z9.animate.set_opacity(0.1),
            ac_game.animate.set_opacity(0.1),
            lf_image_raw.show_passing_flash(),
            lf_output_final.show_passing_flash(),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'loop through same input, different output',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'loop through different input',
            skip_animations=False,
        )
        # ************************************************************

        # ************************************************************
        self.next_section(
            'make big map clean',
            skip_animations=False,
        )
        # ************************************************************
        self.play(Succession(
            AnimationGroup(
                lf_image_raw.unwrite_shape_texts(),
                lf_output_final.unwrite_shape_texts(),
            ),
            AnimationGroup(
                ac_a1.animate.set_opacity(1.0),
                ac_z9.animate.set_opacity(1.0),
                ac_game.animate.set_opacity(1.0),
            )
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'focus on input',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            annotation_final.animate.shift(RIGHT*10),
            ac_z9.animate.shift(RIGHT*10),
            ac_game.animate.shift(RIGHT*10),
            lf_output_final.animate.shift(RIGHT*10),
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'save for next scene',
            skip_animations=False,
        )
        # ************************************************************
        everything = Group(
            image_raw, annotation_final,
            ac_a1, ac_z9,
            lf_image_raw, ac_game, lf_output_final,
        )
        save_everything(S007_EVERYTHING, everything)
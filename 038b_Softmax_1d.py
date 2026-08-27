from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import *
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
import torch
import numpy as np

EMPTY_CONFIG = {
    'dim': UNKNOWN,
}

INIT_CONFIG = {
    'dim': 0,
}

FONT_SIZE_ANNO = 24
FONT_SIZE_TICK = 16

TENSOR_VGAP_1D = 1.0
TENSOR_HGAP_1D = 1.0

COLOR_SOURCE = GREEN
COLOR_TARGET = RED

wt = 0.5

class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('038a')

        # raw module
        torch_module = torch.nn.Softmax(**INIT_CONFIG)

        # raw 1d tensor
        t_i1 = -5 + 10 * torch.rand(6)
        t_o1 = torch_module(t_i1)
        arr_i1 = t_i1.detach().numpy()
        arr_o1 = t_o1.detach().numpy()

        # input tensor mob
        mob_i1 = MTensor1D(
            array=t_i1.detach(),
            style='horizontal',
            mode='card',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_1D,
            DOWN,
        )

        # output tensor mob
        mob_o1 = MTensor1D(
            array=t_o1.detach(),
            style='horizontal',
            mode='card',
            **MEDIUM_TENSOR_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_1D,
            UP,
        )

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_TOP,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'starting module card',
            skip_animations=True,
        )
        # ************************************************************
        # expand empty module card
        self.play(card_module.expand_params(
            params=EMPTY_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # update module card config
        self.play(card_module.update_params(
            INIT_CONFIG,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'show input tensor',
            skip_animations=True,
        )
        # ************************************************************
        self.play(mob_i1.create(
            style='series',
            direction=RIGHT,
            run_time=wt,
        ))

        # show input summary
        card_i1 = InfoCard('in_1').hide_to_corner(UP)
        self.add_fixed_in_frame_mobjects(card_i1)
        self.play(attach_to_ref(
            card_i1,
            card_module,
            UP,
            run_time=wt,
        ))
        self.play(card_i1.expand_summary(
            t2s(t_i1.detach()),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'from formula to output',
            skip_animations=True,
        )
        # ************************************************************
        # assets
        formula = MathTex(
            r"y_i = \frac{e^{x_i}}{\sum_j e^{x_j}}",
            font_size=FONT_SIZE_ANNO,
        ).center()
        denominator = "+".join(
            f"e^{{{value:+.2f}}}" for value in arr_i1
        )

        # introduce formula
        self.play(Write(formula))
        self.wait(wt)

        for index, (input_value, output_value) in enumerate(
            zip(arr_i1, arr_o1)
        ):
            # target equation
            equation = MathTex(
                rf"y_{{{index+1}}} = "
                rf"\frac{{e^{{{input_value:+.2f}}}}}{{{denominator}}}"
                rf" = {output_value:.2f}",
                font_size=FONT_SIZE_ANNO,
            ).move_to(formula)

            if index == 0:
                self.play(Transform(
                    formula,
                    equation,
                    run_time=wt,
                ))
            else:
                self.play(Transform(
                    formula,
                    equation,
                    run_time=wt,
                ))
    
            self.play(GrowFromCenter(
                mob_o1[index],
                rate_func=rate_functions.ease_out_back,
                run_time=wt,
            ))
        self.wait(wt)

        # show output summary
        card_o1 = InfoCard('out_1').hide_to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(card_o1)
        self.play(attach_to_ref(
            card_o1,
            card_module,
            DOWN,
            run_time=wt,
        ))
        self.play(card_o1.expand_summary(
            t2s(t_o1.detach()),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean formula and make space in the right',
            skip_animations=True,
        )
        # ************************************************************
        # remove formula and make tensors closer
        mobs = VGroup(mob_i1, mob_o1)
        self.play(AnimationGroup(
            Unwrite(formula),
            mobs.animate.arrange(DOWN, buff=TENSOR_VGAP_1D),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # make space in the right
        self.play(mobs.animate(
            run_time=wt,
        ).align_to(
            LEFT*TENSOR_HGAP_1D*0.5,
            RIGHT,
        ))
        self.wait(wt)

        # change stroke color for tensors
        self.play(AnimationGroup(
            mob_i1.animate.set_stroke(color=COLOR_SOURCE),
            mob_o1.animate.set_stroke(color=COLOR_TARGET),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'plot explanation',
            skip_animations=True,
        )
        # ************************************************************
        # assets
        axes = Axes(
            x_range=[-0.5, len(arr_i1) - 0.5, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=3,
            axis_config={
                'include_numbers': False,
                'include_ticks': False,
            },
            tips=False,
        )
        axes.y_axis.set_opacity(0)
        one_line = DashedLine(
            axes.c2p(-0.5, 1),
            axes.c2p(len(arr_i1) - 0.5, 1),
            color=GRAY,
            dash_length=0.12,
            stroke_width=2.0,
        )
        ticks = VGroup(*(
            Line(
                axes.c2p(index, 0) + DOWN * 0.1,
                axes.c2p(index, 0) + UP * 0.1,
                stroke_width=2,
            )
            for index in range(len(arr_i1))
        ))
        source_dots = VGroup(*(
            Dot(
                axes.c2p(index, value),
                radius=0.05,
                color=COLOR_SOURCE,
            )
            for index, value in enumerate(arr_i1)
        ))
        source_lines = VGroup(*(
            Line(
                source_dots[index].get_center(),
                source_dots[index + 1].get_center(),
                color=COLOR_SOURCE,
                stroke_width=2.0,
                stroke_opacity=0.5,
            )
            for index in range(len(source_dots) - 1)
        ))
        target_dots = VGroup(*(
            Dot(
                axes.c2p(index, value),
                radius=0.05,
                color=COLOR_TARGET,
            )
            for index, value in enumerate(arr_o1)
        ))
        target_lines = VGroup(*(
            Line(
                target_dots[index].get_center(),
                target_dots[index + 1].get_center(),
                color=COLOR_TARGET,
                stroke_width=2.0,
                stroke_opacity=0.5,
            )
            for index in range(len(target_dots) - 1)
        ))
        plot = VGroup(
            axes,
            one_line,
            ticks,
            source_lines,
            source_dots,
            target_lines,
            target_dots,
        ).align_to(
            RIGHT*TENSOR_HGAP_1D*0.5,
            LEFT,
        )

        # show input plot
        self.play(Succession(
            Create(axes),
            Create(one_line),
            Create(ticks),
            run_time=wt,
        ))
        self.play(AnimationGroup(
            Create(source_lines),
            LaggedStart(
                *(GrowFromCenter(dot) for dot in source_dots),
                lag_ratio=0.12,
            ),
            run_time=wt,
        ))
        self.wait(wt)

        # generate output plot
        self.play(AnimationGroup(
            *(
                TransformFromCopy(line, target_line)
                for line, target_line in zip(source_lines, target_lines)
            ),
            *(
                TransformFromCopy(dot, target_dot)
                for dot, target_dot in zip(source_dots, target_dots)
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through samples',
            skip_animations=True,
        )
        # ************************************************************
        for _ in range(1):
            # new assets
            t_i1 = -5 + 10 * torch.rand(6)
            t_o1 = torch_module(t_i1)
            arr_i1 = t_i1.detach().numpy()
            arr_o1 = t_o1.detach().numpy()
            new_source_lines = VGroup(*(
                Line(
                    axes.c2p(index, value),
                    axes.c2p(index + 1, arr_i1[index + 1]),
                    color=COLOR_SOURCE,
                    stroke_width=2.0,
                    stroke_opacity=0.5,
                )
                for index, value in enumerate(arr_i1[:-1])
            ))
            new_target_lines = VGroup(*(
                Line(
                    axes.c2p(index, value),
                    axes.c2p(index + 1, arr_o1[index + 1]),
                    color=COLOR_TARGET,
                    stroke_width=2.0,
                    stroke_opacity=0.5,
                )
                for index, value in enumerate(arr_o1[:-1])
            ))

            # new input output for tensor view
            self.play(mob_i1.update_values(
                t_i1,
                run_time=wt,
            ))
            self.play(mob_o1.update_values(
                t_o1,
                run_time=wt,
            ))

            # new input output for plot view
            self.play(AnimationGroup(
                *(dot.animate.move_to(axes.c2p(index, value))
                for index, (dot, value) in enumerate(
                    zip(source_dots, arr_i1)
                )),
                *(Transform(line, new_line)
                for line, new_line in zip(
                    source_lines, new_source_lines
                )),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.play(AnimationGroup(
                *(dot.animate.move_to(axes.c2p(index, value))
                for index, (dot, value) in enumerate(
                    zip(target_dots, arr_o1)
                )),
                *(Transform(line, new_line)
                for line, new_line in zip(
                    target_lines, new_target_lines
                )),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

        # ************************************************************
        self.next_section(
            'remove plot and new perspective',
            skip_animations=False,
        )
        # ************************************************************
        # remove plot
        self.play(Unwrite(plot, run_time=wt))
        self.wait(wt)

        # restore tensors
        self.play(AnimationGroup(
            mob_i1.animate.set_stroke(WHITE).set_x(0),
            mob_o1.animate.set_stroke(WHITE).set_x(0),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # new view and more gap
        mobs = VGroup(mob_i1, mob_o1)
        self.move_camera(
            **VIEW_COMPUTE,
            added_anims=[
                mobs.animate.arrange(
                    DOWN,
                    buff=TENSOR_VGAP_1D*2,
                ),
            ],
            run_time=wt*2,
        )

        # cube mode
        self.play(AnimationGroup(
            mob_i1.switch(
                style='series',
                direction=RIGHT,
            ),
            mob_o1.switch(
                style='series',
                direction=RIGHT,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'sample input/output shapes',
            skip_animations=False,
        )
        # ************************************************************
        for tsize in [8, 11, 15]:
            # clean input/output
            self.play(AnimationGroup(
                *(AnimationGroup(
                    tmob.uncreate(
                        style='series',
                        direction=RIGHT,
                        anim=Unwrite,
                    ),
                    cmob.shrink_summary(),
                    lag_ratio=0.5,
                ) for tmob, cmob in zip(
                    [mob_i1, mob_o1],
                    [card_i1, card_o1],
                )),
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

            # new tensor
            t_i1 = torch.randn(tsize)
            t_o1 = torch_module(t_i1)
            mob_i1 = MTensor1D(
                array=t_i1.detach(),
                style='horizontal',
                **MEDIUM_TENSOR_CONFIG,
            )
            mob_o1 = MTensor1D(
                array=t_o1.detach(),
                style='horizontal',
                **MEDIUM_TENSOR_CONFIG,
            )
            VGroup(mob_i1, mob_o1).arrange(
                DOWN,
                TENSOR_VGAP_1D*2,
            )

            # show new input
            self.play(AnimationGroup(
                mob_i1.create(
                    style='series',
                    direction=RIGHT,
                ),
                card_i1.expand_summary(
                    t2s(t_i1.detach()),
                ),
                lag_ratio=0.5,
                run_time=wt,
            ))
            # self.wait(wt)

            # show new output
            self.play(AnimationGroup(
                mob_o1.create(
                    style='series',
                    direction=RIGHT,
                ),
                card_o1.expand_summary(
                    t2s(t_o1.detach()),
                ),
                lag_ratio=0.5,
                run_time=wt,
            ))
            self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean input/output',
            skip_animations=False,
        )
        # ************************************************************
        # clean input/output
        self.play(AnimationGroup(
            *(AnimationGroup(
                tmob.uncreate(
                    style='series',
                    direction=RIGHT,
                    anim=Unwrite,
                ),
                cmob.shrink_summary(),
                lag_ratio=0.5,
            ) for tmob, cmob in zip(
                [mob_i1, mob_o1],
                [card_i1, card_o1],
            )),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_i1,
            card_module,
            card_o1,
        )
        export_mobs(__file__, mobs)     # NOTE: used by next
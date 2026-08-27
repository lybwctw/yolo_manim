from manim import *

from utils.general import import_mobs, export_mobs
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *

FONT_SIZE_ANNO = 20
FONT_SIZE_TICK = 16

wt = 1.0

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('035a')

        # show initial card
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'Sigmoid function',
            skip_animations=False,
        )
        # ************************************************************
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=4.5,
            y_length=4.5,
            axis_config={
                "include_numbers": True,
                'font_size': FONT_SIZE_TICK,
                'tip_width': 0.2,
                'tick_size': 0.03,
                'line_to_number_buff': 0.15,
            },
        )
        graph = axes.plot(
            sigmoid,
            x_range=[-5, 4.5],
            color=MAROON,
            stroke_width=3,
            use_smoothing=False,
        )
        formula = MathTex(
            r"\sigma(x) = \frac{1}{1 + e^{-x}}",
            font_size=FONT_SIZE_ANNO,
        ).align_to(
            axes.get_right(),
            LEFT,
        ).align_to(
            axes,
            UP,
        )

        x_tracker = ValueTracker(0.0)
        dot = Dot(
            axes.c2p(x_tracker.get_value(), sigmoid(x_tracker.get_value())),
            color=YELLOW,
            radius=0.04,
        )
        dot.add_updater(
            lambda mob: mob.move_to(
                axes.c2p(x_tracker.get_value(), sigmoid(x_tracker.get_value()))
            )
        )

        x_value = DecimalNumber(
            x_tracker.get_value(),
            num_decimal_places=2,
            include_sign=True,
            font_size=FONT_SIZE_ANNO,
            align_to_dot=True,
        )
        arrow = MathTex(r"\rightarrow", font_size=24)
        y_value = DecimalNumber(
            sigmoid(x_tracker.get_value()),
            num_decimal_places=2,
            include_sign=True,
            font_size=FONT_SIZE_ANNO,
            align_to_dot=True,
        )
        xy_map = VGroup(x_value, arrow, y_value).arrange(RIGHT, buff=0.20)
        xy_map.next_to(
            formula,
            DOWN,
        ).align_to(
            formula,
            RIGHT,
        )
        # show axes, graph, formula
        self.play(Succession(
            Write(axes),
            Write(graph),
            Write(formula),
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'value map for Sigmoid function',
            skip_animations=False,
        )
        # ************************************************************
        def update_mapping(_):
            x_value.set_value(x_tracker.get_value())
            y_value.set_value(sigmoid(x_tracker.get_value()))

        self.play(Succession(
            Write(dot),
            Write(xy_map),
            run_time=wt*2,
        ))
        self.wait(wt)

        xy_map.add_updater(update_mapping)

        # from 0.0 -> +4.5
        self.play(
            x_tracker.animate.set_value(4.5),
            rate_func=smooth,
            run_time=wt*3,
        )
        self.wait(wt)

        # from +4.5 -> -4.5
        self.play(
            x_tracker.animate.set_value(-4.5),
            rate_func=smooth,
            run_time=wt*5,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            Unwrite(xy_map),
            Unwrite(formula),
            Unwrite(dot),
            Unwrite(graph),
            Unwrite(axes),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            card_module,
        )
        export_mobs(__file__, mobs)
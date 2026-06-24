from manim import *
from utils.general import import_mobs
from utils.ylabel import YLabel
from utils.constants import *

# FIXME: move to end of 017
OPERATOR_TXT_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 12,
    'color': BLACK,
}
OPERATOR_BG_CONFIG = {
    'stroke_width': 0,
    'fill_color': LOGO_WHITE,
    'fill_opacity': 1.0,
}
OPERATOR_BG_CONFIG_LOWER = {
    'stroke_width': 0,
    'fill_color': PURE_BLUE,
    'fill_opacity': 1.0,
}
OPERATOR_BG_CONFIG_UPPER = {
    'stroke_width': 0,
    'fill_color': PURE_RED,
    'fill_opacity': 1.0,
}

OPERATOR_BUFF = 0.8
OPEARTOR_SHIFT = 0.6

wt = SHORT_DURATION
class Demo(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'update col 1 and col 3 with [-140] operator',
            skip_animations=True,
        )
        # ************************************************************
        tensor_nms = import_mobs('017')
        tensor_nms.scale(1.5)
        self.add(tensor_nms)
        self.wait(wt)
        # self.add(tensor_nms)
        # self.wait(wt)
        # # scale up tensor
        # self.play(tensor_nms.animate(
        #     run_time=wt,
        # ).scale(1.5))
        # self.wait(wt)

        # create two [-140] operators for y1 and y2
        ops_shrink = [
            YLabel(
                include_text=True,
                text='-140',
                label_txt_config=OPERATOR_TXT_CONFIG,
                label_bg_config=OPERATOR_BG_CONFIG,
            ).next_to(
                tensor_nms[:, col_idx],
                UP,
                buff=OPERATOR_BUFF,
            ).align_to(
                tensor_nms[:, col_idx],
                RIGHT,
            )
            for col_idx in [1, 3]
        ]
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_shrink),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        for col_idx, operator in zip([1, 3], ops_shrink):
            # push down shrink operators
            self.play(operator.animate(
                run_time=0.5*wt,
                rate_func=rate_functions.ease_out_back,
            ).shift(DOWN*OPEARTOR_SHIFT))

            # remove operator and update column
            self.play(tensor_nms.update_col(
                index=col_idx,
                data=tensor_nms.data[:,col_idx] - 140,
                aargs={'lag_ratio': 0.5, 'run_time': 1.0},
            ))

        # remove operators
        self.play(AnimationGroup(
            *(ShrinkToCenter(
                operator,
            ) for operator in ops_shrink),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'update col 0, 1, 2, 3 with [*1.5] operator',
            skip_animations=True,
        )
        # ************************************************************
        # create four [*1.5] operators for xyxy
        ops_scale = [
            YLabel(
                include_text=True,
                text='*1.5',
                label_txt_config=OPERATOR_TXT_CONFIG,
                label_bg_config=OPERATOR_BG_CONFIG,
            ).next_to(
                tensor_nms[:, col_idx],
                UP,
                buff=OPERATOR_BUFF,
            ).align_to(
                tensor_nms[:, col_idx],
                RIGHT,
            )
            for col_idx in range(4) 
        ]
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_scale),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        for col_idx, operator in zip(range(4), ops_scale):
            # push down shrink operators
            self.play(operator.animate(
                run_time=0.5*wt,
                rate_func=rate_functions.ease_out_back,
            ).shift(DOWN*OPEARTOR_SHIFT))

            # remove operator and update column
            self.play(tensor_nms.update_col(
                index=col_idx,
                data=tensor_nms.data[:,col_idx] * 1.5,
                aargs={'lag_ratio': 0.5, 'run_time': 1.0},
            ))

        # remove operators
        self.play(AnimationGroup(
            *(ShrinkToCenter(
                operator,
            ) for operator in ops_scale),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'check boundary with check operators',
            skip_animations=False,
        )
        # ************************************************************
        ops_check_lower = [
            YLabel(
                include_text=True,
                text='<0',
                label_txt_config=OPERATOR_TXT_CONFIG,
                label_bg_config=OPERATOR_BG_CONFIG_LOWER,
            ).next_to(
                tensor_nms[:, col_idx],
                UP,
                buff=OPERATOR_BUFF,
            ).align_to(
                tensor_nms[:, col_idx],
                RIGHT,
            ) for col_idx in range(4) 
        ]
        ops_check_upper = [
            YLabel(
                include_text=True,
                text='>{:>3d}'.format(bound),
                label_txt_config=OPERATOR_TXT_CONFIG,
                label_bg_config=OPERATOR_BG_CONFIG_UPPER,
            ).next_to(
                tensor_nms[:, col_idx],
                UP,
                buff=OPERATOR_BUFF,
            ).align_to(
                tensor_nms[:, col_idx],
                RIGHT,
            ) for col_idx, bound in zip(range(4), [960,540,960,540])
        ]


        self.wait()     # NOTE: remove this
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_check_upper),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
from manim import *
from utils.general import import_mobs
from utils.ylabel import YLabel
from utils.tensor_2d import Tensor2D
from utils.constants import *

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

FAST_SCALE_FACTOR = 1.3
FAST_SCALE_FACTOR_R = 1 / FAST_SCALE_FACTOR

UPPER_BOUNDS = [960, 540, 960, 540]

wt = SHORT_DURATION
class MainScene(Scene):
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

            # update column
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

            # update column
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
            skip_animations=True,
        )
        # ************************************************************
        # prepare operators
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
            ) for col_idx, bound in zip(range(4), UPPER_BOUNDS)
        ]

        # check lower boundaries
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_check_lower),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        for col_idx, operator in zip(range(4), ops_check_lower):
            # push down shrink operators
            self.play(operator.animate(
                run_time=0.5*wt,
                rate_func=rate_functions.ease_out_back,
            ).shift(DOWN*OPEARTOR_SHIFT))

            # update colors for unusual mobs
            self.play(AnimationGroup(
                *(Succession(
                    mob.animate.scale(FAST_SCALE_FACTOR).set_color(
                        PURE_BLUE if x < 0 else WHITE,
                    ),
                    ApplyMethod(mob.scale, FAST_SCALE_FACTOR_R),
                ) for x, mob in zip(
                    tensor_nms.data[:, col_idx],
                    tensor_nms[:, col_idx],
                )),
                lag_ratio=0.2,
                run_time=wt,
            ))
        self.wait(wt)

        # remove lower operators
        self.play(AnimationGroup(
            *(ShrinkToCenter(
                operator,
            ) for operator in ops_check_lower),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # check upper boundaries
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_check_upper),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        for col_idx, operator in zip(range(4), ops_check_upper):
            ub = UPPER_BOUNDS[col_idx]
            # push down shrink operators
            self.play(operator.animate(
                run_time=0.5*wt,
                rate_func=rate_functions.ease_out_back,
            ).shift(DOWN*OPEARTOR_SHIFT))

            # update colors for unusual mobs
            self.play(AnimationGroup(
                # FIXME: text color issue
                *(Succession(
                    mob.animate.scale(FAST_SCALE_FACTOR).set_color(
                        PURE_RED if x > ub else mob.get_color() if mob.get_color() != BLACK else WHITE
                    ),
                    ApplyMethod(mob.scale, FAST_SCALE_FACTOR_R),
                ) for x, mob in zip(
                    tensor_nms.data[:, col_idx],
                    tensor_nms[:, col_idx],
                )),
                lag_ratio=0.2,
                run_time=wt,
            ))
        self.wait(wt)

        # remove upper operators
        self.play(AnimationGroup(
            *(ShrinkToCenter(
                operator,
            ) for operator in ops_check_upper),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clip into boundary with clip operators',
            skip_animations=True,
        )
        # ************************************************************
        # prepare operators
        ops_clip_lower = [
            YLabel(
                include_text=True,
                text='=0',
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
        ops_clip_upper = [
            YLabel(
                include_text=True,
                text='={:>3d}'.format(bound),
                label_txt_config=OPERATOR_TXT_CONFIG,
                label_bg_config=OPERATOR_BG_CONFIG_UPPER,
            ).next_to(
                tensor_nms[:, col_idx],
                UP,
                buff=OPERATOR_BUFF,
            ).align_to(
                tensor_nms[:, col_idx],
                RIGHT,
            ) for col_idx, bound in zip(range(4), UPPER_BOUNDS)
        ]

        # clip into lower boundaries
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_clip_lower),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        for col_idx, operator in zip(range(4), ops_clip_lower):
            # push down shrink operators
            self.play(operator.animate(
                run_time=0.5*wt,
                rate_func=rate_functions.ease_out_back,
            ).shift(DOWN*OPEARTOR_SHIFT))

            # update colors for unusual mobs
            self.play(tensor_nms.update_col(
                index=col_idx,
                data=np.clip(
                    tensor_nms.data[:,col_idx],
                    0,
                    None,
                ),
                keep_color=True,
                aargs={'lag_ratio': 0.5, 'run_time': 1.0},
            ))

        # remove operators
        self.play(AnimationGroup(
            *(ShrinkToCenter(
                operator,
            ) for operator in ops_clip_lower),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # clip into upper boundaries
        self.play(AnimationGroup(
            *(GrowFromCenter(
                operator,
                rate_func=rate_functions.ease_out_back,
            ) for operator in ops_clip_upper),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        for col_idx, operator in zip(range(4), ops_clip_upper):
            ub = UPPER_BOUNDS[col_idx]
            # push down shrink operators
            self.play(operator.animate(
                run_time=0.5*wt,
                rate_func=rate_functions.ease_out_back,
            ).shift(DOWN*OPEARTOR_SHIFT))

            # update colors for unusual mobs
            self.play(tensor_nms.update_col(
                index=col_idx,
                data=np.clip(
                    tensor_nms.data[:,col_idx],
                    None,
                    ub,
                ),
                keep_color=True,
                aargs={'lag_ratio': 0.5, 'run_time': 1.0},
            ))

        # remove operators
        self.play(AnimationGroup(
            *(ShrinkToCenter(
                operator,
            ) for operator in ops_clip_upper),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'remove invalid rows',
            skip_animations=False,
        )
        # ************************************************************
        res_data = np.empty((0, 6))
        res_objs = []
        res_mobs = VGroup()
        rows_remove = VGroup()

        # prepare fade animations
        anims = []
        for row_data, row_mobs in zip(tensor_nms.data, tensor_nms.rows):
            if (row_mobs[0].get_color() == row_mobs[2].get_color() == PURE_RED) or \
               (row_mobs[0].get_color() == row_mobs[2].get_color() == PURE_BLUE) or \
               (row_mobs[1].get_color() == row_mobs[3].get_color() == PURE_RED) or \
               (row_mobs[1].get_color() == row_mobs[3].get_color() == PURE_BLUE):
                anims.append(AnimationGroup(
                    *(mob.animate.set_color(GRAY).fade(0.3)
                       for mob in row_mobs),
                    lag_ratio=0.0,
                ))
                rows_remove.add(row_mobs)
            else:
                res_data = np.vstack([res_data, row_data])
                res_objs.append([*row_mobs])
                res_mobs.add(row_mobs)

        # fade then remove invalid rows
        self.play(AnimationGroup(
            *anims,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
        self.play(AnimationGroup(
            *(Uncreate(row, lag_ratio=0.0)
              for row in rows_remove),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # arrange into final tensor
        tensor_final = Tensor2D(
            data=res_data,
            formatters=tensor_nms.formatters,
            col_ratios=tensor_nms.col_ratios,
            decimal_config=tensor_nms.decimal_config,
            cell_width=tensor_nms.cell_width,
            cell_height=tensor_nms.cell_height,
            objs=res_objs,
            mobs=res_mobs,
        )
        self.play(ApplyMethod(
            tensor_final.arrange_matrix,
            ORIGIN,
            rate_func=rate_functions.ease_out_back,
            run_time=1.0*wt,
        ))
        self.wait(wt)

        # recolor into plain WHITE
        self.play(AnimationGroup(
            *(row.animate.set_color(WHITE)
              for row in tensor_final.rows),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)
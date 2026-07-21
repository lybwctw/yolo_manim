from manim import *

from utils.info_card import InfoCard
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.mtensor import MTensor_3D
from utils.general import *
from utils.constants import *
from utils.constants_3d import *

import torch

TENSOR_VGAP_3D = 1.2
TENSOR_HGAP_3D = 0.8

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        # cards
        cards, _ = import_mobs('029a')
        (
            card_i1,
            card_i2,
            card_module,
            card_o1,
        ) = cards

        # arrays
        t_i1 = np.random.randn(3,4,5)
        t_i2 = np.random.randn(3,4,5)
        t_i3 = np.random.randn(4,3,2)
        t_o1 = t_i1 + t_i2

        # tensor mobs
        tensor_i1 = MTensor_3D(
            array=t_i1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ).align_to(
            LEFT*TENSOR_HGAP_3D,
            RIGHT,
        )
        tensor_i2 = MTensor_3D(
            array=t_i2,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ).align_to(
            RIGHT*TENSOR_HGAP_3D,
            LEFT,
        )
        tensor_i3 = MTensor_3D(
            array=t_i3,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            UP*TENSOR_VGAP_3D,
            DOWN,
        ).align_to(
            LEFT*TENSOR_HGAP_3D,
            RIGHT,
        ).align_to(
            tensor_i1,
            IN,
        )
        tensor_o1 = MTensor_3D(
            array=t_o1,
            **MEDIUM_CUBE_CONFIG,
        ).align_to(
            DOWN*TENSOR_VGAP_3D,
            UP,
        )

        # add initial mobs
        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(cards)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce cube inputs',
            skip_animations=True,
        )
        # ************************************************************
        # create input tensors
        self.play(AnimationGroup(
            tensor_i1.create(
                style='beam',
                direction=OUT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={},
            ),
            card_i1.expand_summary(shape_str(t_i1)),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # create card summaries
        self.play(AnimationGroup(
            tensor_i2.create(
                style='beam',
                direction=OUT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
                gargs={},
            ),
            card_i2.expand_summary(shape_str(t_i2)),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute output',
            skip_animations=True,
        )
        # ************************************************************
        # prepare for highlight
        tensor_i1.prepare_highlight_loop()
        tensor_i2.prepare_highlight_loop()
        c, h, w = t_i1.shape
        masks_in = np.eye(c*h*w, dtype=bool).reshape(c*h*w, c, h, w)

        # pause in the first inputs
        self.play(AnimationGroup(
            tensor_i1.highlight(masks_in[0]),
            tensor_i2.highlight(masks_in[0]),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # generate the first output
        self.play(GrowFromCenter(
            tensor_o1[0,0,0],
            rate_func=rate_functions.ease_out_back,
            run_time=wt,
        ))

        # loop into the last output
        self.play(AnimationGroup(
            tensor_i1.highlight_loop(
                masks=masks_in[1:],
                back=False,
                rate_func=smooth,
            ),
            tensor_i2.highlight_loop(
                masks=masks_in[1:],
                back=False,
                rate_func=smooth,
            ),
            Succession(
                *(GrowFromCenter(
                    tensor_o1[i,j,k],
                    rate_func=rate_functions.ease_out_back,
                ) for i, j, k in np.ndindex(c, h, w)),
                rate_func=smooth,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # back to original hl states
        self.play(AnimationGroup(
            tensor_i1.highlight(),
            tensor_i2.highlight(),
            lag_ratio=0.0,
            run_time=wt,
        ))

        # show output card shape
        self.play(card_o1.expand_summary(
            shape_str(t_o1),
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'vectorized thinking',
            skip_animations=False,
        )
        # ************************************************************
        # remove output
        tensor_o1.save_state()
        self.play(AnimationGroup(
            tensor_o1.uncreate(
                style='beam',
                direction=IN,
                anim=ShrinkToCenter,
                gargs={'run_time': wt},
            ),
            card_o1.remove_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # inputs breath
        self.play(AnimationGroup(
            AnimationGroup(
                *(mob.animate(
                    rate_func=rate_functions.there_and_back,
                ).scale(0.8)
                for mob in tensor_i1.mobs),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(mob.animate(
                    rate_func=rate_functions.there_and_back,
                ).scale(0.8)
                for mob in tensor_i2.mobs),
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=wt*0.5,
        ))

        # pop create an output copy
        tensor_o1.restore()
        self.play(AnimationGroup(
            AnimationGroup(
                *(GrowFromCenter(
                    mob,
                    rate_func=rate_functions.ease_out_back,
                ) for mob in tensor_o1.mobs),
                lag_ratio=0.0,
            ),
            card_o1.expand_summary(shape_str(t_o1)),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'unmatched inputs',
            skip_animations=False,
        )
        # ************************************************************
        # remove output
        self.play(AnimationGroup(
            tensor_o1.uncreate(
                style='beam',
                direction=IN,
                anim=ShrinkToCenter,
            ),
            card_o1.remove_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))

        # remove first input
        self.play(AnimationGroup(
            tensor_i1.uncreate(
                style='beam',
                direction=IN,
                anim=ShrinkToCenter,
            ),
            card_i1.remove_summary(),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # introduce unmatched input
        self.play(AnimationGroup(
            tensor_i3.create(
                style='beam',
                direction=OUT,
                anim=GrowFromCenter,
                aargs={'rate_func': rate_functions.ease_out_back},
            ),
            card_i1.expand_summary(shape_str(t_i3)),
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # failed breath and generation
        self.play(AnimationGroup(
            AnimationGroup(
                *(mob.animate(
                    rate_func=rate_functions.there_and_back,
                ).scale(0.8)
                for mob in tensor_i3.mobs),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(mob.animate(
                    rate_func=rate_functions.there_and_back,
                ).scale(0.8)
                for mob in tensor_i2.mobs),
                lag_ratio=0.0,
            ),
            card_module.suggest_failure(),
            lag_ratio=0.0,
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'clean',
        #     skip_animations=True,
        # )
        # # ************************************************************
        # # remove tensors 
        # self.play(AnimationGroup(
        #     tensor_i1.uncreate(
        #         style='beam',
        #         direction=IN,
        #         anim=ShrinkToCenter,
        #         gargs={},
        #     ),
        #     tensor_i2.uncreate(
        #         style='beam',
        #         direction=IN,
        #         anim=ShrinkToCenter,
        #         gargs={},
        #     ),
        #     tensor_o2.uncreate(
        #         style='beam',
        #         direction=IN,
        #         anim=ShrinkToCenter,
        #         gargs={},
        #     ),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))

        # # remove card summaries
        # self.play(AnimationGroup(
        #     card_i1.remove_summary(),
        #     card_i2.remove_summary(),
        #     card_o1.remove_summary(),
        #     lag_ratio=0.0,
        #     run_time=wt,
        # ))
        # self.wait(wt)
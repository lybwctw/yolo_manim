from manim import *

from utils.mtensor import *
from utils.show_shape_3d import *
from utils.constants_3d import *
from utils.info_card import *
from utils.general import *

import numpy as np

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'introduce concept of tensor',
            skip_animations=False,
        )
        # ************************************************************
        self.set_camera_orientation(
            **VIEW_TOP,
        )
        card = InfoCard('tensor')
        card.head_mob.save_state()
        card.head_mob.scale(10.0)

        # introduce text 'tensor'
        self.play(Write(card.head_mob))
        self.wait(wt)

        # scale down and add background
        self.play(card.head_mob.animate(
            rate_func=rate_functions.ease_out_expo,
            run_time=wt*0.5,
        ).restore())
        self.play(FadeIn(
            card.frame_mob,
            run_time=wt*0.5,
        ))

        # fix and to edge
        self.add_fixed_in_frame_mobjects(card)
        self.play(card.animate(
            rate_func=rate_functions.ease_out_expo,
            run_time=wt*0.5,
        ).to_edge(
            LEFT,
            buff=CARD_EDGE_BUFF,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'top view: 1d tensor',
            skip_animations=False,
        )
        # ************************************************************
        # init tensor
        rtensor = np.random.randn(9)
        mtensor = MTensor1D(
            array=rtensor,
            mode='card',
            style='horizontal',
            **MEDIUM_TENSOR_CONFIG,
        )

        # introduce tensor
        self.play(mtensor.create(
            style='series',
            direction=RIGHT,
            run_time=wt,
        ))
        self.wait(wt)

        # introduce card
        self.play(card.expand_params(
            params={
                'ndim': 1,
                'shape': t2s(rtensor),
            },
            run_time=wt,
        ))
        self.wait(wt)

        # show shape of tensor
        self.play(ShowShape3D(
            self,
            mtensor,
            view='top',
            run_time=wt,
        ))
        self.wait(wt)

        # sync tensor and card on shape
        self.play(AnimationGroup(
            *(Wiggle(mob, scale_value=2.0) for mob in [
                card.value_objs['shape'],
                *mtensor.shape_texts,
            ]),
            lag_ratio=0.0,
            run_time=wt*2,
        ))
        self.wait(wt)

        # hide shape
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # tensor values
        self.play(mtensor.update_values(
            np.random.randn(9),
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'to 3d cubes: ignore values for now',
            skip_animations=False,
        )
        # ************************************************************
        # 3d view
        self.move_camera(
            **VIEW_INTRO,
            run_time=wt,
        )
        self.wait(wt)

        # to cubes
        self.play(mtensor.switch(
            style='series',
            direction=RIGHT,
            run_time=wt,
        ))
        self.wait(wt)

        # shape again
        self.play(ShowShape3D(
            self,
            mtensor,
            view='intro',
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'vertical view on tensor',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )
        self.wait(wt)

        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'erect view on tensor',
            skip_animations=False,
        )
        # ************************************************************
        self.play(Rotate(
            mtensor,
            angle=90*DEGREES,
            axis=UP,
            run_time=wt,
        ))
        mtensor.style = 'erect' # manual style update
        self.wait(wt)

        # shape again
        self.play(ShowShape3D(
            self,
            mtensor,
            view='compute',
            run_time=wt,
        ))
        self.wait(wt)
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean 1d tensor',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mtensor.uncreate(
            style='series',
            direction=RIGHT,
            anim=Unwrite,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = VGroup(card)
        export_mobs(__file__, mobs)     # NOTE: used by 2d
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
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        self.set_camera_orientation(
            **VIEW_INTRO,
        )
        mobs = import_mobs('026c')
        (card,) = mobs

        self.add_fixed_in_frame_mobjects(card)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'intro view: cube mode',
            skip_animations=True,
        )
        # ************************************************************
        # init tensor
        rtensor = np.random.randn(5,6,4,3)
        mtensor = MTensor4D(
            array=rtensor,
            mode='cube',
            style='horizontal',
            **SMALL_TENSOR_CONFIG,
        )

        # introduce tensor
        self.play(mtensor.create(
            style='beam',
            direction=OUT,
            lag_ratio=0.1,
            run_time=wt,
        ))
        self.wait(wt)

        # update card
        self.play(card.update_params(
            params={
                'ndim': 4,
                'shape': t2s(rtensor),
            },
            run_time=wt,
        ))
        self.wait(wt)

        # show shape of tensor
        self.play(ShowShape3D(
            self,
            mtensor,
            view='intro',
            lag_ratio=1.0,
            run_time=wt*4,
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

        # ************************************************************
        self.next_section(
            'intro view: card mode',
            skip_animations=True,
        )
        # ************************************************************
        self.play(mtensor.switch(
            style='beam',
            direction=IN,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute view: card mode',
            skip_animations=True,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute view: cube mode',
            skip_animations=True,
        )
        # ************************************************************
        self.play(mtensor.switch(
            style='beam',
            direction=OUT,
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # show shape of tensor
        self.play(ShowShape3D(
            self,
            mtensor,
            view='compute',
            lag_ratio=1.0,
            run_time=wt*4,
        ))
        self.wait(wt)

        # hide shape
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean 4d tensor and card',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mtensor.uncreate(
            style='beam',
            direction=IN,
            anim=Unwrite,
            lag_ratio=0.0,
            run_time=wt,
        ))

        self.play(card.shrink_params(
            run_time=wt*0.5,
        ))
        self.play(Unwrite(
            card,
            run_time=wt*0.5,
        ))
        self.wait(wt)

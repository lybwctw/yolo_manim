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
        mobs = import_mobs('026b')
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
        rtensor = np.random.randn(4,5,6)
        mtensor = MTensor3D(
            array=rtensor,
            mode='cube',
            **MEDIUM_TENSOR_CONFIG,
        )

        # introduce tensor
        self.play(mtensor.create(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        self.wait(wt)

        # update card
        self.play(card.update_params(
            params={
                'ndim': 3,
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
            run_time=wt*3,
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
            skip_animations=False,
        )
        # ************************************************************
        self.play(mtensor.switch(
            style='beam',
            direction=IN,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute view: card mode',
            skip_animations=False,
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
            skip_animations=False,
        )
        # ************************************************************
        self.play(mtensor.switch(
            style='beam',
            direction=OUT,
            run_time=wt,
        ))
        self.wait(wt)

        # show shape of tensor
        self.play(ShowShape3D(
            self,
            mtensor,
            view='compute',
            lag_ratio=1.0,
            run_time=wt*3,
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
            'clean 3d tensor',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mtensor.uncreate(
            style='beam',
            direction=IN,
            anim=Unwrite,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = VGroup(card)
        export_mobs(__file__, mobs)     # NOTE: used by 4d
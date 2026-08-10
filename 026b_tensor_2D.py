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
            skip_animations=False,
        )
        # ************************************************************
        self.set_camera_orientation(
            **VIEW_TOP,
        )
        mobs = import_mobs('026a')
        (card,) = mobs

        self.add_fixed_in_frame_mobjects(card)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'top view: 2d tensor',
            skip_animations=False,
        )
        # ************************************************************
        # init tensor
        rtensor = np.random.randn(4,5)
        mtensor = MTensor2D(
            array=rtensor,
            mode='card',
            style='horizontal',
            **MEDIUM_TENSOR_CONFIG,
        )

        # introduce tensor
        self.play(mtensor.create(
            style='layer',
            direction=RIGHT,
            run_time=wt,
        ))
        self.wait(wt)

        # update card
        self.play(card.update_params(
            params={
                'ndim': 2,
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
            lag_ratio=1.0,
            run_time=wt*2,
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
            np.random.randn(4,5),
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
            style='layer',
            direction=RIGHT,
            run_time=wt,
        ))
        self.wait(wt)

        # shape again
        self.play(ShowShape3D(
            self,
            mtensor,
            view='intro',
            lag_ratio=1.0,
            run_time=wt*2,
        ))
        self.wait(wt)
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute view: horizontal 2d',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )
        self.wait(wt)

        # shape again
        self.play(ShowShape3D(
            self,
            mtensor,
            view='compute',
            lag_ratio=1.0,
            run_time=wt*2,
        ))
        self.wait(wt)
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # clean for new tensor
        self.play(mtensor.uncreate(
            style='layer',
            direction=RIGHT,
            anim=Unwrite,
            run_time=wt,
        ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute view: erect 2d',
            skip_animations=False,
        )
        # ************************************************************
        # init tensor
        rtensor = np.random.randn(7,6)
        mtensor = MTensor2D(
            array=rtensor,
            mode='cube',
            style='erect',
            **MEDIUM_TENSOR_CONFIG,
        )

        # introduce tensor
        self.play(mtensor.create(
            style='layer',
            direction=UP,
            run_time=wt,
        ))
        # self.wait(wt)

        # update card
        self.play(card.update_params(
            params={
                # 'ndim': 2,
                'shape': t2s(rtensor),
            },
            run_time=wt,
        ))
        self.wait(wt)

        # shape again
        self.play(ShowShape3D(
            self,
            mtensor,
            view='compute',
            lag_ratio=1.0,
            run_time=wt*2,
        ))
        self.wait(wt)
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'intro view: erect 2d',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_INTRO,
            run_time=wt,
        )
        self.wait(wt)

        # shape again
        self.play(ShowShape3D(
            self,
            mtensor,
            view='intro',
            lag_ratio=1.0,
            run_time=wt*2,
        ))
        self.wait(wt)
        self.play(HideShape3D(
            mtensor,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'clean 2d tensor',
            skip_animations=False,
        )
        # ************************************************************
        self.play(mtensor.uncreate(
            style='layer',
            direction=DOWN,
            anim=Unwrite,
            run_time=wt,
        ))
        self.wait(wt)

        mobs = VGroup(card)
        export_mobs(__file__, mobs)     # NOTE: used by 3d
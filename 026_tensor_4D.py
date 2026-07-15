from manim import *
from utils.mtensor import MCube, MTensor_4D
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.constants_3d import *

DECIMAL_4D_CONFIG = {
    'font_size': 12,
}

wt = 1.0

class MainScene(ThreeDScene):
    def construct(self):
        # TODO, introduce top-left corner image as reference
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        tensor = MTensor_4D(
            array=np.random.randn(6,5,3,4),
            mode='cube',
            size=0.25,
            padding=0.0,
            decimal_config=DECIMAL_4D_CONFIG,
        )

        # ************************************************************
        self.next_section(
            'left view',
            skip_animations=False,
        )
        # ************************************************************
        self.set_camera_orientation(
            **VIEW_INTRO,
        )

        self.play(tensor.create(
            style='beam',
            direction=OUT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={},
            ggargs={'lag_ratio': 0.1, 'run_time': wt}
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='left',
            aargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'right view',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )

        self.play(ShowShape3D(
            self,
            tensor,
            facing='right',
            aargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(tensor.uncreate(
            style='beam',
            direction=IN,
            anim=ShrinkToCenter,
            aargs={},
            gargs={},
            ggargs={'lag_ratio': 0.1, 'run_time': wt},
        ))
        self.wait(wt)
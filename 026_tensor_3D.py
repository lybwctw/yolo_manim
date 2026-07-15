from manim import *
from utils.mtensor import MCube, MTensor_3D
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.constants_3d import *

DECIMAL_3D_CONFIG = {
    'font_size': 16,
}

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # TODO, introduce top-left corner image as reference
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=True,
        )
        # ************************************************************
        tensor = MTensor_3D(
            array=np.random.randn(4,5,6),
            mode='card',
            size=0.5,
            padding=0.0,
            decimal_config=DECIMAL_3D_CONFIG,
        )

        # ************************************************************
        self.next_section(
            'card left view',
            skip_animations=True,
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
            gargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='card left',
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
            'cube left view',
            skip_animations=True,
        )
        # ************************************************************
        # FIXME: decimals dim before switching!!
        self.play(tensor.switch_mode(
            style='beam',
            direction=OUT,
            aargs={'run_time': wt},
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
            'cube right view',
            skip_animations=True,
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

        # self.play(tensor.uncreate(
        #     style='beam',
        #     direction=IN,
        #     anim=ShrinkToCenter,
        #     aargs={},
        #     gargs={'run_time': wt},
        # ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'cube erect right view',
            skip_animations=True,
        )
        # ************************************************************
        self.play(Rotate(
            tensor,
            angle=90*DEGREES,
            axis=RIGHT,
            run_time=wt,
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='right erect',
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
            'cube erect left view',
            skip_animations=True,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_INTRO,
            run_time=wt,
        )
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='left erect',
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
            'back to cube left view',
            skip_animations=False,
        )
        # ************************************************************
        self.play(Rotate(
            tensor,
            angle=-90*DEGREES,
            axis=RIGHT,
            run_time=wt,
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

        self.play(tensor.uncreate(
            style='beam',
            direction=IN,
            anim=ShrinkToCenter,
            aargs={},
            gargs={'run_time': wt},
        ))
        self.wait(wt)
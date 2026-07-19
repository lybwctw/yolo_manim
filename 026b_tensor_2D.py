from manim import *
from utils.mtensor import MCube, MTensor_2D
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.constants_3d import *

DECIMAL_2D_CONFIG = {
    'font_size': 16,
}

wt = 1.0
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        tensor = MTensor_2D(
            array=np.random.randn(4,5),
            mode='card',
            size=0.5,
            padding=0.0,
            decimal_config=DECIMAL_2D_CONFIG,
        )

        # ************************************************************
        self.next_section(
            'horizontal 2d',
            skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.create(
            direction=DOWN,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait()

        self.play(ShowShape3D(
            self,
            tensor,
            facing='horizontal',
            aargs={'lag_ratio': 0.5, 'run_time': 3*wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '3d 2d',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_INTRO,
            run_time=wt,
        )
        self.wait(wt)

        self.play(tensor.switch_mode(
            direction=RIGHT,
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
            'another view',
            skip_animations=False,
        )
        # ************************************************************
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )
        self.wait(wt)

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

        # ************************************************************
        self.next_section(
            'erect right view',
            skip_animations=False,
        )
        # ************************************************************
        # TODO, make show shape positioning more natural
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
            'erect left view',
            skip_animations=False,
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

        self.play(tensor.uncreate(
            direction=RIGHT,
            anim=ShrinkToCenter,
            aargs={},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)
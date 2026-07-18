from manim import *
from utils.mtensor import MCube, MTensor_1D
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.constants_3d import *

import numpy as np

DECIMAL_1D_CONFIG = {
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
        tensor = MTensor_1D(
            array=np.random.randn(9),
            mode='card',
            size=0.5,
            padding=0.0,
            decimal_config=DECIMAL_1D_CONFIG,
        )

        # ************************************************************
        self.next_section(
            'horizontal 1d',
            skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.create(
            direction=RIGHT,
            anim=GrowFromCenter,
            aargs={'rate_func': rate_functions.ease_out_back},
            gargs={'lag_ratio': 0.5, 'run_time': wt},
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='horizontal',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # NOTE: no update effect until 3d version?
        # self.play(tensor.update_values(
        #     np.random.randn(9),
        #     aargs={
        #         'lag_ratio': 0.0,
        #         'run_time': 3.0,
        #     },
        # ))
        # self.wait()

        # ************************************************************
        self.next_section(
            'vertical 1d',
            skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.mobs.animate(
            run_time=1.0,
        ).arrange(
            DOWN,
            buff=0.0,
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='vertical',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'reverse horizontal 1d',
            skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.mobs.animate(
            run_time=1.0,
        ).arrange(
            LEFT,
            buff=0.0,
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='horizontal reverse',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'reverse vertical 1d',
            skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.mobs.animate(
            run_time=1.0,
        ).arrange(
            UP,
            buff=0.0,
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='vertical reverse',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back to horizontal 1d',
           skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.mobs.animate(
            run_time=1.0,
        ).arrange(
            RIGHT,
            buff=0.0,
        ))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='horizontal',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '3d 1d',
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
            aargs={'run_time': wt},
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
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '3d erect 1d',
            skip_animations=False,
        )
        # ************************************************************
        self.play(tensor.mobs.animate(
            run_time=wt,
        ).arrange(IN, buff=0.0))
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='right erect',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '3d extended 1d',
            skip_animations=False,
        )
        # ************************************************************
        # intro view expanded 1d tensor
        self.move_camera(
            **VIEW_INTRO,
            run_time=wt,
            added_anims=[
                tensor.mobs.animate.arrange(
                    RIGHT,
                    buff=0.5,
                ),
            ]
        )
        self.wait(wt)

        self.play(ShowShape3D(
            self,
            tensor,
            facing='left',
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        self.play(HideShape3D(
            tensor,
            aargs={'run_time': wt},
        ))
        self.wait(wt)

        # compute view expanded 1d tensor
        self.move_camera(
            **VIEW_COMPUTE,
            run_time=wt,
        )

        self.play(ShowShape3D(
            self,
            tensor,
            facing='right',
            aargs={'run_time': wt},
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
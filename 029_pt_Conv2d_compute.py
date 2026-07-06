from manim import *

from utils.general import import_mobs, export_mobs
from utils.mtensor import MTensor
from utils.constant_modules import *
from utils.constants import *

wt = SHORT_DURATION
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        mobs = import_mobs('028')
        (
            card_module, module
        ) = mobs

        self.set_camera_orientation(
            **VIEW_COMPUTE,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.add(module)
        self.wait(wt)

        # fade module card
        card_module.save_state()
        self.play(card_module.animate(
            run_time=wt,
        ).fade(0.5))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce input',
            skip_animations=False,
        )
        # ************************************************************
        tinput = MTensor(
        )
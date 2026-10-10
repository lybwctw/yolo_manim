from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.info_card import *
from utils.constants import *
from utils.constants_3d import *
from utils.name_tag import *

from modules.ut_Conv import *
from modules.ut_Bottleneck import *
from modules.ut_C2f import *
from modules.ut_SPPF import *
from modules.ut_Detect import *

# from ultralytics.nn.modules import Detect

import torch

INIT_CONFIG = {
    'ch': 8,
    'c2': 4,
    'c3': 4,
    'reg_max': 5,      # 4 probs for each direction (16 by default)
    'nc': 3,           # 3 classes
}

TENSOR_LABEL_CONFIG = {
    'font': 'JetBrains Mono',
    'font_size': 10,
    'color': GRAY,
}

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # module card
        card_module, _ = import_mobs('044a')

        # raw module with random init
        module_config = INIT_CONFIG
        # ut_module = Detect(**module_config)   # not used

        # module graph
        graph_module = MGraph_Detect(module_config)

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_INTRO,
        )
        self.add_fixed_in_frame_mobjects(card_module)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce graph',
            skip_animations=False,
        )
        # ************************************************************
        # create unexpanded graph
        self.play(graph_module.create(
            run_time=wt,
        ))
        self.wait()

        # expand module card
        self.play(card_module.expand_params(
            params=module_config,
            run_time=wt,
        ))
        self.wait(wt)

        # expand and connect graph
        self.play(graph_module.more_space(
            run_time=wt,
        ))
        self.play(graph_module.expand(
            run_time=wt,
        ))
        # self.wait(wt)
        self.play(graph_module.connect(
            lag_ratio=0.5,
            run_time=wt*5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'tags on sub module args',
            skip_animations=False,
        )
        # ************************************************************
        # TODO...

        # ************************************************************
        self.next_section(
            'prepare for compute',
            skip_animations=False,
        )
        # ************************************************************
        # graph to right edge
        self.play(graph_module.animate(
            run_time=wt,
        ).scale(
            0.8
        ).to_edge(RIGHT, buff=MGRAPH_EDGE_BUFF))
        self.wait(wt)


        mobs = VGroup(card_module, graph_module)
        export_mobs(__file__, mobs)      # used by next
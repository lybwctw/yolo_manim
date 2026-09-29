# ************************************************************
# Compute steps for fake yolov8n, part 1.
# ************************************************************
from manim import *

from utils.general import import_mobs, export_mobs
from utils.show_shape_3d import ShowShape3D, HideShape3D
from utils.ftensor import *
from utils.info_card import *
from utils.constants_3d import *
from utils.constants import *
from utils.general import *
from utils.name_tag import *
import torch
import numpy as np

from modules.ut_Conv import UT_Conv
from modules.ut_Bottleneck import UT_Bottleneck
from modules.ut_C2f import UT_C2f
from modules.ut_SPPF import UT_SPPF
from modules.ut_Detect import UT_Detect

TENSOR_VGAP_MINI = 0.5
TENSOR_VGAP_SMALL = 1.0
TENSOR_VGAP_MEDIUM = 2.0
TENSOR_VGAP_LARGE = 3.0

INIT_SCALE = 0.5

RUNNING_X = 6.0
FAKE_HALF = 2/3

# for reference
# [0]  16 -> 8
# [1]  32 -> 12
# [2]  32 -> 12
# [3]  64 -> 16
# [4]  64 -> 16
# [5]  128 -> 20
# [6]  128 -> 20
# [7]  256 -> 24
# [8]  256 -> 24
# [9]  256 -> 24
# [10] 256 -> 24
# [11] 384 -> 26
# [12] 128 -> 20
# [13] 128 -> 20
# [14] 192 -> 22
# [15] 64 -> 16
# [16] 64 -> 16
# [17] 192 -> 22
# [18] 128 -> 20
# [19] 128 -> 20
# [20] 384 -> 26
# [21] 256 -> 24
# [22] 
# [23]
# [24]

wt = 0.5
class MainScene(ThreeDScene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init mobs',
            skip_animations=False,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('045c')
        mm_modules, card, graph = mobs

        cam_args = {
            **VIEW_COMPUTE,
            'theta': -125*DEGREES,
            'focal_distance': 100,
            'zoom': 0.35,
        }
        self.set_camera_orientation(
            **cam_args,
        )
        self.add_fixed_in_frame_mobjects(card, graph)
        self.add(mm_modules)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'init input tensor',
            skip_animations=False,
        )
        # ************************************************************
        mt_running = FTensor3D(
            shape=(3,640,640),
            size_config={
                'width': 64*UNIT_FTENSOR_SIZE,
                'height': 64*UNIT_FTENSOR_SIZE,
                'depth': 3*UNIT_FTENSOR_SIZE,
            },
            opaque=True,
        ).scale(INIT_SCALE)
        mt_running.next_to(mm_modules[0], UP)
        self.play(mt_running.create(
            ref='bottom',
            run_time=wt*0.1,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[0] apply Conv',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[0]
        mask_module = np.eye(len(mm_modules), dtype=bool)[0]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor, skipped

        # apply module
        self.play(mm_modules[0].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(16,320,320),
            scale_factor=(8/3, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[1/1] apply Conv',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[1]
        mask_module = np.eye(len(mm_modules), dtype=bool)[1]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[1],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[1].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(32,160,160),
            scale_factor=(12/8, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[2/2] apply C2f',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[2]
        mask_module = np.eye(len(mm_modules), dtype=bool)[2]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[2],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[2].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.translate(
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[3/3] apply Conv',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[3]
        mask_module = np.eye(len(mm_modules), dtype=bool)[3]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[3],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[3].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(64,80,80),
            scale_factor=(16/12, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[4/4] apply C2f, backup',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[4]
        mask_module = np.eye(len(mm_modules), dtype=bool)[4]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[4],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[4].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.translate(
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c4 = mt_running.copy()
        mt_c4.set_opacity(0.3)
        self.play(FadeIn(mt_c4, run_time=wt*0.1))
        self.play(mt_c4.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[4],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[5/5] apply Conv',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[5]
        mask_module = np.eye(len(mm_modules), dtype=bool)[5]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[5],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[5].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(128,40,40),
            scale_factor=(20/16, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[6/6] apply C2f, backup',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[6]
        mask_module = np.eye(len(mm_modules), dtype=bool)[6]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[6],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[6].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.translate(
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c6 = mt_running.copy()
        mt_c6.set_opacity(0.3)
        self.play(FadeIn(mt_c6, run_time=wt*0.1))
        self.play(mt_c6.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[6],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[7/7] apply Conv',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[7]
        mask_module = np.eye(len(mm_modules), dtype=bool)[7]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[7],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[7].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(256,20,20),
            scale_factor=(24/20, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[8/8] apply C2f',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[8]
        mask_module = np.eye(len(mm_modules), dtype=bool)[8]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[8],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[8].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.translate(
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[9/9] apply SPPF',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[9]
        mask_module = np.eye(len(mm_modules), dtype=bool)[9]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[9],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[9].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.translate(
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c9 = mt_running.copy()
        mt_c9.set_opacity(0.3)
        self.play(FadeIn(mt_c9, run_time=wt*0.1))
        self.play(mt_c9.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[9],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[10/-] apply Upsample',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module (tarnish all)
        mask_graph = np.eye(graph.ncards, dtype=bool)[10]
        mask_module = np.zeros(len(mm_modules), dtype=bool)
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor, skipped

        # apply module
        self.play(mt_running.stretch_3d(
            new_shape=(256,40,40),
            scale_factor=(1.0, 1/FAKE_HALF, 1/FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[11/-] apply concat',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card
        mask_graph = np.eye(graph.ncards, dtype=bool)[11]
        self.play(graph.highlight(
            mask_graph,
            run_time=wt*0.1,
        ))
        self.wait(wt)

        # prepare result mt_running
        res_running = mt_running.copy()
        res_running.stretch_to_fit_depth(
            res_running.depth + mt_c6.depth
        )

        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).move_to(
            res_running,
            aligned_edge=OUT,
        ))
        # self.wait(wt)

        # concat mt_c6 into running
        self.play(mt_c6.animate(
            run_time=wt*0.5,
        ).move_to(
            res_running,
            aligned_edge=IN,
        ))
        self.wait(wt)

        # fade in result running
        self.play(AnimationGroup(
            Unwrite(mt_running),
            Unwrite(mt_c6),
            FadeIn(res_running),
            run_time=wt*0.5,
        ))
        mt_running = res_running
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[12/10] apply C2f, backup',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[12]
        mask_module = np.eye(len(mm_modules), dtype=bool)[10]
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[10],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[10].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(128,80,80),
            scale_factor=(16/44, 1.0, 1.0),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c12 = mt_running.copy()
        mt_c12.set_opacity(0.3)
        self.play(FadeIn(mt_c12, run_time=wt*0.1))
        self.play(mt_c12.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[10],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[13/-] apply Upsample',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card and module (tarnish all)
        mask_graph = np.eye(graph.ncards, dtype=bool)[13]
        mask_module = np.zeros(len(mm_modules), dtype=bool)
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)
        
        # move running tensor, skipped

        # apply module
        self.play(mt_running.stretch_3d(
            new_shape=(128,80,80),
            scale_factor=(1.0, 1/FAKE_HALF, 1/FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[14/-] apply concat',
            skip_animations=False,
        )
        # ************************************************************
        # highlight card
        mask_graph = np.eye(graph.ncards, dtype=bool)[14]
        self.play(graph.highlight(
            mask_graph,
            run_time=wt*0.1,
        ))
        self.wait(wt)

        # prepare result mt_running
        res_running = mt_running.copy()
        res_running.stretch_to_fit_depth(
            res_running.depth + mt_c4.depth
        )

        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).move_to(
            res_running,
            aligned_edge=OUT,
        ))
        # self.wait(wt)

        # concat mt_c4 into running
        self.play(mt_c4.animate(
            run_time=wt*0.5,
        ).move_to(
            res_running,
            aligned_edge=IN,
        ))
        self.wait(wt)

        # show shape on graph

        # fade in result running
        self.play(AnimationGroup(
            Unwrite(mt_running),
            Unwrite(mt_c4),
            FadeIn(res_running),
            run_time=wt*0.5,
        ))
        mt_running = res_running
        self.wait(wt)

        # export
        mobs = VGroup(
            mm_modules, card, graph,
            mt_running,
            mt_c9, mt_c12,
        )
        export_mobs(__file__, mobs)     # used by next
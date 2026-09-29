# ************************************************************
# Compute steps for fake yolov8n, part 2.
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
            skip_animations=True,
        )
        # ************************************************************
        # load card and graph
        mobs = import_mobs('045d')
        (
            mm_modules, card, graph,
            mt_running,
            mt_c9, mt_c12,
        ) = mobs

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
        self.add(mm_modules, mt_running, mt_c9, mt_c12)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[15/11] apply C2f, backup',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[15]
        mask_module = np.eye(len(mm_modules), dtype=bool)[11]
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
            mm_modules[11],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[11].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(64,80,80),
            scale_factor=(16/36, 1.0, 1.0),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c15 = mt_running.copy()
        mt_c15.set_opacity(0.3)
        self.play(FadeIn(mt_c15, run_time=wt*0.1))
        self.play(mt_c15.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[11],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[16/12] apply Conv',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[16]
        mask_module = np.eye(len(mm_modules), dtype=bool)[12]
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
            mm_modules[12],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[12].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(64,40,40),
            scale_factor=(1.0, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[17/-] apply concat',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card
        mask_graph = np.eye(graph.ncards, dtype=bool)[17]
        self.play(graph.highlight(
            mask_graph,
            run_time=wt*0.1,
        ))
        self.wait(wt)

        # prepare result mt_running
        res_running = mt_running.copy()
        res_running.stretch_to_fit_depth(
            res_running.depth + mt_c12.depth
        )

        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).move_to(
            res_running,
            aligned_edge=OUT,
        ))
        # self.wait(wt)

        # concat mt_c12 into running
        self.play(mt_c12.animate(
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
            Unwrite(mt_c12),
            FadeIn(res_running),
            run_time=wt*0.5,
        ))
        mt_running = res_running
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[18/13] apply C2f, backup',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[18]
        mask_module = np.eye(len(mm_modules), dtype=bool)[13]
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
            mm_modules[13],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[13].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(128,40,40),
            scale_factor=(20/36, 1.0, 1.0),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c18 = mt_running.copy()
        mt_c18.set_opacity(0.3)
        self.play(FadeIn(mt_c18, run_time=wt*0.1))
        self.play(mt_c18.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[13],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[19/14] apply Conv',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[19]
        mask_module = np.eye(len(mm_modules), dtype=bool)[14]
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
            mm_modules[14],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[14].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(128,20,20),
            scale_factor=(1.0, FAKE_HALF, FAKE_HALF),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # ************************************************************
        self.next_section(
            '[20/-] apply concat',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card
        mask_graph = np.eye(graph.ncards, dtype=bool)[20]
        self.play(graph.highlight(
            mask_graph,
            run_time=wt*0.1,
        ))
        self.wait(wt)

        # prepare result mt_running
        res_running = mt_running.copy()
        res_running.stretch_to_fit_depth(
            res_running.depth + mt_c12.depth
        )

        # move running tensor
        self.play(mt_running.animate(
            run_time=wt*0.5,
        ).move_to(
            res_running,
            aligned_edge=OUT,
        ))
        # self.wait(wt)

        # concat mt_c9 into running
        self.play(mt_c9.animate(
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
            Unwrite(mt_c9),
            FadeIn(res_running),
            run_time=wt*0.5,
        ))
        mt_running = res_running
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[21/15] apply C2f, backup',
            skip_animations=True,
        )
        # ************************************************************
        # highlight card and module
        mask_graph = np.eye(graph.ncards, dtype=bool)[21]
        mask_module = np.eye(len(mm_modules), dtype=bool)[15]
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
            mm_modules[15],
            RIGHT,
        ).set_x(
            RUNNING_X,
        ))
        self.wait(wt)

        # apply module
        self.play(mm_modules[15].breath(
            run_time=wt*0.5,
        ))
        self.play(mt_running.stretch_3d(
            new_shape=(256,20,20),
            scale_factor=(24/44, 1.0, 1.0),
            run_time=wt*0.5,
        ))
        self.wait(wt)

        # show shape on graph

        # make a copy
        mt_c21 = mt_running.copy()
        mt_c21.set_opacity(0.3)
        self.play(FadeIn(mt_c21, run_time=wt*0.1))
        self.play(mt_c21.animate(
            run_time=wt*0.5,
        ).next_to(
            mm_modules[15],
            LEFT,
        ).set_x(
            -RUNNING_X,
        # ).set_opacity(
        #     1.0,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            '[22/16-23/17-24/18] apply heads',
            skip_animations=True,
        )
        # ************************************************************
        # remove running
        self.play(Unwrite(mt_running, run_time=wt))

        # highlight head cards and modules
        mask_graph = np.zeros(graph.ncards, dtype=bool)
        mask_graph[22:] = True
        mask_module = np.zeros(len(mm_modules), dtype=bool)
        mask_module[16:] = True
        self.play(AnimationGroup(
            graph.highlight(mask_graph, run_time=wt*0.1),
            highlight_vgroup(mm_modules, mask_module, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # move backup tensors
        self.play(AnimationGroup(
            mt_c15.animate(run_time=wt).set_opacity(1.0).next_to(mm_modules[16],LEFT).set_x(-RUNNING_X),
            mt_c18.animate(run_time=wt).set_opacity(1.0).next_to(mm_modules[17],LEFT).set_x(-RUNNING_X),
            mt_c21.animate(run_time=wt).set_opacity(1.0).next_to(mm_modules[18],LEFT).set_x(-RUNNING_X),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # prepare output tensors
        mt_22_box = mt_c15.copy().stretch_to_fit_depth(mt_c15.depth*16/16).set_x(RUNNING_X)
        mt_22_cls = mt_c15.copy().stretch_to_fit_depth(mt_c15.depth*3/16).set_x(RUNNING_X*1.6)
        mt_23_box = mt_c18.copy().stretch_to_fit_depth(mt_c18.depth*16/20).set_x(RUNNING_X)
        mt_23_cls = mt_c18.copy().stretch_to_fit_depth(mt_c18.depth*3/20).set_x(RUNNING_X*1.6)
        mt_24_box = mt_c21.copy().stretch_to_fit_depth(mt_c21.depth*16/24).set_x(RUNNING_X)
        mt_24_cls = mt_c21.copy().stretch_to_fit_depth(mt_c21.depth*3/24).set_x(RUNNING_X*1.6)

        # apply module
        self.play(AnimationGroup(
            mm_modules[16].breath(
                run_time=wt*0.5,
            ),
            mm_modules[17].breath(
                run_time=wt*0.5,
            ),
            mm_modules[18].breath(
                run_time=wt*0.5,
            ),
            lag_ratio=0.5,
        ))
        self.play(AnimationGroup(
            AnimationGroup(
                GrowFromCenter(mt_22_box, rate_func=rate_functions.ease_out_back),
                GrowFromCenter(mt_22_cls, rate_func=rate_functions.ease_out_back),
                lag_ratio=0.5,
                run_time=wt,
            ),
            AnimationGroup(
                GrowFromCenter(mt_23_box, rate_func=rate_functions.ease_out_back),
                GrowFromCenter(mt_23_cls, rate_func=rate_functions.ease_out_back),
                lag_ratio=0.5,
                run_time=wt,
            ),
            AnimationGroup(
                GrowFromCenter(mt_24_box, rate_func=rate_functions.ease_out_back),
                GrowFromCenter(mt_24_cls, rate_func=rate_functions.ease_out_back),
                lag_ratio=0.5,
                run_time=wt,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'simplified view',
            skip_animations=False,
        )
        # ************************************************************
        # remove backups, show initial input
        mt_input = FTensor3D(
            shape=(3,640,640),
            size_config={
                'width': 64*UNIT_FTENSOR_SIZE,
                'height': 64*UNIT_FTENSOR_SIZE,
                'depth': 3*UNIT_FTENSOR_SIZE,
            },
            opaque=True,
        ).scale(INIT_SCALE).next_to(mm_modules[0], UP*5)
        self.play(AnimationGroup(
            Unwrite(mt_c15, run_time=wt),
            Unwrite(mt_c18, run_time=wt),
            Unwrite(mt_c21, run_time=wt),
            Write(mt_input, run_time=wt),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # smaller zoom, reposition outputs
        mt_outputs = VGroup(
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        self.move_camera(
            zoom=0.25,              # NOTE
            added_anims=[
                mt_outputs.animate(
                    run_time=wt,
                ).next_to(mm_modules[-1], DOWN*5),
            ],
            run_time=wt,
        )
        self.wait(wt)

        # lightup all graph cards and modules
        self.play(AnimationGroup(
            graph.highlight(None, run_time=wt*0.1),
            highlight_vgroup(mm_modules, None, run_time=wt*0.1),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # export
        mobs = VGroup(
            mm_modules, card, graph,
            mt_input,
            mt_22_box, mt_22_cls,
            mt_23_box, mt_23_cls,
            mt_24_box, mt_24_cls,
        )
        export_mobs(__file__, mobs)     # used by next
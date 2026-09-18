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
from modules.ut_YOLOv8 import *

# from ultralytics.nn.modules import YOLOv8

import torch

INIT_CONFIG = {
    'scale': 'n',
    # 'nc': 3,
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
        cards_model, _ = import_mobs('045a')

        # raw module with random init
        module_config = INIT_CONFIG
        # ut_module = Detect(**module_config)   # not used

        # module graph
        graph_model = MGraph_YOLOv8(module_config)

        # show initial mobs
        self.set_camera_orientation(
            **VIEW_INTRO,
        )
        self.add_fixed_in_frame_mobjects(cards_model)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'introduce graph',
            skip_animations=False,
        )
        # ************************************************************
        # create unexpanded graph
        self.play(graph_model.create(
            run_time=wt,
            rate_func=smooth,
        ))
        self.wait()

        # connect without expand summary
        self.play(graph_model.connect(
            lag_ratio=0.5,
            run_time=wt*10,
        ))
        self.wait(wt)

        # loop though cards
        masks = np.eye(graph_model.ncards,dtype=bool)
        self.play(graph_model.highlight_loop(
            masks=masks,
            rate_func=smooth,
            run_time=wt*10,
        ))
        self.play(graph_model.highlight(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'reposition heads',
            skip_animations=False,
        )
        # ************************************************************
        self.play(graph_model.reposition_heads(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(graph_model.animate(
            run_time=wt,
        ))  # set_y(0.3)?
        self.wait(wt)

        # # loop though cards
        # masks = np.eye(graph_model.ncards,dtype=bool)
        # self.play(graph_model.highlight_loop(
        #     masks=masks,
        #     rate_func=smooth,
        #     run_time=wt*10,
        # ))
        # self.play(graph_model.highlight(
        #     run_time=wt,
        # ))
        # self.wait(wt)

        # ************************************************************
        self.next_section(
            'arrange into network style',
            skip_animations=False,
        )
        # ************************************************************
        self.play(graph_model.reposition_all(
            lag_ratio=0.0,
            run_time=wt*3,
        ))
        self.wait(wt)

        # loop though cards
        masks = np.eye(graph_model.ncards,dtype=bool)
        self.play(graph_model.highlight_loop(
            masks=masks,
            rate_func=smooth,
            run_time=wt*10,
        ))
        self.play(graph_model.highlight(
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'before summaries on different scales',
            skip_animations=False,
        )
        # ************************************************************
        # clean lines
        self.play(AnimationGroup(
            *(FadeOut(line) for line in graph_model.lines),
            lag_ratio=0.0,
            run_time=wt,
        ))
        graph_model.remove(graph_model.lines)
        # self.wait(wt)

        # rearrange in series
        self.play(graph_model.mobs_card.animate(
            run_time=wt,
        ).arrange(
            DOWN,
            buff=CARD_BUFF_V_SMALL,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'create 4 graph copies',
            skip_animations=False,
        )
        # ************************************************************
        graphs = VGroup(
            graph_model,
            graph_model.copy(),
            graph_model.copy(),
            graph_model.copy(),
            graph_model.copy(),
        )
        self.add_fixed_in_frame_mobjects(graphs)
        # self.wait(wt)

        graphs.generate_target()
        graphs.target.scale(0.8).arrange(RIGHT, buff=1.5)
        self.play(MoveToTarget(graphs, run_time=wt))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'summaries on 5 scales',
            skip_animations=False,
        )
        # ************************************************************
        sss = [
            [v[1] for v in LAYER_ARGS['n'].values()],
            [v[1] for v in LAYER_ARGS['s'].values()],
            [v[1] for v in LAYER_ARGS['m'].values()],
            [v[1] for v in LAYER_ARGS['l'].values()],
            [v[1] for v in LAYER_ARGS['x'].values()],
        ]

        self.play(AnimationGroup(
            *(graph.expand(
                summaries=summaries,
                rate_func=smooth,
                lag_ratio=0.5,
                run_time=wt*5,
            ) for graph, summaries in zip(graphs, sss)),
            lag_ratio=0.0,
        ))
        self.wait(wt)

        # TODO: loop through cards and graphs?

        # attach cards to top of graphs
        self.play(AnimationGroup(
            *(card.animate.next_to(graph, UP, buff=0.2)
             for card, graph in zip(cards_model, graphs)),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'nc as summary for model cards',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            *(card.expand_summary('3', direction='center') for card in cards_model),
            lag_ratio=0.5,
            run_time=wt*3,
        ))
        self.wait(wt)

        # highlight head layers for each graph
        mask = np.zeros(graphs[0].ncards,dtype=bool)
        mask[-3:] = True
        self.play(AnimationGroup(
            *(graph.highlight(mask) for graph in graphs),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # nc -> 20
        self.play(AnimationGroup(
            Succession(
                cards_model[0].update_summary('20'),
                graphs[0].mobs_card[-3].update_summary('64 64 64 16 20'),
                graphs[0].mobs_card[-2].update_summary('128 64 64 16 20'),
                graphs[0].mobs_card[-1].update_summary('256 64 64 16 20'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[1].update_summary('20'),
                graphs[1].mobs_card[-3].update_summary('128 64 128 16 20'),
                graphs[1].mobs_card[-2].update_summary('256 64 128 16 20'),
                graphs[1].mobs_card[-1].update_summary('512 64 128 16 20'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[2].update_summary('20'),
                graphs[2].mobs_card[-3].update_summary('192 64 192 16 20'),
                graphs[2].mobs_card[-2].update_summary('384 64 192 16 20'),
                graphs[2].mobs_card[-1].update_summary('576 64 192 16 20'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[3].update_summary('20'),
                graphs[3].mobs_card[-3].update_summary('256 64 256 16 20'),
                graphs[3].mobs_card[-2].update_summary('512 64 256 16 20'),
                graphs[3].mobs_card[-1].update_summary('512 64 256 16 20'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[4].update_summary('20'),
                graphs[4].mobs_card[-3].update_summary('320 80 320 16 20'),
                graphs[4].mobs_card[-2].update_summary('640 80 320 16 20'),
                graphs[4].mobs_card[-1].update_summary('640 80 320 16 20'),
                run_time=wt*3,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # nc -> 80
        self.play(AnimationGroup(
            Succession(
                cards_model[0].update_summary('80'),
                graphs[0].mobs_card[-3].update_summary('64 64 80 16 80'),
                graphs[0].mobs_card[-2].update_summary('128 64 80 16 80'),
                graphs[0].mobs_card[-1].update_summary('256 64 80 16 80'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[1].update_summary('80'),
                graphs[1].mobs_card[-3].update_summary('128 64 128 16 80'),
                graphs[1].mobs_card[-2].update_summary('256 64 128 16 80'),
                graphs[1].mobs_card[-1].update_summary('512 64 128 16 80'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[2].update_summary('80'),
                graphs[2].mobs_card[-3].update_summary('192 64 192 16 80'),
                graphs[2].mobs_card[-2].update_summary('384 64 192 16 80'),
                graphs[2].mobs_card[-1].update_summary('576 64 192 16 80'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[3].update_summary('80'),
                graphs[3].mobs_card[-3].update_summary('256 64 256 16 80'),
                graphs[3].mobs_card[-2].update_summary('512 64 256 16 80'),
                graphs[3].mobs_card[-1].update_summary('512 64 256 16 80'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[4].update_summary('80'),
                graphs[4].mobs_card[-3].update_summary('380 80 380 16 80'),
                graphs[4].mobs_card[-2].update_summary('640 80 380 16 80'),
                graphs[4].mobs_card[-1].update_summary('640 80 380 16 80'),
                run_time=wt*3,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # nc -> 133
        self.play(AnimationGroup(
            Succession(
                cards_model[0].update_summary('133'),
                graphs[0].mobs_card[-3].update_summary('64 64 100 16 133'),
                graphs[0].mobs_card[-2].update_summary('128 64 100 16 133'),
                graphs[0].mobs_card[-1].update_summary('256 64 100 16 133'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[1].update_summary('133'),
                graphs[1].mobs_card[-3].update_summary('128 64 128 16 133'),
                graphs[1].mobs_card[-2].update_summary('256 64 128 16 133'),
                graphs[1].mobs_card[-1].update_summary('512 64 128 16 133'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[2].update_summary('133'),
                graphs[2].mobs_card[-3].update_summary('192 64 192 16 133'),
                graphs[2].mobs_card[-2].update_summary('384 64 192 16 133'),
                graphs[2].mobs_card[-1].update_summary('576 64 192 16 133'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[3].update_summary('133'),
                graphs[3].mobs_card[-3].update_summary('256 64 256 16 133'),
                graphs[3].mobs_card[-2].update_summary('512 64 256 16 133'),
                graphs[3].mobs_card[-1].update_summary('512 64 256 16 133'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[4].update_summary('133'),
                graphs[4].mobs_card[-3].update_summary('380 80 380 16 133'),
                graphs[4].mobs_card[-2].update_summary('640 80 380 16 133'),
                graphs[4].mobs_card[-1].update_summary('640 80 380 16 133'),
                run_time=wt*3,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # nc -> 3
        self.play(AnimationGroup(
            Succession(
                cards_model[0].update_summary('3'),
                graphs[0].mobs_card[-3].update_summary('64 64 64 16 3'),
                graphs[0].mobs_card[-2].update_summary('128 64 64 16 3'),
                graphs[0].mobs_card[-1].update_summary('256 64 64 16 3'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[1].update_summary('3'),
                graphs[1].mobs_card[-3].update_summary('128 64 128 16 3'),
                graphs[1].mobs_card[-2].update_summary('256 64 128 16 3'),
                graphs[1].mobs_card[-1].update_summary('512 64 128 16 3'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[2].update_summary('3'),
                graphs[2].mobs_card[-3].update_summary('192 64 192 16 3'),
                graphs[2].mobs_card[-2].update_summary('384 64 192 16 3'),
                graphs[2].mobs_card[-1].update_summary('576 64 192 16 3'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[3].update_summary('3'),
                graphs[3].mobs_card[-3].update_summary('256 64 256 16 3'),
                graphs[3].mobs_card[-2].update_summary('512 64 256 16 3'),
                graphs[3].mobs_card[-1].update_summary('512 64 256 16 3'),
                run_time=wt*3,
            ),
            Succession(
                cards_model[4].update_summary('3'),
                graphs[4].mobs_card[-3].update_summary('320 80 320 16 3'),
                graphs[4].mobs_card[-2].update_summary('640 80 320 16 3'),
                graphs[4].mobs_card[-1].update_summary('640 80 320 16 3'),
                run_time=wt*3,
            ),
            lag_ratio=0.5,
        ))
        self.wait(wt)

        # # # ************************************************************
        # # self.next_section(
        # #     'prepare for compute',
        # #     skip_animations=False,
        # # )
        # # # ************************************************************
        # # # graph to right edge
        # # self.play(graph_model.animate(
        # #     run_time=wt,
        # # ).scale(
        # #     0.8
        # # ).to_edge(RIGHT, buff=MGRAPH_EDGE_BUFF))
        # # self.wait(wt)


        # # mobs = VGroup(card_module, graph_model)
        # # export_mobs(__file__, mobs)      # used by next

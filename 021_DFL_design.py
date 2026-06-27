from manim import *

from utils.general import import_mobs, export_mobs
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.image_pad import ImagePad
from utils.explainer import Explainer
from utils.anchor_point import DIRECTION_SERIES

from utils.constants import *

import random

N_COMPUTE_SAMPLES = 5
SAMPLE_IDX = 190

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=True,
        )
        # ************************************************************
        background = ImagePad(padded=True).set_opacity(0.1)
        e32 = Explainer.from_file(
            background=background,
            version=32,
        )
        s32 = Group(background, e32)
        self.add(s32)
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'compute on one sample anchor point',
            skip_animations=False,
        )
        # ************************************************************
        self.play(e32.show_anchor_points(
            lag_ratio=0.5,
            run_time=wt,
        ))
        self.wait(wt)

        # sample anchor point, other anchor points
        sap, oaps = e32.random_ap(SAMPLE_IDX)

        # focus on sample anchor point
        self.play(
            sap.mob.animate.set_opacity(1.0),       # TODO: make opacity variable
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.1)
                for ap in oaps),
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=wt,
        )
        self.wait(wt)

        cps = sap.create_DFL_computations(
            buff=0.25,
            text_config={
                'color': GRAY,
                'font_size': 12,
            },
        ).shift(RIGHT*3)
        for i, direction in enumerate(DIRECTION_SERIES):
            # show probcells
            self.play(sap.show_pcells(
                direction=direction,
                box_config={},
                lag_ratio = 0.5,
                run_time = wt,
            ))
            self.wait(wt)

            # show prob in probcells
            self.play(sap.show_pcells_text(
                direction=direction,
                text_config={
                    'font_size': 10,
                },
                gargs={
                    'lag_ratio': 0.5,
                    'run_time': wt,
                },
            ))
            self.wait(wt)

            # make room in the right for first iteration
            if i == 0:
                self.play(s32.animate(
                    run_time=wt,
                ).shift(LEFT*3))
                self.wait(wt)

            # compute from distribution into distance
            self.play(Create(cps[i]))
            self.wait(wt)

            # hide prob in probcells
            self.play(sap.hide_pcells_text(
                direction=direction,
                gargs={
                    'lag_ratio': 0.5,
                    'run_time': wt,
                },
            ))
            self.wait(wt)

            # show arrows
            self.play(sap.show_arrows(
                direction=direction,
                arrow_config={},
                run_time=wt,
            ))
            self.wait(wt)
        
        # highlight pcells borders
        pcells = VGroup(
            pc for pcs in sap.pcells.values() for pc in pcs
        )
        self.play(AnimationGroup(
            *(pc.mob_box.animate(
                rate_func=rate_functions.there_and_back,
            ).set_stroke(
                color=WHITE,
                opacity=1.0,
            ) for pc in pcells),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through several samples',
            skip_animations=False,
        )
        # ************************************************************
        sample_idxs = random.sample(
            range(len(e32.anchor_points)),
            N_COMPUTE_SAMPLES,
        )

        for idx in sample_idxs:
            # clean old probcells
            self.play(sap.hide_pcells(
                lag_ratio=0.3,
                run_time=wt,
            ))
            self.wait(wt)

            # clean old arrows
            self.play(sap.hide_arrows(
                lag_ratio=0.0,
                run_time=wt,
            ))

            # focus on new anchor point
            sap, oaps = e32.random_ap(idx)
            self.play(
                sap.mob.animate.set_opacity(1.0),
                AnimationGroup(
                    *(ap.mob.animate.set_opacity(0.1)
                    for ap in oaps),
                    lag_ratio=0.0,
                ),
                lag_ratio=0.0,
                run_time=wt,
            )
            self.wait(wt)

            # show probcells
            self.play(sap.show_pcells(
                box_config={},
                lag_ratio=0.0,
                run_time=wt,
            ))
            self.wait(wt)

            # transfrom computations
            cps_new = sap.create_DFL_computations(
                buff=0.25,
                text_config={
                    'color': GRAY,
                    'font_size': 12,
                },
            ).move_to(cps, aligned_edge=UL)
            self.play(Transform(
                cps,
                cps_new,
                run_time=wt,
            ))
            self.wait(wt)

            # show arrows
            self.play(sap.show_arrows(
                arrow_config={},
                lag_ratio=0.3,
                run_time=wt,
            ))
        
        # clean jobs
        self.play(sap.hide_pcells(
            lag_ratio=0.3,
            run_time=wt,
        ))
        self.play(sap.hide_arrows(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            *(ap.mob.animate.set_opacity(1.0)
            for ap in e32.anchor_points),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.play(AnimationGroup(
            Uncreate(cps, lag_ratio=0.0),
            s32.animate.center(),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # # ************************************************************
        # self.next_section(
        #     'digital representation of distributions*4',
        #     skip_animations=False,
        # )
        # # ************************************************************
        # export_mobs(__file__, s32)
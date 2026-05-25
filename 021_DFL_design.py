from manim import *

from utils.constants import *
from utils.general import import_mobs, export_mobs
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.image_pad import ImagePad
from utils.explainer import Explainer
from utils.anchor_point import DIRECTION_SERIES

import random

N_COMPUTE_SAMPLES = 5

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init all mobs',
            skip_animations=False,
        )
        # ************************************************************
        background = ImagePad(padded=True).set_opacity(0.1)
        e32 = Explainer.from_file(
            background=background,
            version=32,
        )
        s32 = Group(background, e32)
        self.add(s32)
        self.wait()

        # ************************************************************
        self.next_section(
            'compute on one sample anchor point',
            skip_animations=False,
        )
        # ************************************************************
        self.play(e32.show_anchor_points(
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.5)

        compute_idx = 190
        # sample anchor point, other anchor points
        sap, oaps = e32.random_ap(compute_idx)

        # focus on sample anchor point
        self.play(
            sap.mob.animate.set_opacity(1.0),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.1)
                for ap in oaps),
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=0.5,
        )
        self.wait(0.5)

        cps = sap.create_DFL_computations(
            buff=0.25,
            text_config={
                'font_size': 12,
            },
        ).shift(RIGHT*3)
        for i, direction in enumerate(DIRECTION_SERIES):
            # show probcells
            self.play(sap.show_pcells_direction(
                direction=direction,
                label_config={
                    'font_size': 10,
                    'color': WHITE,
                },
                box_config={},
                lag_ratio = 0.5,
                run_time = 0.5,
            ))
            self.wait(0.5)

            # show prob in probcells
            self.play(sap.show_pcells_text_direction(
                direction=direction,
                lag_ratio=0.5,
                run_time=0.5
            ))
            self.wait(0.5)

            # make room in the right for first iteration
            if i == 0:
                self.play(s32.animate(
                    run_time=0.5,
                ).shift(LEFT*3))
                self.wait(0.5)

            # compute from distribution into distance
            self.play(Create(cps[i]))
            self.wait(0.5)

            # hide prob in probcells
            self.play(sap.hide_pcells_text_direction(
                direction=direction,
                lag_ratio=0.5,
                run_time=0.5
            ))
            self.wait(0.5)

            # show arrow
            self.play(sap.show_arrow_direction(
                direction=direction,
                arrow_config={},
                run_time=0.5,
            ))
            self.wait(0.5)
        
        # highlight prob number for each direction
        sap.pcells.save_state()
        self.play(AnimationGroup(
            *(pc.mob_box.animate.set_stroke(
                color=WHITE,
                opacity=1.0,
            ) for pc in sap.pcells),
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(0.5)
        self.play(sap.pcells.animate(
            lag_ratio=0.0,
            run_time=0.5,
        ).restore())
        self.wait(0.5)

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
                run_time=0.5,
            ))
            self.wait(0.5)

            # clean old arrows
            self.play(sap.hide_arrows(
                lag_ratio=0.0,
                run_time=0.5,
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
                run_time=0.5,
            )
            self.wait(0.5)

            # show probcells
            self.play(sap.show_pcells(
                label_config={},
                box_config={},
                lag_ratio=0.0,
                run_time=0.5,
            ))
            self.wait(0.5)

            # transfrom computations
            cps_new = sap.create_DFL_computations(
                buff=0.25,
                text_config={
                    'font_size': 12,
                },
            ).move_to(cps, aligned_edge=UL)
            self.play(Transform(
                cps,
                cps_new,
                run_time=0.5,
            ))
            self.wait(0.5)

            # show arrows
            self.play(sap.show_arrows(
                arrow_config={},
                aargs={},
                gargs={
                    'lag_ratio': 0.3,
                    'run_time': 0.5,
                },
            ))
        
        # clean jobs
        self.play(sap.hide_pcells(
            lag_ratio=0.3,
            run_time=0.5,
        ))
        self.play(sap.hide_arrows(
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.play(AnimationGroup(
            *(ap.mob.animate.set_opacity(1.0)
            for ap in e32.anchor_points),
            lag_ratio=0.0,
        ))
        self.play(AnimationGroup(
            Uncreate(cps),
            s32.animate.center(),
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'digital representation of distributions*4',
            skip_animations=False,
        )
        # ************************************************************
        export_mobs(__file__, s32)
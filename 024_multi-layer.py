from manim import *

from utils.constants import *
from utils.layers_fake import LayersFake
from utils.multi_arrow import MultiArrow
from utils.arrow_comment import ArrowComment
from utils.show_shape import ShowShape, HideShape
from utils.general import import_mobs, export_mobs, random_path
from utils.image_pad import ImagePad
from utils.explainer import Explainer

SAMPLE_IDX_8 = 6400//2 - 80//2
SAMPLE_IDX_16 = 1600//2 - 40//2
SAMPLE_IDX_32 = 400//2 - 20//2

N_SAMPLES = 100

class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'stride 32 system',
            skip_animations=True,
        )
        # ************************************************************
        # NOTE: b->background, e->explainer, s->system
        b32 = ImagePad(padded=True).set_opacity(0.1)
        b16 = b32.copy().shift(LEFT*10)
        b8 = b32.copy().shift(LEFT*10)
        e32 = Explainer.from_file(
            background=b32,
            version=32,
            dot_config=MEDIUM_DOT_CONFIG,
            rect_config=MEDIUM_RECT_CONFIG,
        )
        e16 = Explainer.from_file(
            background=b16,
            version=16,
            dot_config=SMALL_DOT_CONFIG,
            rect_config=SMALL_RECT_CONFIG,
        )
        e8 = Explainer.from_file(
            background=b8,
            version=8,
            dot_config=MINI_DOT_CONFIG,
            rect_config=MINI_RECT_CONFIG,
        )
        s32 = Group(b32, e32)
        s16 = Group(b16, e16)
        s8 = Group(b8, e8)
        
        self.add(s32)
        self.wait()

        self.play(e32.show_anchor_points(
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait()

        # ************************************************************
        self.next_section(
            'hard examples for stride 32',
            skip_animations=True,
        )
        # ************************************************************
        # TODO

        # ************************************************************
        self.next_section(
            'instroduce stride 16/8 background',
            skip_animations=True,
        )
        # ************************************************************
        mobs = Group(b8, b16, s32)
        mobs.generate_target()
        mobs.target.scale(0.8)
        mobs.target.arrange(
            direction=RIGHT,
            # buff=1.0,
        ).center()
        self.play(MoveToTarget(
            mobs,
            run_time=0.5,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'instroduce stride 16/8 explainer',
            skip_animations=True,
        )
        # ************************************************************

        self.play(AnimationGroup(
            s8[-1].show_anchor_points(
                lag_ratio=0.0,
            ),
            s16[-1].show_anchor_points(
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=0.3,
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'capture for 3 versions of strides',
            skip_animations=True,
        )
        # ************************************************************
        self.wait(0.5)
        self.play(AnimationGroup(
            s8[-1].to_rects(
                rect_config={},
                aargs={},
                gargs={},
            ),
            s16[-1].to_rects(
                rect_config={},
                aargs={},
                gargs={},
            ),
            s32[-1].to_rects(
                rect_config={},
                aargs={},
                gargs={},
            ),
            run_time=0.5,
            lag_ratio=0.0,
        ))
        self.wait(0.3)

        # ************************************************************
        self.next_section(
            'hards example for stride 32/16/8',
            skip_animations=True,
        )
        # ************************************************************
        # TODO

        # ************************************************************
        self.next_section(
            'back to dots for stride 32/16/8',
            skip_animations=True,
        )
        # ************************************************************
        self.wait(0.5)
        self.play(AnimationGroup(
            s8[-1].to_dots(
                dot_config={},
                aargs={},
                gargs={},
            ),
            s16[-1].to_dots(
                dot_config={},
                aargs={},
                gargs={},
            ),
            s32[-1].to_dots(
                dot_config={},
                aargs={},
                gargs={},
            ),
            run_time=0.5,
            lag_ratio=0.0,
        ))
        self.wait(0.3)

        # ************************************************************
        self.next_section(
            'focus on sample anchor point for each map',
            skip_animations=True,
        )
        # ************************************************************
        sap_8, oaps_8 = s8[-1].random_ap(SAMPLE_IDX_8)
        sap_16, oaps_16 = s16[-1].random_ap(SAMPLE_IDX_16)
        sap_32, oaps_32 = s32[-1].random_ap(SAMPLE_IDX_32)

        self.wait(0.5)
        self.play(AnimationGroup(
            sap_8.mob.animate.set_opacity(1.0),
            sap_16.mob.animate.set_opacity(1.0),
            sap_32.mob.animate.set_opacity(1.0),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.1)
                for ap in oaps_8),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.1)
                for ap in oaps_16),
                lag_ratio=0.0,
            ),
            AnimationGroup(
                *(ap.mob.animate.set_opacity(0.1)
                for ap in oaps_32),
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=0.5,
        ))

        # ************************************************************
        self.next_section(
            'show pcells for each sample anchor point',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            sap_8.show_pcells(
                label_config={},
                box_config={},
                lag_ratio=0.0,
            ),
            sap_16.show_pcells(
                label_config={},
                box_config={},
                lag_ratio=0.0,
            ),
            sap_32.show_pcells(
                label_config={},
                box_config={},
                lag_ratio=0.0,
            ),
            lag_ratio=0.0,
            run_time=0.5,
        ))
        self.wait(0.5)
        # highlight borders for pcells
        self.play(AnimationGroup(
            AnimationGroup(
                *(pc.mob_box.animate.set_stroke(
                    color=WHITE,
                    opacity=1.0,
                    width=0.3,
                ) for pc in sap_8.pcells),
                lag_ratio=0.0,
                run_time=0.5,
            ),
            AnimationGroup(
                *(pc.mob_box.animate.set_stroke(
                    color=WHITE,
                    opacity=1.0,
                    width=0.5,
                ) for pc in sap_16.pcells),
                lag_ratio=0.0,
                run_time=0.5,
            ),
            AnimationGroup(
                *(pc.mob_box.animate.set_stroke(
                    color=WHITE,
                    opacity=1.0,
                    width=1.0,
                ) for pc in sap_32.pcells),
                lag_ratio=0.0,
                run_time=0.5,
            ),
        ))
        self.wait(0.5)

        # ************************************************************
        self.next_section(
            'loop through random aps for each stride',
            skip_animations=False,
        )
        # TODO: naming of variables
        # TODO: better looping path, fashion and cool
        # ************************************************************
        sample_idxs_8 = random_path(
            n=N_SAMPLES,
            step=6,
            shape=e8.shape,
            start_idx=SAMPLE_IDX_8,
        )
        sample_idxs_16 = random_path(
            n=N_SAMPLES,
            step=4,
            shape=e16.shape,
            start_idx=SAMPLE_IDX_16,
        )
        sample_idxs_32 = random_path(
            n=N_SAMPLES,
            step=2,
            shape=e32.shape,
            start_idx=SAMPLE_IDX_32,
        )
        for idx_8, idx_16, idx_32 in zip(sample_idxs_8, sample_idxs_16, sample_idxs_32):
            _sap_8, _oaps_8 = e8.random_ap(idx_8)
            _sap_16, _oaps_16 = e16.random_ap(idx_16)
            _sap_32, _oaps_32 = e32.random_ap(idx_32)

            pcs_8 = _sap_8.create_pcells(
                label_config={},
                box_config={},
            )
            pcs_16 = _sap_16.create_pcells(
                label_config={},
                box_config={},
            )
            pcs_32 = _sap_32.create_pcells(
                label_config={},
                box_config={},
            )
            # for pc8, pc16, pc32 in zip(pcs_8, pcs_16, pcs_32):
            #     pc8.mob_box.set_stroke(
            #         color=WHITE,
            #         opacity=1.0,
            #         width=0.3,
            #     )
            #     pc16.mob_box.set_stroke(
            #         color=WHITE,
            #         opacity=1.0,
            #         width=0.5,
            #     )
            #     pc32.mob_box.set_stroke(
            #         color=WHITE,
            #         opacity=1.0,
            #         width=1.0,
            #     )
            self.play(
                Transform(
                    sap_8.pcells,
                    pcs_8,
                    rate_func=rate_functions.linear,
                ),
                Transform(
                    sap_16.pcells,
                    pcs_16,
                    rate_func=rate_functions.linear,
                ),
                Transform(
                    sap_32.pcells,
                    pcs_32,
                    rate_func=rate_functions.linear,
                ),
                _sap_8.mob.animate.set_opacity(1.0),
                _sap_16.mob.animate.set_opacity(1.0),
                _sap_32.mob.animate.set_opacity(1.0),
                AnimationGroup(
                    *(ap.mob.animate.set_opacity(0.1)
                    for ap in _oaps_8),
                    lag_ratio=0.0,
                ),
                AnimationGroup(
                    *(ap.mob.animate.set_opacity(0.1)
                    for ap in _oaps_16),
                    lag_ratio=0.0,
                ),
                AnimationGroup(
                    *(ap.mob.animate.set_opacity(0.1)
                    for ap in _oaps_32),
                    lag_ratio=0.0,
                ),
                lag_ratio=0.0,
                run_time=0.1,
            )
        self.wait(0.5)
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

N_SAMPLES = 3

wt = SHORT_DURATION
class MainScene(Scene):
    def construct(self):
        # ************************************************************
        self.next_section(
            'init [b/e/s][8/16/32]',
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
        
        # start with system 32
        self.add(s32)
        self.wait()

        self.play(e32.show_anchor_points(
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'hard examples for stride 32',
            skip_animations=True,
        )
        # ************************************************************
        # TODO

        # ************************************************************
        self.next_section(
            'instroduce stride 8/16 background',
            skip_animations=True,
        )
        # ************************************************************
        mobs = Group(b8, b16, s32)
        mobs.generate_target()
        mobs.target.scale(0.8)
        OFFSET = 4.5
        mobs.target[0].shift(np.array([-OFFSET, 0, 0]) - mobs.target[0][0].get_center())
        mobs.target[1].shift(np.array([      0, 0, 0]) - mobs.target[1][0].get_center())
        mobs.target[2].shift(np.array([+OFFSET, 0, 0]) - mobs.target[2][0].get_center())
        self.play(MoveToTarget(
            mobs,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'instroduce 8/16 anchor points capture',
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
            run_time=wt,
        ))
        self.wait(wt)

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
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'back to dots for stride 8/16/32',
            skip_animations=True,
        )
        # ************************************************************
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
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'focus on sample anchor point for each map',
            skip_animations=False,
        )
        # ************************************************************
        sap_8, oaps_8 = s8[-1].random_ap(SAMPLE_IDX_8)
        sap_16, oaps_16 = s16[-1].random_ap(SAMPLE_IDX_16)
        sap_32, oaps_32 = s32[-1].random_ap(SAMPLE_IDX_32)

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
            run_time=wt,
        ))

        # ************************************************************
        self.next_section(
            'show pcells for each sample anchor point',
            skip_animations=False,
        )
        # ************************************************************
        self.play(AnimationGroup(
            sap_8.show_pcells(
                box_config={},
                lag_ratio=0.5,
            ),
            sap_16.show_pcells(
                box_config={},
                lag_ratio=0.5,
            ),
            sap_32.show_pcells(
                box_config={},
                lag_ratio=0.5,
            ),
            lag_ratio=0.0,
            run_time=wt,
        ))
        self.wait(wt)

        # ************************************************************
        self.next_section(
            'loop through random aps for each stride',
            skip_animations=False,
        )
        # ************************************************************
        # TODO: better looping path, fashion and cool
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

            pcs_8 = _sap_8.create_pcells(box_config={})
            pcs_16 = _sap_16.create_pcells(box_config={})
            pcs_32 = _sap_32.create_pcells(box_config={})
            self.play(AnimationGroup(
                AnimationGroup(
                    *(Transform(pcs1, pcs2)
                      for pcs1, pcs2 in zip(sap_8.pcells.values(), pcs_8.values())),
                    *(ap.mob.animate.set_opacity(0.1)
                      for ap in _oaps_8),
                    _sap_8.mob.animate.set_opacity(1.0),
                ),
                AnimationGroup(
                    *(Transform(pcs1, pcs2)
                      for pcs1, pcs2 in zip(sap_16.pcells.values(), pcs_16.values())),
                    *(ap.mob.animate.set_opacity(0.1)
                      for ap in _oaps_16),
                    _sap_16.mob.animate.set_opacity(1.0),
                ),
                AnimationGroup(
                    *(Transform(pcs1, pcs2)
                      for pcs1, pcs2 in zip(sap_32.pcells.values(), pcs_32.values())),
                    *(ap.mob.animate.set_opacity(0.1)
                      for ap in _oaps_32),
                    _sap_32.mob.animate.set_opacity(1.0),
                ),
                lag_ratio=0.0,
                run_time=wt,
            ))
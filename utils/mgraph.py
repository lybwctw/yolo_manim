import sys
sys.path.append('..')

from manim import *
from utils.info_card import *

MCARD_BUFF_MINI = 0.1
MCARD_BUFF_SMALL = 0.2
MCARD_BUFF_MEDIUM = 0.35
MCARD_BUFF_BIG = 1.0

MGRAPH_EDGE_BUFF = 0.3

LINE_CONFIG_DEFAULT = {
    'stroke_width': 2.0,
    'color': WHITE,
    'stroke_opacity': 0.8,
}

SHAPE_CONFIG_DEFAULT = {
    'font': 'JetBrains Mono',
    'font_size': 10,
    'color': GRAY,
}

class MGraph(VMobject):
    def __init__(
        self,
        module_config: dict = {},
    ):
        super().__init__()
        self.module_config = module_config

        objs_card, mobs_card = self.create_cards()
        self.objs_card = objs_card
        self.mobs_card = mobs_card

        self.hl_state = np.ones(self.ncards, dtype=bool)

        self.add(mobs_card)

    def create_cards(
        self,
    ) -> tuple:
        raise NotImplementedError()

    def create(
        self,
        **aargs,
    ) -> Animation:
        return AnimationGroup(
            *(GrowFromCenter(
                card,
                rate_func=rate_functions.ease_out_back,
                fixed=True,
            ) for card in self.mobs_card),
            **aargs,
            _on_finish=lambda _: self.add(self.mobs_card),
        )

    def create(
        self,
        **aargs,
    ) -> Animation:
        return AnimationGroup(
            *(GrowFromCenter(
                card,
                rate_func=rate_functions.ease_out_back,
                fixed=True,
            ) for card in self.mobs_card),
            **aargs,
            _on_finish=lambda _: self.add(self.mobs_card),
        )

    def expand(
        self,
        **aargs,
    ) -> Animation:
        raise NotImplementedError()

    def connect(
        self,
        **aargs,
    ) -> Animation:
        raise NotImplementedError()

    def highlight(
        self,
        mask: np.ndarray | None = None,
        **aargs,
    ) -> Animation:
        """Borrowed from MTensor.
        """
        if mask is None:
            mask = np.ones(self.ncards, dtype=bool)
        
        mask_start = self.hl_state
        mask_end = mask

        mask_hl = ~mask_start & mask_end
        mask_dm = ~mask_end & mask_start

        anims_hl = [
            self.mobs_card[idx].lightup() for idx in range(self.ncards) if mask_hl[idx]
            # mob.lightup()
            # for mob in np.array(self.mobs_card,dtype=object)[mask_hl]
        ]
        anims_dm = [
            self.mobs_card[idx].tarnish() for idx in range(self.ncards) if mask_dm[idx]
            # mob.tarnish()
            # for mob in np.array(self.mobs_card,dtype=object)[mask_dm]
        ]

        self.hl_state = mask
        return AnimationGroup(
            *anims_hl,
            *anims_dm,
            **aargs,
        )
    def highlight_loop(
        self,
        masks: list | np.ndarray,
        back: bool = False,              # back to initial state or not
        **aargs,
    ) -> AnimationGroup:
        """Borrowed from MTensor.
        """
        # convert 1st dim into list
        if isinstance(masks, np.ndarray):
            masks = list(masks)

        if back:
            masks_start = [self.hl_state] + masks
            masks_end = masks + [self.hl_state]
        else:
            masks_start = [self.hl_state] + masks[:-1]
            masks_end = masks

        anims_loop = []
        for start, end in zip(masks_start, masks_end):
            mask_hl = ~start & end
            mask_dm = ~end & start
            anims_hl = [
                self.mobs_card[idx].lightup() for idx in range(self.ncards) if mask_hl[idx]
                # mob.lightup()
                # for mob in np.array(self.mobs_card,dtype=object)[mask_hl]
            ]
            anims_dm = [
                self.mobs_card[idx].tarnish() for idx in range(self.ncards) if mask_dm[idx]
                # mob.tarnish()
                # for mob in np.array(self.mobs_card,dtype=object)[mask_dm]
            ]
            # anims_hl = [mob.lightup() for mob in self[mask_hl]]
            # anims_dm = [mob.tarnish() for mob in self[mask_dm]]
            anims_loop.append(AnimationGroup(
                *anims_hl,
                *anims_dm,
                lag_ratio=0.0,  # highlight/fade at the same time
            ))
        
        if not back:
            self.hl_state = masks_end[-1]

        return Succession(
            *anims_loop,
            # rate_func=smooth,
            **aargs,
        )

    def show_shape(
        self,
        text: str = 'None',
        index: int = 0,
        direction: np.ndarray = LEFT,
        buff: float | None = 0.1,
        **aargs,
    ) -> Animation:
        if not hasattr(self, 'objs_shape'):
            self.objs_shape = {}

        tmob = Text(
            text,
            **SHAPE_CONFIG_DEFAULT,
        ).next_to(
            self.lines[index],
            direction,
            buff=buff,
        )

        self.objs_shape[index] = tmob

        return Create(
            tmob,
            fixed=True,
            **aargs,
            _on_finish=lambda _: self.add(tmob),
        )

    def update_shape(
        self,
        text: str = 'None',
        index: int = 0,
        direction: np.ndarray = LEFT,
        buff: float | None = 0.1,
        **aargs,
    ) -> Animation:
        """User's responsiblity to ensure the index is valid.
        """
        if not hasattr(self, 'objs_shape'):
            self.objs_shape = {}

        nmob = Text(
            text,
            **SHAPE_CONFIG_DEFAULT,
        ).next_to(
            self.lines[index],
            direction,
            buff=buff,
        )

        smob_old = self.objs_shape[index]
        self.remove(smob_old)
        self.objs_shape[index] = nmob

        return AnimationGroup(
            Uncreate(smob_old),
            Create(self.objs_shape[index], fixed=True),
            lag_ratio=0.0,
            _on_finish=lambda _: self.add(self.objs_shape[index]),
            **aargs,
        )

    def show_shapes(
        self,
        texts: list,
        indices: list,
        directions: list,
        buff: float | list = 0.1,
        **aargs,
    ) -> Animation:
        """FIXME: not verified yet.
        """
        if not hasattr(self, 'objs_shape'):
            self.objs_shape = {}

        if isinstance(buff, float):
            buff = [buff] * len(texts)

        smobs = VGroup()
        for text, index, direction, bf in zip(
            texts, indices, directions, buff
        ):
            tmob = Text(
                text,
                **SHAPE_CONFIG_DEFAULT,
            ).next_to(
                self.lines[index],
                direction,
                buff=bf,
            )

            self.objs_shape[index] = tmob
            smobs.add(tmob)

        return AnimationGroup(
            *(Create(
                smob,
                fixed=True,
            ) for smob in smobs),
            _on_finish=lambda _: self.add(*smobs),
            **aargs,
        )

    def hide_shapes(
        self,
        **aargs,
    ) -> Animation:
        smobs = VGroup(smob for smob in self.objs_shape.values())
        del self.objs_shape
        return AnimationGroup(
            *(Uncreate(
                smob,
            ) for smob in smobs),
            _on_finish=lambda _: self.remove(*smobs)
            **aargs,
        )

    @property
    def ncards(self):
        return len(self.mobs_card)
from manim import *
from typing import Any

DEFAULT_SHAPE_PATH_CONFIG = {
    'color': PURE_YELLOW,
    'width': 3,
    'opacity': 1.0,
}

DEFAULT_SHAPE_TEXT_CONFIG = {
    'buff': 0.15,
    'font_size': 15,
    'font': 'JetBrains Mono',
    'color': WHITE,
}

DEFAULT_SHOW_AARGS = {
    'lag_ratio': 0.0,
    'run_time': 1.0,
}

DEFAULT_HIDE_AARGS = {
    'lag_ratio': 0.0,
    'run_time': 1.0,
}

class ShowShape(AnimationGroup):
    """
    Example
    -------
    from manim import *
    from utils.image_raw import ImageRaw
    from utils.show_shape import ShowShape, HideShape
    from utils.constants import *

    class Demo(Scene):
        def construct(self):
            img = ImageRaw(path=PATH_IMAGE_960)
            self.add(img)
            self.play(ShowShape(
                img,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
                aargs={'run_time': 1.0},
            ))
            self.wait()
            self.play(HideShape(
                img,
                aargs={'run_time': 1.0},
            ))
            self.wait()
    """
    def __init__(
        self,
        mob: Any = None,
        path_config: dict = {},     # color, width, opacity
        text_config: dict = {},     # font_size, font, buff, color
        aargs: dict = {},           # lag_ratio, run_time
    ):
        path_config = {**DEFAULT_SHAPE_PATH_CONFIG, **path_config}
        text_config = {**DEFAULT_SHAPE_TEXT_CONFIG, **(text_config or {})}
        aargs = {**DEFAULT_SHOW_AARGS, **(aargs or {})}

        # NOTE: mob class SHOULD implement these methods
        path = mob.get_shape_path(**path_config)
        texts = mob.get_shape_text(**(text_config or {}))

        mob.shape_texts = texts      # as child of mob
        mob.add(mob.shape_texts)

        super().__init__(
            ShowPassingFlash(
                path,
                time_width=1.0,
            ),
            AnimationGroup(
                *(Write(t) for t in texts),
                lag_ratio=0.5,
            ),
            **aargs,
        )

class HideShape(AnimationGroup):
    """
    Example
    -------
    from manim import *
    from utils.image_raw import ImageRaw
    from utils.show_shape import ShowShape, HideShape
    from utils.constants import *

    class Demo(Scene):
        def construct(self):
            img = ImageRaw(path=PATH_IMAGE_960)
            self.add(img)
            self.play(ShowShape(
                img,
                text_config=MEDIUM_SHAPE_TEXT_CONFIG,
                aargs={'run_time': 1.0},
            ))
            self.wait()
            self.play(HideShape(
                img,
                aargs={'run_time': 1.0},
            ))
            self.wait()
    """
    def __init__(
        self,
        mob: Any = None,
        aargs: dict = {},           # lag_ratio, run_time
    ):
        texts = getattr(mob, "shape_texts", VGroup())
        mob.remove(texts)

        aargs = {**DEFAULT_HIDE_AARGS, **(aargs or {})}
        super().__init__(
            *(Unwrite(t) for t in texts),
            **aargs,
        )

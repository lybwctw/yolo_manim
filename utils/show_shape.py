from manim import *

SHAPE_PATH_CONFIG = {
    'color': PURE_YELLOW,
    'width': 3,
    'opacity': 1.0,
}

SHAPE_TEXT_CONFIG = {
    'buff': 0.25,
    'font_size': 20,
    'font': 'JetBrains Mono',
}

PATH_AARGS = {
    'time_width': 2.0,
    'run_time': 2.0,
}

TEXT_AARGS = {
    'lag_ratio': 0.8,
    'run_time': 2.0,
}

GARGS = {
}


class ShowShapeMixin:
    def get_shape_path(self, **path_config) -> VMobject:
        raise NotImplementedError

    def get_shape_text(self, buff, **text_config) -> VGroup:
        raise NotImplementedError

class ShowShape(AnimationGroup):
    def __init__(
        self,
        shape: ShowShapeMixin | None = None,
        path_config: dict = {},     # path config: color, width, opacity
        text_config: dict = {},     # text config: font_size, font
        path_aargs: dict = {},      # ShowPassingFlash args
        text_aargs: dict = {},      # text Writing group args
        gargs: dict = {},           # lag_ratio
    ):
        path_config = {**SHAPE_PATH_CONFIG, **path_config}
        text_config = {**SHAPE_TEXT_CONFIG, **text_config}
        path_aargs = {**PATH_AARGS, **path_aargs}
        text_aargs = {**TEXT_AARGS, **text_aargs}
        gargs = {**GARGS, **gargs}

        path = shape.get_shape_path(**path_config)
        texts = shape.get_shape_text(**text_config)

        shape._shape_texts = texts  # store on the mobject
        shape.add(shape._shape_texts)

        super().__init__(
            ShowPassingFlash(
                path,
                **path_aargs,
            ),
            AnimationGroup(
                *(Write(t) for t in texts),
                **text_aargs,
            ),
            **gargs,
        )

class HideShape(AnimationGroup):
    def __init__(
        self,
        shape: ShowShapeMixin | None = None,
        **gargs,
    ):
        texts = getattr(shape, "_shape_texts", VGroup())
        shape.remove(texts)

        super().__init__(
            *(Unwrite(t) for t in texts),
            **gargs,
        )
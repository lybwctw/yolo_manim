from manim import *

# camera related
VIEW_INTRO = {
    'phi': 60 * DEGREES,
    'theta': -75 * DEGREES,
}
VIEW_COMPUTE = {
    'phi': 60 * DEGREES,
    'theta': -155 * DEGREES,
}

# cube related
SMALL_CUBE_SIZE = 0.3
MEDIUM_CUBE_SIZE = 0.5
SMALL_FONT_SIZE = 10
MEDIUM_FONT_SIZE = 18

# mtensor related
SMALL_TENSOR_CONFIG = {
    'size': 0.3,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}
MEDIUM_TENSOR_CONFIG = {
    'size': 0.5,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {'font_size': 18},
}
BIG_TENSOR_CONFIG = {
    'size': 0.7,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}
SMALL_CARD_CONFIG = {
    'mode': 'card',
    **SMALL_TENSOR_CONFIG,
}
MEDIUM_CARD_CONFIG = {
    'mode': 'card',
    **MEDIUM_TENSOR_CONFIG,
}
BIG_CARD_CONFIG = {
    'mode': 'card',
    **BIG_TENSOR_CONFIG,
}
SMALL_CUBE_CONFIG = {
    'mode': 'cube',
    **SMALL_TENSOR_CONFIG,
}
MEDIUM_CUBE_CONFIG = {
    'mode': 'cube',
    **MEDIUM_TENSOR_CONFIG,
}
BIG_CUBE_CONFIG = {
    'mode': 'cube',
    **BIG_TENSOR_CONFIG,
}

# TODO: more censor
BIG_1D_CONFIG = {
    'mode': 'cube',
    'size': 0.3,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}
BIG_3D_CONFIG = {
    'mode': 'cube',
    'size': 0.3,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}
BIG_4D_CONFIG = {
    'block_direction': RIGHT,
    'block_gap': 0.3,
    'mode': 'cube',
    'size': 0.3,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}

# info card related
CARD_FADE_VALUE = 0.8
CARD_OUT_OFFSET = 2.0
CARD_CENTER_Y = 0.0
CARD_EDGE_BUFF = 0.3
CARD_GAP = 0.2
CARD_INIT_UP = 7.0
CARD_INIT_DOWN = -7.0
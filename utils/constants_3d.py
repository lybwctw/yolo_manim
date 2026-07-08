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
MEDIUM_MTENSOR_CONFIG = {
    'size': SMALL_CUBE_SIZE,
    'mode': 'cube',
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {'font_size': SMALL_FONT_SIZE},       # FIXME
}

# # namecard related
# align_card = lambda m: m.to_edge(LEFT).shift(UP*0.3).set_z_index(999)
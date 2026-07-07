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

# namecard related
align_card = lambda m: m.to_edge(LEFT).shift(UP*0.3).set_z_index(999)

# mtensor config
MEDIUM_MTENSOR_CONFIG = {
    'size': SMALL_CUBE_SIZE,
    'mode': 'cube',
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {'font_size': SMALL_FONT_SIZE},       # FIXME
}


# pt.Conv2d config
PT_Conv2d_CONFIG = {
    'in_channels': 6,
    'out_channels': 5,
    'kernel_size': 3,
    'stride': 1,
    'padding': 1,
    'bias': False,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 'zeros',
}
PT_Conv2d_LEVELS = {
    'in_channels': 0,
    'out_channels': 0,
    'kernel_size': 0,
    'stride': 0,
    'padding': 0,
    'bias': 0,
    'dilation': 1,
    'groups': 1,
    'padding_mode': 1,
}
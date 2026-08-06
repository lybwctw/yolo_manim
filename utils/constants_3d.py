from manim import *

# camera related
VIEW_TOP = {
    'phi': 0 * DEGREES,
    'theta': -90 * DEGREES,
}
VIEW_INTRO = {
    'phi': 60 * DEGREES,
    'theta': -75 * DEGREES,
}
VIEW_COMPUTE = {
    'phi': 60 * DEGREES,
    'theta': -155 * DEGREES,
}

# general mtensor config
SMALL_TENSOR_CONFIG = {
    'side_length': 0.3,
    'font_size': 12,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}
MEDIUM_TENSOR_CONFIG = {
    'side_length': 0.5,
    'font_size': 18,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}
BIG_TENSOR_CONFIG = {
    'side_length': 0.7,
    'font_size': 24,
    'padding': 0.0,
    'cube_config': {},
    'square_config': {},
    'decimal_config': {},
}

# # card config
# SMALL_CARD_CONFIG = {'mode': 'card', **SMALL_TENSOR_CONFIG}
# MEDIUM_CARD_CONFIG = {'mode': 'card', **MEDIUM_TENSOR_CONFIG}
# BIG_CARD_CONFIG = {'mode': 'card', **BIG_TENSOR_CONFIG}

# # cube config
# SMALL_CUBE_CONFIG = {'mode': 'cube', **SMALL_TENSOR_CONFIG}
# MEDIUM_CUBE_CONFIG = {'mode': 'cube', **MEDIUM_TENSOR_CONFIG}
# BIG_CUBE_CONFIG = {'mode': 'cube', **BIG_TENSOR_CONFIG}

# # 1D mtensor config
# SMALL_1D_CUBE_CONFIG = SMALL_CUBE_CONFIG
# SMALL_1D_CARD_CONFIG = SMALL_CARD_CONFIG
# MEDIUM_1D_CUBE_CONFIG = MEDIUM_CUBE_CONFIG
# MEDIUM_1D_CARD_CONFIG = MEDIUM_CARD_CONFIG
# BIG_1D_CUBE_CONFIG = BIG_CUBE_CONFIG
# BIG_1D_CARD_CONFIG = BIG_CARD_CONFIG

# # 2D mtensor config
# SMALL_2D_CUBE_CONFIG = SMALL_CUBE_CONFIG
# SMALL_2D_CARD_CONFIG = SMALL_CARD_CONFIG
# MEDIUM_2D_CUBE_CONFIG = MEDIUM_CUBE_CONFIG
# MEDIUM_2D_CARD_CONFIG = MEDIUM_CARD_CONFIG
# BIG_2D_CUBE_CONFIG = BIG_CUBE_CONFIG
# BIG_2D_CARD_CONFIG = BIG_CARD_CONFIG

# # 3D mtensor config
# SMALL_3D_CUBE_CONFIG = SMALL_CUBE_CONFIG
# SMALL_3D_CARD_CONFIG = SMALL_CARD_CONFIG
# MEDIUM_3D_CUBE_CONFIG = MEDIUM_CUBE_CONFIG
# MEDIUM_3D_CARD_CONFIG = MEDIUM_CARD_CONFIG
# BIG_3D_CUBE_CONFIG = BIG_CUBE_CONFIG
# BIG_3D_CARD_CONFIG = BIG_CARD_CONFIG

# # 4D mtensor config
# SMALL_4D_CUBE_CONFIG = {**SMALL_CUBE_CONFIG, 'block_direction': RIGHT, 'block_gap': 0.3}
# SMALL_4D_CARD_CONFIG = {**SMALL_CARD_CONFIG, 'block_direction': RIGHT, 'block_gap': 0.3}
# MEDIUM_4D_CUBE_CONFIG = {**MEDIUM_CUBE_CONFIG, 'block_direction': RIGHT, 'block_gap': 0.4}
# MEDIUM_4D_CARD_CONFIG = {**MEDIUM_CARD_CONFIG, 'block_direction': RIGHT, 'block_gap': 0.4}
# BIG_4D_CUBE_CONFIG = {**BIG_CUBE_CONFIG, 'block_direction': RIGHT, 'block_gap': 0.5}
# BIG_4D_CARD_CONFIG = {**BIG_CARD_CONFIG, 'block_direction': RIGHT, 'block_gap': 0.5}

from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

# ------------- info card ---------------------
IC_HEAD = 'BatchNorm2d'
IC_PARAMS = {
    'num_features': UNKNOWN,
    'eps': UNKNOWN,
    'momentum': UNKNOWN,
    'affine': UNKNOWN,
    'track_running_stats': UNKNOWN,
}
IC_IGNORES = [
    'momentum',
    'affine',
    'track_running_stats',
]
IC_HEAD_CONFIG = {}
IC_FRAME_CONFIG = {
    'fill_color': ORANGE,
}
IC_COMMON_CONFIG = {}
IC_IGNORE_CONFIG = {}

def create_ic_BatchNorm2d():
    """Create empty InfoCard.
    """
    return InfoCard(
        head=IC_HEAD,
        params=IC_PARAMS,
        ignores=IC_IGNORES,
        head_config=IC_HEAD_CONFIG,
        frame_config=IC_FRAME_CONFIG,
        common_config=IC_COMMON_CONFIG,
        ignore_config=IC_IGNORE_CONFIG,
    )


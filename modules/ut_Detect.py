from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

# ------------- info card ---------------------
IC_HEAD = 'Detect'
IC_PARAMS = {
    'nc': UNKNOWN,
    'ch': UNKNOWN,
}
IC_IGNORES = [
]
IC_HEAD_CONFIG = {}
IC_FRAME_CONFIG = {
    'fill_color': PURE_BLUE,
}
IC_COMMON_CONFIG = {}
IC_IGNORE_CONFIG = {}

def create_ic_Detect():
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




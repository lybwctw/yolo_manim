from __future__ import annotations
import sys
sys.path.append('..')

from manim import *

from utils.info_card import *

# ------------- info card ---------------------
IC_HEAD = 'add'
IC_PARAMS = {}
IC_IGNORES = []
IC_HEAD_CONFIG = {}
IC_FRAME_CONFIG = {
    'fill_color': TEAL,
}
IC_COMMON_CONFIG = {}
IC_IGNORE_CONFIG = {}

def create_ic_add():
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
from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
from utils.mtensor import *
from utils.constants import *
from utils.constants_3d import *
from utils.info_card import *

# ------------- info card ReLU ---------------------
IC_HEAD_ReLU = 'ReLU'
IC_PARAMS_ReLU = {}
IC_IGNORES_ReLU = []
IC_HEAD_CONFIG_ReLU = {}
IC_FRAME_CONFIG_ReLU = {
    'fill_color': ORANGE,
}
IC_COMMON_CONFIG_ReLU = {}
IC_IGNORE_CONFIG_ReLU = {}

def create_ic_ReLU():
    """Create empty InfoCard.
    """
    return InfoCard(
        head=IC_HEAD_ReLU,
        params=IC_PARAMS_ReLU,
        ignores=IC_IGNORES_ReLU,
        head_config=IC_HEAD_CONFIG_ReLU,
        frame_config=IC_FRAME_CONFIG_ReLU,
        common_config=IC_COMMON_CONFIG_ReLU,
        ignore_config=IC_IGNORE_CONFIG_ReLU,
    )

# ------------- info card SiLU ---------------------
IC_HEAD_SiLU = 'SiLU'
IC_PARAMS_SiLU = {}
IC_IGNORES_SiLU = []
IC_HEAD_CONFIG_SiLU = {}
IC_FRAME_CONFIG_SiLU = {
    'fill_color': ORANGE,
}
IC_COMMON_CONFIG_SiLU = {}
IC_IGNORE_CONFIG_SiLU = {}

def create_ic_SiLU():
    """Create empty InfoCard.
    """
    return InfoCard(
        head=IC_HEAD_SiLU,
        params=IC_PARAMS_SiLU,
        ignores=IC_IGNORES_SiLU,
        head_config=IC_HEAD_CONFIG_SiLU,
        frame_config=IC_FRAME_CONFIG_SiLU,
        common_config=IC_COMMON_CONFIG_SiLU,
        ignore_config=IC_IGNORE_CONFIG_SiLU,
    )

# ------------- info card Sigmoid ---------------------
IC_HEAD_Sigmoid = 'Sigmoid'
IC_PARAMS_Sigmoid = {}
IC_IGNORES_Sigmoid = []
IC_HEAD_CONFIG_Sigmoid = {}
IC_FRAME_CONFIG_Sigmoid = {
    'fill_color': ORANGE,
}
IC_COMMON_CONFIG_Sigmoid = {}
IC_IGNORE_CONFIG_Sigmoid = {}

def create_ic_Sigmoid():
    """Create empty InfoCard.
    """
    return InfoCard(
        head=IC_HEAD_Sigmoid,
        params=IC_PARAMS_Sigmoid,
        ignores=IC_IGNORES_Sigmoid,
        head_config=IC_HEAD_CONFIG_Sigmoid,
        frame_config=IC_FRAME_CONFIG_Sigmoid,
        common_config=IC_COMMON_CONFIG_Sigmoid,
        ignore_config=IC_IGNORE_CONFIG_Sigmoid,
    )

# ------------- info card Softmax ---------------------
IC_HEAD_Softmax = 'Softmax'
IC_PARAMS_Softmax = {
    'dim': UNKNOWN,
}
IC_IGNORES_Softmax = []
IC_HEAD_CONFIG_Softmax = {}
IC_FRAME_CONFIG_Softmax = {
    'fill_color': ORANGE,
}
IC_COMMON_CONFIG_Softmax = {}
IC_IGNORE_CONFIG_Softmax = {}

def create_ic_Softmax():
    """Create empty InfoCard.
    """
    return InfoCard(
        head=IC_HEAD_Softmax,
        params=IC_PARAMS_Softmax,
        ignores=IC_IGNORES_Softmax,
        head_config=IC_HEAD_CONFIG_Softmax,
        frame_config=IC_FRAME_CONFIG_Softmax,
        common_config=IC_COMMON_CONFIG_Softmax,
        ignore_config=IC_IGNORE_CONFIG_Softmax,
    )
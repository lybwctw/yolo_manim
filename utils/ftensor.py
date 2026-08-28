from __future__ import annotations
import sys
sys.path.append('..')

from manim import *
import itertools
import random
import numpy as np
import torch

from utils.mcube import MCube
from utils.constants_3d import *

class FTensor3D(VMobject):
    def __init__(
        self,
    ):
        super().__init__()

    def create(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        pass

    def breath(
        self,
        **aargs,
    ):
        pass

    def uncreate(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        pass


class FTensor4D(VMobject):
    def __init__(
        self,
    ):
        super().__init__()

    def create(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        pass

    def breath(
        self,
        **aargs,
    ):
        pass

    def uncreate(
        self,
        direction: str = 'center',      # top/center/bottom
        **aargs,
    ):
        pass
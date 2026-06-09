import sys
sys.path.append('..')

from manim import *
import pickle
import os
import cv2
import torch
import numpy as np
import random

from utils.color_cell import ColorCell
from utils.line_matrix import LineMatrix
from utils.constants import DIR_PICKLE

def export_mobs(path_source, mobs, suffix=''):
    """Dump manim mobs according to given path.
    
    Args:
        path_source: Source file path to extract base name
        mobs: Manim objects to pickle
        suffix: Optional suffix to append (e.g., 'a', 'b', 'c')
    """
    base_name = os.path.basename(path_source).split('.')[0]
    # Split base_name into leading digits and rest (e.g., '001_pixel_focus' -> '001', '_pixel_focus')
    i = 0
    while i < len(base_name) and base_name[i].isdigit():
        i += 1
    digits = base_name[:i]
    rest = base_name[i:]
    
    if suffix:
        name_target = digits + suffix + rest + '.pkl'
    else:
        name_target = base_name + '.pkl'
    path_target = os.path.join(DIR_PICKLE, name_target)
    os.makedirs(DIR_PICKLE, exist_ok=True)  # make sure pickle dir exists
    with open(path_target, 'wb') as f:
        pickle.dump(mobs, f)

def import_mobs(hint, suffix=''):
    """Find pickle files starts with hint and load the first one.
    
    Args:
        hint: Starting pattern to match file name (e.g., '001', '002')
        suffix: Optional suffix to match (e.g., 'a', 'b', 'c')
    """
    path = None
    target_prefix = hint + suffix
    for name in os.listdir(DIR_PICKLE):
        if name.startswith(target_prefix):
            path = os.path.join(DIR_PICKLE, name)
            break
    if path is None:
        search_term = f"'{hint}{suffix}'" if suffix else f"'{hint}'"
        raise FileNotFoundError(
            f"No pickle file found with hint {search_term} in {DIR_PICKLE}"
            )

    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def scale_manager_target(manager, everything, scale):
    """
    scale mobs in manager.target
    scale mobs in everything while not in manager
    """
    for mob in manager.target:
        mob.scale(scale)
    for mob in everything:
        if mob not in manager:
            mob.scale(scale)


def tensor_to_line_matrix(
    tensor: VGroup | None = None,       # vgroup of ints
    lmatrix: LineMatrix | None = None,  # line matrix object
    targs: dict | None = None,                   # Transform args
    gargs: dict | None = None,                   # inner AnimationGroup args
    ggargs: dict | None = None,                  # outter AnimationGroup args
):
    """From a tensor matrix into line matrix (mini version).
    """
    anim = AnimationGroup(
        *(AnimationGroup(
            *(Transform(t, l, **targs) for t,l in zip(tensor[i], lmatrix.mobs[i])),
            **gargs,
        ) for i in range(len(tensor))),
        **ggargs,
    )
    return anim


def compute_iou(box, boxes):
    """
    box: (4,)
    boxes: (m, 4)
    """

    xx1 = np.maximum(box[0], boxes[:, 0])
    yy1 = np.maximum(box[1], boxes[:, 1])
    xx2 = np.minimum(box[2], boxes[:, 2])
    yy2 = np.minimum(box[3], boxes[:, 3])

    w = np.maximum(0, xx2 - xx1)
    h = np.maximum(0, yy2 - yy1)

    inter = w * h

    area1 = (
        (box[2] - box[0])
        * (box[3] - box[1])
    )

    area2 = (
        (boxes[:, 2] - boxes[:, 0])
        * (boxes[:, 3] - boxes[:, 1])
    )

    union = area1 + area2 - inter

    return inter / union

def random_boxes(n, max_coord=640):
    # random corners
    p1 = np.random.randint(
        0,
        max_coord,
        size=(n, 2),
    )

    p2 = np.random.randint(
        0,
        max_coord,
        size=(n, 2),
    )

    # enforce x1<x2, y1<y2
    xy1 = np.minimum(p1, p2)
    xy2 = np.maximum(p1, p2)

    boxes = np.hstack([
        xy1,
        xy2,
    ])

    return boxes


def sf2dir(sf: int) -> str:
    size = 640 // sf
    return f"{sf:03d}_{size:02d}x{size:02d}"

def random_path(
    n: int,
    step: int,
    shape: tuple,
    start_idx: int,
) -> list:
    """generate random idx path in anchor point grid.
    """
    h, w = shape
    row, col = divmod(start_idx, w)
    sample_idxs = []
    for _ in range(n):
        dr, dc = random.choice([
            (-step, -step), (-step, 0), (-step, step),
            (0,     -step),             (0,     step),
            ( step, -step), ( step, 0), ( step, step),
        ])
        row = min(max(row + dr, 0), h - 1)
        col = min(max(col + dc, 0), w - 1)
        sample_idxs.append(row*w + col)
    return sample_idxs

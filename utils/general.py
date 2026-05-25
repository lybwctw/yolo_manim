import sys
sys.path.append('..')

from manim import *
import pickle
import os
import cv2
import torch
import numpy as np

from utils.color_cell import ColorCell
from utils.line_matrix import LineMatrix
from utils.constants import DIR_PICKLE

def export_mobs(path_source, mobs):
    """Dump manim mobs according to given path.
    """
    name_target = os.path.basename(path_source).split('.')[0] + '.pkl'
    path_target = os.path.join(DIR_PICKLE, name_target)
    os.makedirs(DIR_PICKLE, exist_ok=True)  # make sure pickle dir exists
    with open(path_target, 'wb') as f:
        pickle.dump(mobs, f)

def import_mobs(hint):
    """Find pickle files starts with hint and load the first one.
    """
    path = None
    for name in os.listdir(DIR_PICKLE):
        if name.startswith(hint):
            path = os.path.join(DIR_PICKLE, name)
            break
    if path is None:
        raise FileNotFoundError(
            f"No pickle file found with hint '{hint}' in {DIR_PICKLE}"
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

def load_central_cells(
        path,
        rows,
        cols,
        target_height,
    ):
    """
    Load central pixels and convert into cells vmobjects
    """
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    r0 = (h - rows) // 2
    c0 = (w - cols) // 2
    ps = img[r0:r0+rows, c0:c0+cols]

    cells = VGroup()
    for i in range(rows):
        for j in range(cols):
            r, g, b = ps[i, j]
            cells.add(ColorCell(r, g, b))
    cells.arrange_in_grid(
        rows=rows,
        cols=cols,
        buff=0,
    ).scale_to_fit_height(target_height)

    return cells

def tensor_to_line_matrix(
    tensor: VGroup | None = None,       # vgroup of ints
    lmatrix: LineMatrix | None = None,  # line matrix object
    targs: dict = {},                   # Transform args
    gargs: dict = {},                   # inner AnimationGroup args
    ggargs: dict = {},                  # outter AnimationGroup args
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

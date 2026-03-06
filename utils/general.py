from manim import *
import pickle
import cv2
from .color_cell import ColorCell

def save_everything(file, everything):
    with open(file, 'wb') as f:
        pickle.dump(everything, f)

def load_everything(file):
    with open(file, 'rb') as f:
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
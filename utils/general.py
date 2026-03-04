from manim import *
import pickle

# def save_scene_start(key, value):
#     with open(key, 'w') as f:
#         f.write(str(value))


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
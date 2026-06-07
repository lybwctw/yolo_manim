from manim import *
import os

# path related
DIR_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
DIR_ASSETS = os.path.join(DIR_ROOT, 'assets')
DIR_IMAGES = os.path.join(DIR_ASSETS, 'images')
DIR_LABELS = os.path.join(DIR_ASSETS, 'labels')
DIR_NUMPY = os.path.join(DIR_ASSETS, 'numpy')
DIR_TENSOR = os.path.join(DIR_ASSETS, 'ultralytics')
DIR_PICKLE = os.path.join(DIR_ROOT, 'pickle')

PATH_IMAGE_640 = os.path.join(DIR_IMAGES, 'sample_640x360.jpg')
PATH_IMAGE_960 = os.path.join(DIR_IMAGES, 'sample_960x540.jpg')
PATH_IMAGE_1280 = os.path.join(DIR_IMAGES, 'sample_1280x720.jpg')
PATH_LABEL = os.path.join(DIR_LABELS, 'labels.txt')
# PATH_LABEL = 'assets/images/labels.txt'

# dataset related
KK_NAMES = ['kunkun', 'coke', 'pepsi']
KK_COLORS = [GREEN, RED, BLUE]
KK_NAME_MAP = dict(enumerate(KK_NAMES))     # idx into name
KK_COLOR_MAP = dict(enumerate(KK_COLORS))   # idx into color

# shape related
SMALL_SHAPE_TEXT_CONFIG = {
    'buff': 0.10,
    'font_size': 10,
    'font': 'JetBrains Mono',
    'color': WHITE,
}
MEDIUM_SHAPE_TEXT_CONFIG = {
    'buff': 0.15,
    'font_size': 15,
    'font': 'JetBrains Mono',
    'color': WHITE,
}
BIG_SHAPE_TEXT_CONFIG = {
    'buff': 0.25,
    'font_size': 25,
    'font': 'JetBrains Mono',
    'color': WHITE,
}

# duration related
SHORT_DURATION = 0.5
MEDIUM_DURATION = 1.0
LONG_DURATION = 3.0

# joint constants between scenes
J000_IMAGE_HEIGHT = 4.0
J005_ANNO_HEIGHT = 4.0

# explainer related
MINI_DOT_CONFIG = {
    'side_length': 0.002,
    'stroke_width': 1,
}
SMALL_DOT_CONFIG = {
    'side_length': 0.005,
    'stroke_width': 2,
}
MEDIUM_DOT_CONFIG = {
    'side_length': 0.01,
    'stroke_width': 3,
}

MINI_RECT_CONFIG = {
    'stroke_width': 0.2
}
SMALL_RECT_CONFIG = {
    'stroke_width': 0.5,
}
MEDIUM_RECT_CONFIG = {
    'stroke_width': 1.0,
}

# # FIXME: all others
# PATH_TENSOR_32_BOX = None
# PATH_TENSOR_32_CLS = None

# PATH_TXT_DECODE = None

# PATH_TXT_RES = None

# INIT_WIDTH_ARROW_COMMENT = 1.0

# # scene init related
# CONFIG_DIR = 'config'
# S001_IMAGE_RAW = os.path.join(CONFIG_DIR, 's001_image_raw.txt',)
# S002_ANNOTATION_FINAL = os.path.join(CONFIG_DIR, 's002_annotation_final.txt',)
# S003_ANNOTATION_REPAD = os.path.join(CONFIG_DIR, 's003_annotation_repad.txt')

# # mini
# MINI_32_DIST_PATH = 'assets/numpy/mini_32_dist.npy'
# MINI_32_PROB_PATH = 'assets/numpy/mini_32_prob.npy'

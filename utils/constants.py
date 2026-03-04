from manim import *
import os

# kk dataset config
KK_NAME_MAP = {
    0: 'kunkun',
    1: 'coke',
    2: 'pepsi',
}
KK_COLOR_MAP = {
    0: GREEN,
    1: RED,
    2: BLUE,
}

# everything filename
S001_EVERYTHING = 's001_everything.pkl'


PATH_IMAGE_640 = 'assets/images/sample_640_360.jpg'
PATH_LABEL_640 = 'assets/images/labels.txt'

PATH_TENSOR_32_BOX = None
PATH_TENSOR_32_CLS = None

PATH_TXT_DECODE = None

PATH_TXT_RES = None

INIT_WIDTH_ARROW_COMMENT = 1.0

# scene init related
CONFIG_DIR = 'config'
S001_IMAGE_RAW = os.path.join(CONFIG_DIR, 's001_image_raw.txt',)
S002_ANNOTATION_FINAL = os.path.join(CONFIG_DIR, 's002_annotation_final.txt',)
S003_ANNOTATION_REPAD = os.path.join(CONFIG_DIR, 's003_annotation_repad.txt')
from manim import *
import os

# path related
DIR_ROOT = 'D:/deeplearning/yolo_manim'
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
PATH_LABEL = 'assets/images/labels.txt'

# kk dataset related
KK_NAMES = ['kunkun', 'coke', 'pepsi']
KK_COLORS = [GREEN, RED, BLUE]
KK_NAME_MAP = dict(enumerate(KK_NAMES))
KK_COLOR_MAP = dict(enumerate(KK_COLORS))

# FIXME: all others
# everything filename
S000_EVERYTHING = 's000_everything.pkl'
S001_EVERYTHING = 's001_everything.pkl'
S002_EVERYTHING = 's002_everything.pkl'

S004_EVERYTHING = 's004_everything.pkl'
S005_EVERYTHING = 's005_everything.pkl'
S006_EVERYTHING = 's006_everything.pkl'
S007_EVERYTHING = 's007_everything.pkl'

S009_EVERYTHING = 's009_everything.pkl'
S010_EVERYTHING = 's010_everything.pkl'
S011_EVERYTHING = 's011_everything.pkl'
S012_EVERYTHING = 's012_everything.pkl'
S013_EVERYTHING = 's013_everything.pkl'

S015_EVERYTHING = 's015_everything.pkl'

S017_EVERYTHING_PP = 's017_everything_pp.pkl'       # for 018 postprocess
S017_EVERYTHING_BM = 's017_everything_bm.pkl'       # for 019 big map

S019_EVERYTHING = 's019_everything.pkl'


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

# mini
MINI_32_DIST_PATH = 'assets/numpy/mini_32_dist.npy'
MINI_32_PROB_PATH = 'assets/numpy/mini_32_prob.npy'
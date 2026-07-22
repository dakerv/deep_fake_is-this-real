"""
Deepfake Detection - Data Sampling Pipeline

===========================================

Creates balanced sampled datasets for training the 
deepfake detection model.

The script ranomdly selects images from the original datasets and copies them into seperate sampled folders.

Classes
-------

1. REAL CLASS: Sampled from FFHQ and CelebDF datasets.
--------------
2. SYNTHETIC CLASS: StyleGAN3 Fake Faces
-------------------
3. SWAPPED CLASS: FFHQ Face Swap Dataset
-----------------

Pipeline
--------
1. Load original datasets
2. Randomly sample images
3. Combine the two real datasets
4. Create balanced sampled datasets

Expected folder structure
-------------------------

raw_data/
│
├── real/
│   ├── real_full/
│   │   ├── FFHQ_real/
│   │   └── CelebDF_real/
│   │
│   └── real_sampled/
│
├── synthetic/
│   ├── synthetic_full/
│   └── synthetic_sampled/
│
└── swapped/
    ├── swapped_full/
    └── swapped_sampled/

Author: Vanessa Daker
"""

import random
import shutil
from pathlib import Path

# =============
# Configuration
# =============

RANDOM_SEED = 42

# Number of images per class
REAL_IMAGES = 3000
SYNTHETIC_IMAGES = 3000
SWAPPED_IMAGES = 3000

# Real dataset contribution
FFHQ_IMAGES = 1500
CELEBDF_IMAGES = 1500

RAW_DIR = Path("raw_data")

FFHQ_SOURCE = (
    RAW_DIR /
    "real" /
    "real_full" /
    "FFHQ_real"
)

CELEBDF_SOURCE = (
    RAW_DIR /
    "real" /
    "real_full" /
    "CelebDF_real"
)

SYNTHETIC_SOURCE = (
    RAW_DIR /
    "synthetic" /
    "synthetic_full"
)

SWAPPED_SOURCE = (
    RAW_DIR /
    "swapped" /
    "swapped_full"
)

REAL_DEST = (
    RAW_DIR /
    "real" /
    "real_sampled"
)

SYNTHETIC_DEST = (
    RAW_DIR /
    "synthetic" /
    "synthetic_sampled"
)

SWAPPED_DEST = (
    RAW_DIR /
    "swapped" /
    "swapped_sampled"
)

def get_image_files(folder):
    """
    Retrieve all image files from a folder.

    Supported formats:
    - JPG
    - JPEG
    - PNG

    Parameters
    ----------
    folder : Path
        Folder containing images.

    Returns
    -------
    list
        A list of image file paths.
    """
    
    image_files = []

    for extension in ("*.jpg", "*.jpeg", "*.png"):
        image_files.extend(folder.glob(extension))

    return image_files

random.seed(RANDOM_SEED)
"""
Deepfake Detection - Image Preprocessing Pipeline
=================================================

Prepares a balanced three-class image dataset for training an
EfficientNet-B0 deepfake detection model.

Classes:
    - Real
    - Swapped (face-swapped images)
    - Synthetic (AI-generated faces)

Pipeline
--------
1. Load sampled images for each class
2. Detect the largest face in every image
3. Crop and resize the face to 224 × 224 pixels
4. Save cropped faces into class folders
5. Split the dataset into train, validation and test sets

Expected folder structure
-------------------------

raw_data/
│
├── real/
│   ├── real_full/
│   └── real_sampled/
│
├── synthetic/
│   ├── synthetic_full/
│   └── synthetic_sampled/
│
├── swapped/
│   ├── swapped_full/
│   └── swapped_sampled/
│
cropped_faces/
dataset/

Author: Vanessa Daker
"""

import random
import shutil
from pathlib import Path

import cv2
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# =============================================================================
# Configuration
# =============================================================================

# Root folders
RAW_DIR = Path("raw_data")
CROPPED_DIR = Path("cropped_faces")
OUTPUT_DIR = Path("dataset")

# Image settings
IMG_SIZE = 224

# Dataset split ratios
TRAIN_SPLIT = 0.70
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15

# Random seed for reproducibility
RANDOM_SEED = 42

# Maximum number of images to process from each class.
# Keeping the classes balanced improves model training.
MAX_IMAGES_PER_CLASS = 2000

# Class names
CLASSES = [
    "real",
    "synthetic",
    "swapped"
]

random.seed(RANDOM_SEED)


# =============================================================================
# Face Detector
# =============================================================================

def get_face_detector():
    """
    Load the face detector.

    First tries to use MTCNN because it is much more accurate for
    deep learning projects.

    If MTCNN is unavailable, automatically falls back to OpenCV's
    Haar Cascade detector.
    """

    try:
        from mtcnn import MTCNN

        print("✓ Using MTCNN face detector")
        return "mtcnn", MTCNN()

    except ImportError:

        print("⚠ MTCNN not installed.")
        print("  Falling back to Haar Cascade detector.")

        cascade_path = (
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        detector = cv2.CascadeClassifier(cascade_path)

        return "haar", detector
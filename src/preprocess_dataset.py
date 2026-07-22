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
    
# =============================================================================
# Face Detection
# =============================================================================

def crop_largest_face(image, detector_type, detector, margin=0.25):
    """
    Detect all faces in an image and return the largest face with
    additional padding around it.

    Parameters
    ----------
    image : numpy.ndarray
        Input image (OpenCV format).

    detector_type : str
        "mtcnn" or "haar"

    detector :
        Loaded detector object.

    margin : float
        Percentage of padding added around the detected face.

    Returns
    -------
    Cropped face image, or None if no face is found.
    """

    height, width = image.shape[:2]

    if detector_type == "mtcnn":

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        detections = detector.detect_faces(rgb)

        boxes = []

        for detection in detections:

            x, y, w, h = detection["box"]

            # MTCNN occasionally returns slightly negative coordinates.
            x = max(0, x)
            y = max(0, y)

            boxes.append((x, y, w, h))

    else:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        boxes = detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

    if len(boxes) == 0:
        return None

    # Choose the largest detected face.
    x, y, w, h = max(boxes, key=lambda b: b[2] * b[3])

    pad_x = int(w * margin)
    pad_y = int(h * margin)

    x1 = max(0, x - pad_x)
    y1 = max(0, y - pad_y)

    x2 = min(width, x + w + pad_x)
    y2 = min(height, y + h + pad_y)

    face = image[y1:y2, x1:x2]

    if face.size == 0:
        return None

    return face


# =============================================================================
# Face Cropping and Preprocessing
# =============================================================================

def process_class_folder(
    source_dir,
    destination_dir,
    detector_type,
    detector,
    label
):
    """
    Process one image class.

    Steps
    -----
    1. Read every sampled image.
    2. Detect the largest face.
    3. Crop the face.
    4. Resize to IMG_SIZE.
    5. Save into cropped_faces/<class>.
    """

    destination_dir.mkdir(parents=True, exist_ok=True)

    image_files = []

    for extension in ("*.jpg", "*.jpeg", "*.png"):
        image_files.extend(source_dir.glob(extension))

    random.shuffle(image_files)

    kept = 0
    skipped = 0

    progress = tqdm(
        image_files,
        desc=f"Processing {label}"
    )

    for image_path in image_files:

        if kept >= max_images:
            break

        image = cv2.imread(str(image_path))

        if image is None:
            skipped += 1
            continue

        face = crop_largest_face(
            image,
            detector_type,
            detector
        )

        if face is None:
            skipped += 1
            continue

        try:

            face = cv2.resize(
                face,
                (IMG_SIZE, IMG_SIZE)
            )

        except Exception:
            skipped += 1
            continue

        output_path = destination_dir / image_path.name

        cv2.imwrite(
            str(output_path),
            face
        )

        kept += 1

        progress.update(1)

    progress.close()

    print(f"\n{label.upper()} SUMMARY")
    print("-" * 35)
    print(f"Images processed : {kept}")
    print(f"Images skipped   : {skipped}")
    print()

# =============================================================================
# Dataset Splitting
# =============================================================================

def split_dataset(cropped_dir, output_dir):
    """
    Split each class into training, validation and testing datasets.
    """

    for class_name in CLASSES:

        class_dir = cropped_dir / class_name

        if not class_dir.exists():
            print(f"Warning: {class_name} folder not found.")
            continue

        images = list(class_dir.glob("*.jpg"))

        if len(images) == 0:
            print(f"Warning: No images found for {class_name}.")
            continue

        train_files, temp_files = train_test_split(
            images,
            train_size=TRAIN_SPLIT,
            random_state=RANDOM_SEED,
            shuffle=True
        )

        validation_ratio = VAL_SPLIT / (VAL_SPLIT + TEST_SPLIT)

        val_files, test_files = train_test_split(
            temp_files,
            train_size=validation_ratio,
            random_state=RANDOM_SEED,
            shuffle=True
        )

        for split_name, file_list in [

            ("train", train_files),
            ("val", val_files),
            ("test", test_files)

        ]:

            split_dir = output_dir / split_name / class_name
            split_dir.mkdir(parents=True, exist_ok=True)

            for image in file_list:

                shutil.copy2(
                    image,
                    split_dir / image.name
                )

        print(
            f"{class_name:<10}"
            f" Train: {len(train_files):4}"
            f" | Val: {len(val_files):4}"
            f" | Test: {len(test_files):4}"
        )


# =============================================================================
# Main
# =============================================================================

def main():

    print("=" * 60)
    print("Deepfake Dataset Preprocessing")
    print("=" * 60)

    detector_type, detector = get_face_detector()

    datasets = {

        "real": (
            RAW_DIR / "real" / "real_sampled",
            CROPPED_DIR / "real"
        ),

        "synthetic": (
            RAW_DIR / "synthetic" / "synthetic_sampled",
            CROPPED_DIR / "synthetic"
        ),

        "swapped": (
            RAW_DIR / "swapped" / "swapped_sampled",
            CROPPED_DIR / "swapped"
        )

    }

    print("\nStep 1/2 - Cropping faces\n")

    for label, (source, destination) in datasets.items():

        if not source.exists():

            print(f"Skipping '{label}' (folder not found)")
            continue

        process_class_folder(
            source,
            destination,
            detector_type,
            detector,
            label
        )

    print("\nStep 2/2 - Splitting dataset\n")

    split_dataset(
        CROPPED_DIR,
        OUTPUT_DIR
    )

    print("\n" + "=" * 60)
    print("Preprocessing completed successfully!")
    print("=" * 60)

    print("\nOutput folders:")

    print("cropped_faces/")
    print("dataset/train/")
    print("dataset/val/")
    print("dataset/test/")


if __name__ == "__main__":
    main()
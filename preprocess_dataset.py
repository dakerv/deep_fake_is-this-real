"""
Deepfake Detection - Dataset Preprocessing Pipeline
=====================================================
Prepares a 3-class dataset (real / face_swap / synthetic) for training
an EfficientNet-B0 classifier.

Pipeline steps:
    1. Extract frames from FaceForensics++ videos (face_swap class only)
    2. Detect + crop faces from all raw images/frames
    3. Resize + save into a clean class-labeled folder structure
    4. Split into train/val/test sets

Expected raw input layout (you organize downloads into this first):

    raw_data/
        real/                  <- FFHQ / CelebA-HQ images (.jpg/.png)
        synthetic/             <- StyleGAN / 140k-fake images (.jpg/.png)
        face_swap_videos/      <- FaceForensics++ FaceSwap + Deepfakes .mp4 files

Output layout:

    dataset/
        train/{real,face_swap,synthetic}/
        val/{real,face_swap,synthetic}/
        test/{real,face_swap,synthetic}/

Install requirements first:
    pip install opencv-python mtcnn scikit-learn tqdm --break-system-packages
"""

import os
import cv2
import random
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
RAW_DIR = Path("raw_data")
FRAMES_DIR = Path("extracted_frames")     # intermediate: frames pulled from video
CROPPED_DIR = Path("cropped_faces")       # intermediate: face-cropped images per class
OUTPUT_DIR = Path("dataset")              # final train/val/test split

IMG_SIZE = 224                # EfficientNet-B0 default input size
FRAMES_PER_VIDEO = 15          # cap frames extracted per FF++ video (avoid near-duplicate overload)
TRAIN_SPLIT, VAL_SPLIT, TEST_SPLIT = 0.7, 0.15, 0.15
RANDOM_SEED = 42

CLASSES = ["real", "face_swap", "synthetic"]

random.seed(RANDOM_SEED)

# ---------------------------------------------------------------------------
# Step 1: Extract frames from FaceForensics++ videos (face_swap class)
# ---------------------------------------------------------------------------
def extract_frames_from_videos(video_dir: Path, out_dir: Path, frames_per_video: int = FRAMES_PER_VIDEO):
    """Uniformly sample frames from each video and save as .jpg."""
    out_dir.mkdir(parents=True, exist_ok=True)
    video_files = list(video_dir.glob("*.mp4")) + list(video_dir.glob("*.avi"))

    if not video_files:
        print(f"  No videos found in {video_dir} — skipping frame extraction.")
        return

    for video_path in tqdm(video_files, desc="Extracting frames"):
        cap = cv2.VideoCapture(str(video_path))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            cap.release()
            continue

        # Evenly spaced frame indices across the video
        indices = sorted(random.sample(range(total_frames), min(frames_per_video, total_frames)))
        idx_set = set(indices)

        frame_num = 0
        saved = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_num in idx_set:
                out_path = out_dir / f"{video_path.stem}_frame{frame_num}.jpg"
                cv2.imwrite(str(out_path), frame)
                saved += 1
            frame_num += 1
        cap.release()


# ---------------------------------------------------------------------------
# Step 2: Face detection + cropping
# ---------------------------------------------------------------------------
def get_face_detector():
    """Lazy-load MTCNN detector (falls back to OpenCV Haar cascade if unavailable)."""
    try:
        from mtcnn import MTCNN
        return ("mtcnn", MTCNN())
    except ImportError:
        print("  mtcnn not installed, falling back to OpenCV Haar cascade (less accurate).")
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        return ("haar", cv2.CascadeClassifier(cascade_path))


def crop_largest_face(image, detector_type, detector, margin: float = 0.25):
    """Detect faces in an image and return the crop of the largest one, with margin."""
    h, w = image.shape[:2]

    if detector_type == "mtcnn":
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(rgb)
        boxes = [r["box"] for r in results]
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        boxes = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    if len(boxes) == 0:
        return None

    # pick largest box by area
    x, y, bw, bh = max(boxes, key=lambda b: b[2] * b[3])

    # add margin around the face
    mx, my = int(bw * margin), int(bh * margin)
    x1, y1 = max(0, x - mx), max(0, y - my)
    x2, y2 = min(w, x + bw + mx), min(h, y + bh + my)

    return image[y1:y2, x1:x2]


def process_class_folder(src_dir: Path, dst_dir: Path, detector_type, detector, label: str):
    """Crop faces from every image in src_dir, resize, save to dst_dir."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    image_files = [p for p in src_dir.glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")]

    kept, skipped = 0, 0
    for img_path in tqdm(image_files, desc=f"Cropping faces ({label})"):
        img = cv2.imread(str(img_path))
        if img is None:
            skipped += 1
            continue

        face = crop_largest_face(img, detector_type, detector)
        if face is None or face.size == 0:
            skipped += 1
            continue

        face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE))
        out_path = dst_dir / f"{img_path.stem}.jpg"
        cv2.imwrite(str(out_path), face_resized)
        kept += 1

    print(f"  {label}: kept {kept}, skipped {skipped} (no face detected / unreadable)")


# ---------------------------------------------------------------------------
# Step 3: Train / val / test split
# ---------------------------------------------------------------------------
def split_dataset(cropped_dir: Path, output_dir: Path):
    for class_name in CLASSES:
        class_dir = cropped_dir / class_name
        if not class_dir.exists():
            print(f"  Warning: {class_dir} does not exist, skipping.")
            continue

        images = list(class_dir.glob("*.jpg"))
        if not images:
            print(f"  Warning: no images found for class '{class_name}'.")
            continue

        train_files, temp_files = train_test_split(
            images, train_size=TRAIN_SPLIT, random_state=RANDOM_SEED
        )
        val_ratio = VAL_SPLIT / (VAL_SPLIT + TEST_SPLIT)
        val_files, test_files = train_test_split(
            temp_files, train_size=val_ratio, random_state=RANDOM_SEED
        )

        for split_name, files in [("train", train_files), ("val", val_files), ("test", test_files)]:
            split_dir = output_dir / split_name / class_name
            split_dir.mkdir(parents=True, exist_ok=True)
            for f in files:
                shutil.copy(f, split_dir / f.name)

        print(f"  {class_name}: train={len(train_files)}, val={len(val_files)}, test={len(test_files)}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main():
    print("Step 1: Extracting frames from FaceForensics++ videos (face_swap class)")
    extract_frames_from_videos(RAW_DIR / "face_swap_videos", FRAMES_DIR / "face_swap")

    print("\nStep 2: Detecting and cropping faces for each class")
    detector_type, detector = get_face_detector()

    # real + synthetic: crop directly from raw images
    process_class_folder(RAW_DIR / "real", CROPPED_DIR / "real", detector_type, detector, "real")
    process_class_folder(RAW_DIR / "synthetic", CROPPED_DIR / "synthetic", detector_type, detector, "synthetic")

    # face_swap: crop from the frames we just extracted
    if (FRAMES_DIR / "face_swap").exists():
        process_class_folder(FRAMES_DIR / "face_swap", CROPPED_DIR / "face_swap", detector_type, detector, "face_swap")

    print("\nStep 3: Splitting into train/val/test")
    split_dataset(CROPPED_DIR, OUTPUT_DIR)

    print("\nDone. Final dataset structure is in ./dataset/{train,val,test}/{real,face_swap,synthetic}/")


if __name__ == "__main__":
    main()

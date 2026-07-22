from pathlib import Path
import random
import shutil

# ----------------------------
# Configuration
# ----------------------------
RANDOM_SEED = 42
NUM_IMAGES = 2000

SOURCE_DIR = Path("raw_data/real_full")
DEST_DIR = Path("raw_data/real")

random.seed(RANDOM_SEED)

# ----------------------------
# Create destination folder
# ----------------------------
DEST_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Find all images
# ----------------------------
image_files = list(SOURCE_DIR.glob("*.jpg", "*.jpeg", ".*png"))

print(f"Found {len(image_files)} images.")

# ----------------------------
# Check enough images exist
# ----------------------------
if len(image_files) < NUM_IMAGES:
    raise ValueError(
        f"Only found {len(image_files)} images."
    )

# ----------------------------
# Randomly select images
# ----------------------------
selected = random.sample(image_files, NUM_IMAGES)

print(f"Selected {len(selected)} images.")

# ----------------------------
# Copy them
# ----------------------------
for img in selected:
    shutil.copy(img, DEST_DIR / img.name)

print("Done!")
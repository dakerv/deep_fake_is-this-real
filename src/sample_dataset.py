"""
Deepfake Detection - Data Sampling Pipeline

===========================================

Creates balanced sampled datasets for training the 
deepfake detection model.

The script randomly selects images from the original datasets and copies them into separate sampled folders.

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

# Real dataset contribution
FFHQ_IMAGES = 1500
CELEBDF_IMAGES = 1500

# Number of images per class
REAL_IMAGES = FFHQ_IMAGES + CELEBDF_IMAGES
SYNTHETIC_IMAGES = 3000
SWAPPED_IMAGES = 3000

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

random.seed(RANDOM_SEED)

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
        image_files.extend(folder.rglob(extension))

    return image_files

def clear_folder(folder):
    """
    Remove all files and subfolders inside a directory.

    The folder itself is recreated after clearing.

    Parameters
    ----------
    folder : Path
        Folder to empty.
    """

    if folder.exists():

        for item in folder.iterdir():

            if item.is_file():

                item.unlink()

            elif item.is_dir():

                shutil.rmtree(item)

    else:

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

def sample_images (source, destination, number):
   """
    Randomly select images from a source folder
    and copy them into a destination folder.

    Parameters
    ----------
    source : Path
        Folder containing original images.

    destination : Path
        Folder where sampled images will be copied.

    number : int
        Number of images to sample.

    """

   # Create destination folder if it does not exist
   destination.mkdir(
       parents=True,
       exist_ok=True
    )

   # Find all images
   image_files = get_image_files(source)

   print(f"\nSource: {source}")
   print(f"Available images: {len(image_files)}")


   # Check enough images exist
   if len(image_files) < number:

        raise ValueError(
            f"Not enough images available. "
            f"Requested {number}, found {len(image_files)}"
        )


   # Random selection
   selected_images = random.sample(
        image_files,
        number
    )

   # Copy images
   for image in selected_images:

        shutil.copy2(
            image,
            destination / image.name
        )


   print(
        f"Copied {number} images to {destination}"
    ) 

# =============
# Main Pipeline
# =============

def main():

    print("=" * 60)
    print("Deepfake Dataset Sampling")
    print("=" * 60)

    print("\nCleaning sampled folders...\n")

    clear_folder(REAL_DEST)
    clear_folder(SYNTHETIC_DEST)
    clear_folder(SWAPPED_DEST)


    print("\nSampling real images...\n")

    # Sample FFHQ real images
    sample_images(
        FFHQ_SOURCE,
        REAL_DEST,
        FFHQ_IMAGES
    )


    # Sample CelebDF real images
    sample_images(
        CELEBDF_SOURCE,
        REAL_DEST,
        CELEBDF_IMAGES
    )


    print("\nSampling synthetic images...\n")

    sample_images(
        SYNTHETIC_SOURCE,
        SYNTHETIC_DEST,
        SYNTHETIC_IMAGES
    )


    print("\nSampling swapped images...\n")

    sample_images(
        SWAPPED_SOURCE,
        SWAPPED_DEST,
        SWAPPED_IMAGES
    )


    print("\n" + "=" * 60)
    print("Dataset sampling completed successfully!")
    print("=" * 60)



if __name__ == "__main__":
    main()

print("\nFinal sampled dataset:")
print("----------------------")
print("Real images: 3000")
print("Synthetic images: 3000")
print("Swapped images: 3000")
print("Total images: 9000")
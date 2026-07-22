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
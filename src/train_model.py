"""
EfficientNet-B0 Training Pipeline
---------------------------------

Trains the EfficientNet-B0 convolutional neural network using
transfer learning for the three-classes of my deepfake image
classification.

Classes:
--------
- Real
- Swapped
- Synthetic

Pipeline:
---------
1. Load preprocessed dataset
2. Create EfficientNet-B0 model
3. Replace ImageNet classifier with three-class classifier
4. Train model
5. Validate model performance
6. Save best performing model

Author: Vanessa Daker
"""
import torch
import torch.nn as nn #neural network layers and loss functions
from torch.optim import Adam #chosen optimizer
from torchvision.models import (
    efficientnet_b0, #loads CNN architecture
    EfficientNet_B0_Weights #pretrained ImageNet weights
)
from dataset_loader import create_dataloaders

# =============
# Configuration
# =============

DATASET_DIR = "dataset"
MODEL_SAVE_PATH = "models/efficientnet_b0.pth"
BATCH_SIZE = 32
EPOCHS = 15
LEARNING_RATE = 0.0001 #standard starting point for transfer learning
NUM_CLASSES = 3
DEVICE = (
    "cpu"
)

# ======================
# Basic Environment Test
# ======================

if __name__ == "__main__":
    print ("=" * 60)
    print ("EfficientNet-B0 Training Pipeline")
    print ("=" * 60)

    print(f"PyTorch version: {torch.__version__}")
    print(f"Using device: {DEVICE}")

# ===============
# Load the Datset
# ===============
train_loader, val_loader, test_loader = create_dataloaders(
    DATASET_DIR,
    BATCH_SIZE
)

#Test script
print ("\nDataset loaded successfully!")

print(f"Training batches: {len(train_loader)}")
print(f"Validation batches: {len(val_loader)}")
print(f"Testing batches: {len(test_loader)}")

# ==============
# Model Creation
# ==============

weights = EfficientNet_B0_Weights.DEFAULT

model = efficientnet_b0(
    weights=weights
)

# EfficientNet predicts 1000 ImageNet classes, but we need
# only three.
model.classifier[1] = nn.Linear(
    1280, #1280 feature values
    NUM_CLASSES #my three classes
)
model.to(DEVICE)

# ====
# Test
# ====

print ("\nModel created successfully!")
print (model)

# ========================================
# Forward Pass Test (NO LEARNING DONE YET)
# ========================================

model.eval() # switch model to evaluation mode (testing)

images,labels = next(iter(train_loader))

images = images.to(DEVICE)
labels = labels.to(DEVICE)

with torch.no_grad():
    outputs = model(images)

# ==========
# Extra Test
# ==========
print("\nForward pass successful!")

print("Input shape:")
print(images.shape)

print("\nOutput shape:")
print(outputs.shape)

print("\nPredictions:")
print(outputs)



"""

# Loss function for multi-class classification
criterion = nn.CrossEntropyLoss()

# Using Adam as our optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)
"""
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
BATCH_SIZE = 8
EPOCHS = 1
LEARNING_RATE = 0.0001 # baseline configuration
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



# ===========================
# Loss Function and Optimizer
# ===========================


# Loss function for three-class classification
# Measures how far predicted class scores are from correct
# class.
criterion = nn.CrossEntropyLoss()

# Using Adam as optimizer, updates model's weights during
# training to reduce loss.
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

print("\nLoss function and optimizer created successfully!")
print(f"Loss function: {criterion}")
print(f"Optimizer: Adam")
print(f"Learning rate: {LEARNING_RATE}")


# =========================
# Training and Validation
# =========================

import time

print("\nStarting training...")

epoch_start_time = time.time()

for epoch in range(EPOCHS):

    print(f"\nStarting epoch {epoch + 1}/{EPOCHS}")

    model.train()

    running_train_loss = 0.0
    correct_train = 0
    total_train = 0

    start_time = time.time()

    for batch_index, (images, labels) in enumerate(train_loader):

        # Move data to CPU
        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        # Clear the previous gradients
        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        # Track training loss
        running_train_loss += loss.item()

        # Calculate predictions
        _, predicted = torch.max(outputs, 1)

        total_train += labels.size(0)
        correct_train += (predicted == labels).sum().item()

        if (batch_index + 1) % 10 == 0:
            elapsed = time.time() - start_time
            # Printing every 100 batches to as progress report.
            print(
                f"Batch {batch_index + 1}/{len(train_loader)} "
                f"| Loss: {loss.item():.4f}"
                f"| Time: {elapsed:.2f}s"
            )

    # =====================
    # Training Results
    # =====================

    train_loss = running_train_loss / len(train_loader)

    train_accuracy = (
        100 * correct_train / total_train
    )

    # =====================
    # Validation Phase
    # =====================

    model.eval()

    running_val_loss = 0.0
    correct_val = 0
    total_val = 0

    print("\nStarting validation...")

    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            # Forward pass
            outputs = model(images)

            # Calculate validation loss
            loss = criterion(outputs, labels)

            running_val_loss += loss.item()

            # Calculate predictions
            _, predicted = torch.max(outputs, 1)

            total_val += labels.size(0)
            correct_val += (predicted == labels).sum().item()

    # =====================
    # Validation Results
    # =====================

    val_loss = running_val_loss / len(val_loader)

    val_accuracy = (
        100 * correct_val / total_val
    )

    # =====================
    # Epoch Summary
    # =====================

    epoch_time = time.time() - epoch_start_time

    print("\n" + "=" * 60)

    print(
        f"Epoch [{epoch + 1}/{EPOCHS}] completed"
    )

    print(
        f"Training Loss: {train_loss:.4f}"
    )

    print(
        f"Training Accuracy: {train_accuracy:.2f}%"
    )

    print(
        f"Validation Loss: {val_loss:.4f}"
    )

    print(
        f"Validation Accuracy: {val_accuracy:.2f}%"
    )

    print(
        f"Epoch Time: {epoch_time:.2f} seconds"
    )

    print("=" * 60)

    """
        # Stop after two batches for this diagnostic
        if batch_index == 49:
            break
    """

    print("\nFirst training batch completed successfully.")
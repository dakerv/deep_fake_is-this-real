"""
Deepfake Detection - Final Model Evaluation
--------------------------------------------

Evaluates the selected EfficientNet-B0 model on the
held-out test dataset.

The test dataset is not used during model training or
model selection.

Classes:
    - Real
    - Synthetic
    - Swapped

Author: Vanessa Elinam Daker
"""

import torch
import torch.nn as nn
from torchvision.models import efficientnet_b0
from dataset_loader import create_dataloaders

# =====================
# Configuration
# =====================

DATASET_DIR = "dataset"

# Best model stored here
MODEL_PATH = "models/efficientnet_b0.pth"

BATCH_SIZE = 8
NUM_CLASSES = 3

DEVICE = "cpu"

CLASS_NAMES = [
    "real",
    "synthetic",
    "swapped"
]

# =====================
# Load Dataset
# =====================

train_loader, val_loader, test_loader = create_dataloaders(
    DATASET_DIR,
    BATCH_SIZE
)

print("\nTest dataset loaded successfully!")

print(f"Test batches: {len(test_loader)}")
print(f"Test images: {len(test_loader.dataset)}")

# =====================
# Create Model
# =====================

model = efficientnet_b0(
    weights=None
)

model.classifier[1] = nn.Linear(
    1280,
    NUM_CLASSES
)

# =====================
# Load Best Model
# =====================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model.to(DEVICE)

print("\nBest model loaded successfully!")

print(
    f"Model selected from epoch: "
    f"{checkpoint['epoch']}"
)

print(
    f"Validation accuracy: "
    f"{checkpoint['val_accuracy']:.2f}%"
)

"""
# =====================
# Test Model
# =====================

model.eval()

correct = 0
total = 0

print("\nStarting final test evaluation...")


with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        outputs = model(images)

        _, predicted = torch.max(
            outputs,
            1
        )

        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()


# =====================
# Test Accuracy
# =====================

test_accuracy = (
    100 * correct / total
)

print("\n" + "=" * 60)

print("FINAL TEST RESULTS")

print("=" * 60)

print(
    f"Correct predictions: "
    f"{correct}/{total}"
)

print(
    f"Test Accuracy: "
    f"{test_accuracy:.2f}%"
)

print("=" * 60)
"""

# =====================
# Final Test Evaluation
# =====================

from sklearn.metrics import (
    confusion_matrix,
    classification_report
)

model.eval()

all_predictions = []
all_labels = []

correct = 0
total = 0

print("\nStarting final test evaluation...")

with torch.no_grad():

    for images, labels in test_loader:

        images = images.to(DEVICE)
        labels = labels.to(DEVICE)

        #Forward pass
        outputs = model(images)

        # Get predicted class
        _, predicted = torch.max(
            outputs,
            1
        )

        # Store predictions and actual labels
        all_predictions.extend(
            predicted.cpu().numpy()
        )

        all_labels.extend(
            labels.cpu().numpy()
        )

        # Track overall accuracy
        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()

# =====================
# Overall Accuracy
# =====================

test_accuracy = (
    100 * correct / total
)

print("\n" + "=" * 60)

print("FINAL TEST RESULTS")

print("=" * 60)

print(
    f"Correct predictions: "
    f"{correct}/{total}"
)

print(
    f"Test Accuracy: "
    f"{test_accuracy:.2f}%"
)


# =====================
# Confusion Matrix
# =====================

cm = confusion_matrix(
    all_labels,
    all_predictions
)

print("\nConfusion Matrix:")
print(cm)


# =====================
# Classification Report
# =====================

print("\nClassification Report:")

print(
    classification_report(
        all_labels,
        all_predictions,
        target_names=CLASS_NAMES,
        digits=4
    )
)

print("=" * 60)

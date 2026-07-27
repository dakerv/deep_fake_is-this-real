# =============
# Configuration
# =============

DATASET_DIR = "dataset"

BATCH_SIZE = 32
EPOCHS = 15
LEARNING_RATE = 1e-4

NUM_CLASSES = 3

MODEL_SAVE_PATH = "models/efficientnet_b0.pth"

DEVICE = (
    "cpu"
)

# Load the Datset
train_loader, val_loader, test_loader = create_dataloaders(
    DATASET_DIR,
    BATCH_SIZE
)

from torchvision.models import (
    efficientnet_b0,
    EfficientNet_B0_Weights
)

weights = EfficientNet_B0_Weights.DEFAULT

model = efficientnet_b0(
    weights=weights
)

# EfficientNet predicts 1000 ImageNet classes, but we need
# only three.
model.classifier[1] = nn.Linear(
    1280,
    NUM_CLASSES
)
model.to(DEVICE)

# Loss function for multi-class classification
criterion = nn.CrossEntropyLoss()

# Using Adam as our optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)
from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

"""
Current folder structure
------------------------

dataset/

├── train/
│   ├── real/
│   ├── synthetic/
│   └── swapped/
│
├── val/
│   ├── real/
│   ├── synthetic/
│   └── swapped/
│
└── test/
    ├── real/
    ├── synthetic/
    └── swapped/

Pytorch needs code that answers three questions:
1. How many images exist?
2. Give an image number - returns (image, label)
3. Convert image to format a CNN expects - channels x height x width

The loader loads the preprocessed image dataset into
Pytorch for training, validation and testing. 

The module defines a custom Dataset class that reads images
and assigns class labels, applies image transformations and
returns tensors suitable for EfficientNet.

Pipeline
--------
1. Load images paths
2. Assign numerical labels
3. Apply image transformations
4. Create PyTorch datasets
5. Build Dataloaders for training

Author: Vanessa Daker

"""

# =============
# Dataset Class
# =============

class DeepfakeDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)
        self.transform = transform

        self.classes = [
            "real",
            "synthetic",
            "swapped"
        ]

        self.class_to_index = {
            class_name: index
            for index, class_name in enumerate(self.classes)
        }

        self.images = []
        self.load_images()

    def load_images(self):
        #Collect every image path
        for class_name in self.classes:
            class_folder = self.root_dir / class_name
            label = self.class_to_index[class_name]

            for extension in ("*.jpg", "*.jpeg", "*.png"):
                for image_path in class_folder.glob(extension):
                    self.images.append((image_path, label))

                self.images.append(
                    (
                        image_path,
                        label
                    )
                )

    # ------------------------
    # Required Dataset Methods
    # ------------------------            

    def __len__(self):
        """
        Return the total number of images in the dataset
        """
        return len(self.images)

    def __getitem__(self, index):
        """
        Retrieve one image and its corresponding label. The
        image is read and then converted to RGB, transformed
        into a tensor and returned with its numerical label.
        """

        image_path, label = self.images[index]
        #To prevent grayscale images from getting through
        # and causing confusion, everything is converted to
        # RGB.
        image = Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label

def get_transforms():
        # Augmenting the data during training alone.
        # Exposes the model to slightly different versions
        # to reduce overfitting.
        train_transform = transforms.Compose(
            [
               transforms.RandomHorizontalFlip(),
               transforms.RandomRotation(10),

               transforms.ToTensor(),

               transforms.Normalize(
                   mean= [
                       0.485,
                       0.456,
                       0.406
                   ],
                   std=[
                       0.229,
                       0.224,
                       0.225
                   ]
               )
            ]
        )

        # No augmentation done on validation.
        # The performance is evaluated on original data.
        val_transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[
                        0.485,
                        0.456,
                        0.406
                    ],
                    std=[
                        0.229,
                        0.224,
                        0.225
                    ]
                )
            ]
        )

        return train_transform, val_transform

def create_dataloaders(data_dir, batch_size=32):
        
        train_transform, val_transform = get_transforms()

        train_dataset = DeepfakeDataset(
            Path(data_dir) / "train",
            train_transform
        )

        val_dataset = DeepfakeDataset(
            Path(data_dir) / "val",
            val_transform
        )

        test_dataset = DeepfakeDataset(
            Path(data_dir) / "test",
            val_transform
        )

        #Randomise the order of training images per epoch
        #to reduce learning bias.
        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False
        )

        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False
        )

        return train_loader, val_loader, test_loader

DATASET_DIR = Path("dataset")

# ===================
# Test Dataset Loader
# ===================

if __name__ == "__main__":
        train_loader, val_loader, test_loader = create_dataloaders(DATASET_DIR)

        print("Train batches:", len(train_loader))
        print("Validation batches:", len(val_loader))
        print("Test batches:", len(test_loader))

        images, labels = next(iter(train_loader))

        print("Image batch shape:", images.shape)
        print("Label batch shape:", labels.shape)

        print("Labels:", labels)

        print(train_loader.dataset.classes)
        print(train_loader.dataset.class_to_index)
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

"""

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
        for class_name in self.classes:
            class_folder = self.root_dir / class_name
            label = self.class_to_index[class_name]

            for image_path in class_folder.glob("*"):

                self.images.append(
                    (
                        image_path,
                        label
                    )
                )

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        image_path, label = self.images[index]
        image = Image.open(image_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image, label

    def get_transforms():
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

    if __name__ == "__main__":
        train_loader, val_loader, test_loader = create_dataloaders()

    print("Train batches:", len(train_loader))
    print("Validation batches:", len(val_loader))
    print("Test batches:", len(test_loader))

    images, labels = next(iter(train_loader))

    print("Image batch shape:", images.shape)
    print("Label batch shape:", labels.shape)

    print("Labels:", labels)
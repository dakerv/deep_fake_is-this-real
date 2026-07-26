from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

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
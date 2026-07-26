from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class DeepfakeDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        se7dlf.root_dir = Path(root_dir)
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
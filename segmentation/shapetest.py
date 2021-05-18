# Notebook geeft het op als ik hier probeer om de code te testen,
# dus ik doe het maar gewoon in een .py file  - Gerrit

from dataset import SegmentationDataset
from torch.utils.data import DataLoader
from torchvision import transforms

seg_dataset = SegmentationDataset("data/AmazonNew", "PNG", "Masks", transforms=transforms.Compose([transforms.ToTensor()]))
seg_dataloader = DataLoader(seg_dataset, batch_size=1, shuffle=False, num_workers=0)
samples = next(iter(seg_dataloader))
# Display the image and mask tensor shape
# We see the tensor size is correct bxcxhxw, where b is batch size, c is number of channels, h is height, w is width
print(samples['image'].shape)
print(samples['mask'].shape)
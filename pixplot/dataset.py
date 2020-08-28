import torch
import os
import numpy as np
from torch.utils.data import Dataset, DataLoader
from glob2 import glob
from PIL import Image

class PixPlotDataset(Dataset):
    def __init__(self, root_dir):
        """
        Args:
            root_dir (string): Directory with all images
        """
        self.root_dir = root_dir
        self.imagePaths = sorted(glob(root_dir))

    def __len__(self):
        return len(self.imagePaths)
    
    def __getitem__(self, idx):
        im = Image.open(self.imagePaths[idx]).convert("RGB").resize((299,299))
        data = np.array(im.getdata())
        data = 2*( data.reshape( (im.size[0], im.size[1], 3) ).astype( np.float32 )/255 ) - 1
        data = data.transpose((2, 0, 1))
        # for some reason, it says this isn't a method of torch but it definitely is
        data = torch.from_numpy(data)
        return {'filename': os.path.basename(self.imagePaths[idx]),'data':data}
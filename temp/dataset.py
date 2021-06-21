"""Functions and classes that help organise data flow."""

import keras
import os
import random
import numpy as np
from tensorflow.keras.preprocessing.image import load_img

class SatelliteImages(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i: i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i: i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            img = load_img(path, target_size=self.img_size)
            data = np.array(img)[:, :, 0]
            data = np.expand_dims(data, 2)
            y[j] = data
            y[j] = np.divide(y[j], 255)
        return x, y

def file_loader(input_dir: str, target_dir: str, img_size: tuple = (512, 512), num_classes: int = 2, batch_size: int = 1, seed: int = 1337) -> iter:
    input_dir = input_dir
    target_dir = target_dir
    img_size = img_size # 512x512
    num_classes = num_classes  # 2 soorten labels, zoals eerder besproken
    batch_size = batch_size  # Hoeveel afbeeldingen er in één batch moeten.

    input_img_paths = sorted([
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
        if fname.endswith(".png")])

    target_img_paths = sorted([
        os.path.join(target_dir, fname)
        for fname in os.listdir(target_dir)
        if fname.endswith(".png") and not fname.startswith(".")])

    val_samples = int(len(input_img_paths) * 0.2)
    seed = seed
    random.Random(seed).shuffle(input_img_paths)
    random.Random(seed).shuffle(target_img_paths)
    train_input_img_paths = input_img_paths[:-val_samples]
    train_target_img_paths = target_img_paths[:-val_samples]
    val_input_img_paths = input_img_paths[-val_samples:]
    val_target_img_paths = target_img_paths[-val_samples:]

    # Instantiate data Sequences for each split
    train_gen = SatelliteImages(batch_size, img_size, train_input_img_paths, train_target_img_paths)
    val_gen = SatelliteImages(batch_size, img_size, val_input_img_paths, val_target_img_paths)

    return train_gen, val_gen

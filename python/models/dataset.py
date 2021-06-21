"""Functions and classes that help organise data flow."""
from os import listdir as os_listdir
from os import path as os_path
from random import SystemRandom
from typing import List, Tuple

import numpy as np
from keras.utils import Sequence
from tensorflow.keras.preprocessing.image import load_img


class SatelliteImages(Sequence):
    """Sequence class to iterate over the data as Numpy arrays."""

    def __init__(
        self,
        batch_size: int,
        img_size: Tuple[int, int],
        input_img_paths: List[str],
        target_img_paths: List[str],
    ):
        """Open format and save the locations.

        Parameters
        ----------
        batch_size
            The amount of images to process each train iteration.
        img_size
            The width and height of the images.
        input_img_paths
            A list with all the input image paths.
        target_img_paths
            A list with all the target image paths.
        """
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self) -> int:
        """Return the total length of all the images divided by the batch size to get the length per batch size."""
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """Return tuple with (input, target) correspond to batch with an id of idx.

        Parameters
        ----------
        idx
            The current batch id

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            The input and target images.
        """
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]

        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, img_path in enumerate(batch_input_img_paths):
            img = load_img(img_path, target_size=self.img_size)
            x[j] = img

        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        for j, img_path in enumerate(batch_target_img_paths):
            img = load_img(img_path, target_size=self.img_size)
            data = np.array(img)[:, :, 0]
            data = np.expand_dims(data, 2)
            y[j] = data
            y[j] = np.divide(y[j], 255)

        return x, y


def file_loader(
    input_dir: str,
    target_dir: str,
    img_size: Tuple[int, int] = (512, 512),
    batch_size: int = 1,
    seed: int = 1337,
) -> Tuple[SatelliteImages, SatelliteImages]:
    """Return a train and value generator to fit the model.

    Parameters
    ----------
    input_dir
        The string path to the input images folder.
    target_dir
        The string path to the target images folder.
    img_size
        The current batch id
    batch_size
        The current batch id
    seed
        The current batch id

    Returns
    -------
    Tuple[SatelliteImages, SatelliteImages]
        The train and value generators.
    """
    input_img_paths = sorted(
        [
            os_path.join(input_dir, fname)
            for fname in os_listdir(input_dir)
            if fname.endswith(".png")
        ]
    )

    target_img_paths = sorted(
        [
            os_path.join(target_dir, fname)
            for fname in os_listdir(target_dir)
            if fname.endswith(".png") and not fname.startswith(".")
        ]
    )

    #: Splits the input and target images into train/validation sets.
    random_gen = SystemRandom(seed)
    val_samples = int(len(input_img_paths) * 0.2)
    random_gen.shuffle(input_img_paths)
    random_gen.shuffle(target_img_paths)
    train_input_img_paths = input_img_paths[:-val_samples]
    train_target_img_paths = target_img_paths[:-val_samples]
    val_input_img_paths = input_img_paths[-val_samples:]
    val_target_img_paths = target_img_paths[-val_samples:]

    #: Instantiate data Sequences for each split.
    train_gen = SatelliteImages(
        batch_size, img_size, train_input_img_paths, train_target_img_paths
    )
    val_gen = SatelliteImages(
        batch_size, img_size, val_input_img_paths, val_target_img_paths
    )

    return train_gen, val_gen

"""The data preperation and model training pipeline."""

from python.models.dataset import file_loader
from python.models.metrics import MeanIoU, Precision, Recall
from python.models.model import model_getter, standard_unet_model, train_model

from matplotlib import pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
from PIL import Image
import numpy as np
import PIL
import keras
import random

from python.helpers.model import visualise_from_history

def data_science_pipeline_unet():
    """Everything comes preconfigured, so there's no need for parameters or return values."""
    #: Definitions

    image_folder = r"C:\Users\gvand\Projecten\Pycharm\BB8\src\data\Model Input Data\West_Bengal_15_geolocations_v2\true_colours_images_testset_v2"
    mask_folder = r"C:\Users\gvand\Projecten\Pycharm\BB8\src\data\Model Input Data\West_Bengal_15_geolocations_v2\mask_completed"
    image_size = (512, 512)
    num_classes = 2
    batch_size = 1

    #: Data preperation
    train_gen, val_gen, train_input_img_paths, train_target_img_paths, val_input_img_paths, val_target_img_paths = file_loader(
        image_folder,
        mask_folder
    )

    #: the model metrics are calculated during compilation
    model = model_getter(standard_unet_model, image_size, num_classes)

    #: Fit the model
    model_history = train_model(
        model,
        "rmsprop",
        "sparse_categorical_crossentropy",
        [MeanIoU(num_classes=2), Precision(), Recall()],
        train_gen,
        val_gen,
    )

    #: Evaluation and validation.
    visualise_from_history(model_history, ["mean_iou", "precision", "recall", "loss"])

    # Generate predictions for all images in the validation set

    val_preds = model.predict(val_gen)

    def display_mask(i):
        """Quick utility to display a model's prediction."""
        mask = np.argmax(val_preds[i], axis=-1)
        mask = np.expand_dims(mask, axis=-1)
        img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(mask))
        plt.imshow(img)

    # Display results for validation image #0
    i = random.randrange(0, len(val_input_img_paths) - 1)

    # Display input image
    with Image.open(val_input_img_paths[i]) as image:
        im_array = np.array(image)
        plt.imshow(im_array)

    # Display ground-truth target mask
    img = PIL.ImageOps.autocontrast(load_img(val_target_img_paths[i]))
    plt.imshow(img)

    # Display mask predicted by our model
    display_mask(i)  # Note that the model only sees inputs at 150x150.

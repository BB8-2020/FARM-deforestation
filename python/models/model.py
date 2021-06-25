"""Functions that create and train the model."""
from typing import Callable

from keras import Model
from keras import backend as keras_backend
from keras import callbacks as keras_callbacks
from keras.callbacks import History

from python.models.dataset import SatelliteImages


def model_getter(
    model_build_func: Callable[[tuple, int], Model], img_size: tuple, num_classes: int
) -> Model:
    """Create and return a model.

    Parameters
    ----------
    model_build_func
        The function that builds the desired model type and returns it.
    img_size
        A tuple defining the pixel dimensions of used images
    num_classes
        The amount of classes to classify.

    Returns
    -------
    model
        The created UNET model.
    """
    #: Free up RAM in case the model definition cells were run multiple times.
    keras_backend.clear_session()
    #: Build the model.
    model = model_build_func(img_size, num_classes)
    return model


def train_model(
    model: Model,
    optimizer: str,
    loss: str,
    metrics: list,
    train_iter: SatelliteImages,
    val_iter: SatelliteImages,
    epochs: int = 8,
    checkpoint_name: str = "./h5/image_segmentation.h5",
) -> History:
    """Train the model and return the history.

    Parameters
    ----------
    model
        The model to fit.
    optimizer
        The optimizer to use for the fitting.
    loss
        The loss function for the fitting.
    metrics
        The metric types to use.
    train_iter
        The train iterator to get the train data.
    val_iter
        The value iterator to get the value data.
    epochs
        The amount of epochs to train.
    checkpoint_name
        The checkpoint name in which the best results will be saved..

    Returns
    -------
    model_history
        The History object of the fitted model.
    """
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    callbacks = [keras_callbacks.ModelCheckpoint(checkpoint_name, save_best_only=True)]
    #: Train the model, doing validation at the end of each epoch.
    model_history = model.fit(
        train_iter, epochs=epochs, callbacks=callbacks, validation_data=val_iter
    )
    return model_history

"""Functions that create and train the model."""
from typing import Callable

from keras import Input, Model
from keras import backend as keras_backend
from keras import callbacks as keras_callbacks
from keras import layers as keras_layers
from keras.callbacks import History

from python.model.dataset import SatelliteImages


def standard_unet_model(img_size: tuple = (512, 512), num_classes: int = 2) -> Model:
    """Create and return a UNET model.

    Parameters
    ----------
    img_size
        The image size in pixel dimensions.
    num_classes
        The amount of classes to classify.

    Returns
    -------
    model
        The created UNET model.
    """
    inputs = Input(shape=img_size + (3,))

    #: [First half of the network: downsampling inputs].
    x = keras_layers.Conv2D(32, 3, strides=2, padding="same")(inputs)
    x = keras_layers.BatchNormalization()(x)
    x = keras_layers.Activation("relu")(x)

    #: Set aside residual.
    previous_block_activation = x

    #: Blocks 1, 2, 3 are identical apart from the feature depth.
    for filters in [64, 128, 256]:
        x = keras_layers.Activation("relu")(x)
        x = keras_layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = keras_layers.BatchNormalization()(x)

        x = keras_layers.Activation("relu")(x)
        x = keras_layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = keras_layers.BatchNormalization()(x)

        x = keras_layers.MaxPooling2D(3, strides=2, padding="same")(x)

        #: Project residual.
        residual = keras_layers.Conv2D(filters, 1, strides=2, padding="same")(
            previous_block_activation
        )
        #: Add back residual.
        x = keras_layers.add([x, residual])
        #: Set aside next residual.
        previous_block_activation = x

    #: [Second half of the network: upsampling inputs].
    for filters in [256, 128, 64, 32]:
        x = keras_layers.Activation("relu")(x)
        x = keras_layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = keras_layers.BatchNormalization()(x)

        x = keras_layers.Activation("relu")(x)
        x = keras_layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = keras_layers.BatchNormalization()(x)

        x = keras_layers.UpSampling2D(2)(x)

        #: Project residual.
        residual = keras_layers.UpSampling2D(2)(previous_block_activation)
        residual = keras_layers.Conv2D(filters, 1, padding="same")(residual)
        #: Add back residual.
        x = keras_layers.add([x, residual])
        #: Set aside next residual.
        previous_block_activation = x

    #: Add a per-pixel classification layer.
    outputs = keras_layers.Conv2D(num_classes, 3, activation="softmax", padding="same")(
        x
    )

    #: Define the model.
    model = Model(inputs, outputs)
    return model


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
    checkpoint_name: str = "image_segmentation.h5",
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

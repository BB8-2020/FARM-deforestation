"""File to host a standard unet implementation."""
from keras import Input, Model
from keras import layers as keras_layers


def get_unet_model(img_size: tuple = (512, 512), num_classes: int = 2) -> Model:
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

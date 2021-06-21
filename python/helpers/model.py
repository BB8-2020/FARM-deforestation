"""Functions for processing the output of the model."""
from typing import List

import numpy as np
from keras import preprocessing as keras_preprocessing
from keras.callbacks import History
from matplotlib import pyplot as plt
from PIL import ImageOps


def process_mask(data: np.ndarray) -> np.ndarray:
    """Convert model data to a processed mask.

    Parameters
    ----------
    data
        The model data.

    Returns
    -------
    img
        The processed mask.
    """
    mask = np.argmax(data, axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    img = ImageOps.autocontrast(keras_preprocessing.image.array_to_img(mask))
    return img


def display_mask(data: np.ndarray):
    """Display a model's prediction.

    Parameters
    ----------
    data
        The model data.
    """
    mask = np.argmax(data, axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    img = ImageOps.autocontrast(keras_preprocessing.image.array_to_img(mask))
    plt.imshow(img)


def process_mask_confidence_treshold(
    data: np.ndarray, conf_treshold: float = None, conf_basevalue: float = 0.0
) -> np.ndarray:
    """Extract the model predictions by a confidence treshold.

    If the confidence treshold is not entered, the function behaves normally.
    Additionally, a base value may be given to which a prediction defaults if the treshold is not reached.

    Parameters
    ----------
    data
        The model data.
    conf_treshold
        The confidence threshold to check.
    confbasevalue
        The confidence base value.

    Returns
    -------
    results
        The indexes of the mask where the confidence is higher then the condition.
    """
    if conf_treshold is not None:
        #: Get indices of highest element in probability list (base predictions).
        maxindices = np.argmax(data, axis=-1)
        #: Create matrice for final predictions.
        results = np.zeros(maxindices.shape)
        #: Iterate over matrice and assign iterator to a object so we can get it's multi_index.
        iterator = np.nditer(maxindices, flags=["multi_index"])
        for x in iterator:
            if (
                data[(iterator.multi_index[0], iterator.multi_index[1], x)]
                >= conf_treshold
            ):
                results[
                    (iterator.multi_index[0], iterator.multi_index[1])
                ] = maxindices[(iterator.multi_index[0], iterator.multi_index[1])]
            else:
                results[iterator.multi_index] = conf_basevalue
        return results
    else:
        results = np.argmax(data, axis=-1)
    return results


def visualise_from_history(model_history: History, metrics: List[str]):
    """Visualizes the model history.

    Parameters
    ----------
    model_history
        The model history data.
    metrics
        The metrics to plot from the model history.
    """
    for metric in metrics:
        plt.plot(
            model_history.history["{}".format(metric)], label="train_{}".format(metric)
        )
        plt.plot(
            model_history.history["val_{}".format(metric)],
            label="val_{}".format(metric),
        )
    plt.legend()
    plt.show()

"""Functions for processing the output of the model."""
import numpy as np
import PIL
import keras
from matplotlib import pyplot as plt
from typing import Union, List

def process_mask(data):
    """Utility to translate the output of the model into a mask."""
    mask = np.argmax(data, axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(mask))
    return img

def display_mask(data):
    """Quick utility to display a model's prediction."""
    mask = np.argmax(data, axis=-1)
    mask = np.expand_dims(mask, axis=-1)
    img = PIL.ImageOps.autocontrast(keras.preprocessing.image.array_to_img(mask))
    plt.imshow(img)

def process_mask_confidence_treshold(data, conftreshold=None, confbasevalue=0):
    """Utility to extract model predictions by a confidence treshold. If the confidence
    treshold is not entered, the function behaves normally. Additionally, a base value
    may be given to which a prediction defaults if the treshold is not reached."""
    as_matrix = data.copy()
    if conftreshold is not None:
        # Get indices of highest element in probability list (base predictions)
        maxindices = np.argmax(data, axis=-1)
        # Create matrice for final predictions
        results = np.zeros(maxindices.shape)
        # Iterate over matrice
        # Assign iterator to a object so we can get it's multi_index.
        iterator = np.nditer(maxindices, flags=['multi_index'])
        for x in iterator:
            if data[(iterator.multi_index[0], iterator.multi_index[1], x)] >= conftreshold:
                results[(iterator.multi_index[0], iterator.multi_index[1])] = maxindices[
                    (iterator.multi_index[0], iterator.multi_index[1])]
            else:
                results[iterator.multi_index] = confbasevalue
        return results
    else:
        results = np.argmax(data, axis=-1)
    return results

def visualise_from_history(historyobject, metric: Union[str,List[str]]) -> None:
    if isinstance(metric, str):  # Only one metric given
        plt.plot(historyobject.history['{}'.format(metric)], label="train_{}".format(metric))
        plt.plot(historyobject.history['val_{}'.format(metric)], label="val_{}".format(metric))
        plt.legend()
        plt.show()

    elif isinstance(metric, list):  # Multiple metrics given
        for single in metric:
            if not isinstance(single,str):
                raise NotImplementedError("Metric visualisation only works with strings for metrics!")
            plt.plot(historyobject.history['{}'.format(single)], label="train_{}".format(single))
            plt.plot(historyobject.history['val_{}'.format(single)], label="val_{}".format(single))
        plt.legend()
        plt.show()
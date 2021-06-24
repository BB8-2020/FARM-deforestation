"""Helper file to extend the pyplot functionality."""
from typing import List, Tuple

from keras.callbacks import History
from matplotlib import pyplot as plt


def get_axes_row_col(i: int, ncols: int) -> Tuple[int, int]:
    """Get the row and column to render a plot in.

    Parameters
    ----------
    i
        The index of the model.
    ncols
        The amount of columns (amount of models).

    Returns
    -------
    (row, col)
        The row and column to render the plot in.
    """
    row = i // ncols
    col = i % ncols
    return row, col


def plot_model_history(metric: str, history: History, models: List[dict]):
    """Plot a metric for all the models history's.

    Parameters
    ----------
    metric
        The metric to plot (ex: mean_iou).
    history
        The history object that contains the data of all epochs.
    models
        The models list refrence with the names, getter functions and optimizer names.
    """
    ncols = len(models)
    fig, ax = plt.subplots(nrows=1, ncols=ncols, squeeze=False)
    fig.set_size_inches(18.5, 10.5)

    for i, model in enumerate(models):
        row, col = get_axes_row_col(i, ncols)
        ax[row, col].plot(history[i][metric], label=f"{model['name']} train_loss")
        ax[row, col].plot(
            history[i][f"val_{metric}"], label=f"{model['name']} val_loss"
        )

    plt.legend()
    plt.suptitle(f"History of {metric}", fontsize=20)
    plt.tight_layout()
    plt.show()

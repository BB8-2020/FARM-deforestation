"""Metrics for validating model performance."""
from typing import Any, List, Optional

import numpy as np
from tensorflow import math as tf_math
from tensorflow.keras import metrics


class MeanIoU(metrics.MeanIoU):
    """Class to calculate the MeanIoU."""

    def __init__(
        self,
        num_classes: int = None,
        name: str = "mean_iou",
        dtype: Optional[Any] = None,
    ):
        """Initialize this MeanIoU class.

        Parameters
        ----------
        num_classes
            The amount of distinct classes for the image segmentation.
        name
            The name of this MeanIoU method.
        dtype
            The dytype of the data.
        """
        super(MeanIoU, self).__init__(num_classes=num_classes, name=name, dtype=dtype)

    def update_state(
        self, y_true: List[int], y_pred: List[int], sample_weight: Optional[Any] = None
    ) -> Any:
        """Update the state of this MeanIoU class.

        Parameters
        ----------
        y_true
            The ground truth values, with the same dimensions as `y_pred`.
        y_pred
            The predicted values. Each element must be in the range `[0, 1]`
        sample_weight
            Optional weighting of each example.

        Returns
        -------
        Any
            The updated the given confusion matrix of all the variables.
        """
        y_pred, y_true = np.array(y_pred), np.array(y_true)
        if len(y_pred.shape) >= 2:
            y_pred = tf_math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)


class Precision(metrics.Precision):
    """Class to calculate the Precision."""

    def __init__(self, name: str = "precision", dtype: Optional[Any] = None):
        """Initialize this Precision class.

        Parameters
        ----------
        name
            The name of this Precision method.
        dtype
            The dytype of the data.
        """
        super(Precision, self).__init__(name=name, dtype=dtype)

    def update_state(
        self, y_true: List[int], y_pred: List[int], sample_weight: Optional[Any] = None
    ) -> Any:
        """Update the state of this Precision class.

        Parameters
        ----------
        y_true
            The ground truth values, with the same dimensions as `y_pred`.
        y_pred
            The predicted values. Each element must be in the range `[0, 1]`
        sample_weight
            Optional weighting of each example.

        Returns
        -------
        Any
            The updated the given confusion matrix of all the variables.
        """
        y_pred, y_true = np.array(y_pred), np.array(y_true)
        if len(y_pred.shape) >= 2:
            y_pred = tf_math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)


class Recall(metrics.Recall):
    """Class to calculate the Recall."""

    def __init__(self, name: str = "recall", dtype: Optional[Any] = None):
        """Initialize this Recall class.

        Parameters
        ----------
        name
            The name of this Recall method.
        dtype
            The dytype of the data.
        """
        super(Recall, self).__init__(name=name, dtype=dtype)

    def update_state(
        self, y_true: List[int], y_pred: List[int], sample_weight: Optional[Any] = None
    ) -> Any:
        """Update the state of this Recall class.

        Parameters
        ----------
        y_true
            The ground truth values, with the same dimensions as `y_pred`.
        y_pred
            The predicted values. Each element must be in the range `[0, 1]`
        sample_weight
            Optional weighting of each example.

        Returns
        -------
        Any
            The updated the given confusion matrix of all the variables.
        """
        y_pred, y_true = np.array(y_pred), np.array(y_true)
        if len(y_pred.shape) >= 2:
            y_pred = tf_math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)

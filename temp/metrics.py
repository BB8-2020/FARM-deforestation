"""Metrics for validating model performance."""

import tensorflow as tf

class MeanIoU(tf.keras.metrics.MeanIoU):
    def __init__(self, y_true=None, y_pred=None, num_classes=None, name='mean_iou', dtype=None):
        super(MeanIoU, self).__init__(num_classes = num_classes, name=name, dtype=dtype)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)


class Precision(tf.keras.metrics.Precision):
    def __init__(self, y_true=None, y_pred=None, name='precision', dtype=None):
        super(Precision, self).__init__(name=name, dtype=dtype)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)


class Recall(tf.keras.metrics.Recall):
    def __init__(self, y_true=None, y_pred=None, name='recall', dtype=None):
        super(Recall, self).__init__(name=name, dtype=dtype)

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)
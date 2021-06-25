"""Test functions to check if the helper functions run correctly."""
from pytest import approx
from tensorflow import convert_to_tensor

from python.models.metrics import MeanIoU, Precision, Recall

y_true = convert_to_tensor([0, 1, 1, 1])
y_pred = convert_to_tensor([1, 0, 1, 1])


def test_precision():
    """Test whether the adapted Precision class still works as it's baseline counterpart."""
    # Adapted from docs: https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Precision
    # Note: Our custom class expects a probability matrice instead of
    m = Precision()
    m.update_state(y_true, y_pred)
    assert approx(m.result().numpy()) == 0.6666667

    m = Precision()
    m.update_state(y_true, y_pred, sample_weight=[0, 0, 1, 0])
    assert m.result().numpy() == 1.0


def test_recall():
    """Test whether the adapted Recall class still works as it's baseline counterpart."""
    # Adapted from docs: https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Recall
    m = Recall()
    m.update_state(y_true, y_pred)
    assert approx(m.result().numpy()) == 0.6666667

    m = Recall()
    m.update_state(y_true, y_pred, sample_weight=[0, 0, 1, 0])
    assert m.result().numpy() == 1.0


def test_meaniou():
    """Test whether the adapted Recall class still works as it's baseline counterpart."""
    # Adapted from docs: https://www.tensorflow.org/api_docs/python/tf/keras/metrics/MeanIoU
    m = MeanIoU(num_classes=2)
    m.update_state(y_true, y_pred)
    assert approx(m.result().numpy()) == 0.25

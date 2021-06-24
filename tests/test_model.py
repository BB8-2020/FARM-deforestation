"""Test functions to check if the model functions run correctly."""
from python.model.model import model_getter, standard_unet_model


def test_standard_unet_model():
    """Test whether the standard_unet_model is imported correctly."""
    model = model_getter(standard_unet_model, (512, 512), 2)
    assert len(model.layers) == 72  #: Determine if amount of layers is correct.
    assert model.input_shape == (
        None,
        512,
        512,
        3,
    )  #: Determine if input shape is correct.
    assert (
        model.layers[-1].output.shape[-1] == 2
    )  #: Determine if output channels are the same.

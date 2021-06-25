"""Test functions to check if the model functions run correctly. (Only works locally)"""
# from python.models.filter_model import get_filter_model
# from python.models.model import model_getter
# from python.models.sampling_model import get_sampling_model
# from python.models.unet_model import get_unet_model


# def test_unet_model():
#     """Test whether the standard_unet_model is imported correctly."""
#     model = model_getter(get_unet_model, (512, 512), 2)
#     assert len(model.layers) == 72  #: Determine if amount of layers is correct.
#     assert model.input_shape == (
#         None,
#         512,
#         512,
#         3,
#     )  #: Determine if input shape is correct.
#     assert (
#         model.layers[-1].output.shape[-1] == 2
#     )  #: Determine if output channels are the same.


# def test_filter_model():
#     """Test whether the unet_model with extra filters is imported correctly."""
#     model = model_getter(get_filter_model, (512, 512), 2)
#     assert model.layers[5].filters == 128


# def test_sampling_model():
#     """Test whether the unet_model with extra filters is imported correctly."""
#     model = model_getter(get_sampling_model, (512, 512), 2)
#     assert len(model.layers) == 91  #: Determine if amount of layers is correct.

"""The data preperation and model training pipeline."""
from dataset import file_loader
from metrics import MeanIoU, Precision, Recall
from model import model_getter, standard_unet_model, train_model

from python.helpers.model import visualise_from_history


def data_science_pipeline_unet():
    """Everything comes preconfigured, so there's no need for parameters or return values."""
    #: Data preperation
    train_gen, val_gen = file_loader(
        "../data/Model Input Data/West_Bengal_15_geolocations_v2/true_colours_images_testset_v2",
        "../data/Model Input Data/West_Bengal_15_geolocations_v2/mask_completed",
    )

    #: the model metrics are calculated during compilation
    model = model_getter(standard_unet_model, (512, 512), 2)

    #: Fit the model
    model_history = train_model(
        model,
        "rmsprop",
        "sparse_categorical_crossentropy",
        [MeanIoU(num_classes=2), Precision(), Recall()],
        train_gen,
        val_gen,
    )

    #: Evaluation and validation.
    visualise_from_history(model_history, ["mean_iou", "precision", "recall", "loss"])

"""The data prep / model training pipeline, exported from the u-net notebook"""
from dataset import file_loader, SatelliteImages
from metrics import MeanIoU, Precision, Recall
from model import get_model
from post_processing import visualise_from_history
import random
import keras
import os

def data_science_pipeline_unet():
    """Everything comes preconfigured, so there's no need for parameters."""

    # DATA PREP

    train_gen, val_gen = file_loader("../data/Model Input Data/West_Bengal_15_geolocations_v2/true_colours_images_testset_v2",
                                     "../data/Model Input Data/West_Bengal_15_geolocations_v2/mask_completed")

    # MODEL (Metrics are calculated during compilation)

    model = get_model((512,512), 2)

    model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy",
                  metrics=[MeanIoU(num_classes=2), Precision(), Recall()])
    # model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy", metrics=[MeanIoU(num_classes=2)])
    callbacks = [keras.callbacks.ModelCheckpoint("image_segmentation.h5", save_best_only=True)]

    # Train the model, doing validation at the end of each epoch.
    epochs = 8
    reshistory = model.fit(train_gen, epochs=epochs, callbacks=callbacks, validation_data=val_gen)

    # EVAL/VALIDATION

    visualise_from_history(["mean_iou", "precision", "recall", "loss"])

    
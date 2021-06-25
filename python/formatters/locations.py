"""Formats the locations to have bboxes."""
from numpy import arange as np_arange
from pandas import DataFrame

from python.helpers.formatter import read_dataset, write_dataset


def format_locations():
    """Format the coordinates to have equal spacing between them and cover all the coordinates."""
    df = read_dataset()
    x_min, x_max = df["P1_Longitude"].min(), df["P1_Longitude"].max()
    y_min, y_max = df["P1_Latitude"].min(), df["P1_Latitude"].max()

    y_data, x_data = [], []
    step_size = 0.025
    for y in np_arange(y_min, y_max, step_size):
        for x in np_arange(x_min, x_max, step_size):
            y_data.append(y)
            x_data.append(x)

    new_df = DataFrame({"P1_Longitude": x_data, "P1_Latitude": y_data})
    write_dataset(new_df)


if __name__ == "__main__":
    format_locations()

"""Helper file to open and save the formatted file."""
from math import cos as math_cos
from math import pi as math_pi
from typing import Callable, List

from pandas import DataFrame, ExcelWriter, read_excel
from sentinelhub.constants import CRS
from sentinelhub.geometry import BBox


def format_locations(
    format_name: str,
    df_filter: Callable[[DataFrame], DataFrame],
    *formatters: List[str],
):
    """Open format and save the locations.

    Parameters
    ----------
    format_name
        The save file format name.
    df_filter
        A filter to apply after all the formatters.
    *formatters
        A list of formatters to apply.
    """
    df = read_dataset()

    #: Drops the nan value rows and applies the filter to the P1_Longitude and P1_Latitude columns.
    for column_name in ["P1_Longitude", "P1_Latitude"]:
        for formatter in formatters:
            df[column_name] = df[column_name].apply(formatter)
        df = df[df[column_name].notna()]

    #: Only uses the longitude and latitude and applies the dataframe filter.
    df = df[["P1_Longitude", "P1_Latitude"]]
    df = df if df_filter is None else df_filter(df)

    write_dataset(df, format_name)


def read_dataset() -> DataFrame:
    """Open format and save the locations.

    Returns
    -------
    DataFrame
        The opened dataset in a DataFrame format.
    """
    return read_excel(
        "../../data/Locations/FarmerLocationExtract4Interns.xlsx", engine="openpyxl"
    )


def write_dataset(df: DataFrame, format_name: str):
    """Open format and save the locations.

    Parameters
    ----------
    df
        The given dataframe to save.
    format_name
        The format name to use as an extension to the base file name.
    """
    writer = ExcelWriter(
        f"../../data/Locations/FarmerLocationExtract4Interns_{format_name}.xlsx",
        engine="xlsxwriter",
    )
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()


def deg2rad(degrees: float) -> float:
    """Convert degrees to radius.

    Parameters
    ----------
    degrees
        The degrees (longitude or latitude).

    Returns
    -------
    float
        The radius representation of the given degrees.
    """
    return (math_pi * degrees) / 180.0


def bbox_converter(long: float, lat: float, radius: float) -> BBox:
    """Convert degrees to radius.

    Parameters
    ----------
    long
        The given longitude coordinate.
    lat
        The given latitude coordinate.
    radius
        The given radius amount.

    Returns
    -------
    BBox
        The bounding box of the given coordinates and radius.
    """
    earth_radius = 6.371 * 10 ** 3
    dy = 360 * (radius / earth_radius)
    dx = dy * math_cos(deg2rad(long))
    return BBox([long - dx, lat - dy, long + dx, lat + dy], CRS.WGS84)

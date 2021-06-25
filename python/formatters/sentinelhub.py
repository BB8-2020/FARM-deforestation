"""Formats the locations dataset to the acrgis format."""
from re import split as re_split

import numpy as np
from pandas.core.frame import DataFrame
from scipy import stats

from python.helpers.formatter import format_locations


def dms_to_dd(degrees: str, minutes: str, seconds: str) -> float:
    """Format degrees minutes seconds to dd.

    Parameters
    ----------
    degrees
        The degrees of the dms format.
    minutes
        The minutes of the dms format.
    seconds
        The seconds of the dms format

    Returns
    -------
    dd
        The degree decimal representation of the degree minute second format.
    """
    dd = float(degrees) + (float(minutes) / 60) + (float(seconds[:-1]) / (60 * 60))
    return dd


def parse_dms(dms: str) -> float:
    """Format dms to dd.

    Parameters
    ----------
    dms
        The degrees minutes seconds format.

    Returns
    -------
    Union[float, np.nan]
        The degree decimal representation of the degree minute second format.
    """
    try:
        parts = re_split("[˚']+", dms)
        return dms_to_dd(*parts)
    except (TypeError, ValueError):
        return np.NaN


def df_filter(df: DataFrame) -> DataFrame:
    """Filter the dataframe to remove all the outliers.

    Parameters
    ----------
    df
        The given dataframe to apply this filter on.

    Returns
    -------
    DataFrame
        The filtered dataframe.
    """
    return df[(np.abs(stats.zscore(df)) < np.abs(stats.zscore(df)).mean()).all(axis=1)]


def format_arcgis():
    """Format the locations with the apostrophe and quotation marks filters to be in a format ideal for arcgis."""
    format_locations("arcgis", df_filter, parse_dms)


if __name__ == "__main__":
    format_arcgis()

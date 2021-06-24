"""Test functions to check if all formatters run correctly."""
from pandas import DataFrame
from pytest import approx

from python.formatters.arcgis import (
    apostrophe_filter,
    degree_filter,
    quotation_marks_filter,
)
from python.formatters.sentinelhub import df_filter, parse_dms


def test_arcgis():
    """Test condition to see if the arcgis formatters work correctly."""
    example = "21⁰58\"8.21363'"
    assert degree_filter(example) == "21˚58\"8.21363'"
    assert apostrophe_filter(example) == '21⁰58"8.21363"'
    assert quotation_marks_filter(example) == "21⁰58'8.21363'"
    assert (
        quotation_marks_filter(apostrophe_filter(degree_filter(example)))
        == "21˚58'8.21363\""
    )


def test_sentinelhub():
    """Test condition to see if the sentinelhub formatters work correctly."""
    #: HU building coordinates
    dd_longitude, dd_latitude = 52.0904346, 5.1200795
    dms_longitude, dms_latitude = "52˚5'25.56\"", "5˚7'12.29\""
    assert approx(parse_dms(dms_longitude)) == dd_longitude
    assert approx(parse_dms(dms_latitude)) == dd_latitude

    df = DataFrame({"P1_Longitude": [0, 1, 2, 10], "P1_Latitude": [0, 1, 2, 10]})
    assert df_filter(df).equals(
        DataFrame({"P1_Longitude": [0, 1, 2], "P1_Latitude": [0, 1, 2]})
    )

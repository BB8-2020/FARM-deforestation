"""Test functions to check if all formatters run correctly."""
from python.formatters.arcgis import (
    apostrophe_filter,
    degree_filter,
    quotation_marks_filter,
)
from python.formatters.sentinelhub import (
    apostrophe_quotation_filter,
    degree_filter_sentinelhub,
    dot_filter,
)


def test_arcgis():
    """Test condition to see if the arcgis formatter works correctly."""
    example = "21⁰58\"8.21363'"
    assert degree_filter(example) == "21˚58\"8.21363'"
    assert apostrophe_filter(example) == '21⁰58"8.21363"'
    assert quotation_marks_filter(example) == "21⁰58'8.21363'"
    assert (
        quotation_marks_filter(apostrophe_filter(degree_filter(example)))
        == "21˚58'8.21363\""
    )


def test_sentinelhub():
    """Test condition to see if the sentinelhub formatter works correctly."""
    example = "21⁰58\"8.21363'"
    assert dot_filter(example) == "21⁰58\"821363'"
    assert degree_filter_sentinelhub(example) == "21.58\"8.21363'"
    assert apostrophe_quotation_filter(example) == "21⁰588.21363"
    assert (
        apostrophe_quotation_filter(degree_filter_sentinelhub(dot_filter(example)))
        == "21.58821363"
    )

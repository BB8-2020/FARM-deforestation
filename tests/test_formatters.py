"""Test functions to check if all formatters run correctly."""
from python.formatters.arcgis import format_arcgis
from python.formatters.sentinelhub import format_sentinelhub
from python.helpers.pytest import not_raises


def test_arcgis():
    """Test condition to see if the arcgis formatter works correctly."""
    with not_raises(FileNotFoundError):
        format_arcgis("./")


def test_sentinelhub():
    """Test condition to see if the sentinelhub formatter works correctly."""
    with not_raises(FileNotFoundError):
        format_sentinelhub("./")

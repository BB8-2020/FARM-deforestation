"""Test functions to check if all formatters run correctly."""
from pytest import mark

from python.formatters.arcgis import format_arcgis
from python.formatters.sentinelhub import format_sentinelhub


@mark.xfail(raises=FileNotFoundError)
def test_arcgis():
    """Test condition to see if the arcgis formatter works correctly."""
    format_arcgis()


@mark.xfail(raises=FileNotFoundError)
def test_sentinelhub():
    """Test condition to see if the sentinelhub formatter works correctly."""
    format_sentinelhub()

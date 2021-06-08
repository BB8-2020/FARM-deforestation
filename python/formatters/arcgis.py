"""Formats the locations dataset to the arcgis format."""
from formatter import format_locations


def degree_filter(x):
    """Format to replace the degree symbol with another."""
    return x.replace("⁰", "˚")


def apostrophe_filter(x):
    """Format to have apostrophe be consistent."""
    if x[-1] == "'":
        return x[:-2] + '"' if x[-2] == "'" else x[:-1] + '"'
    return x


def quotation_marks_filter(x):
    """Format to have quotation marks be consistent."""
    if x[5] == '"':
        return x[:4] + "'" + x[6:]
    return x


def format_arcgis():
    """Format the locations with the apostrophe and quotation marks filters to be in a format ideal for arcgis."""
    format_locations("arcgis", degree_filter, apostrophe_filter, quotation_marks_filter)


if __name__ == "__main__":
    format_arcgis()

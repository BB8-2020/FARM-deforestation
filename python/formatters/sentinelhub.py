"""Formats the locations dataset to the sentinelhub format."""
from .formatter import format_locations


def dot_filter(x):
    """Format to replace the dots with nothing."""
    return x.replace(".", "")


def degree_filter(x):
    """Format to replace the degrees symbols with dots."""
    return x.replace("⁰", ".").replace("˚", ".")


def apostrophe_quotation_filter(x):
    """Format to replace quotation mark with nothings."""
    return x.replace("'", "").replace('"', "")


def last_symbol_filter(x):
    """Format to delete the last quotation mark."""
    return x[:-1]


def format_sentinelhub():
    """Format the locations with the given filtes to be in a format ideal for sentinelhub."""
    format_locations(
        "sentinelhub",
        dot_filter,
        degree_filter,
        apostrophe_quotation_filter,
        last_symbol_filter,
    )


if __name__ == "__main__":
    format_sentinelhub()

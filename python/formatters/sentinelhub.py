"""Formats the locations dataset to the sentinelhub format."""
from python.helpers.formatter import format_locations


def dot_filter(coords: str) -> str:
    """Format to replace the dots with nothing.

    Parameters
    ----------
    coords
        The coordinates in string form.

    Returns
    -------
    string
        The coords with the dot symbols removed.
    """
    return coords.replace(".", "")


def degree_filter(coords: str) -> str:
    """Format to replace the degrees symbols with dots.

    Parameters
    ----------
    coords
        The coordinates in string form.

    Returns
    -------
    string
        The coords with the degree symbols replaced with a dot.
    """
    return coords.replace("⁰", ".").replace("˚", ".")


def apostrophe_quotation_filter(coords: str) -> str:
    """Format to replace quotation mark with nothings.

    Parameters
    ----------
    coords
        The coordinates in string form.

    Returns
    -------
    string
        The coords with the apostrophe and quotation symbols removed.
    """
    return coords.replace("'", "").replace('"', "")


def last_symbol_filter(coords: str) -> str:
    """Format to delete the last symbol.

    Parameters
    ----------
    coords
        The coordinates in string form.

    Returns
    -------
    string
        The coords with the last symbol removed.
    """
    return coords[:-1]


def format_sentinelhub(relative_path: str = "../../"):
    """Format the locations with the given filtes to be in a format ideal for sentinelhub.

    Paramters
    ---------
    relative_path
        The relative path to read and write the xlsx files.
    """
    format_locations(
        "sentinelhub",
        relative_path,
        dot_filter,
        degree_filter,
        apostrophe_quotation_filter,
        last_symbol_filter,
    )


if __name__ == "__main__":
    format_sentinelhub()

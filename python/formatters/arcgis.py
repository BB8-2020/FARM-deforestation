"""Formats the locations dataset to the arcgis format."""
from python.helpers.formatter import format_locations


def degree_filter(coords: str) -> str:
    """Format to replace the degree symbol with another.

    Parameters
    ----------
    coords
        The coordinates in string form.

    Returns
    -------
    string
        The coords with consistent degree symbols.
    """
    return coords.replace("⁰", "˚")


def apostrophe_filter(coords: str) -> str:
    """Format to have apostrophe be consistent.

    Parameters
    ----------
    coords
        The coordinates in string form.

    Returns
    -------
    coords
        The coords with consistent apostrophe symbols.
    """
    if coords[-1] == "'":
        return coords[:-2] + '"' if coords[-2] == "'" else coords[:-1] + '"'
    return coords


def quotation_marks_filter(coords: str) -> str:
    """Format to have quotation marks be consistent.

    Paramters
    ---------
    coords
        The coordinates in string form.

    Returns
    -------
    coords
        The coords with consistent quotation marks symbols.
    """
    if coords[5] == '"':
        return coords[:5] + "'" + coords[6:]
    return coords


def format_arcgis(relative_path: str = "../../"):
    """Format the locations with the apostrophe and quotation marks filters to be in a format ideal for arcgis.

    Paramters
    ---------
    relative_path
        The relative path to read and write the xlsx files.
    """
    format_locations(
        "arcgis",
        relative_path,
        degree_filter,
        apostrophe_filter,
        quotation_marks_filter,
    )


if __name__ == "__main__":
    format_arcgis()

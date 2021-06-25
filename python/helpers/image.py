"""Helper for image operations."""
from os import listdir as os_listdir
from typing import Tuple

from numpy import ndarray as np_ndarray
from PIL import Image


def transparent(filename: str):
    """Change colors of photo mask.

    Parameters
    ----------
    filename
        name of file
    """
    img = Image.open("folium_test/data/mask_png/" + filename)
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    pngName = filename.split("_")
    pngYear = pngName[4][:4]
    for y in range(height):
        for x in range(width):
            pixdata[x, y] = convert_pixel(pixdata[x, y], pngYear)

    img.save("folium_test/data/x/" + filename, "PNG")


def convert_pixel(pixel: np_ndarray, png_year: str) -> Tuple[int, int, int, int]:
    """Convert a pixel to a color corresponding to the year layer.

    Parameters
    ----------
    pixel
        The current pixel of the image.
    png_year
        The current year of the image.

    Returns
    -------
    Tuple[int, int, int, int]
        The rgba values to return.
    """
    if pixel == (0, 0, 0, 255):
        return (255, 255, 255, 0)

    if png_year == "2017" and pixel == (255, 255, 255, 255):
        return (0, 245, 212, 255)
    elif png_year == "2018" and pixel == (255, 255, 255, 255):
        return (0, 187, 249, 255)
    elif png_year == "2019" and pixel == (255, 255, 255, 255):
        return (241, 91, 181, 255)

    return pixel


if __name__ == "__main__":
    for filename in os_listdir("folium_test/data/mask_png"):
        if filename.endswith(".png"):
            transparent(filename)

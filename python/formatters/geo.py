"""Formats the locations dataset to the geojson format."""
from typing import Any, List, Tuple

import cv2
import numpy as np
from geojson import Feature, FeatureCollection, Polygon, dump


def get_bounds() -> Tuple[float, float, float, float]:
    """Get the n, e, s and w extents and returning it.

    Returns
    -------
    bounds
        The longitude and latitude bounding box coordinates.
    """
    n_extent = 21.5439876
    e_extent = 87.118996
    s_extent = 21.5339876
    w_extent = 87.108996
    bounds = n_extent, e_extent, s_extent, w_extent
    return bounds


def load_image(file_path: str) -> Any:
    """Load the file path image grayscale it and convert it to a 4 channel rgba before returning it.

    Paramters
    ---------
    file_path
        The path to the file to open.

    Returns
    -------
    img
        The loaded image that has been processed.
    """
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    height, width, *_ = img.shape
    for y in range(height):
        for x in range(width):
            if (img[y, x] == [0, 0, 0, 255]).all():
                img[y, x] = [0, 0, 0, 0]
    return img


def trim_image(img: Any) -> Any:
    """Get the alpha channel and trim everything that is non zero.

    Paramters
    ---------
    img
        The image passed.

    Returns
    -------
    res
        The resolution.
    """
    alpha = img[..., 3]
    y_nonzero, x_nonzero = np.nonzero(alpha)
    res = alpha[
        np.min(y_nonzero) : np.max(y_nonzero), np.min(x_nonzero) : np.max(x_nonzero)
    ]
    _, res = cv2.threshold(res, 64, 255, cv2.THRESH_BINARY)
    return res


def get_approxes(img: Any, precision: float = 0.0001) -> List:
    """Get the approxes of the image by finding the contours and returning it.

    Paramters
    ---------
    img
        The image passed.
    precision
        The precision amount of finding edges.

    Returns
    -------
    approxes
        The approximation of the image shape.
    """
    contours, *_ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    approxes = []
    for contour in contours:
        perim = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, precision * perim, True)
        approxes.append(approx)
    return approxes


def format_geojson():
    """Format the input images to the geojson format."""
    #: Getting the bounds, loading and trimming the image.
    n_extent, e_extent, s_extent, w_extent = get_bounds()
    img = load_image("../data/masks/model/model.png")
    img = trim_image(img)

    #: Getting the width, height and deg per pixel in width and height.
    height, width = img.shape
    height_deg, width_deg = n_extent - s_extent, e_extent - w_extent
    deg_pp_height, deg_pp_width = height_deg / height, width_deg / width

    #: Looping trough the approxes and making polygons out of it.
    features = []
    approxes = get_approxes(img)
    for approx in approxes:
        points = []
        for i in range(approx.shape[0] + 1):
            x, y = approx[i % approx.shape[0], 0]
            lon = w_extent + x * deg_pp_width
            lat = n_extent - y * deg_pp_height
            points.append((lon, lat))
        features.append(
            Feature(geometry=Polygon([points]), properties={"key": "value"})
        )

    #: Making a FeatureCollection out of the featues before writing the result to a file.
    feature_col = FeatureCollection(features)
    with open("../data/masks/geojson/result.json", "w") as f:
        dump(feature_col, f)


if __name__ == "__main__":
    format_geojson()

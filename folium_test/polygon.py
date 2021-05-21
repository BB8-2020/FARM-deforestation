import cv2
import json
import geojson
import numpy as np
from geojson import Feature, Point, FeatureCollection, Polygon, dump
from numpy.core.fromnumeric import shape

img_path = 'folium_test/data/respone_t.png'
def getNESWextents(GeoJSONfile):

    # Load the enclosing rectangle JSON
    with open('folium_test/data/boundries.json', 'r') as datafile:
        data = json.load(datafile)
    feature_collection = FeatureCollection(data['features'])

    lats = []
    lons = []
    for feature in data['features'][0]['geometry']['coordinates'][0]:
        coords = feature
        lons.append(coords[0])
        lats.append(coords[1])

    # Work out N, E, S, W extents of boundaries
    Nextent = max(lats)
    Sextent = min(lats)
    Wextent = min(lons)
    Eextent = max(lons)
    print(lats, lons)
    return Nextent, Eextent, Sextent, Wextent

def loadAndTrimImage(imagefilename):
    """Loads the named image and trims it to the extent of its content"""
    # Open shape image and extract alpha channel
    im = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    print(shape(im))
    alpha = im[..., 3]
    # Find where non-zero, i.e. not black
    y_nonzero, x_nonzero = np.nonzero(alpha)
    # Crop to extent of non-black pixels and return
    res = alpha[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

    # Threshold to pure white on black
    _, res = cv2.threshold(res, 64, 255, cv2.THRESH_BINARY)
    return res

def getVertices(im):
    """Gets the vertices of the shape in im"""

    _, contours, *_ = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    # Should probably sort by contour area here - and take contour with largest area
    perim = cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], 0.01 * perim, True)

    print(f'DEBUG: Found shape with {approx.shape[0]} vertices')
    return approx

if __name__ == "__main__":

    # Get N, E, S, W extents from JSON file
    Nextent, Eextent, Sextent, Wextent = getNESWextents('boundaries.json')
    print(f'DEBUG: Nextent={Nextent}, Eextent={Eextent}, Sextent={Sextent}, Wextent={Wextent}')

    # Load the image and crop to contents
    im = loadAndTrimImage('shape.png')
    print('DEBUG: Trimmed image is "trimmed.png"')
    cv2.imwrite('folium_test/data/trimmed.png', im)

    # Get width and height in pixels
    Hpx, Wpx = im.shape
    # Get width and height in degrees
    Hdeg, Wdeg = Nextent-Sextent, Eextent-Wextent
    # Calculate degrees per pixel in East-West and North-South direction
    degppEW = Wdeg/Wpx
    degppNS = Hdeg/Hpx
    print(f'DEBUG: degppEW={degppEW}, degppNS={degppNS}')

    # Get vertices of shape and stuff into list of features
    features = []
    vertices = getVertices(im)
    for i in range(vertices.shape[0]):
       x, y = vertices[i,0]
       lon = Wextent + x*degppEW
       lat = Nextent - y*degppNS
       print(f'DEBUG: Vertex {i}: imageX={x}, imageY={y}, lon={lon}, lat={lat}')
       point = Point((lon,lat))
       features.append(Feature(geometry=point, properties={"key":"value"}))

    # Convert list of features into a FeatureCollection and write to disk
    featureCol = FeatureCollection(features)
    with open ('folium_test/data/result.json', 'w') as f:
        dump(featureCol, f)
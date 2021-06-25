import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import SentinelHubRequest, BBox, CRS, DataCollection, bbox_to_dimensions
from sentinelhub.constants import MimeType


def plot_image(image, factor=1/255, clip_range=(0, 1), **kwargs):
    """
    Utility function for plotting RGB images.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])


def send_request(evalscript, input_data, coords, config, save_data, data_folder='../data/images'):
    bbox = BBox(bbox=coords, crs=CRS.WGS84)
    request = SentinelHubRequest(data_folder=data_folder, evalscript=evalscript, input_data=input_data, bbox=bbox, config=config, size=[512, 512], responses=[SentinelHubRequest.output_response('default', MimeType.TIFF)])
    response = request.get_data(save_data=save_data)[0]
    return response

# def send_request_geojson(evalscript, input_data, coords, config, save_data, data_folder='../data/images'):
#     bbox = BBox(bbox=coords, crs=CRS.WGS84)
#     request = SentinelHubRequest(data_folder=data_folder, evalscript=evalscript, input_data=input_data, bbox=bbox, config=config, size=[512,512], responses=[SentinelHubRequest.output_response('default', MimeType.JSON)])
#     response = request.get_data(save_data=save_data)[0]
#     return response

simple_request = lambda eval_script, coords, config, save_data, **kwargs: send_request(
    eval_script, 
    [SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A, time_interval=('2018-01-01', '2019-01-01'), **kwargs)], 
    coords, config, save_data
)

# Function that sends a request for an satellite image of a scene and timestamp 
sentinel_request = lambda eval_script, coords, time_interval, config, save_data, data_folder, **kwargs: send_request(
    eval_script, 
    [SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A, time_interval=time_interval, **kwargs)],
    coords, config, save_data, data_folder
)
# Function that sends a request for an satellite image of a scene and timestamp and return the image in GeoJSON
request_geojson = lambda eval_script, coords, time_interval, config, save_data, data_folder, **kwargs: send_request_geojson(
    eval_script, 
    [SentinelHubRequest.input_data(data_collection=DataCollection.SENTINEL2_L2A, time_interval=time_interval, **kwargs)],
    coords, config, save_data, data_folder
)

import numpy as np
import matplotlib.pyplot as plt

from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest
from sentinelhub.constants import MimeType
import os

def export_images(coord, evalscipt, dir, time_start, time_end, cloud_percentage, config):
    """Sends a request for a satellite image and export it to given location"""

    #TODO : Deze kan functie voel ik kan ietsje korter.
    betsiboka_coords_wgs84 = coord
    resolution = 60
    betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
    betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

    request = SentinelHubRequest(
        data_folder = dir, 
        evalscript = evalscipt,
        input_data= [
            SentinelHubRequest.input_data(
                data_collection = DataCollection.SENTINEL2_L2A, 
                time_interval=(time_start, time_end),
                other_args={"dataFilter": {"maxCloudCoverage":0}}

            )
        ], 
        responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF)],
        bbox=betsiboka_bbox,
        size=betsiboka_size,
        config=config
    )
    request.save_data()  # export data to dir

    print(f'The output directory has been created and a tiff file with all 13 bands was saved into ' \
      'the following structure:\n')

    for folder, _, filenames in os.walk(request.data_folder):
        for filename in filenames:
            print(os.path.join(folder, filename))



    
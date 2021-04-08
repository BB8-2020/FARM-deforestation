import numpy as np
import matplotlib.pyplot as plt
from sentinelhub import SentinelHubRequest, bbox_to_dimensions

def plot_image(image, factor=1.0, clip_range = None, **kwargs):
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

def send_request(evalscript, input_data, responses, bbox, size, config):
    request = SentinelHubRequest(evalscript=evalscript, input_data=input_data, responses=responses, bbox=bbox, size=size, config=config)
    return request

def get_resolution(map_bbox, max_width=2500, max_height=2500, keep_aspect=True):
    normal_size = bbox_to_dimensions(map_bbox, resolution=1)
    max_width, max_height = max_width, max_height
    resolution = (normal_size[0] / max_width, normal_size[1] / max_height)
    return max(resolution) if keep_aspect else resolution 

def get_factor(mask_imgs, bias=3.5):
    array = np.asarray(mask_imgs)
    min_value, max_value = np.min(array), np.max(array)
    factor = (min_value + bias) / max_value
    return factor
import json
import folium
from folium import plugins
from folium.features import GeoJsonPopup
from folium.map import Tooltip
from folium.plugins import MiniMap, marker_cluster
from folium.plugins import Geocoder
from folium.plugins import Fullscreen
from folium.plugins import MarkerCluster
import os
import pandas as pd





##################################################################
####################### Initiate map #############################

# Zoom restrictions
min_lon, max_lon = 85, 92
min_lat, max_lat = 19, 29

m = folium.Map(
    # Starting point + Window size
    location=[21.5693, 87.1240],
    width=1000,
    height=600,

    # Tile settings
    tiles=None,
    control_scale=True,

    # Zoom settings
    zoom_start=11,
    min_zoom=6,
    max_bounds=True,
    # min_lat=min_lat,
    # max_lat=max_lat,
    # min_lon=min_lon,
    # max_lon=max_lon
    )



##################################################################
###################### Create markers ############################

tooltip = 'Click for more info'
marker_cluster = MarkerCluster()

csv_data = pd.read_csv('folium_test/data/coordinaten.csv', delimiter='\t', index_col=0)

for index, row in csv_data.iterrows():
    coords = [row['P1_Latitude'], row['P1_Longitude']]
    folium.Marker(coords, popup='<strong>Info</strong>',
    tooltip=tooltip,
    icon=folium.Icon(color='blue', icon='home', prefix='fa')).add_to(marker_cluster)



##################################################################
######################## GeoJSON #################################

# GeoJSON data
overlay1 = os.path.join('folium_test//data', 'mask.json')
overlay2 = os.path.join('folium_test//data', 'result.json')


# add .png to map
overlay3 = os.path.join('folium_test//data', 'respone_t.png')
m.add_child(folium.raster_layers.ImageOverlay(overlay3, opacity=0.8, bounds=[[21.443988, 87.018996], [21.643988, 87.218996]]))

# Create Polygon overlay with GeoJSON data
style1 = {'fillColor': '#228B22', 'color': '#228B22'}
style2 = {'fillColor': '#c21f1f', 'color': '#c21f1f'}

folium.GeoJson(overlay2, name='Woods cut (1990)', style_function=lambda x:style2).add_to(m)
folium.GeoJson(overlay1, name='Woods now', style_function=lambda x:style1).add_to(m)



##################################################################
#################### Add functionalities #########################

MiniMap(toggle_display=True).add_to(m)          # minimap

Geocoder(position='topleft').add_to(m)          # search bar

Fullscreen(position='topleft').add_to(m)        # fullscreen button

folium.LatLngPopup().add_to(m)                  # coordinates popup



##################################################################
######################## layer control ###########################

# Tile-sets
folium.TileLayer('https://api.mapbox.com/styles/v1/lucashu/cknsvax0z0o5q17plts71cl5i/tiles/256/{z}/{x}/{y}@2x?' \
                'access_token=pk.eyJ1IjoibHVjYXNodSIsImEiOiJja25wdXpyc2cwOGxjMzBwZml3aHMxYzlrIn0.' \
                'pqUrF-Xj7AJQX7RYFVMHDg', attr='Mapbox', name='Satellite').add_to(m)
folium.TileLayer('Open Street Map').add_to(m)

# Marker clusters
marker_cluster.add_to(m)

folium.LayerControl().add_to(m)



##################################################################
######################### Save map ###############################

m.save("folium_test//index.html")

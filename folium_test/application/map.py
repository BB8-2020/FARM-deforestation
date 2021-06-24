import json
import folium
from folium import plugins
from folium.features import GeoJsonPopup, VegaLite
from folium.map import Tooltip
from folium.plugins import MiniMap, marker_cluster
from folium.plugins import Geocoder
from folium.plugins import Fullscreen
from folium.plugins import MarkerCluster
from folium.plugins import FloatImage
import os
import pandas as pd
import altair
from area import area



##################################################################
####################### Initiate map #############################

# Zoom restrictions
min_lon, max_lon = 85, 92
min_lat, max_lat = 19, 29

m = folium.Map(
    # Starting point + Window size
    location=[21.7187, 87.1600],
    width=1400,
    height=730,

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

csv_data = pd.read_csv('folium_test/data/coordinaten_farms.csv', delimiter=',')

for index, row in csv_data.iterrows():
    coords = [row['Latitude'], row['Longitude']]
    html = '<p style="font-family:verdana">Farmer Information<br><br>Name: name</p>'
    iframe = folium.IFrame(html)
    popup = folium.Popup(iframe, min_width=200, max_width=200)
    folium.Marker(coords, popup=popup,
    tooltip=tooltip,
    icon=folium.Icon(color='blue', icon='home', prefix='fa')).add_to(marker_cluster)



##################################################################
######################## GeoJSON #################################


# Create Polygon overlay with GeoJSON data



# # # folium.GeoJson(overlay2, name='Woods cut (1990)', style_function=lambda x:style2).add_to(m)
# # # add geojson shape with popup with area data to map
# total_m2 = 25000000
# geo_txt = f'{str(round(total, 2))} m/2 ---- {round(total / total_m2 * 100, 1)}% covered'
# geo_popup = folium.Popup(geo_txt, min_width=100, max_width=200)
# folium.GeoJson(overlay2, name='Stats', style_function=lambda x:style1).add_child(geo_popup).add_to(m)
# folium.GeoJson(overlay2, name='Woods now', style_function=lambda x:style1).add_to(m)

stat_layer = folium.FeatureGroup(name="stats", show=False)

def writeJson(filename, nw, ne, se, sw):
    """
    """
    json_dict = {
            "type": "FeatureCollection",
            "features": [
                {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            sw,
                            se,
                            ne,
                            nw,
                            sw
                        ]
                    ]
                    
                    
                    
                    }}]}
    
    with open('folium_test/data/stat_overlay/' + filename + '.json', 'w') as write:
        json.dump(json_dict, write)


def clac_area(filename):

    total_m2 = 25000000
    f = open('folium_test/data/result_geojson/' + filename,)
    geojson_data = json.load(f)
    total_area = 0
    for shape in geojson_data['features']:
        total_area += area(shape['geometry'])
    
    percentage_coverage = total_area / total_m2 * 100
    return (round(total_area, 2), round(percentage_coverage, 2))


def geoshape():
    """
    """
    checked = []
    stat_dict = {}
    for filename in os.listdir("folium_test/data/result_geojson"):
        if filename.endswith(".json"):
            pngName = filename.split("_")
            pngName_list = [float(x) for x in pngName[:4]]
            pngName = ' '.join(str(e) for e in pngName_list)

            if pngName not in checked:
                checked.append(pngName)
                stat_dict[pngName] = []
                lats, lons = [pngName_list[1], pngName_list[3]], [pngName_list[0], pngName_list[2]]
                nw, ne, se, sw = [min(lons), max(lats)], [max(lons), max(lats)], [max(lons), min(lats)], [min(lons), min(lats)]
                writeJson(filename, nw, ne, se, sw)
            
            area_data = clac_area(filename)
            stat_dict[pngName].append(area_data)

        else:
            continue
    
    return stat_dict


def makeGraph(data):

    df = pd.DataFrame(data, columns=['km/2', '% of area covered in woods'])
    df['Year'] = ['2017', '2018', '2019']
    alt_chart = altair.Chart(df).mark_bar().encode(
        x='Year',
        y='% of area covered in woods'
    )
    return alt_chart

def choseStyle(overlay, data):


    style1 = {'fillColor': '#33DB05', 'color': '#33DB05'} # bebossing
    style2 = {'fillColor': '#E1FF00', 'color': '#E1FF00'} # weinig ontbossing
    style3 = {'fillColor': '#FFE300', 'color': '#FFE300'}
    style4 = {'fillColor': '#FF9E00', 'color': '#FF9E00'}
    style5 = {'fillColor': '#FF2A00', 'color': '#FF2A00'} # meeste ontbossing

    span  = len(data)
    differences = []
    for x in range(0, span - 1):
        differences.append(data[x + 1][1] - data[x][1])
    

    res = max(differences, key=abs)
    # print(res)

    graph = makeGraph(data)

    vega = folium.features.VegaLite(graph)
    geo_popup = folium.Popup(min_width=100, max_width=200)
    vega.add_to(geo_popup)

    if res >= 0:
        stat_layer.add_child(folium.GeoJson(overlay, style_function=lambda x:style1).add_child(geo_popup))
    elif res > -5:
        stat_layer.add_child(folium.GeoJson(overlay, style_function=lambda x:style2).add_child(geo_popup))
    elif res > -10:
        stat_layer.add_child(folium.GeoJson(overlay, style_function=lambda x:style3).add_child(geo_popup))
    elif res > -15:
        stat_layer.add_child(folium.GeoJson(overlay, style_function=lambda x:style4).add_child(geo_popup))
    else:
        stat_layer.add_child(folium.GeoJson(overlay, style_function=lambda x:style5).add_child(geo_popup))

wc_data = geoshape()

for geoFile, key in zip(os.listdir("folium_test/data/stat_overlay"), wc_data):
    if geoFile.endswith(".json"):
        geoOverlay = os.path.join('folium_test//data//stat_overlay', geoFile)
        file_data = wc_data[key]
        choseStyle(geoOverlay, file_data)
        

m.add_child(stat_layer)


layer_2017 = folium.FeatureGroup(name="2018")
layer_2018 = folium.FeatureGroup(name="2019")
layer_2019 = folium.FeatureGroup(name="2020")


files = os.listdir("folium_test/data/x")
for filename, nr in zip(files, range(0, len(files))):
    if filename.endswith(".png"):
        pngName = filename.split("_")
        pngYear = pngName[4][:4]
        pngName = [float(x) for x in pngName[:4]]

        pngOverlay = os.path.join('folium_test//data//x', filename)

        if pngYear == "2017":
            layer_2017.add_child(folium.raster_layers.ImageOverlay(pngOverlay, opacity=0.8, bounds=[[pngName[1], pngName[0]], [pngName[3], pngName[2]]]))
        elif pngYear == "2018":
            layer_2018.add_child(folium.raster_layers.ImageOverlay(pngOverlay, opacity=0.8, bounds=[[pngName[1], pngName[0]], [pngName[3], pngName[2]]]))
        elif pngYear == "2019":
            layer_2019.add_child(folium.raster_layers.ImageOverlay(pngOverlay, opacity=0.8, bounds=[[pngName[1], pngName[0]], [pngName[3], pngName[2]]]))
    else:
        continue

m.add_child(layer_2017)
m.add_child(layer_2018)
m.add_child(layer_2019)





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

legend_1 = "https://i.ibb.co/jrpwXz1/legend1.png"
legend_2 = "https://i.ibb.co/J7mHDvx/untitled.png"
FloatImage(legend_1, bottom=5, left=1).add_to(m)
FloatImage(legend_2, bottom=30, left=1).add_to(m)
##################################################################
######################### Save map ###############################

m.save("folium_test//application//index.html")

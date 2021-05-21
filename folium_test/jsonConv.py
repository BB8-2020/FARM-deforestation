import json
import pandas as pd

def convert():
    result = []
    with open('folium_test/data/result.json') as f:
        data = json.load(f)

        for i in data['features']:
            result.append(i['geometry']['coordinates'])
    
    result_ = result[0:100]
    json_ = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
            [

            ]
        ]
        
        
        
        }}]}

    for x in result_:
        json_['features'][0]['geometry']['coordinates'][0].append(x)
    # print(json_)
    with open('folium_test/data/result2.json', 'w') as write:
        json.dump(json_, write)

# with open('folium_test/data/coordinaten.csv') as csv_file:
#     csv_data = csv.reader(csv_file, delimiter='\t')
#     farm_coords = []
#     for row in csv_data:
#         row = [int(x) for x in row]
#         farm_coords.append(row[1:])

csv_data = pd.read_csv('folium_test/data/coordinaten.csv', delimiter='\t', index_col=0)
print(csv_data)
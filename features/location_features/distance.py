import pandas as pd
import numpy as np
import geopy.distance

data = pd.read_csv("data/McDonald_s_Reviews.csv", encoding='latin-1')

nrows = data.shape[0]

latitudes = data["latitude "]
longitudes = data["longitude"]

unique_coordinates = []
for i in range(nrows):
    lat = latitudes[i]
    lon = longitudes[i]

    if np.isnan(lat) or np.isnan(lon):
        pass
    else:
        coord = (lat, lon)

        if coord not in unique_coordinates:
            unique_coordinates.append(coord)

md_locations_all = pd.read_csv('data/lat_lon.csv')
sw_locations_all = pd.read_csv('data/subway.csv')

n_md_locations = md_locations_all.shape[0]
n_sw_locations = sw_locations_all.shape[0]

md_under5 = []
md_under20 = []
sw_under5 = []
sw_under20 = []

for uc in unique_coordinates:
    md_temp5 = []
    md_temp20= []
    for i in range(n_md_locations):
        coord1 = (md_locations_all["Latitude"][i], md_locations_all["Longitude"][i])
        md_dis = geopy.distance.geodesic(uc, coord1)

        if md_dis < 5:
            md_temp5.append(md_dis)
        if md_dis < 20:
            md_temp20.append(md_dis)

    md_under5.append(len(md_temp5) - 1)        
    md_under20.append(len(md_temp20) - 1)

    sw_temp5 = []
    sw_temp20= []
    for j in range(n_sw_locations):
        coord2 = (sw_locations_all["latitude"][j], sw_locations_all["longitude"][j])
        sw_dis = geopy.distance.geodesic(uc, coord2)

        if sw_dis < 5:
            sw_temp5.append(md_dis)
        if sw_dis < 20:
            sw_temp20.append(md_dis)

    sw_under5.append(len(sw_temp5) - 1)        
    sw_under20.append(len(sw_temp20) - 1)

result = pd.DataFrame()
result["coord"] = unique_coordinates
result["mcdonalds5"] = md_under5
result["mcdonalds20"] = md_under20
result["subway5"] = sw_under5
result["subway20"] = sw_under20

result.to_csv('data/neighbors.csv', index=False)


  
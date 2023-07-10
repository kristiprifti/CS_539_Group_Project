import json
import csv

# Load GeoJSON file
with open('data/raw.githubusercontent.com_gavinr_usa-mcdonalds-locations_master_mcdonalds.geojson') as f:
    data = json.load(f)

# Extract latitude and longitude and write to CSV
with open('data/lat_lon.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Latitude', 'Longitude'])  # Write header

    for feature in data['features']:
        coordinates = feature['geometry']['coordinates']
        longitude, latitude = coordinates  # GeoJSON stores coordinates in [longitude, latitude] order
        writer.writerow([latitude, longitude])  # Write latitude and longitude to CSV

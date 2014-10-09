from geopy.geocoders import GoogleV3
import csv
import re
import time

## import data
data = []
with open('crime_incidents_2013_CSV.csv', 'rb') as csvfile:
    creader = csv.reader(csvfile)
    for row in creader:
        data.append(row)

## filter to only include data with METHOD = 'GUN'
gun_data = []
for d in data:
    if d[4] == 'GUN':
        gun_data.append(d)
gdl = len(gun_data)
print gdl
## Geolocate.  Nominatim, the OSM geocoder, had been a little frustrating so I switched to Google like a rube.
## Note that you are 'supposed to send an API key' and this 'may result in a temporary IP ban'
## https://developers.google.com/maps/documentation/geocoding/#api_key for details

geolocator = GoogleV3()

location_data = []

for i,d in enumerate(gun_data):
    if re.search('BLOCK OF',d[6]):
        s = d[6].split("-")[1].replace(" BLOCK OF","") + ', Washington, DC'
    else:
        s = d[6] + ', Washington, DC'
    try:
        location = geolocator.geocode(s)
        print(location.latitude, location.longitude, i/float(gdl))
        row = []
        for el in d:
            row.append(el)
        row.append(location.latitude)
        row.append(location.longitude)
    except:
        print("ERROR", i/float(gdl))
        row = []
        for el in d:
            row.append(el)
        row.append(0)
        row.append(0)
    location_data.append(row)
    time.sleep(0.2) # delays for 0.2 seconds to prevent API bans

## write it out

with open('gun_data_location.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    header = data[0]
    header.append('lat')
    header.append('lon')
    a.writerow(header)
    a.writerows(location_data)

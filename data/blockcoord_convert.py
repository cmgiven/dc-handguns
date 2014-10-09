import csv
import re
import time
import urllib
import urllib2
from bs4 import BeautifulSoup

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

location_data = []

url = "http://citizenatlas.dc.gov/usng/getusng.asmx/MD_SPCStoLL"

for i,d in enumerate(gun_data):
    try:
        value = d[7] + ',' + d[8]
        params = {'SPCSXYSTR': value}
        en_params = urllib.urlencode(params)
        req = urllib2.Request(url,en_params)
        response = urllib2.urlopen(req)
        the_page = response.read()
        soup = BeautifulSoup(the_page)
        cs = soup.find('convstr')
        row = []
        for el in d:
            row.append(el)
        row.append(cs.text.split(',')[0])
        row.append(cs.text.split(',')[1])
        print(cs.text)
        location_data.append(row)
    except:
        print("ERROR")
## write it out

with open('gun_data_location.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    header = []
    for d in data[0]:
        header.append(d)
    header.append('lat')
    header.append('lon')
    a.writerow(header)
    a.writerows(location_data)

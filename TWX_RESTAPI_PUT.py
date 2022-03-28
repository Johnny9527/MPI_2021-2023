import requests
import json

url =  'https://mpiuktw01.mpiuk.com:8443/Thingworx'
header = {'Content-Type': 'application/json', 'appKey': 'f307c5ef-9022-4aae-ae62-ce55dedbfdc9'}

main = {'testVariable': '43'}

response = requests.put(url + '/Things/APItestThing/Properties/*', headers=header, json=main, verify='C:\SSLcertificate\mpiuktw01.mpiuk.com\gd_bundle-g2-g1.crt')

print(response.status_code)

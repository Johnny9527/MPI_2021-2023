import requests
import json

# ThingWorx API - GET
url =  'https://mpiuktw01.mpiuk.com:8443/Thingworx'
header = {'Accept': 'application/json', 'appKey': 'f307c5ef-9022-4aae-ae62-ce55dedbfdc9'}

response = requests.get(url + '/Things/APItestThing/Properties/testVariable', headers=header, verify=False)

print(response.status_code)
print(response.text)

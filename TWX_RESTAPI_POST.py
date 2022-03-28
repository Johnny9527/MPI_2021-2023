import requests
import json

url = 'https://mpiuktw01.mpiuk.com:8443/Thingworx'

header = {'Content-Type': 'application/json', 'appKey': 'f680a2c3-6cef-43d2-96ef-2a9294603f0e'}

# Add multiple new property into specific Thing.
addMultipleProperty = {"name": "test99", "description": "POST by RESTAPI_appkey", "type": "NUMBER", "persistent": "True", "defaultValue": "100"}

response = requests.post(url + '/Things/APItestThing/Services/AddPropertyDefinitions', headers=header, data=addMultipleProperty, verify=False)

print(response.status_code)
print(response.text)

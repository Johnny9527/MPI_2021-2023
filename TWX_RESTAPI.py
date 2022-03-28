# -*- coding: utf-8 -*-
"""
Created on Wed May 26 14:31:39 2021

@author: chris.paterson
"""

import requests
import json

url =  'https://mpiuktw01.mpiuk.com:8443/Thingworx'
header = {'Accept': 'application/json', 'appKey': 'f307c5ef-9022-4aae-ae62-ce55dedbfdc9'}

response = requests.get(url + '/Things/APItestThing/Properties/testVariable', headers=header, verify=False)

print(response.status_code)
print(response.text)
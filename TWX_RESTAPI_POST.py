# -*- coding: utf-8 -*-
"""
@author: johnny.lee
"""
import requests
import json

url = 'https://mpiuktw01.mpiuk.com:8443/Thingworx'

header = {'Content-Type': 'application/json', 'appKey': 'f680a2c3-6cef-43d2-96ef-2a9294603f0e'}

# Create new Thing.
# addNewThing = {'name': 'NewThing_1',
#                'description': 'Create by code',
#                'thingTemplateName': 'GenericThing'}
#
# response = requests.put(url + '/Resources/EntityServices/Services/CreateThing', headers=header, json=addNewThing, verify=False)

# Add new property into specific Thing.
addNewProperty = {'name': 'test2',
                  'description': 'POST from code',
                  'type': 'NUMBER',
                  'persistent': 'True',
                  'defaultValue': '999'}

response = requests.put(url + '/Things/APItestThing/Services/AddPropertyDefinition', headers=header, json=addNewProperty, verify=False)

print(response.status_code)
print(response.text)

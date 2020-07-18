from __future__ import print_function
import json
import requests
from config import SCOPE
import sys
import json
import util
__author__ = 'Barry Yuan <bayuan@cisco.com>'

util.get_token()

response = util.get_url("dna/intent/api/v1/network-device")
#print(json.dumps(response, indent=2)) 

print ("Parsing device list...") 

devicelist = {'list': []}
for dev in response['response']:
    if dev['series'] in SCOPE:
        if dev['managementIpAddress'].lower() != dev['hostname'].lower():
            print("Found new device, collecting information...")
            devicelist['list'].append(dev)

data = "\n".join([ "{}:\t{}".format(dev['managementIpAddress'],dev['series']) 
                  for dev in devicelist['list']])
util.sep("Parsing complete, here is a list of devices that needs updated, please confirm...")
print (data)

if util.confirm() == "y":
    print ("Confirmed, updating devices...")
    for dev in devicelist['list']:
        util.update_device(dev['managementIpAddress'], dev['hostname'].lower())

    util.sep("Task completed, exiting...")
else:
    util.sep("Task canceled, exiting...")

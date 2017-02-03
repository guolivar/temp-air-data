# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 10:21:30 2017

@author: roycdavies

"""

# ----------------------------------------------------------------------------------------------------
# Import modules
# ----------------------------------------------------------------------------------------------------
import requests
import json
import random
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------
settings_file = './.agent.conf'
# ----------------------------------------------------------------------------------------------------
# Read Setup Info
# ----------------------------------------------------------------------------------------------------
# Open the settings file
settings_file = open(settings_file)
# Read the authurl
settings_line = settings_file.readline().rstrip('\n').split(',')
authurl = settings_line[1]
# Read the apiurl
settings_line = settings_file.readline().rstrip('\n').split(',')
apiurl = settings_line[1]
# Read the sessionid
settings_line = settings_file.readline().rstrip('\n').split(',')
sessionid = settings_line[1]
# Read the treeID
settings_line = settings_file.readline().rstrip('\n').split(',')
treeID = settings_line[1]
# Read the geohash
settings_line = settings_file.readline().rstrip('\n').split(',')
geohash = settings_line[1]
# Read the Email
settings_line = settings_file.readline().rstrip('\n').split(',')
email = settings_line[1]
# Read the Password
settings_line = settings_file.readline().rstrip('\n').split(',')
pwd = settings_line[1]
# Close the settings file
settings_file.close()
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Log into the Imersia API
# ----------------------------------------------------------------------------------------------------
def ImersiaLogin ():
    payload = {'Email': email, 'Password': pwd}
    req = requests.post(authurl, data=payload)

    returndata = json.loads(req.text)
    if (returndata["Success"]):
        return returndata["Token"]
    else:
        return ""
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Send a command to the Imersia API
# ----------------------------------------------------------------------------------------------------
def SendCommand (command, parameters):
    query = json.dumps(parameters)
    headers = {'sessionid' : sessionid, 'user' : email, 'developerid' : 'tempproject'}
    req = requests.post(apiurl + command + '?' + query, headers=headers)
    return (req.text)
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Main Function
# ----------------------------------------------------------------------------------------------------
sessionid = ImersiaLogin ()

if (sessionid == ""):
    print ("Error logging in")
else:
    print ("Logged in - sessionid is : " + sessionid)

    # Post a value to set the water level (0 to 10) and trigger the devices watching
    result = SendCommand ('agent/metadata/setvalue', {'agentid': treeID, 'key': 'waterlevel', 'value': random.randint(0,10)})
    print (result)

    # Post a value to set the pollution level (0 to 5) and trigger the devices watching
    result = SendCommand ('agent/metadata/setvalue', {'agentid': treeID, 'key': 'pollutionlevel', 'value': random.randint(0,5)})
    print (result)

    # Post a value to set the windspeed level (0 to 10) and trigger the devices watching
    result = SendCommand ('agent/metadata/setvalue', {'agentid': treeID, 'key': 'windspeed', 'value': random.randint(0,10)})
    print (result)

    # Post a value to set the particlespeed level (0 to 10) and trigger the devices watching
    result = SendCommand ('agent/metadata/setvalue', {'agentid': treeID, 'key': 'particlespeed', 'value': random.randint(0,10)})
    print (result)

    # Send an event to the analytics system to mark this update
    result = SendCommand ('agent/analytics/log', {'agentid': treeID, 'geohash' : geohash, 'event': 'valuesupdated'})
    print (result)

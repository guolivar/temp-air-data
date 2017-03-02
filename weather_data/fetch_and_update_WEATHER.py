'''
    Fetch weather data from Open Weather Map and update Imersia's agent
OpenWeatherMap:
http://api.openweathermap.org/data/2.5/weather?id=<CityID>&<API_Key>
'''
# Import modules

import requests
import json
import time
import random
import math

# Start timer
start_time = time.time()
# Auxiliary functions
# ----------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------
settings_file = '../.agent_config'
owm_address = 'http://api.openweathermap.org/data/2.5/weather?id='
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
# Read the OpenWeatherMap key
settings_line = settings_file.readline().rstrip('\n').split(',')
owm_key = settings_line[1]
# Read the CityID to fetch from OWM
settings_line = settings_file.readline().rstrip('\n').split(',')
cityID = settings_line[1]
# Thingspeak address
settings_line = settings_file.readline().rstrip('\n').split(',')
thingspk = settings_line[1]
# Thingspeak channel
settings_line = settings_file.readline().rstrip('\n').split(',')
channel = settings_line[1]
# Thinkgspeak readkey
settings_line = settings_file.readline().rstrip('\n').split(',')
readkey = settings_line[1]
# Thinkgspeak writekey
settings_line = settings_file.readline().rstrip('\n').split(',')
writekey = settings_line[1]

# Close the settings file
settings_file.close()
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Log into the Imersia API
# ----------------------------------------------------------------------------------------------------


def ImersiaLogin():
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


def SendCommand(command, parameters):
    query = json.dumps(parameters)
    headers = {'sessionid': sessionid,
               'user': email, 'developerid': 'tempproject'}
    req = requests.post(apiurl + command + '?' + query, headers=headers)
    return (req.text)
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Main programme
# ----------------------------------------------------------------------------------------------------

# Build full address
owm_query = owm_address + cityID + '&APPID=' + owm_key
print(owm_query)
weather_data = requests.get(owm_query).json()
wsp = weather_data["wind"]["speed"]
rh = weather_data["main"]["humidity"]
print(weather_data)
print(weather_data["wind"]["speed"])
print(weather_data["main"]["humidity"])

# Log in to Imersia's sytem
sessionid = ImersiaLogin()
# Push data within the 10 minute interval
for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
    # Extract pm10 and no2 from a wide normal distribution
    noisy_wsp = random.lognormvariate(math.log(wsp), 0.1)
    noisy_rh = random.lognormvariate(math.log(rh), 0.1)
    level_wsp = min(round(10 * (max(0,noisy_wsp) / 5)),10)
    level_rh = min(round(10 * (max(0,noisy_rh-50) / 100)),10)
    print("Wind Speed level ",level_wsp)
    print("RH level ",level_rh)
    # Post a value to set the water level (0 to 10) and trigger the devices watching
    result = SendCommand ('agent/metadata/setvalue', {'agentid': treeID, 'key': 'waterlevel', 'value': level_rh})
    # Post a value to set the windspeed level (0 to 10) and trigger the devices watching
    result = SendCommand ('agent/metadata/setvalue', {'agentid': treeID, 'key': 'windspeed', 'value': level_wsp})
    time.sleep(50)
# Update thingspeak channel
options = {'api_key':writekey,'field3':wsp,'field4':rh}
req = requests.post(thingspk,data=options)
print(req)

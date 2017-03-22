'''
    Fetch air quality data from LAWA and update Imersia's agent
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
# AQICN API key
settings_line = settings_file.readline().rstrip('\n').split(',')
aqicnkey = settings_line[1]


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

#    Sites URLs
urlTakapuna = 'https://api.waqi.info/feed/new-zealand/auckland/takapuna/?token='
urlPenrose = 'https://api.waqi.info/feed/new-zealand/auckland/penrose/?token='
urlHenderson = 'https://api.waqi.info/feed/new-zealand/auckland/henderson/?token='
urlGlenEden = 'https://api.waqi.info/feed/new-zealand/auckland/glen-eden/?token='
urlPakuranga = 'https://api.waqi.info/feed/new-zealand/auckland/pakuranga/?token='
urlPotumahoe = 'https://api.waqi.info/feed/new-zealand/auckland/patumahoe/?token='
# Fetch the data
glen = requests.get(urlGlenEden + aqicnkey).json()
hend = requests.get(urlHenderson + aqicnkey).json()
paku = requests.get(urlPakuranga + aqicnkey).json()
penr = requests.get(urlPenrose + aqicnkey).json()
patu = requests.get(urlPotumahoe + aqicnkey).json()
taka = requests.get(urlTakapuna + aqicnkey).json()

# Get PM10 values
try:
    pm10_glen_value = glen["data"]["iaqi"]['pm10']['v']
except:
    pm10_glen_value = None
try:
    pm10_hend_value = hend["data"]["iaqi"]['pm10']['v']
except:
    pm10_hend_value = None
try:
    pm10_paku_value = paku["data"]["iaqi"]['pm10']['v']
except:
    pm10_paku_value = None
try:
    pm10_penr_value = penr["data"]["iaqi"]['pm10']['v']
except:
    pm10_penr_value = None
try:
    pm10_patu_value = patu["data"]["iaqi"]['pm10']['v']
except:
    pm10_patu_value = None
try:
    pm10_taka_value = taka["data"]["iaqi"]['pm10']['v']
except:
    pm10_taka_value = None

# Calculate the maximnum value
pm10 = max(pm10_penr_value,
             pm10_patu_value,
             pm10_hend_value,
             pm10_paku_value,
             pm10_taka_value,
             pm10_penr_value,
             1)

# Get NO2 data
try:
    no2_glen_value = glen["data"]["iaqi"]['no2']['v']
except:
    no2_glen_value = None
try:
    no2_hend_value = hend["data"]["iaqi"]['no2']['v']
except:
    no2_hend_value = None
try:
    no2_penr_value = penr["data"]["iaqi"]['no2']['v']
except:
    no2_penr_value = None
try:
    no2_patu_value = patu["data"]["iaqi"]['no2']['v']
except:
    no2_patu_value = None
try:
    no2_taka_value = taka["data"]["iaqi"]['no2']['v']
except:
    no2_taka_value = None

# Calculate the maximnum value
no2 = max(no2_penr_value,
            no2_patu_value,
            no2_hend_value,
            no2_taka_value,
            no2_glen_value,
            1)

# The data is only updated hourly so to fill up the time
# add a loop to update the agent with some noise over the data
print("Date ", glen["data"]['time']['s'])
print("PM10 ", pm10)
print("NO2 ", no2)
# Log in to Imersia's sytem
sessionid = ImersiaLogin()

# Push data within the minute
for i in (1, 2, 3, 4, 5):
    # Extract pm10 and no2 from a wide normal distribution
    noisy_pm10 = random.lognormvariate(math.log(pm10), 0.1)
    noisy_no2 = random.lognormvariate(math.log(no2), 0.1)
    level_pm10 = min(round(10 * (max(0, noisy_pm10 - 5) / 50)), 10)
    level_no2 = min(round(5 * (max(0, noisy_no2 - 0) / 20)), 5)
    print("NO2 level ", level_no2)
    print("PM10 level ", level_pm10)
    # Update the pollution
    # Post a value to set the pollution level (0 to 5) and trigger the devices
    # watching
    result = SendCommand('agent/metadata/setvalue',
                         {'agentid': treeID, 'key': 'pollutionlevel', 'value': level_no2})
    # Update the particles
    # Post a value to set the particlespeed level (0 to 10) and trigger the
    # devices watching
    result = SendCommand('agent/metadata/setvalue',
                         {'agentid': treeID, 'key': 'particlespeed', 'value': level_pm10})
    time.sleep(8)
print("--- %s seconds ---" % (time.time() - start_time))
# Update thingspeak channel
options = {'api_key': writekey, 'field1': pm10, 'field2': no2}
req = requests.post(thingspk, data=options)
print(req)

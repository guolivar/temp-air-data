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

'''
    Sites URLs
    Takapuna:   https://api.waqi.info/feed/new-zealand/auckland/takapuna/?token=
    Penrose:    https://api.waqi.info/feed/new-zealand/auckland/penrose/?token=
    Henderson:  https://api.waqi.info/feed/new-zealand/auckland/henderson/?token=
    Glen Eden:  https://api.waqi.info/feed/new-zealand/auckland/glen-eden/?token=
    Pakuranga:  https://api.waqi.info/feed/new-zealand/auckland/pakuranga/?token=
    Potumahoe:  https://api.waqi.info/feed/new-zealand/auckland/patumahoe/?token=
'''
# Fetch the data for PM10
pm10_glen = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_hend = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=5&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_paku = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=1&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_penr = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=7&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_patu = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=2&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_taka = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=23&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()

# Calculate the maximnum value
pm10 = max(pm10_glen["NumericValue"],
           pm10_hend["NumericValue"],
           pm10_paku["NumericValue"],
           pm10_penr["NumericValue"],
           pm10_patu["NumericValue"],
           pm10_taka["NumericValue"])

# Fetch the data for NO2
no2_glen = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_hend = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=5&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_quee = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=9&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_penr = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=7&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_taka = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=23&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_patu = requests.get(
    'https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=2&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()

# Calculate the maximnum value
no2 = max(no2_glen["NumericValue"],
          no2_hend["NumericValue"],
          no2_quee["NumericValue"],
          no2_penr["NumericValue"],
          no2_patu["NumericValue"],
          no2_taka["NumericValue"])

# The data from LAWA is only updated hourly so to fill up the time
# so, add a loop to update the agent with some noise over the data
print("Date ",pm10_glen["DateTime"])
print("PM10 ", pm10)
print("NO2 ", no2)
# Log in to Imersia's sytem
sessionid = ImersiaLogin()

# Push data within the minute
for i in (1, 2, 3, 4, 5):
    # Extract pm10 and no2 from a wide normal distribution
    noisy_pm10 = random.lognormvariate(math.log(pm10), 0.1)
    noisy_no2 = random.lognormvariate(math.log(no2), 0.1)
    level_pm10 = min(round(10 * (max(0,noisy_pm10-10) / 90)),10)
    level_no2 = min(round(5 * (max(0,noisy_no2-20) / 60)),5)
    print("NO2 level ",level_no2)
    print("PM10 level ",level_pm10)
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
options = {'api_key':writekey,'field1':pm10,'field2':no2}
req = requests.post(thingspk,data=options)
print(req)

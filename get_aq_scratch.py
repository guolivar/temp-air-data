import requests

'''
    Sites ID
    Glen Eden:  67 (pm10, no2)
    Queen St:   9 (no2)
    Henderson: 5 (pm10, no2)
    Pakuranga:  1 (pm10)
    Penrose:    7 (pm10, no2, so2)
    Patumahoe:   2 (pm10, no2)
    Takapuna:   23 (pm10, no2)
'''

pm10 = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
no2 = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=9&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()

print("Date",pm10["Date"])
print("Time",pm10["Time"])
print("PM10 - Glen Eden",pm10["NumericValue"])
print("NO2 - Queen Street",no2["NumericValue"])
print("ERROR",pm10["HasError"])

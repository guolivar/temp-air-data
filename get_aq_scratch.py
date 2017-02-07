import requests
r = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly')
parsed=r.json()
print("PM10",parsed["NumericValue"])
print("Date",parsed["DateTime"])
print("ERROR",parsed["HasError"])

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

pm10_glen = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_hend = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=5&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_paku = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=1&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_penr = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=7&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_patu = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=2&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()
pm10_taka = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=23&indicator=pm10&timeIntervalText=Hours&timescaleText=Hourly').json()

no2_ge = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_ge = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_ge = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_ge = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()
no2_ge = requests.get('https://www.lawa.org.nz/umbraco/api/airservice/getLatestSample?baseUrlPageId=34260&featureOfInterest=67&indicator=no2&timeIntervalText=Hours&timescaleText=Hourly').json()





print("Glen Eden",pm10_ge["DateTime"])
print("Queen St",no2_ge["DateTime"])
print("Henderson",pm10_hend["DateTime"])
print("Henderson",pm10_hend["DateTime"])
print("Henderson",pm10_hend["DateTime"])
print("Henderson",pm10_hend["DateTime"])
print("Henderson",pm10_hend["DateTime"])





print("PM10 - Glen Eden",pm10_ge["NumericValue"])
print("NO2 - Queen Street",no2_ge["NumericValue"])
print("ERROR",pm10_ge["HasError"])
print(pm10_ge)

import requests
import json
import datetime

temps = requests.get('https://www.jwst.nasa.gov/content/webbLaunch/flightCurrentState2.0.json?unique=1641457305749')
temps = temps.json()['currentState']

launchDate = temps['launchDateTimeString'].replace('Z', '').replace('T', ' ')
print(launchDate)

with open('fixedData.json') as file:
	flightData = json.load(file)['flightData']

for k,v in flightData[0].items():
    print(k)

print(len(flightData))

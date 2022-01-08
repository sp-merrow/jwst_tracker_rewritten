import requests
import json
import numpy
import os.path
from datetime import datetime

# execute fixFile.py if the fixed json doesn't exist
if not os.path.exists('fixedData.json'):
    exec(open('fixFile.py').read())

# function to find closest elapsedSeconds value in flightData vs current elapsed time
def closest(jList, current):
    arrary = numpy.asarray(jList)
    i = (numpy.abs(arrary - current)).argmin()
    return (arrary[i], i)

# make call to JWST API and parse data as json
apiData = requests.get('https://www.jwst.nasa.gov/content/webbLaunch/flightCurrentState2.0.json?unique=1641457305749')
apiData = apiData.json()['currentState']

# grab launch timestamp from API json data and calculate seconds elapsed since launch
launchTime = datetime.fromisoformat(apiData['launchDateTimeString'][:-1])
elapsed = (datetime.now() - launchTime).total_seconds()

# read in flight data json file
with open('fixedData.json', 'r') as file:
	flightData = json.load(file)['flightData']

# list of all elapsedSeconds values from flightData
secondsList = [i['elapsedSeconds'] for i in flightData]

print(f'Seconds: {closest(secondsList, elapsed)[0]}\nIndex: {closest(secondsList, elapsed)[1]}')
print(f'Bottom neighbor: {secondsList[closest(secondsList, elapsed)[1]-1]}\nTop neighbor: {secondsList[closest(secondsList, elapsed)[1]+1]}')
print(f'Current elapsed: {elapsed}')

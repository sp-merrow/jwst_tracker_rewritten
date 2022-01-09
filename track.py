import requests
import json
import numpy
import os.path
from datetime import datetime
import pytz

finalDistance = 1446331.1322

class essentialFileNotFound(Exception):
    def __str__(self):
	    return 'originalFlightData.json not found'

# abort script if original flight data json does not exist
if not os.path.exists('originalFlightData.json'):
    raise essentialFileNotFound

# execute fixFile.py if the fixed json doesn't exist
if not os.path.exists('fixedData.json'):
    exec(open('fixFile.py').read())

# function to find closest elapsedSeconds value in flightData vs current elapsed time
def closest(jList, current):
    arrary = numpy.asarray(jList)
    i = (numpy.abs(arrary - current)).argmin()
    return (arrary[i], i)

def convertKm(km):
    return km * 0.621371

def convertC(c):
    return (c * 1.8) + 32

# make call to JWST API and parse data as json
apiData = requests.get('https://www.jwst.nasa.gov/content/webbLaunch/flightCurrentState2.0.json?unique=1641457305749')
apiData = apiData.json()['currentState']

# grab launch timestamp from API json data and calculate seconds elapsed since launch
launchTime = datetime.fromisoformat(apiData['launchDateTimeString'][:-1])
elapsed = (datetime.now() - launchTime).total_seconds()

# read flight data json file
with open('fixedData.json', 'r') as file:
	flightData = json.load(file)['flightData']

# list of all elapsedSeconds values from flightData
secondsList = [i['elapsedSeconds'] for i in flightData]

closestIndex = closest(secondsList, elapsed)[1]
closestSeconds = closest(secondsList, elapsed)[0]
closestBatch = flightData[closestIndex]

if 0 < closestIndex < len(flightData) - 1:
    if elapsed < closestSeconds:
        interSeconds = closestSeconds - secondsList[closestIndex-1]
        x = elapsed - secondsList[closestIndex - 1]
        percentage = x/interSeconds
        interDistance = flightData[closestIndex]['distanceTravelledKm'] - flightData[closestIndex-1]['distanceTravelledKm']
        interDistance *= percentage
        distance = flightData[closestIndex-1]['distanceTravelledKm'] + interDistance
        interSpeed = flightData[closestIndex-1]['velocityKmSec'] - flightData[closestIndex]['velocityKmSec']
        interSpeed *= 1 - percentage
        speed = flightData[closestIndex]['velocityKmSec'] + interSpeed
    elif elapsed > closestSeconds:
        interSeconds = secondsList[closestIndex+1] - closestSeconds
        x = elapsed - closestSeconds
        percentage = x/interSeconds
        interDistance = flightData[closestIndex+1]['distanceTravelledKm'] - flightData[closestIndex]['distanceTravelledKm']
        interDistance *= percentage
        interSpeed = flightData[closestIndex]['velocityKmSec'] - flightData[closestIndex+1]['velocityKmSec']
        interSpeed *= 1 - percentage
        speed = flightData[closestIndex+1]['velocityKmSec'] + interSpeed
        distance = flightData[closestIndex]['distanceTravelledKm'] + interDistance
    else:
        distance = flightData[closestIndex]['distanceTravelledKm']
        speed = flightData[closestIndex]['velocityKmSec']
else:
    distance = flightData[closestIndex]['distanceTravelledKm']
    speed = flightData[closestIndex]['velocityKmSec']

l2Distance = finalDistance - distance
l2Distance = round( convertKm(l2Distance), 1)
percentComplete = round( (distance/finalDistance) * 100, 4)
distance = round( convertKm(distance), 1)
speed = round( convertKm(speed), 4)
hotA = round( convertC(apiData['tempWarmSide1C']) )
hotB = round( convertC(apiData['tempWarmSide2C']) )
coldC = round( convertC(apiData['tempCoolSide1C']) )
coldD = round( convertC(apiData['tempCoolSide2C']) )

elapsedTime = (datetime.now() - launchTime)
#elapsedTime = elapsedTime.strftime("%d days, %H hours, %M minutes, %S seconds")
print('The James Webb Space Telescope...\n')
print(f'\t• was launched {elapsedTime} ago')
print(f'\t• is {distance} miles away from Earth')
print(f'\t• is {l2Distance} miles away from the L2 Point')
print(f'\t• has completed {percentComplete}% of its journey')
print(f'\t• is travelling at {speed} miles per second')
print('\nOn the warm side of the spacecraft...\n')
print(f'\t• the aft sunshield pallet is at {hotA}°F')
print(f'\t• the spacecraft equipment panel is at {hotB}°F')
print('\nAnd on the cool side of the spacecraft...\n')
print(f'\t• the primary mirror is at {coldC}°F')
print(f'\t• the intrument radiator is at {coldD}°F')

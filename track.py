import requests
from bs4 import BeautifulSoup as bs
import json

temps = requests.get('https://www.jwst.nasa.gov/content/webbLaunch/flightCurrentState2.0.json?unique=1641457305749')
temps = temps.json()['currentState']

fullSite = requests.get('https://www.jwst.nasa.gov/content/webbLaunch/whereIsWebb.html')
soup = bs(fullSite.text, 'html.parser')

rawJ = soup.find_all('script')
for s in rawJ:
    if 'var data=' in s.text:
        data = s.text.strip()
        break

data = data.split('var data=')[1]
data = data.rsplit(';', 1)[0]
data = data.replace("\'", "\"")


accumulator = ''
parsedData = ''
accumulateMode = False
for c, char in enumerate(data):
    if char == ':':
        accumulateMode = True
        parsedData += char
    elif accumulateMode and char in {',', '}'}:
        accumulateMode = False
        if accumulator[0] == '0' and accumulator[1] == 'x' and '(' not in accumulator:
            parsedData += str(int(accumulator, 0)) + ','
        elif '(' in accumulator and accumulator[0] == '0' and accumulator[1] == 'x':
            workingList = ['']
            index = 0
            for i in accumulator:
                if i == '(':
                    index += 1
                    workingList[index] = ''
                    continue
                if i == ')':
                    continue
                workingList[index] += i

            for c, i in enumerate(workingList):
                if c == 0:
                    parsedData += '(' +  str(int(i, 0))
                else:
                    parsedData += str(int(i, 0)) + ')'
        else:
	        parsedData += accumulator + char
        accumulator = ''
    elif accumulateMode:
        accumulator += char
    else:
        parsedData += char

            
print(data[:50])            
#data = json.loads(data)

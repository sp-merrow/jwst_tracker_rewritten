newData = ''

with open('originalFlightData.json', 'r') as file:
    for line in file.readlines():
        needNew = False
        if '.' in line:
            needNew = True
            newLine = ''
            fixPos = None
            for c, char in enumerate(line):
                if c+1 <= len(line) and char == " " and line[c+1] == '.':
                    newLine += ' 0.'
                    fixPos = c
                elif char == '.':
                    if fixPos and c == fixPos+1:
                        continue
                    else:
                        newLine += char
                else:
                    newLine += char
	            
        if '0x1b62fa' not in line and 'NOTE' not in line:
            if needNew:
                newData += newLine
            else:
                newData += line

with open('fixedData.json', 'w') as new:
	new.write(newData)

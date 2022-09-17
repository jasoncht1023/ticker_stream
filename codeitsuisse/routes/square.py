import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tickerStreamPart1', methods=['POST'])
def to_cumulative(stream: list):
    output = str(stream[0][:5])
    dataList = list()
    for record in stream:
        recordList = list(record[6:].split(','))
        recordList[2] = str(round(float(recordList[1]) * float(recordList[2]), 1))
        recordStr = ''
        for i in recordList:
            recordStr = recordStr + ','
            recordStr = recordStr + i
        dataList.append(recordStr)
    dataList.sort()
    for record in dataList:
        output = output + record
    outputList = list()
    outputList.append(output)
    return(outputList)

@app.route('/tickerStreamPart2', methods=['POST'])
def to_cumulative_delayed(stream: list, quantity_block: int):
    outputList = list()
    streamSorted = sorted(stream, key = lambda x: (x[6], x))
    ticker = streamSorted[0][6]
    cumQuan = 0
    cumNotion = 0
    for record in streamSorted:
        recordList = list(record.split(','))
        if (recordList[1] != ticker):
            ticker = recordList[1]
            cumQuan = 0
            cumNotion = 0
        while (recordList[2] != '0'):
            cumNotion += float(recordList[3])
            cumQuan += 1
            recordList[2] = str(int(recordList[2]) - 1)
            if (cumQuan % quantity_block == 0):
                found = False
                index = 0
                while (found == False and index < len(outputList)):
                    if (outputList[index][0] == recordList[0]):
                        found = True
                    index += 1
                if (found == True):
                    outputList[index].extend([',', ticker, ',', str(cumQuan), ',', str(cumNotion)])
                else:
                    outputList.append([recordList[0], ',', ticker, ',', str(cumQuan), ',', str(cumNotion)])
    outputList.sort()
    for i in range(len(outputList)):
        outputList[i] = ''.join(outputList[i])
    return outputList




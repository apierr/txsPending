import json, sys, os
from query import Query

class WriteJson:

    def __init__(self):
        self.query = Query()

    def _writeJsonFile(self, file_name, json_data):
        directory = './html/json'
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open('/'.join([directory, file_name]), 'w')
        f.write(json.dumps(json_data))

    def setDelta(self):
        deltaTimes = {
            'delta' : [],
            'gasLimit' : [],
            'gasPrice' : [],
            'titles': {
                'delta': 'Pending Time (sec)',
                'gasLimit': 'Gas limit',
                'gasPrice': 'Gas Price (GWei))'
            }
        }
        for deltaTime in self.query.getDeltaTime():
            deltaTimes['delta'].append(deltaTime[0])
            deltaTimes['gasLimit'].append(deltaTime[1])
            deltaTimes['gasPrice'].append(deltaTime[2])
        self._writeJsonFile('deltaVsGasLimit.json', deltaTimes)
        #return deltaTimes

        # for deltaTime in session.execute(sql):
        #     deltaTimes['x'].append(deltaTime[0])
        #     deltaTimes['y'].append(deltaTime[1])
        #     deltaTimes['z'].append(deltaTime[2])
        # return deltaTimes
        #     deltaTimes.append(deltaTime)
        # session.commit()
        # return deltaTimes

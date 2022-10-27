
import json
import os
import sys
import pathlib
dir = str(pathlib.Path(__file__).resolve().parent)
sys.path.append(dir + '/../')
from crawling.model.race import RaceModel

if os.path.exists(dir + '/list.json') == True:
    exit

raceModel = RaceModel()
with open(dir + '/list.json', 'w') as jsonfile:
    json.dump(raceModel.listUrlKey(), jsonfile, indent=4)

crawl = json.load(open(dir + '/list.json', 'r'))
for item1 in crawl:
    print(item1['url_key'])

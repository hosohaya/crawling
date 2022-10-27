
from datetime import datetime as dt
from crawling.model.race import RaceModel

now = dt.now()
nowstr = now.strftime('%Y/%m/%d %H:%M:%S')

raceModel = RaceModel()
data = raceModel.find(2)
data['id'] = 1
data['scale'] = 10
raceModel.setValueFromItem(data)
raceModel.updateOnlyNull()

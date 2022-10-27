
import json
import urllib.request
from crawling.model.horse import HorseModel
from crawling.model.jockey import JockeyModel
from crawling.model.race import RaceModel
from crawling.model.record import RecordModel
from crawling.model.group import GroupModel
from crawling.model.trainer import TrainerModel
from crawling.model.venue import VenueModel
from crawling.model.payout import PayoutModel


class Local:
    host = None
    # host = 'http://localhost'
    # host = 'https://keibaeye.com'
    method = "POST"
    headers = {"Content-Type" : "application/json"}
    horseModel = None
    jockeyModel = None
    raceModel = None
    recordModel = None
    groupModel = None
    trainerModel = None
    venueModel = None
    payoutModel = None

    def __init__(self):
        self.horseModel = HorseModel()
        self.jockeyModel = JockeyModel()
        self.raceModel = RaceModel()
        self.recordModel = RecordModel()
        self.groupModel = GroupModel()
        self.trainerModel = TrainerModel()
        self.venueModel = VenueModel()
        self.payoutModel = PayoutModel()

    def parse(self, view):
        data = {}
        data['base_code'] = view.base_code
        self.venueModel.setValueFromItem(data)
        venueId = self.venueModel.getVenueIdByBaseCode()

        raceId = self.raceModel.getId("url_key", view.url_key)
        if raceId == None:
            data = view.getRace()
            self.raceModel.values['venue_id'] = venueId
            self.raceModel.setValueFromItem(data)
            self.raceModel.save()
            raceId = self.raceModel.getRaceId()
        else:
            data = view.getRace()
            self.raceModel.values['id'] = raceId
            self.raceModel.values['venue_id'] = venueId
            self.raceModel.setValueFromItem(data)
            self.raceModel.update()

        for i, record in enumerate(view.records):
            data = view.getHorse(i)
            self.horseModel.setValueFromItem(data)
            horse = self.horseModel.getHorse()
            if horse == None:
                data = view.getGroup(i)
                self.groupModel.setValueFromItem(data)
                groupId = self.groupModel.getGroupId()
                if groupId == None:
                    self.groupModel.save()
                    groupId = self.groupModel.getGroupId()

                self.horseModel.values['group_id'] = groupId
                self.horseModel.save()
                horse = self.horseModel.getHorse()
            else:
                self.horseModel.values['id'] = horse['id']
                self.horseModel.values['group_id'] = horse['group_id']
                self.horseModel.update()

            data = view.getJockey(i)
            self.jockeyModel.setValueFromItem(data)
            jockey = self.jockeyModel.getJockey()
            if jockey == None:
                data = view.getJockeyGroup(i)
                self.groupModel.setValueFromItem(data)
                groupId = self.groupModel.getGroupId()
                if groupId == None:
                    self.groupModel.save()
                    groupId = self.groupModel.getGroupId()

                self.jockeyModel.values['group_id'] = groupId
                self.jockeyModel.save()
                jockey = self.jockeyModel.getJockey()

            data = view.getTrainer(i)
            self.trainerModel.setValueFromItem(data)
            trainer = self.trainerModel.getTrainer()
            if trainer == None:
                data = view.getGroup(i)
                self.groupModel.setValueFromItem(data)
                groupId = self.groupModel.getGroupId()
                if groupId == None:
                    self.groupModel.save()
                    groupId = self.groupModel.getGroupId()

                self.trainerModel.values['group_id'] = groupId
                self.trainerModel.save()
                trainer = self.trainerModel.getTrainer()

            data = view.getRecord(i)
            self.recordModel.values['race_id'] = raceId
            self.recordModel.values['horse_id'] = horse['id']
            self.recordModel.values['horse_name'] = horse['name']
            self.recordModel.values['jockey_id'] = jockey['id']
            self.recordModel.values['jockey_name'] = jockey['name']
            self.recordModel.values['trainer_id'] = trainer['id']
            self.recordModel.values['trainer_name'] = trainer['name']
            self.recordModel.setValueFromItem(data)
            recordId = self.recordModel.getRecordId()
            if recordId == None:
                self.recordModel.save()
            else:
                self.recordModel.values['id'] = recordId
                self.recordModel.update()

        for i, payout in enumerate(view.payouts):
            data = view.getPayout(i)
            self.payoutModel.values['race_id'] = raceId
            self.payoutModel.setValueFromItem(data)
            payoutId = self.payoutModel.getPayoutId()
            if payoutId == None:
                self.payoutModel.save()
            else:
                self.payoutModel.values['id'] = payoutId
                self.payoutModel.update()

        ##############################
        # サーバーへデータ送信
        ##############################
        if self.host != None:
            race = self.raceModel.find(raceId)
            race['date_time'] = race['date_time'].strftime("%Y-%m-%d %H:%M:%S")
            del race['created_at'], race['updated_at']
            
            url = "{}/data/race/add".format(self.host)
            json_data = json.dumps(race).encode("utf-8")

            request = urllib.request.Request(url, 
                data=json_data, method=self.method, headers=self.headers)
            with urllib.request.urlopen(request) as response:
                response_body = response.read().decode("utf-8")
                # print(response_body)

            payouts = self.payoutModel.getSendData(raceId)
            for i, payout in enumerate(payouts):
                del payout['created_at'], payout['updated_at']
                url = "{}/data/payout/add".format(self.host)
                json_data = json.dumps(payout).encode("utf-8")

                request = urllib.request.Request(url, 
                    data=json_data, method=self.method, headers=self.headers)
                with urllib.request.urlopen(request) as response:
                    response_body = response.read().decode("utf-8")
                    # print(response_body)

            raceCodes = self.recordModel.getSendData(raceId)
            for i, raceCode in enumerate(raceCodes):
                horse = self.horseModel.getSendData(raceCode['horse_id'])
                del horse['created_at'], horse['updated_at']
                url = "{}/data/horse/add".format(self.host)
                json_data = json.dumps(horse).encode("utf-8")

                request = urllib.request.Request(url, 
                    data=json_data, method=self.method, headers=self.headers)
                with urllib.request.urlopen(request) as response:
                    response_body = response.read().decode("utf-8")
                    # print(response_body)

                jockey = self.jockeyModel.getSendData(raceCode['jockey_id'])
                del jockey['created_at'], jockey['updated_at']
                url = "{}/data/jockey/add".format(self.host)
                json_data = json.dumps(jockey).encode("utf-8")

                request = urllib.request.Request(url, 
                    data=json_data, method=self.method, headers=self.headers)
                with urllib.request.urlopen(request) as response:
                    response_body = response.read().decode("utf-8")
                    # print(response_body)

                trainer = self.trainerModel.getSendData(raceCode['trainer_id'])
                del trainer['created_at'], trainer['updated_at']
                url = "{}/data/trainer/add".format(self.host)
                json_data = json.dumps(trainer).encode("utf-8")

                request = urllib.request.Request(url, 
                    data=json_data, method=self.method, headers=self.headers)
                with urllib.request.urlopen(request) as response:
                    response_body = response.read().decode("utf-8")
                    # print(response_body)

                del raceCode['created_at'], raceCode['updated_at']
                url = "{}/data/record/add".format(self.host)
                json_data = json.dumps(raceCode).encode("utf-8")

                request = urllib.request.Request(url, 
                    data=json_data, method=self.method, headers=self.headers)
                with urllib.request.urlopen(request) as response:
                    response_body = response.read().decode("utf-8")
                    # print(response_body)
        
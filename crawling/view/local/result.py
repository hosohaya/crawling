
from crawling.view.local.local import LocalView


class ResultView(LocalView):
    def __init__(self):
        super().__init__()

    def setValue(self, response):
        self.title = self.setLocalTitle(response.xpath('//span[@class="plus1bold01"]/text()').get(''))
        if self.title == '':
            return False
        str1 = response.xpath('//span[@class="plus1bold01"]/parent::node()/text()[position()=2]').get('')
        self.distance = self.setLocalDistance(str1)
        self.course = self.setLocalCourse(str1)
        self.rotation = self.setLocalRotation(str1)
        self.weather = self.setLocalWeather(str1)
        self.going = self.setLocalGoing(str1)
        self.type1 = self.trimLocal(response.xpath('//span[@class="plus1bold02"]/text()').get(''))
        self.type2 = self.trimLocal(response.xpath('//span[@class="plus1bold02"]/parent::node()/parent::node()/text()[position()=2]').get(''))
        self.prize1 = self.setLocalPrize(response.xpath('//td[contains(text(), "賞金　1着")]/parent::node()/td[position()=1]/text()').get(''))
        self.prize2 = self.setLocalPrize(response.xpath('//td[contains(text(), "賞金　1着")]/parent::node()/td[position()=2]/text()').get(''))
        self.prize3 = self.setLocalPrize(response.xpath('//td[contains(text(), "賞金　1着")]/parent::node()/td[position()=3]/text()').get(''))
        self.prize4 = self.setLocalPrize(response.xpath('//td[contains(text(), "賞金　1着")]/parent::node()/td[position()=4]/text()').get(''))
        self.prize5 = self.setLocalPrize(response.xpath('//td[contains(text(), "賞金　1着")]/parent::node()/td[position()=5]/text()').get(''))
        
        self.records = []
        for i, elem in enumerate(response.xpath('//td[@class="dbtbl"]/table/tr[@bgcolor="#FFFFFF"]')):
            position = str(i + 1)
            record = {}
            record['ranking'] = self.trimLocalRecord(position, response, '/td[position()=1]/span/text()')
            record['frame'] = self.trimLocalRecord(position, response, '/td[position()=2]/text()')
            record['number'] = self.trimLocalRecord(position, response, '/td[position()=3]/text()')
            record['horse'] = self.trimLocalRecord(position, response, '/td[position()=4]/span/a/text()')
            record['group'] = self.trimLocalRecord(position, response, '/td[position()=5]/text()')
            localRecord6 = self.trimLocalRecord(position, response, '/td[position()=6]/span/text()')
            record['gender'] = self.setLocalGender(localRecord6)
            record['age'] = self.setLocalAge(localRecord6)
            record['birthday'] = ''
            record['hair'] = ''
            record['father'] = ''
            record['mother'] = ''
            record['mothers_father'] = ''
            record['blinker'] = ''
            record['weight'] = ''
            record['fluctuation'] = ''
            record['owner'] = ''
            record['producer'] = ''
            record['burden'] = self.trimLocalRecord(position, response, '/td[position()=7]/text()')
            localRecord8 = self.getLocalRecord(position, response, '/td[position()=8]/a/text()')
            record['jockey'] = self.setLocalJockey(localRecord8)
            record['jockey_mark'] = self.setLocalJockeyMark(localRecord8)
            record['jockey_group'] = self.setLocalJockeyOrganization(localRecord8)
            record['trainer'] = self.trimLocalRecord(position, response, '/td[position()=9]/a/text()')
            record['weight'] = self.trimLocalRecord(position, response, '/td[position()=10]/text()')
            record['fluctuation'] = self.trimLocalRecord(position, response, '/td[position()=11]/text()')
            record['time'] = self.trimLocalRecord(position, response, '/td[position()=12]/text()')
            record['diff'] = self.trimLocalRecord(position, response, '/td[position()=13]/text()')
            record['workout'] = self.trimLocalRecord(position, response, '/td[position()=14]/text()')
            record['popular'] = self.trimLocalRecord(position, response, '/td[position()=15]/text()')
            record['odds'] = ''
            record['corner'] = ''
            self.records.append(record)

        workout = self.trimLocalWorkout(response.xpath('//td[contains(text(), "コーナー通過順")]/parent::node()/parent::node()/tr[position()=1]/td/text()[position()=1]').get(''))
        self.workout1 = self.setLocalWorkout1F(workout)
        self.workout2 = self.setLocalWorkout2F(workout)
        self.workout3 = self.setLocalWorkout3F(workout)
        self.workout4 = self.setLocalWorkout4F(workout)
        self.halon_time = self.trimLocal(response.xpath('//td[contains(text(), "コーナー通過順")]/parent::node()/parent::node()/tr[position()=2]/td/text()[position()=2]').get(''))
        self.corner1 = self.setLocalCorner(response.xpath('//td[contains(text(), "コーナー通過順")]/parent::node()/parent::node()/tr[position()=3]/td/text()[position()=2]').get(''))
        self.corner2 = self.setLocalCorner(response.xpath('//td[contains(text(), "コーナー通過順")]/parent::node()/parent::node()/tr[position()=3]/td/text()[position()=3]').get(''))
        self.corner3 = self.setLocalCorner(response.xpath('//td[contains(text(), "コーナー通過順")]/parent::node()/parent::node()/tr[position()=3]/td/text()[position()=4]').get(''))
        self.corner4 = self.setLocalCorner(response.xpath('//td[contains(text(), "コーナー通過順")]/parent::node()/parent::node()/tr[position()=3]/td/text()[position()=5]').get(''))
        
        cnt = 2
        totalCnt = len(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td'))

        self.payouts = []
        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'tan1', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'tan1', 2, cnt))
        cnt = cnt + 3

        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'huku', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'huku', 2, cnt))
        if self.isLocalSubPayout(response, 3, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'huku', 3, cnt))
        if self.isLocalSubPayout(response, 4, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'huku', 4, cnt))
        if self.isLocalSubPayout(response, 5, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'huku', 5, cnt))
        if self.isLocalSubPayout(response, 6, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'huku', 6, cnt))
        cnt = cnt + 3

        if totalCnt == 25 or totalCnt == 28:
            if self.isLocalSubPayout(response, 1, cnt):
                self.payouts.append(self.setLocalPayoutData(response, 'waku', 1, cnt))
            if self.isLocalSubPayout(response, 2, cnt):
                self.payouts.append(self.setLocalPayoutData(response, 'waku', 2, cnt))
            cnt = cnt + 3

        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'ren2', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'ren2', 2, cnt))
        cnt = cnt + 3

        if totalCnt == 28:
            if self.isLocalSubPayout(response, 1, cnt):
                self.payouts.append(self.setLocalPayoutData(response, 'wakutan', 1, cnt))
            if self.isLocalSubPayout(response, 2, cnt):
                self.payouts.append(self.setLocalPayoutData(response, 'wakutan', 2, cnt))
            cnt = cnt + 3

        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'tan2', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'tan2', 2, cnt))
        cnt = cnt + 3

        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'wide', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'wide', 2, cnt))
        if self.isLocalSubPayout(response, 3, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'wide', 3, cnt))
        if self.isLocalSubPayout(response, 4, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'wide', 4, cnt))
        if self.isLocalSubPayout(response, 5, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'wide', 5, cnt))
        if self.isLocalSubPayout(response, 6, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'wide', 6, cnt))
        cnt = cnt + 3

        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'ren3', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'ren3', 2, cnt))
        cnt = cnt + 3

        if self.isLocalSubPayout(response, 1, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'tan3', 1, cnt))
        if self.isLocalSubPayout(response, 2, cnt):
            self.payouts.append(self.setLocalPayoutData(response, 'tan3', 2, cnt))
        cnt = cnt + 3
        return True
    
    def getRace(self):
        item = {}
        item['url_key'] = self.url_key
        item['win5'] = ''
        item['number'] = self.number
        item['title'] = self.title
        item['scale'] = ''
        item['date_time'] = "{} 00:00:00".format(self.date)
        item['course'] = self.course
        item['distance'] = self.distance
        item['rotation'] = self.rotation
        item['weather'] = self.weather
        item['going'] = self.going
        item['times'] = ''
        item['days'] = ''
        item['type1'] = self.type1
        item['type2'] = self.type2
        item['type3'] = ''
        item['type4'] = ''
        item['type5'] = ''
        item['prize1'] = self.prize1
        item['prize2'] = self.prize2
        item['prize3'] = self.prize3
        item['prize4'] = self.prize4
        item['prize5'] = self.prize5
        item['option1'] = ''
        item['option2'] = ''
        item['option3'] = ''
        item['option4'] = ''
        item['option5'] = ''
        item['halon_time'] = self.halon_time
        item['workout1'] = self.workout1
        item['workout2'] = self.workout2
        item['workout3'] = self.workout3
        item['workout4'] = self.workout4
        item['corner1'] = self.corner1
        item['corner2'] = self.corner2
        item['corner3'] = self.corner3
        item['corner4'] = self.corner4
        item['approval_flag'] = 0
        item['delete_flag'] = 0
        return item

    def getHorse(self, i):
        item = {}
        item['name'] = self.records[i]['horse']
        item['scrapy_name'] = self.records[i]['horse']
        item['gender'] = self.records[i]['gender']
        item['delete_flag'] = 0
        return item

    def getJockeyGroup(self, i):
        item = {}
        item['category'] = '2'
        item['name'] = self.records[i]['jockey_group']
        item['delete_flag'] = 0
        return item

    def getJockey(self, i):
        item = {}
        item['name'] = self.records[i]['jockey']
        item['scrapy_name'] = self.records[i]['jockey']
        item['orders'] = ''
        item['delete_flag'] = 0
        return item

    def getGroup(self, i):
        item = {}
        item['category'] = '2'
        item['name'] = self.records[i]['group']
        item['delete_flag'] = 0
        return item

    def getTrainer(self, i):
        item = {}
        item['name'] = self.records[i]['trainer']
        item['scrapy_name'] = self.records[i]['trainer']
        item['orders'] = ''
        item['delete_flag'] = 0
        return item

    def getRecord(self, i):
        item = {}
        item['horse_name'] = self.records[i]['horse']
        item['horse_mark'] = '1'
        item['age'] = self.records[i]['age']
        item['gender'] = self.records[i]['gender']
        item['birthday'] = self.records[i]['birthday']
        item['hair'] = self.records[i]['hair']
        item['father'] = self.records[i]['father']
        item['mother'] = self.records[i]['mother']
        item['mothers_father'] = self.records[i]['mothers_father']
        item['blinker'] = self.records[i]['blinker']
        item['weight'] = self.records[i]['weight']
        item['fluctuation'] = self.records[i]['fluctuation']
        item['owner'] = self.records[i]['owner']
        item['producer'] = self.records[i]['producer']
        item['jockey_name'] = self.records[i]['jockey']
        item['jockey_mark'] = self.records[i]['jockey_mark']
        item['burden'] = self.records[i]['burden']
        item['trainer_name'] = self.records[i]['trainer']
        item['ranking'] = self.records[i]['ranking']
        item['frame'] = self.records[i]['frame']
        item['number'] = self.records[i]['number']
        item['time'] = self.records[i]['time']
        item['diff'] = self.records[i]['diff']
        item['popular'] = self.records[i]['popular']
        item['odds'] = self.records[i]['odds']
        item['workout'] = self.records[i]['workout']
        item['corner'] = self.records[i]['corner']
        item['scrapy_flag'] = 0
        item['delete_flag'] = 0
        return item

    def getPayout(self, i):
        item = {}
        item['category'] = self.payouts[i]['category']
        item['no'] = self.payouts[i]['no']
        item['number1'] = self.payouts[i]['number1']
        item['number2'] = self.payouts[i]['number2']
        item['number3'] = self.payouts[i]['number3']
        item['popular'] = self.payouts[i]['popular']
        item['payout'] = self.payouts[i]['payout']
        item['delete_flag'] = 0
        return item

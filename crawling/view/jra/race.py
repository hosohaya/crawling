
from crawling.view.jra.jra import JraView


class RaceView(JraView):
    def __init__(self):
        super().__init__()

    def getViewName(self):
        return 'race'

    def setValue(self, response):
        self.venue = self.trim(response.xpath('//div[@class="RaceData02"]/span[position()=2]/text()').get(default=''))
        if self.venue == '':
            return False
        self.url_key = self.setUrlKey(response.xpath('//li[@class="Active"]/a/@href').get(default=''))
        self.win5 = self.setWin5(response)
        self.number = self.setNumber(response.xpath('//span[@class="RaceNum"]/text()[position()=2]').get(default=''))
        self.title = self.trim(response.xpath('//div[@class="RaceName"]/text()').get(default=''))
        self.scale = self.setScale(response)
        self.date = self.setDate(self.url_key, response.xpath('//dl[@id="RaceList_DateList"]/dd[@class="Active"]/a/text()').get(default=''))
        self.start_time = self.setStartTime(response.xpath('//div[@class="RaceData01"]/text()[position()=1]').get(default=''))
        courseStr = self.trim(response.xpath('//div[@class="RaceData01"]/span[position()=1]/text()').get(default=''))
        weatherStr = self.trim(response.xpath('//div[@class="RaceData01"]/text()[position()=2]').get(default=''))
        self.course = self.setCourse(courseStr[0:1] + weatherStr)
        self.distance = self.setDistance(courseStr[1:])
        self.rotation = self.setRotation(weatherStr)
        self.weather = self.setWeather(weatherStr)
        self.going = self.setGoing(response.xpath('//div[@class="RaceData01"]/span[position()=3]/text()').get(default=''))
        self.times = self.setTimes(response.xpath('//div[@class="RaceData02"]/span[position()=1]/text()').get(default=''))
        self.days = self.setDays(response.xpath('//div[@class="RaceData02"]/span[position()=3]/text()').get(default=''))
        self.type1 = self.trim(response.xpath('//div[@class="RaceData02"]/span[position()=4]/text()').get(default=''))
        self.type2 = self.trim(response.xpath('//div[@class="RaceData02"]/span[position()=5]/text()').get(default=''))
        self.type3 = self.trim(response.xpath('//div[@class="RaceData02"]/span[position()=6]/text()').get(default=''))
        self.type4 = self.trim(response.xpath('//div[@class="RaceData02"]/span[position()=7]/text()').get(default=''))
        self.type5 = self.trim(response.xpath('//div[@class="RaceData02"]/span[position()=8]/text()').get(default=''))
        prizeStr = self.setPrize(response.xpath('//div[@class="RaceData02"]/span[position()=9]/text()').get(default=''))
        self.prize1 = prizeStr[0:1][0]
        self.prize2 = prizeStr[1:2][0]
        self.prize3 = prizeStr[2:3][0]
        self.prize4 = prizeStr[3:4][0]
        self.prize5 = prizeStr[4:5][0]
        self.option1 = ''
        self.option2 = ''
        self.option3 = ''
        self.option4 = ''
        self.option5 = ''
        self.halon_time = ''
        self.workout1 = ''
        self.workout2 = ''
        self.workout3 = ''
        self.workout4 = ''
        self.corner1 = self.setCorner(response, 1)
        self.corner2 = self.setCorner(response, 2)
        self.corner3 = self.setCorner(response, 3)
        self.corner4 = self.setCorner(response, 4)

        self.records = []
        for i, num in enumerate(response.xpath('//tr[contains(@class, "HorseList")]/td[contains(@class, "Umaban")]').getall()):
            position = str(i + 1)
            record = {}
            record['horse'] = self.getList(response, position, '//span[@class="HorseName"]/a/text()')
            record['horse_mark'] = self.setHorseMark(response, position)
            str1 = self.getList(response, position, '/td[contains(@class, "Barei Txt_C")]/text()')
            record['age'] = self.setAge(str1)
            record['gender'] = self.setGender(str1)
            record['birthday'] = ''
            record['hair'] = ''
            record['father'] = ''
            record['mother'] = ''
            record['mothers_father'] = ''
            record['blinker'] = ''
            record['weight'] = self.getList(response, position, '/td[@class="Weight"]/text()')
            record['fluctuation'] = self.getList(response, position, '/td[@class="Weight"]/small/text()')
            record['owner'] = ''
            record['producer'] = ''
            jockey = self.setJockey(response, position)
            record['jockey'] = self.setJockeyName(jockey)
            record['jockey_mark'] = self.setJockeyMark(jockey)
            record['burden'] = self.getList(response, position, '/td[contains(@class, "Barei Txt_C")]/following-sibling::td[@class="Txt_C"]/text()')
            record['trainer'] = self.getList(response, position, '/td[contains(@class, "Trainer")]/a/text()')
            record['group'] = self.getList(response, position, '/td[contains(@class, "Trainer")]/span/text()')
            record['ranking'] = ''
            record['frame'] = self.getList(response, position, '/td[contains(@class, "Waku")]/span/text()')
            record['number'] = self.getList(response, position, '/td[contains(@class, "Umaban")]/text()')
            record['time'] = ''
            record['diff'] = ''
            record['popular'] = self.setOddsPopular(self.getList(response, position, '/td[@class="Txt_R Popular"]/span/text()'))
            record['odds'] = self.setOdds(self.getList(response, position, '/td[@class="Popular Popular_Ninki Txt_C"]/span/text()'))
            record['workout'] = ''
            record['corner'] = ''
            self.records.append(record)
        
        self.payouts = []
        return True
    
    def getVenue(self):
        item = {}
        item['name'] = self.venue
        return item

    def getRace(self):
        item = {}
        item['url_key'] = self.url_key
        item['win5'] = self.win5
        item['number'] = self.number
        item['title'] = self.title
        item['scale'] = self.scale
        item['date_time'] = "{} {}:00".format(self.date, self.start_time)
        item['course'] = self.course
        item['distance'] = self.distance
        item['rotation'] = self.rotation
        item['weather'] = self.weather
        item['going'] = self.going
        item['times'] = self.times
        item['days'] = self.days
        item['type1'] = self.type1
        item['type2'] = self.type2
        item['type3'] = self.type3
        item['type4'] = self.type4
        item['type5'] = self.type5
        item['prize1'] = self.prize1
        item['prize2'] = self.prize2
        item['prize3'] = self.prize3
        item['prize4'] = self.prize4
        item['prize5'] = self.prize5
        item['option1'] = self.option1
        item['option2'] = self.option2
        item['option3'] = self.option3
        item['option4'] = self.option4
        item['option5'] = self.option5
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

    def getJockey(self, i):
        item = {}
        item['group_id'] = 2
        item['name'] = self.records[i]['jockey']
        item['scrapy_name'] = self.records[i]['jockey']
        item['orders'] = ''
        item['delete_flag'] = 0
        return item

    def getGroup(self, i):
        item = {}
        item['category'] = '1'
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
        item['horse_mark'] = self.records[i]['horse_mark']
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

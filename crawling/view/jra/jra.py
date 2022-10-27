
from crawling.view.view import View
import re


class JraView(View):
    def __init__(self):
        super().__init__()

    def trim(self, str):
        str = str.replace(' ', '')
        str = str.replace('　', '')
        str = str.replace('(', '')
        str = str.replace(')', '')
        str = str.replace('（', '')
        str = str.replace('）', '')
        str = str.replace('\r', '')
        str = str.replace('\n', '')
        str = str.replace('\r\n', '')
        return str

    def getList(self, response, position, xpath):
        return self.trim(response.xpath('//tr[contains(@class, "HorseList")][position()=' + position + ']' + xpath).get(default=''))
    
    def setDate(self, str1, str2):
        str1 = self.trim(str1)
        str2 = self.trim(str2)
        year = str1[0:4]
        month = ""
        day = ""
        if '月' in str2:
            month = str(str2[0:str2.find('月')]).zfill(2)
            day = str(str2[str2.find('月') + 1:str2.find('日')]).zfill(2)
        if '/' in str2:
            month = str(str2[0:str2.find('/')]).zfill(2)
            day = str(str2[str2.find('/') + 1:]).zfill(2)
        return '{}-{}-{}'.format(year, month, day)

    def setUrlKey(self, str):
        str = str.replace('?race_id=', '')
        return self.trim(str)
    
    def setOddsPopular(self, str):
        str = self.setOdds(str)
        str = str.replace('.', '')
        return str

    def setOdds(self, str):
        str = str.replace('-', '')
        str = str.replace('*', '')
        return str

    def setStartTime(self, str):
        str = self.trim(str)
        str = str.replace('発走', '')
        str = str.replace('/', '')
        if not str:
            str = '00:00'
        return str

    def setRotation(self, str):
        return self.paramList.keyRotation(str)

    def setWeather(self, str):
        return self.paramList.keyWeather(str)

    def setGoing(self, str):
        str = self.trim(str)
        str = str.replace('/馬場:', '')
        return self.paramList.keyGoing(str)

    def setDistance(self, str):
        str = str.replace('m', '')
        return str

    def setAge(self, str):
        str = str.replace('牡', '')
        str = str.replace('牝', '')
        str = str.replace('セ', '')
        return self.trim(str)
    
    def setDiff(self, str):
        str = str.replace('大', '大差')
        str = str.replace('.', ' ')
        return str

    def setGender(self, str):
        return self.paramList.keyGender(str)

    def setPrize(self, str):
        str = self.trim(str)
        str = str.replace('本賞金', '')
        str = str.replace(':', '')
        str = str.replace('万円', '')
        return str.split(',')

    def setNumber(self, str):
        str = self.trim(str)
        str = str.replace('R', '')
        return str

    def setCourse(self, str):
        if '障' in str:
            if '芝ダート' in str:
                return '5'
            elif '芝ダ' in str:
                return '5'
            if 'ダート芝' in str:
                return '6'
            elif 'ダ芝' in str:
                return '6'
            elif '芝' in str:
                return '3'
            elif 'ダ' in str:
                return '4'
            elif 'ダート' in str:
                return '4'
            else:
                return ''
        else:
            return self.paramList.keyCourse(str)

    def setTimes(self, str):
        str = self.trim(str)
        str = str.replace('回', '')
        return str

    def setDays(self, str):
        str = self.trim(str)
        str = str.replace('日目', '')
        return str

    def setRanks(self, str):
        str = self.trim(str)
        return self.paramList.keyRanks(str)

    def setYen(self, str):
        str = self.trim(str)
        str = str.replace('円', '')
        str = str.replace(',', '')
        return str

    def setPopular(self, str):
        str = self.trim(str)
        str = str.replace('人気', '')
        str = str.replace(',', '')
        return str

    def setHorse(self, response, position):
        horse = self.getList(response, position, '/td[@class="Horse_Info"]/span/a/text()')
        if horse == '':
            raise ValueError("error horse.")
        return horse
    
    def setJockey(self, response, position):
        jockey = self.getList(response, position, '/td[contains(@class, "Jockey")]/a/text()')
        if not jockey:
            jockey = self.getList(response, position, '/td[contains(@class, "Jockey")]/a/font/text()')
        if not jockey:
            jockey = self.getList(response, position, '/td[contains(@class, "Jockey")]/font/text()')
        if not jockey:
            jockey = self.getList(response, position, '/td[contains(@class, "Jockey")]/text()')
        if not jockey:
            raise ValueError("error jockey.")
        return jockey

    def setTrainer(self, response, position):
        trainer = self.getList(response, position, '/td[@class="Trainer"]/a/text()')
        if trainer == '':
            raise ValueError("error trainer.")
        return trainer
    
    def setJockeyName(self, str):
        str = self.trim(str)
        str = str.replace('☆', '')
        str = str.replace('◇', '')
        str = str.replace('△', '')
        str = str.replace('▲', '')
        str = str.replace('★', '')
        if not str:
            str = '未定'
        return str

    def setJockeyMark(self, str):
        return self.paramList.keyJockeyMark(str)

    def setScale(self, response):
        scale = ''
        for num in reversed(range(1, 31)):
            if len(response.xpath('//div[@class="RaceName"]/span[contains(@class, "GradeType' + 
                str(num) + '") and not(contains(@class, "Icon_GradePos01"))]')) != 0:
                scale = str(num)
                break
        return scale

    def setWin5(self, response):
        win5 = ''
        if len(response.xpath('//div[@class="RaceName"]/span[contains(@class, "Icon_GradePos01")]')) != 0:
            win5 = '1'
        return win5

    def setCorner(self, response, position):
        result = ""
        corners = response.xpath('//table[contains(@class, "Corner_Num")]/tbody/tr[position()=' + str(position) + ']/td/span/text()').getall()
        for i, corner in enumerate(response.xpath('//table[contains(@class, "Corner_Num")]/tbody/tr[position()=' + str(position) + ']/td/text()').getall()):
            if len(corners) > i:
                result += corner + corners[i]
            else:
                result += corner
        return result

    def setHorseMark(self, response, position):
        result = ""
        maruchi = len(response.xpath('//tr[contains(@class, "HorseList")][position()=' + str(position) + ']/td[@class="Horse_Info"]/span/span[contains(@class, "Icon_MaruChi")]'))
        marugai = len(response.xpath('//tr[contains(@class, "HorseList")][position()=' + str(position) + ']/td[@class="Horse_Info"]/span/span[contains(@class, "Icon_MaruGai")]'))
        kakuchi = len(response.xpath('//tr[contains(@class, "HorseList")][position()=' + str(position) + ']/td[@class="Horse_Info"]/span/span[contains(@class, "Icon_kakuChi")]'))
        kakugai = len(response.xpath('//tr[contains(@class, "HorseList")][position()=' + str(position) + ']/td[@class="Horse_Info"]/span/span[contains(@class, "Icon_kakuGai")]'))
        if maruchi > 0 and marugai > 0:
            result = '13'
        elif maruchi > 0 and kakugai > 0:
            result = '14'
        elif kakuchi > 0 and marugai > 0:
            result = '23'
        elif kakuchi > 0 and kakugai > 0:
            result = '24'
        elif maruchi > 0:
            result = '1'
        elif marugai > 0:
            result = '3'
        elif kakuchi > 0:
            result = '2'
        elif kakugai > 0:
            result = '4'
        return result

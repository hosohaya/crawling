
from crawling.view.view import View
import re


class LocalView(View):
    def __init__(self):
        super().__init__()

    def setLocalParam(self, date, number, base_code):
        self.date = date
        self.number = number
        self.base_code = base_code
        self.url_key = '{}_{}_{}'.format(date, number, base_code)
        return True
    
    def trimLocal(self, str1):
        str1 = str1.replace(' ', '')
        str1 = str1.replace('　', '')
        str1 = str1.replace('(', '')
        str1 = str1.replace(')', '')
        str1 = str1.replace('（', '')
        str1 = str1.replace('）', '')
        str1 = str1.replace('\r', '')
        str1 = str1.replace('\n', '')
        str1 = str1.replace('\r\n', '')
        str1 = str1.replace('\xa0', '')
        return str1

    def trimLocalDistance(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str1.replace('芝', '')
        str1 = str1.replace('ダート', '')
        str1 = str1.replace('障害', '')
        return str1

    def setLocalTitle(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str1.replace('\u3000', '')
        return str1
    
    def setLocalDate(self, str1):
        str1 = self.trimLocal(str1)
        year = str1[0:4]
        month = ""
        day = ""
        if '月' in str1:
            month = str(str1[str1.find('年') + 1:str1.find('月')]).zfill(2)
            day = str(str1[str1.find('月') + 1:str1.find('日')]).zfill(2)
        return '{}-{}-{}'.format(year, month, day)

    def setLocalDistance(self, str1):
        str1 = self.trimLocalDistance(str1)
        distance = ""
        if 'm' in str1:
            distance = str(str1[0:str1.find('m')])
        if 'ｍ' in str1:
            distance = str(str1[0:str1.find('ｍ')])
        return distance

    def setLocalCourse(self, str1):
        if '芝' in str1:
            return 1
        elif 'ダート' in str1:
            return 2
        elif '障害' in str1:
            return 3
        else:
            return 0

    def setLocalRotation(self, str1):
        if '直' in str1:
            return 1
        elif '左' in str1:
            return 2
        elif '右' in str1:
            return 3
        else:
            return 0

    def setLocalWeather(self, str1):
        if '晴' in str1:
            return 1
        elif '曇' in str1:
            return 2
        elif '小雨' in str1:
            return 3
        elif '雨' in str1:
            return 4
        elif '小雪' in str1:
            return 5
        elif '雪' in str1:
            return 6
        else:
            return 0

    def setLocalGoing(self, str1):
        str1 = self.trimLocal(str1)
        going = ""
        if '馬場：' in str1:
            going = str(str1[str1.find('馬場：') + 3:])
        return self.paramList.keyGoing(going)

    def setLocalPrize(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str1.replace(',', '')
        str1 = str1.replace('1着', '')
        str1 = str1.replace('2着', '')
        str1 = str1.replace('3着', '')
        str1 = str1.replace('4着', '')
        str1 = str1.replace('5着', '')
        str1 = str(re.sub(r"\D", "", str1))
        return str1

    def setLocalGender(self, str1):
        if '牡' in str1:
            return 1
        elif '牝' in str1:
            return 2
        elif 'セン' in str1:
            return 3
        else:
            return 0

    def setLocalAge(self, str1):
        str1 = str(re.sub(r"\D", "", str1))
        return str1

    def setLocalJockey(self, str1):
        result = ""
        if '(' in str1:
            result = str(str1[0:str1.find('(')])
        result = result.replace('☆', '')
        result = result.replace('◇', '')
        result = result.replace('△', '')
        result = result.replace('▲', '')
        result = result.replace('★', '')
        return self.trimLocal(result)

    def setLocalJockeyMark(self, str1):
        return self.paramList.keyJockeyMark(str1)

    def setLocalJockeyOrganization(self, str1):
        result = ""
        if '(' in str1:
            result = str(str1[str1.find('(') + 1:])
        return self.trimLocal(result)

    def trimLocalWorkout(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str1.replace('上り', '')
        return str1

    def setLocalWorkout1F(self, str1):
        result = ""
        if '1F' in str1:
            result = str(str1[str1.find('1F') + 2:])
        return self.trimLocal(result)

    def setLocalWorkout2F(self, str1):
        result = ""
        if '2F' in str1:
            if '1F' in str1:
                result = str(str1[str1.find('2F') + 2:str1.find('1F')])
            else:
                result = str(str1[str1.find('2F') + 2:])
        return self.trimLocal(result)

    def setLocalWorkout3F(self, str1):
        result = ""
        if '3F' in str1:
            if '2F' in str1:
                result = str(str1[str1.find('3F') + 2:str1.find('2F')])
            else:
                result = str(str1[str1.find('3F') + 2:])
        return self.trimLocal(result)

    def setLocalWorkout4F(self, str1):
        result = ""
        if '4F' in str1:
            if '3F' in str1:
                result = str(str1[str1.find('4F') + 2:str1.find('3F')])
            else:
                result = str(str1[str1.find('4F') + 2:])
        return self.trimLocal(result)

    def setLocalCorner(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str1.replace('１角', '')
        str1 = str1.replace('２角', '')
        str1 = str1.replace('３角', '')
        str1 = str1.replace('４角', '')
        str1 = str1.replace('１コーナー', '')
        str1 = str1.replace('２コーナー', '')
        str1 = str1.replace('３コーナー', '')
        str1 = str1.replace('４コーナー', '')
        return str1

    def setLocalPayout(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str1.replace(',', '')
        str1 = str(re.sub(r"\D", "", str1))
        return str1

    def setLocalNumber1(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str(str1.split('-')[0])
        return str1

    def setLocalNumber2(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str(str1.split('-')[1])
        return str1

    def setLocalNumber3(self, str1):
        str1 = self.trimLocal(str1)
        str1 = str(str1.split('-')[2])
        return str1

    def getLocalRecord(self, position, response, xpath):
        return response.xpath('//td[@class="dbtbl"]/table/tr[@bgcolor="#FFFFFF"][position()=' + position + ']' + xpath).get(default='')
    
    def trimLocalRecord(self, position, response, xpath):
        return self.trimLocal(response.xpath('//td[@class="dbtbl"]/table/tr[@bgcolor="#FFFFFF"][position()=' + position + ']' + xpath).get(default=''))
    
    def setLocalPayoutData(self, response, category, no, position):
        payout = {}
        payout['category'] = category
        payout['no'] = str(no)
        if category == 'tan1' or category == 'huku':
            payout['number1'] = self.trimLocal(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position) + ']/text()[position()=' + str(no) + ']').get(''))
            payout['number2'] = ''
            payout['number3'] = ''
        elif category == 'tan3' or category == 'ren3':
            payout['number1'] = self.setLocalNumber1(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position) + ']/text()[position()=' + str(no) + ']').get(''))
            payout['number2'] = self.setLocalNumber2(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position) + ']/text()[position()=' + str(no) + ']').get(''))
            payout['number3'] = self.setLocalNumber3(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position) + ']/text()[position()=' + str(no) + ']').get(''))
        else:
            payout['number1'] = self.setLocalNumber1(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position) + ']/text()[position()=' + str(no) + ']').get(''))
            payout['number2'] = self.setLocalNumber2(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position) + ']/text()[position()=' + str(no) + ']').get(''))
            payout['number3'] = ''
        payout['popular'] = self.trimLocal(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position + 2) + ']/text()[position()=' + str(no) + ']').get(''))
        payout['payout'] = self.setLocalPayout(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position + 1) + ']/text()[position()=' + str(no) + ']').get(''))
        return payout
    
    def isLocalSubPayout(self, response, no, position):
        if self.trimLocal(response.xpath('//td[contains(text(), "払戻金")]/parent::node()/parent::node()/tr[position()=4]/td[position()=' + str(position + 2) + ']/text()[position()=' + str(no) + ']').get('')) == '':
            return False
        return True
    
import re


class ParamList:
    def __init__(self):
        pass

    def trim(self, str):
        str = str.replace('.', '')
        str = str.replace(':', '')
        return str
    
    def keyRotation(self, str):
        if '右外内' in str:
            return '51'
        elif '右外 内' in str:
            return '51'
        elif '右外-内' in str:
            return '51'
        elif '左外内' in str:
            return '52'
        elif '左外 内' in str:
            return '52'
        elif '左外-内' in str:
            return '52'
        elif '右外' in str:
            return '11'
        elif '右 外' in str:
            return '11'
        elif '右-外' in str:
            return '11'
        elif '左外' in str:
            return '12'
        elif '左 外' in str:
            return '12'
        elif '左-外' in str:
            return '12'
        elif '外内' in str:
            return '6'
        elif '外 内' in str:
            return '6'
        elif '外-内' in str:
            return '6'
        elif '内' in str:
            return '5'
        elif '直' in str:
            return '4'
        elif '外' in str:
            return '3'
        elif '左' in str:
            return '2'
        elif '右' in str:
            return '1'
        else:
            return ''

    def valRotation(self, str):
        if '51' == str:
            return '右外-内'
        elif '52' == str:
            return '左外-内'
        elif '11' == str:
            return '右 外'
        elif '12' == str:
            return '左 外'
        elif '6' == str:
            return '外 内'
        elif '5' == str:
            return '内'
        elif '4' == str:
            return '直'
        elif '3' == str:
            return '外'
        elif '2' == str:
            return '左'
        elif '1' == str:
            return '右'
        else:
            return ''

    def keyWeather(self, str):
        if '晴' in str:
            return '1'
        elif '曇' in str:
            return '2'
        elif '小雨' in str:
            return '3'
        elif '雨' in str:
            return '4'
        elif '小雪' in str:
            return '5'
        elif '雪' in str:
            return '6'
        else:
            return ''

    def valWeather(self, str):
        if '1' == str:
            return '晴'
        elif '2' == str:
            return '曇'
        elif '3' == str:
            return '小雨'
        elif '4' == str:
            return '雨'
        elif '5' == str:
            return '小雪'
        elif '6' == str:
            return '雪'
        else:
            return ''

    def keyGoing(self, str):
        if '不' in str:
            return '4'
        elif '良' in str:
            return '1'
        elif '稍' in str:
            return '2'
        elif '重' in str:
            return '3'
        else:
            return ''

    def valGoing(self, str):
        if '4' == str:
            return '不'
        elif '1' == str:
            return '良'
        elif '2' == str:
            return '稍'
        elif '3' == str:
            return '重'
        else:
            return ''

    def keyGender(self, str):
        if '牡' in str:
            return '1'
        elif '牝' in str:
            return '2'
        elif 'セ' in str:
            return '3'
        else:
            return ''

    def valGender(self, str):
        if '1' == str:
            return '牡'
        elif '2' == str:
            return '牝'
        elif '3' == str:
            return 'セ'
        else:
            return ''

    def keyCourse(self, str):
        if '芝' in str:
            return '1'
        elif 'ダート' in str:
            return '2'
        elif 'ダ' in str:
            return '2'
        elif '障' in str:
            return '3'
        else:
            return ''

    def valCourse(self, str):
        if '1' == str:
            return '芝'
        elif '2' == str:
            return 'ダ'
        elif '3' == str:
            return '障'
        else:
            return ''

    def keyRanks(self, str1):
        if '中止' in str1:
            return '90'
        elif '除外' in str1:
            return '91'
        elif '取消' in str1:
            return '92'
        elif '失格' in str1:
            return '93'
        else:
            return str(re.sub("\\D", "", str1))

    def valRanks(self, str):
        if '90' == str:
            return '中止'
        elif '91' == str:
            return '除外'
        elif '92' == str:
            return '取消'
        elif '93' == str:
            return '失格'
        else:
            return str

    def keyJockeyMark(self, str):
        if '☆' in str:
            return '1'
        elif '◇' in str:
            return '2'
        elif '△' in str:
            return '3'
        elif '▲' in str:
            return '4'
        elif '★' in str:
            return '5'
        else:
            return ''

    def valJockeyMark(self, str):
        if '1' == str:
            return '☆'
        elif '2' == str:
            return '◇'
        elif '3' == str:
            return '△'
        elif '4' == str:
            return '▲'
        elif '5' == str:
            return '★'
        else:
            return ''

    def convertNull(self, str):
        if str is None:
            return '0'
        elif '' == str:
            return '0'
        else:
            return str

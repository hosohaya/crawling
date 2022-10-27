
from crawling.model.model import Model
from crawling.model.race import RaceModel
from crawling.model.venue import VenueModel


class RecordModel(Model):
    table = "records"

    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("race_id", "BIGINT NOT NULL")
        self.setColumn("horse_id", "BIGINT NOT NULL")
        self.setColumn("horse_name", "VARCHAR(255)")
        self.setColumn("horse_mark", "VARCHAR(2)")
        self.setColumn("age", "VARCHAR(2) NOT NULL")
        self.setColumn("gender", "VARCHAR(1)")
        self.setColumn("birthday", "VARCHAR(5)")
        self.setColumn("hair", "VARCHAR(10)")
        self.setColumn("father", "VARCHAR(50)")
        self.setColumn("mother", "VARCHAR(50)")
        self.setColumn("mothers_father", "VARCHAR(50)")
        self.setColumn("blinker", "VARCHAR(1)")
        self.setColumn("weight", "VARCHAR(3) NOT NULL")
        self.setColumn("fluctuation", "VARCHAR(10) NOT NULL")
        self.setColumn("owner", "VARCHAR(50)")
        self.setColumn("producer", "VARCHAR(50)")
        self.setColumn("jockey_id", "BIGINT NOT NULL")
        self.setColumn("jockey_name", "VARCHAR(255)")
        self.setColumn("jockey_mark", "VARCHAR(2)")
        self.setColumn("burden", "VARCHAR(10) NOT NULL")
        self.setColumn("trainer_id", "BIGINT NOT NULL")
        self.setColumn("trainer_name", "VARCHAR(255)")
        self.setColumn("ranking", "VARCHAR(2) NOT NULL")
        self.setColumn("frame", "VARCHAR(2) NOT NULL")
        self.setColumn("number", "VARCHAR(2) NOT NULL")
        self.setColumn("time", "VARCHAR(10) NOT NULL")
        self.setColumn("diff", "VARCHAR(20)")
        self.setColumn("popular", "VARCHAR(2)")
        self.setColumn("odds", "VARCHAR(10)")
        self.setColumn("workout", "VARCHAR(10)")
        self.setColumn("corner", "VARCHAR(20)")
        self.setColumn("scrapy_flag", "INT(1)")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getRecordId(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' AND `{}` = '{}' LIMIT 1".format(
            self.primaryKey, self.table, 'race_id', self.values['race_id'], 'horse_id', self.values['horse_id'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def getSendData(self, raceId):
        sql = "SELECT * FROM `{}` WHERE `{}` = '{}'".format(
            self.table, 'race_id', raceId)
        Model.db.execute(sql)
        return Model.db.fetchall()
    
    def deleteNotRace(self, raceId):
        sql = "UPDATE `{}` SET delete_flag = '1' WHERE race_id = '{}' AND (number IS NULL OR number = '')".format(
            self.table, raceId)
        print(sql)
        Model.db.execute(sql)
        Model.con.commit()

    def getDaily(self, year, month, day):
        sql = "SELECT"
        sql += " rec.ranking, rec.frame, rec.number AS no, rec.age, rec.burden, rec.time, rec.weight"
        sql += ", ra.id AS race, ra.number AS race_no, DATE_FORMAT(ra.date_time, '%Y-%m-%d') AS date, ra.going, ra.distance, ra.course, ra.rotation"
        sql += ", rec.horse_id AS horse, rec.gender"
        sql += ", rec.jockey_id AS jockey"
        sql += ", rec.trainer_id AS trainer"
        sql += ", ven.id AS venue"
        sql += " FROM `{}` AS rec".format(self.table)
        sql += " JOIN `{}` AS ra ON ra.id = rec.race_id".format(RaceModel.table)
        sql += " JOIN `{}` AS ven ON ven.id = ra.venue_id".format(VenueModel.table)
        sql += " WHERE DATE_FORMAT(ra.date_time, '%Y-%m-%d') = '{}-{}-{}' AND rec.delete_flag = '0'".format(year, month, day)
        sql += " ORDER BY date ASC, LENGTH(venue) ASC, venue ASC, LENGTH(race) ASC, race ASC, LENGTH(no) ASC, no ASC"
        Model.db.execute(sql)
        return Model.db.fetchall()

    def getAi1Daily(self, year, month, day):
        questions = []
        answers = []
        for record in self.getDaily(year, month, day):
            if record['time'] == None or record['time'] == '':
                continue
            question = '{} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['distance']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['course']).zfill(1),
                str(record['going']).zfill(1),
                str(self.paramList.convertNull(record['rotation'])).zfill(2),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = str(self.paramList.trim(record['time'])).zfill(4)
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['distance']).zfill(4) + "M",
                str(record['venue']).zfill(2),
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(record['going'])),
                str(self.paramList.valRotation(record['rotation'])),
                str(record['burden']))
            answerOrg = str(record['time'])
            print('DATE:{} RACE:{} NO:{} Q:{} A:{}'.format(record['date'], record['race_no'], record['no'], questionOrg, answerOrg))
        return {'question': questions, 'answer': answers}

    def getAi2Daily(self, year, month, day):
        questions = []
        answers = []
        for record in self.getDaily(year, month, day):
            if record['time'] == None or record['time'] == '':
                continue
            question = '{} {} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['gender']).zfill(1),
                str(record['jockey']).zfill(4),
                str(record['frame'].zfill(2)),
                str(record['distance']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['course']).zfill(1),
                str(record['going']).zfill(1),
                str(self.paramList.convertNull(record['rotation'])).zfill(2),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = str(self.paramList.trim(record['time'])).zfill(4)
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(self.paramList.valGender(record['gender'])),
                str(record['jockey']).zfill(4),
                str(record['frame'].zfill(2)),
                str(record['distance']).zfill(4) + "M",
                str(record['venue']).zfill(2),
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(record['going'])),
                str(self.paramList.valRotation(record['rotation'])),
                str(record['burden']))
            answerOrg = str(record['time'])
            print('DATE:{} RACE:{} NO:{} Q:{} A:{}'.format(record['date'], record['race_no'], record['no'], questionOrg, answerOrg))
        return {'question': questions, 'answer': answers}

    def getAi3Daily(self, year, month, day):
        questions = []
        answers = []
        for record in self.getDaily(year, month, day):
            if record['time'] == None or record['time'] == '':
                continue
            question = '{} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['trainer']).zfill(4),
                str(record['distance']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['course']).zfill(1),
                str(record['going']).zfill(1),
                str(self.paramList.convertNull(record['rotation'])).zfill(2),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = str(self.paramList.trim(record['time'])).zfill(4)
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['trainer']).zfill(4),
                str(record['distance']).zfill(4) + "M",
                str(record['venue']).zfill(2),
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(record['going'])),
                str(self.paramList.valRotation(record['rotation'])),
                str(record['burden']))
            answerOrg = str(record['time'])
            print('DATE:{} RACE:{} NO:{} Q:{} A:{}'.format(record['date'], record['race_no'], record['no'], questionOrg, answerOrg))
        return {'question': questions, 'answer': answers}

    def getAi4Daily(self, year, month, day):
        questions = []
        answers = []
        for record in self.getDaily(year, month, day):
            if record['time'] == None or record['time'] == '':
                continue
            question = '{} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['distance']).zfill(4),
                str(record['course']).zfill(1),
                str(record['going']).zfill(1),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = str(self.paramList.trim(record['time'])).zfill(4)
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['distance']).zfill(4) + "M",
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(record['going'])),
                str(record['burden']))
            answerOrg = str(record['time'])
            print('DATE:{} RACE:{} NO:{} Q:{} A:{}'.format(record['date'], record['race_no'], record['no'], questionOrg, answerOrg))
        return {'question': questions, 'answer': answers}

    def getRace(self, date, placeId, raceNo):
        sql = "SELECT"
        sql += " rec.ranking, rec.frame, rec.number AS no, rec.age, rec.burden, rec.time, rec.weight"
        sql += ", ra.id AS race, ra.number AS race_no, DATE_FORMAT(ra.date_time, '%Y-%m-%d') AS date, ra.going, ra.distance, ra.course, ra.rotation"
        sql += ", rec.horse_id AS horse, rec.gender"
        sql += ", rec.jockey_id AS jockey"
        sql += ", rec.trainer_id AS trainer"
        sql += ", ven.id AS venue"
        sql += " FROM `{}` AS rec".format(self.table)
        sql += " JOIN `{}` AS ra ON ra.id = rec.race_id".format(RaceModel.table)
        sql += " JOIN `{}` AS ven ON ven.id = ra.venue_id".format(VenueModel.table)
        sql += " WHERE DATE_FORMAT(ra.date_time, '%Y%m%d') = '{}' AND ra.venue_id = '{}' AND ra.number = '{}' AND rec.delete_flag = '0'".format(date, placeId, raceNo)
        sql += " ORDER BY date ASC, LENGTH(venue) ASC, venue ASC, LENGTH(race) ASC, race ASC, LENGTH(no) ASC, no ASC"
        Model.db.execute(sql)
        return Model.db.fetchall()

    def getAi1Race(self, date, placeId, raceNo, cond):
        questions = []
        answers = []
        i = 1
        for record in self.getRace(date, placeId, raceNo):
            if record['horse'] == None or record['horse'] == '':
                continue
            if record['age'] == None or record['age'] == '':
                continue
            if record['jockey'] == None or record['jockey'] == '':
                continue
            if record['distance'] == None or record['distance'] == '':
                continue
            if record['venue'] == None or record['venue'] == '':
                continue
            if record['course'] == None or record['course'] == '':
                continue
            if record['burden'] == None or record['burden'] == '':
                continue
            question = '{} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['distance']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['course']).zfill(1),
                str(cond).zfill(1),
                str(self.paramList.convertNull(record['rotation'])).zfill(2),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = {
                'no': str(i).zfill(2),
                'frame': str(record['frame']),
                'number': str(record['no']),
                'race': str(record['race']),
                'horse': str(record['horse']),
                'jockey': str(record['jockey']),
                'trainer': str(record['trainer'])
            }
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['distance']).zfill(4) + "M",
                str(record['venue']).zfill(2),
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(cond)),
                str(self.paramList.valRotation(record['rotation'])),
                str(record['burden']))
            i += 1
            print('DATE:{} RACE:{} NO:{} Q:{}'.format(record['date'], record['race_no'], record['no'], questionOrg))
        return {'question': questions, 'answer': answers}

    def getAi2Race(self, date, placeId, raceNo, cond):
        questions = []
        answers = []
        i = 1
        for record in self.getRace(date, placeId, raceNo):
            if record['horse'] == None or record['horse'] == '':
                continue
            if record['age'] == None or record['age'] == '':
                continue
            if record['gender'] == None or record['gender'] == '':
                continue
            if record['jockey'] == None or record['jockey'] == '':
                continue
            if record['frame'] == None or record['frame'] == '':
                continue
            if record['distance'] == None or record['distance'] == '':
                continue
            if record['venue'] == None or record['venue'] == '':
                continue
            if record['course'] == None or record['course'] == '':
                continue
            if record['burden'] == None or record['burden'] == '':
                continue
            question = '{} {} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['gender']).zfill(1),
                str(record['jockey']).zfill(4),
                str(record['frame'].zfill(2)),
                str(record['distance']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['course']).zfill(1),
                str(cond).zfill(1),
                str(self.paramList.convertNull(record['rotation'])).zfill(2),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = {
                'no': str(i).zfill(2),
                'frame': str(record['frame']),
                'number': str(record['no']),
                'race': str(record['race']),
                'horse': str(record['horse']),
                'jockey': str(record['jockey']),
                'trainer': str(record['trainer'])
            }
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(self.paramList.valGender(record['gender'])),
                str(record['jockey']).zfill(4),
                str(record['frame'].zfill(2)),
                str(record['distance']).zfill(4) + "M",
                str(record['venue']).zfill(2),
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(cond)),
                str(self.paramList.valRotation(record['rotation'])),
                str(record['burden']))
            i += 1
            print('DATE:{} RACE:{} NO:{} Q:{}'.format(record['date'], record['race_no'], record['no'], questionOrg))
        return {'question': questions, 'answer': answers}

    def getAi3Race(self, date, placeId, raceNo, cond):
        questions = []
        answers = []
        i = 1
        for record in self.getRace(date, placeId, raceNo):
            if record['horse'] == None or record['horse'] == '':
                continue
            if record['age'] == None or record['age'] == '':
                continue
            if record['jockey'] == None or record['jockey'] == '':
                continue
            if record['trainer'] == None or record['trainer'] == '':
                continue
            if record['distance'] == None or record['distance'] == '':
                continue
            if record['venue'] == None or record['venue'] == '':
                continue
            if record['course'] == None or record['course'] == '':
                continue
            if record['burden'] == None or record['burden'] == '':
                continue
            question = '{} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['trainer']).zfill(4),
                str(record['distance']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['course']).zfill(1),
                str(cond).zfill(1),
                str(self.paramList.convertNull(record['rotation'])).zfill(2),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = {
                'no': str(i).zfill(2),
                'frame': str(record['frame']),
                'number': str(record['no']),
                'race': str(record['race']),
                'horse': str(record['horse']),
                'jockey': str(record['jockey']),
                'trainer': str(record['trainer'])
            }
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['trainer']).zfill(4),
                str(record['distance']).zfill(4) + "M",
                str(record['venue']).zfill(2),
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(cond)),
                str(self.paramList.valRotation(record['rotation'])),
                str(record['burden']))
            i += 1
            print('DATE:{} RACE:{} NO:{} Q:{}'.format(record['date'], record['race_no'], record['no'], questionOrg))
        return {'question': questions, 'answer': answers}

    def getAi4Race(self, date, placeId, raceNo, cond):
        questions = []
        answers = []
        i = 1
        for record in self.getRace(date, placeId, raceNo):
            if record['horse'] == None or record['horse'] == '':
                continue
            if record['age'] == None or record['age'] == '':
                continue
            if record['jockey'] == None or record['jockey'] == '':
                continue
            if record['venue'] == None or record['venue'] == '':
                continue
            if record['distance'] == None or record['distance'] == '':
                continue
            if record['course'] == None or record['course'] == '':
                continue
            if record['burden'] == None or record['burden'] == '':
                continue
            question = '{} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['distance']).zfill(4),
                str(record['course']).zfill(1),
                str(cond).zfill(1),
                str(self.paramList.trim(record['burden'])).zfill(3))
            questions.append(question)
            answer = {
                'no': str(i).zfill(2),
                'frame': str(record['frame']),
                'number': str(record['no']),
                'race': str(record['race']),
                'horse': str(record['horse']),
                'jockey': str(record['jockey']),
                'trainer': str(record['trainer'])
            }
            answers.append(answer)
            questionOrg = '{} {} {} {} {} {} {} {}'.format(
                str(record['horse']).zfill(6),
                str(record['age'].zfill(2)),
                str(record['jockey']).zfill(4),
                str(record['venue']).zfill(2),
                str(record['distance']).zfill(4) + "M",
                str(self.paramList.valCourse(record['course'])),
                str(self.paramList.valGoing(cond)),
                str(record['burden']))
            i += 1
            print('DATE:{} RACE:{} NO:{} Q:{}'.format(record['date'], record['race_no'], record['no'], questionOrg))
        return {'question': questions, 'answer': answers}

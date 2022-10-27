
from crawling.model.model import Model
import datetime


class RaceModel(Model):
    table = "races"

    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("venue_id", "BIGINT NOT NULL")
        self.setColumn("url_key", "VARCHAR(255) NOT NULL")
        self.setColumn("win5", "VARCHAR(1)")
        self.setColumn("number", "VARCHAR(2) NOT NULL")
        self.setColumn("title", "VARCHAR(255) NOT NULL")
        self.setColumn("scale", "VARCHAR(1)")
        self.setColumn("date_time", "DATETIME(6) NOT NULL")
        self.setColumn("course", "VARCHAR(1) NOT NULL")
        self.setColumn("distance", "VARCHAR(4) NOT NULL")
        self.setColumn("rotation", "VARCHAR(2) NOT NULL")
        self.setColumn("weather", "VARCHAR(1) NOT NULL")
        self.setColumn("going", "VARCHAR(1) NOT NULL")
        self.setColumn("times", "VARCHAR(2) NOT NULL")
        self.setColumn("days", "VARCHAR(2) NOT NULL")
        self.setColumn("type1", "VARCHAR(255)")
        self.setColumn("type2", "VARCHAR(255)")
        self.setColumn("type3", "VARCHAR(255)")
        self.setColumn("type4", "VARCHAR(255)")
        self.setColumn("type5", "VARCHAR(255)")
        self.setColumn("prize1", "VARCHAR(10)")
        self.setColumn("prize2", "VARCHAR(10)")
        self.setColumn("prize3", "VARCHAR(10)")
        self.setColumn("prize4", "VARCHAR(10)")
        self.setColumn("prize5", "VARCHAR(10)")
        self.setColumn("option1", "VARCHAR(10)")
        self.setColumn("option2", "VARCHAR(10)")
        self.setColumn("option3", "VARCHAR(10)")
        self.setColumn("option4", "VARCHAR(10)")
        self.setColumn("option5", "VARCHAR(10)")
        self.setColumn("halon_time", "VARCHAR(255)")
        self.setColumn("workout1", "VARCHAR(255)")
        self.setColumn("workout2", "VARCHAR(255)")
        self.setColumn("workout3", "VARCHAR(255)")
        self.setColumn("workout4", "VARCHAR(255)")
        self.setColumn("corner1", "VARCHAR(255)")
        self.setColumn("corner2", "VARCHAR(255)")
        self.setColumn("corner3", "VARCHAR(255)")
        self.setColumn("corner4", "VARCHAR(255)")
        self.setColumn("approval_flag", "INT(1)")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getRaceId(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(self.primaryKey, self.table, 'url_key', self.values['url_key'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def getSendData(self, date, venueId, number):
        sql = "SELECT * FROM `{}`".format(self.table)
        sql += " WHERE DATE_FORMAT(date_time, '%Y%m%d') = '{}'".format(date)
        sql += " AND venue_id = {}".format(venueId)
        sql += " AND number = {}".format(number)
        sql += " LIMIT 1"
        Model.db.execute(sql)
        data = None
        for record in Model.db.fetchall():
            data = record
        return data

    def listUrlKey(self):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        sql = "SELECT DISTINCT r.url_key FROM records c INNER JOIN {} r ON r.id = c.race_id WHERE c.scrapy_flag = 0 AND r.date_time BETWEEN '{}' AND '{}' ORDER BY r.date_time ASC".format(
            self.table, yesterday, now)
        Model.db.execute(sql)
        return Model.db.fetchall()

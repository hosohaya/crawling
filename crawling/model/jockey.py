
from crawling.model.model import Model


class JockeyModel(Model):
    table = "jockeys"

    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("group_id", "BIGINT")
        self.setColumn("name", "VARCHAR(255) NOT NULL")
        self.setColumn("scrapy_name", "VARCHAR(255)")
        self.setColumn("orders", "VARCHAR(1)")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getJockeyId(self):
        sql = "SELECT `{}` FROM `{}` WHERE FIND_IN_SET('{}', REPLACE(REPLACE(`{}`, ' ', ''), ' ', '')) LIMIT 1".format(
            self.primaryKey, self.table, self.values['scrapy_name'], 'scrapy_name')
        # sql = "SELECT `{}` FROM `{}` WHERE REPLACE(REPLACE(`{}`, ' ', ''), ' ', '') = '{}' LIMIT 1".format(
        #     self.primaryKey, self.table, 'scrapy_name', self.values['scrapy_name'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def getJockey(self):
        sql = "SELECT * FROM `{}` WHERE FIND_IN_SET('{}', REPLACE(REPLACE(`{}`, ' ', ''), ' ', '')) LIMIT 1".format(
            self.table, self.values['scrapy_name'], 'scrapy_name')
        # sql = "SELECT * FROM `{}` WHERE REPLACE(REPLACE(`{}`, ' ', ''), ' ', '') = '{}' LIMIT 1".format(
        #     self.table, 'scrapy_name', self.values['scrapy_name'])
        Model.db.execute(sql)
        result = None
        for record in Model.db.fetchall():
            result = record
        return result

    def getSendData(self, id):
        sql = "SELECT * FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(
            self.table, self.primaryKey, id)
        Model.db.execute(sql)
        data = None
        for record in Model.db.fetchall():
            data = record
        return data

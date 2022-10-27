
from crawling.model.model import Model


class HorseModel(Model):
    table = "horses"

    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("group_id", "BIGINT")
        self.setColumn("name", "VARCHAR(255) NOT NULL")
        self.setColumn("scrapy_name", "VARCHAR(255)")
        self.setColumn("gender", "VARCHAR(1) NOT NULL")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getHorseId(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(
            self.primaryKey, self.table, 'scrapy_name', self.values['scrapy_name'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def getHorse(self):
        sql = "SELECT * FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(
            self.table, 'scrapy_name', self.values['scrapy_name'])
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

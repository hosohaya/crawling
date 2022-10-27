
from crawling.model.model import Model


class PayoutModel(Model):
    table = "payouts"
    
    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("race_id", "BIGINT NOT NULL")
        self.setColumn("category", "VARCHAR(50)")
        self.setColumn("no", "VARCHAR(2)")
        self.setColumn("number1", "VARCHAR(2)")
        self.setColumn("number2", "VARCHAR(2)")
        self.setColumn("number3", "VARCHAR(2)")
        self.setColumn("popular", "VARCHAR(10)")
        self.setColumn("payout", "VARCHAR(10)")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getPayoutId(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' AND `{}` = '{}' AND `{}` = '{}' LIMIT 1".format(
            self.primaryKey, self.table, 'race_id', self.values['race_id'], 
            'category', self.values['category'], 'no', self.values['no'])
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

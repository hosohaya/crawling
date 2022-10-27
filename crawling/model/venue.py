
from crawling.model.model import Model


class VenueModel(Model):
    table = "venues"

    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("category", "VARCHAR(1) NOT NULL")
        self.setColumn("base_code", "VARCHAR(2)")
        self.setColumn("name", "VARCHAR(50) NOT NULL")
        self.setColumn("orders", "BIGINT NOT NULL")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getVenueId(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(
            self.primaryKey, self.table, 'name', self.values['name'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def getVenueIdByBaseCode(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(
            self.primaryKey, self.table, 'base_code', self.values['base_code'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def saveVenue(self, id, name):
        sql = "INSERT INTO `{}` (`{}`, `{}`) VALUES ('{}', '{}')".format(self.table, 'id', 'name', id, name)
        print(sql)
        Model.db.execute(sql)
        Model.con.commit()

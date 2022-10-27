
from crawling.model.model import Model


class GroupModel(Model):
    table = "groups"

    def __init__(self):
        super().__init__()
        self.setColumn("id", "BIGINT NOT NULL AUTO_INCREMENT")
        self.setColumn("category", "VARCHAR(1) NOT NULL")
        self.setColumn("name", "VARCHAR(255) NOT NULL")
        self.setColumn("delete_flag", "INT(1)")
        self.setColumn("created_at", "DATETIME(6)")
        self.setColumn("updated_at", "DATETIME(6)")
        # self.createTable()

    def getGroupId(self):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(
            self.primaryKey, self.table, 'name', self.values['name'])
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def saveGroup(self, id, name):
        sql = "INSERT INTO `{}` (`{}`, `{}`) VALUES ('{}', '{}')".format(self.table, 'id', 'name', id, name)
        print(sql)
        Model.db.execute(sql)
        Model.con.commit()

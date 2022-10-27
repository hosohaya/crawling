
import mysql.connector

from datetime import datetime as dt
from crawling.lib.param_list import ParamList


class Model:
    con = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'hoso0601',
        database = 'keibaeye',
    )
    db = None
    count = 0

    table = ""
    primaryKey = "id"
    columns = {}
    values = {}
    orders = []
    
    paramList = None

    def __init__(self):
        # print(self.con.is_connected())
        # print('Model::__init__')
        if Model.count == 0:
            Model.db = Model.con.cursor(buffered=True, dictionary=True)
            # print('db open.')
        Model.count += 1
        self.primaryKey = "id"
        self.columns = {}
        self.values = {}
        self.orders = []
        self.paramList = ParamList()
    
    def __del__(self):
        # print('Model::__del__')
        Model.count -= 1
        if Model.count == 0:
            Model.db.close()
            Model.con.close()
            # print('db close.')

    def setColumn(self, column, define):
        self.columns[column] = define
        self.orders.append(column)
    
    def setValue(self, column, value):
        self.values[column] = value
    
    def setValueFromItem(self, item):
        for column, value in item.items():
            self.setValue(column, value)

    def createTable(self):
        sql = "CREATE TABLE IF NOT EXISTS `{}` (".format(self.table)
        for column in self.orders:
            sql += "`{}` {},".format(column, self.columns[column])
        sql += "PRIMARY KEY ({})".format(self.primaryKey)
        sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"
        # print(sql)
        Model.db.execute(sql)

    def save(self):
        now = dt.now()
        nowstr = now.strftime('%Y/%m/%d %H:%M:%S')
        sqlColumn = ""
        sqlValue = ""
        cnt = 0
        # print(self.columns)
        # print(self.values)
        for column in self.orders:
            cnt += 1
            if column == self.primaryKey:
                continue
            if column == 'created_at' or column == 'updated_at':
                if column not in self.values or not self.values[column]:
                    self.values[column] = nowstr
            sqlColumn += "`{}`".format(column)
            sqlValue += "'{}'".format(self.values[column])
            if cnt != len(self.columns):
                sqlColumn += ", "
                sqlValue += ", "
        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(self.table, sqlColumn, sqlValue)
        print(sql)
        Model.db.execute(sql)
        Model.con.commit()

    def update(self):
        now = dt.now()
        nowstr = now.strftime('%Y/%m/%d %H:%M:%S')
        sqlSet = ""
        cnt = 0
        # print(self.columns)
        # print(self.values)
        for column in self.orders:
            cnt += 1
            if column == self.primaryKey:
                continue
            if column == 'created_at':
                continue
            if column == 'updated_at':
                if column not in self.values or not self.values[column]:
                    self.values[column] = nowstr
            sqlSet += "`{}` = '{}'".format(column, self.values[column])
            if cnt != len(self.columns):
                sqlSet += ", "
        sql = "UPDATE `{}` SET {} WHERE `{}` = '{}'".format(self.table, sqlSet, self.primaryKey, self.values[self.primaryKey])
        print(sql)
        Model.db.execute(sql)
        Model.con.commit()

    def updateOnlyNull(self):
        if self.primaryKey not in self.values:
            return None
        sql = "SELECT * FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(self.table, self.primaryKey, self.values[self.primaryKey])
        Model.db.execute(sql)
        result = None
        for record in Model.db.fetchall():
            result = record
        if not result:
            return result
        now = dt.now()
        nowstr = now.strftime('%Y/%m/%d %H:%M:%S')
        sqlSet = ""
        cnt = 0
        for column in result:
            cnt += 1
            if column == self.primaryKey:
                continue
            if column == 'created_at':
                continue
            if column == 'updated_at':
                if column not in self.values or not self.values[column]:
                    self.values[column] = nowstr
            else:
                if result[column] or result[column] == 0:
                    continue
            if column not in self.values:
                continue
            sqlSet += "`{}` = '{}'".format(column, self.values[column])
            if cnt != len(result):
                sqlSet += ", "
        sql = "UPDATE `{}` SET {} WHERE `{}` = '{}'".format(self.table, sqlSet, self.primaryKey, self.values[self.primaryKey])
        print(sql)
        Model.db.execute(sql)
        Model.con.commit()

    def isExists(self, column, value):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(self.primaryKey, self.table, column, value)
        Model.db.execute(sql)
        flag = False
        for record in Model.db.fetchall():
            if record[self.primaryKey]:
                flag = True
        return flag

    def find(self, id):
        sql = "SELECT * FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(self.table, self.primaryKey, id)
        Model.db.execute(sql)
        result = None
        for record in Model.db.fetchall():
            result = record
        return result

    def getId(self, column, value):
        sql = "SELECT `{}` FROM `{}` WHERE `{}` = '{}' LIMIT 1".format(self.primaryKey, self.table, column, value)
        Model.db.execute(sql)
        id = None
        for record in Model.db.fetchall():
            id = record[self.primaryKey]
        return id

    def getAll(self):
        sql = "SELECT * FROM `{}`".format(self.table)
        Model.db.execute(sql)
        return Model.db.fetchall()
    
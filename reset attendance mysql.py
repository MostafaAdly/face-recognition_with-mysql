import mysql.connector
import json
import pathlib


def path():
    return pathlib.Path(__file__).parent.resolve()


with open(f'{path()}/mysql.json') as f:
    mysqldb = json.load(f)


def connectMySQL():
    return mysql.connector.connect(
        host=mysqldb["host"],
        user=mysqldb["user"],
        password=mysqldb["pass"],
        database=mysqldb["database"]
    )


mysqlQuery = connectMySQL()

cur = mysqlQuery.cursor()
cur.execute("delete from `attendance` where 1")
mysqlQuery.commit()

print("deleted.")

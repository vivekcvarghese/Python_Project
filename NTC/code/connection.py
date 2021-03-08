import MySQLdb

def connect_db():
    database = MySQLdb.connect (host="localhost", user = "root", passwd = "root", db = "ntc")
    cursor = database.cursor()
    return cursor, database


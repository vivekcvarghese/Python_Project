import MySQLdb

from flask import request
from flask_restful import Resource

class User(Resource):

    def post(self):

        jdata = request.get_json()
        username = jdata['username']
        password = jdata['password']

        database = MySQLdb.connect (host="localhost", user = "root", passwd = "root", db = "ntc")
        cursor = database.cursor()

        query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username,password)
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return {"login":"success"}
        else:
            return {"login":"invalid credentials"}
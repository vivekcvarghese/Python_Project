import MySQLdb

from connection import connect_db
from flask import request
from flask_restful import Resource

class User(Resource):

    def post(self):
    
        jdata = request.get_json()
        username = jdata['username']
        password = jdata['password']
        
        cursor, database = connect_db()
          
        query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username,password)
        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()

        database.close()

        if result:
            return {"login":"success"}
        else:
            return {"login":"invalid credentials"}


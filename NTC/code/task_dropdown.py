import json

from connection import connect_db
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class DropDown(Resource):

    def get(self):

        cursor, database = connect_db()
        title = []
        query = "SHOW COLUMNS FROM task_dropdown"
        cursor.execute(query)
        res = cursor.fetchall()
        for i in res:
            title.append(i[0])
  
        query1 = "SELECT * FROM task_dropdown" 
        cursor.execute(query1)
        result = cursor.fetchall()
        op = {}
        
        for j in title:
            op[j] = []

        for row in result:
            i = 0
            for j in title:
                if row[i] != None:
                    op[j].append(row[i])
                i+=1

        cursor.close()
        database.close()

        return op
import json

from connection import connect_db
from flask import request
from flask_restful import Resource

class AddEmployee(Resource):


    def post(self):

        jdata = request.get_json()
        data = jdata['inputs']
        try:
            if data["id"] == "":
                AddEmployee.insert(data)
            else:
                AddEmployee.update(data)
        except:
            return {"response":"Failed"}

        return {"response":"Success"}
    def get(self):

        cursor, database = connect_db()

        query = "SELECT * FROM target_table"
        cursor.execute(query)
        result = cursor.fetchall()

        output = []
        for i in result:
            op = {}
            op["id"] = i[0]
            op["empcode"] = i[1]
            op["name"] = i[2]
            op["doj"] = i[3]
            op["search"] = i[4]
            op["client"] = i[5]
            op["task"] = i[6]

            output.append(op)
        
        cursor.close()
        database.close()
    
        output = json.dumps(output, indent = 4)   
        return output
        
    @classmethod
    def insert(cls, data):
        cursor, database = connect_db()
        query = """INSERT INTO employee (empcode, name, doj, search, client, TASK) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (data['empcode'], data['name'], data['doj'], data['search'], data['client'],
        data['task'])
        cursor.execute(query, values)
       
        cursor.close()
        database.commit()
        database.close()
        return

    @classmethod
    def update(cls, data):
        cursor, database = connect_db()
      
        query = """UPDATE  employee SET(empcode = %s, name = %s, doj = %s, search = %s, 
                client = %s, TASK = %s) WHERE id = {}""".format(data["id"])
        values = (data['empcode'], data['name'], data['doj'], data['search'], data['client'],
        data['task'])
        cursor.execute(query, values)
    
        cursor.close()
        database.commit()
        database.close()
        return

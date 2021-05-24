import json
import datetime

from models.employee import EmployeeModel
from flask import request
from flask_restful import Resource

def getEmployeeDetails(query):

        cursor, database = connect_db()
        cursor.execute(query)
        result = cursor.fetchall()

        output = []
        for i in result:
            op = {}
            op["empcode"] = i[1]
            op["name"] = i[2]
            if i[3] == None:
                op["doj"] = "NA"
            else:
                op["doj"] = i[3].strftime("%Y-%m-%d")
            op["search"] = i[4]
            op["client"] = i[5]
            op["task"] = i[6]
            op["id"] = i[0]

            output.append(op)
        
        cursor.close()
        database.close()
    
        output = json.dumps(output, indent = 4)   
        return output


class AddEmployee(Resource):


    def post(self):

        jdata = request.get_json()
        data = jdata['inputs']
        try:
            if data["id"] == "":
                emp = EmployeeModel(data['empcode'], data['name'], data['doj'], data['search'], data['client'], data['task'])
            else:
                emp = EmployeeModel.getSingleEmployee(data["id"])[0]
                emp.empcode = data['empcode']
                emp.name = data['name']
                emp.doj = data['doj']
                emp.search = data['search']
                emp.client = data['client']
                emp.task = data['task']
            emp.insert()
        except:
            return {"response":"Failed"}

        return {"response":"Success"}
    def get(self):

        res = EmployeeModel.getAllEmployees()
        return EmployeeModel.setOutputFormat(res)

class EditEmployee(Resource):

    def delete(self, empid):
        cursor, database = connect_db()

        query = "DELETE FROM employee WHERE id = {}".format(empid)
        cursor.execute(query)

        cursor.close()
        database.commit()
        database.close()

        return

    def get(self, empid):

        res = EmployeeModel.getSingleEmployee(empid)
        return EmployeeModel.setOutputFormat(res)
import json
from datetime import datetime

from models.employee import EmployeeModel
from flask import request
from flask_restful import Resource

class AddEmployee(Resource):

    def post(self):

        jdata = request.get_json()
        data = jdata['inputs']
        try:
            if data["id"] == "":
                emp = EmployeeModel(data['empcode'], data['name'], data['doj'], data['search'], data['client'], data['task'], datetime.now(), data['username'], datetime.now(), data['username'], 0)
            else:
                emp = EmployeeModel.getSingleEmployee(data["id"])[0]
                emp.empcode = data['empcode']
                emp.name = data['name']
                emp.doj = data['doj']
                emp.search = data['search']
                emp.client = data['client']
                emp.TASK = data['task']
                emp.updated_on = datetime.now()
                emp.updated_by = data['username']
            emp.insert()
        except:
            return {"response":"Failed"}

        return {"response":"Success"}
    def get(self):

        res = EmployeeModel.getAllEmployees()
        return EmployeeModel.setOutputFormat(res)

class EditEmployee(Resource):

    def post(self,empid):
        jdata = request.get_json()
        user = jdata['username']

        emp = EmployeeModel.getSingleEmployee(empid)[0]
        emp.deleted = 1
        emp.updated_on = datetime.now()
        emp.updated_by = user
        emp.insert()
        return

    def get(self, empid):

        res = EmployeeModel.getSingleEmployee(empid)
        return EmployeeModel.setOutputFormat(res)
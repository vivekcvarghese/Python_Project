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

            emp = EmployeeModel(data['empcode'], data['name'], data['doj'], data['search'], data['client'], ",".join(data['task']),
                data['shift'],data['production_status'],data['training_duration'], data['planned_out_of_review_date'], data['actual_out_of_review_date'],
                data['delay_reason'], data['delay_review_duration'], datetime.now(), data['username'], datetime.now(), data['username'], 0)
            emp.insert()
        except:
            return {"response":"Failed"}

        return {"response":"Success"}
    def get(self):

        res = EmployeeModel.getAllEmployees()
        return EmployeeModel.setOutputFormat(res,2)

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
        return EmployeeModel.setOutputFormat(res,1)
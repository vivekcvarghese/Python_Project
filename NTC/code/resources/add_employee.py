import json
from db import db
from datetime import datetime

from models.employee import EmployeeModel
from flask import request
from flask_restful import Resource

class AddEmployee(Resource):

    def post(self):
        #add and update employee
        jdata = request.get_json()
        data = jdata['inputs']   
        try:
            if data["id"] == "":
                result = db.session.query(EmployeeModel.empcode).filter(EmployeeModel.empcode == data['empcode']).all()
                if result:
                    return {"response":"Employee Code already exist !"}
                emp = EmployeeModel(data['empcode'], data['name'], data['doj'], data['search'], data['client'], ",".join(data['task']),
                    data['shift'],data['production_status'],data['training_duration'], data['planned_out_of_review_date'], data['actual_out_of_review_date'],
                    data['delay_reason'], data['delay_review_duration'], datetime.now(), data['username'], datetime.now(), data['username'], 0)
            else:
                res = db.session.query(EmployeeModel.created_on,EmployeeModel.created_by).filter(EmployeeModel.id == data["id"]).one()
                 # insert new record of same employee to keep track of update history
                emp = EmployeeModel(data['empcode'], data['name'], data['doj'], data['search'], data['client'], ",".join(data['task']),
                    data['shift'],data['production_status'],data['training_duration'], data['planned_out_of_review_date'], data['actual_out_of_review_date'],
                    data['delay_reason'], data['delay_review_duration'], res[0], res[1], datetime.now(), data['username'], 0)  
            emp.insert()
        except:
            return {"response":"Failed"}
        return {"response":"Success"}
    
    def get(self):
        res = EmployeeModel.getAllEmployees()
        return EmployeeModel.setOutputFormat(res,2)

class EditEmployee(Resource):
# delete employee method
    def post(self,empid):
        jdata = request.get_json()
        data = jdata['inputs']
        # to find created by and created on
        res = db.session.query(EmployeeModel.created_on,EmployeeModel.created_by).filter(EmployeeModel.id == data["id"]).one()
        
        # insert new record to keep track update history
        emp = EmployeeModel(data['empcode'], data['name'], data['doj'], data['search'], data['client'],  ",".join(data['task']),
                data['shift'],data['production_status'],data['training_duration'], data['planned_out_of_review_date'], data['actual_out_of_review_date'],
                data['delay_reason'], data['delay_review_duration'], res[0], res[1], datetime.now(), data['username'], 1)
        emp.insert()
        # set delete flag of particular employee(to be deleted) records to 1
        db.session.query(EmployeeModel).filter(EmployeeModel.empcode == data['empcode']).update({EmployeeModel.deleted:1})
        db.session.commit()
        return

    def get(self, empid):

        res = EmployeeModel.getSingleEmployee(empid)
        return EmployeeModel.setOutputFormat(res,1)
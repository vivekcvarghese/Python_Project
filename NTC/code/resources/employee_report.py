import json
import datetime
import math

from flask import request
from flask_restful import Resource
from models.fetch_emp_status import EmployeeRprtModel
from models.target_table import TargetModel

class EmployeeReport(Resource):


    def post(self):

        jdata = request.get_json()
        data = jdata['inputs']

        res = TargetModel.GetBandValue(data['Process'])
       
        if res != None and data['status'] == 'Completed/Submitted' :
            target_time = 1/res[0] 
            price = res[1]
        else:
            target_time = 0
            price = 0


        if data['id'] == "":

            emp = EmployeeRprtModel(data['username'], data['account_name'], data['date'], data['orderNumber'], data['Client'],
            data['Task'], data['Process'], data['state'], data['startTime'], data['endTime'], data['totalTime'],
            data['status'], target_time, 0, price)
        else:
            emp = EmployeeRprtModel.singleStatus(data['id'])
            emp.order_number = data['orderNumber']
            emp.date_dt = data['date']
            emp.Client = data['Client']
            emp.Task = data['Task']
            emp.Process = data['Process']
            emp.state = data['state']
            emp.startTime = data['startTime']
            emp.endTime = data['endTime']
            emp.totalTime = data['totalTime']
            emp.status = data['status']
            emp.TargetTime = target_time
            emp.revenue = price
            emp.DayWiseBand = 0

        emp.save_to_db()

        EmployeeRprtModel.getDWB(data['account_name'], data['date'])
        return {"status": "submitted"}
    
    def get(self):
        return EmployeeRprtModel.fetchStatus(0)

     
        
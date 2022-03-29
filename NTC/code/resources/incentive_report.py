import json
from db import db
from sqlalchemy import func
from flask import request
from flask_restful import Resource
from models.report_table import EmployeeRprtModel
from models.employee import EmployeeModel
from models.target_table import TargetModel
from flask_jwt_extended import jwt_required

class IncentiveRprt(Resource):

    # @jwt_required()
    def get(self):
        # data = request.get_json()
        date_condition = []
        emp_details = EmployeeModel.getAllEmployees()
        result = []
        for i in emp_details:
            res = {}
            res["empcode"] = i.empcode
            res["name"] = i.name
            if i.doj == None:
                res["doj"] = "NA"
            else:
                res["doj"] = i.doj.strftime("%Y-%m-%d")
            res["production_status"] = i.production_status
            res["shift"] = i.shift    
            res["search"] = i.search
            res["client"] = i.client
            res["task"] = i.TASK
            res["process"] = i.process
            res["state"] = i.state
            #.band1,TargetModel.band2,TargetModel.band3
            #state must be added in filter
            band_values = db.session.query(TargetModel).filter(TargetModel.Client == i.client, TargetModel.Task == i.TASK, TargetModel.Process == i.process).first()

            res["band1"] = band_values.band1
            res["band2"] = band_values.band2
            res["band3"] = band_values.band3

            orders = db.session.query(func.count(EmployeeRprtModel.order_number)).filter(EmployeeRprtModel.account_name == i.empcode, EmployeeRprtModel.status == 'Completed/Submitted', *date_condition).first()
            res["order_count"] = orders[0]

            if  orders[0] < band_values.band1:
                res["productivity_band"] = "Band 0"
            elif orders[0] >= band_values.band1 and orders[0] < band_values.band2:
                res["productivity_band"] = "Band 1"
            elif orders[0] >= band_values.band2 and orders[0] < band_values.band3:
                res["productivity_band"] = "Band 2"
            elif orders[0] >= band_values.band3:
                res["productivity_band"] = "Band 3"
            else:
                res["productivity_band"] = ""
            res["quality_band"] = ""
            res["final_band"] = ""

            result.append(res)
        
        return result
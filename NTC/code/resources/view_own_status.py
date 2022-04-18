import json
import datetime 

from models.report_table import EmployeeRprtModel
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class ViewOwnStatus(Resource):
    @jwt_required()
    def post(self):

        jdata = request.get_json()
        date = jdata['dateFilter']
        end_date = jdata['enddateFilter']
        account_name = jdata['account_name']

        result = EmployeeRprtModel.myStatus(date,end_date, account_name)
        
        output = []
        for row in result:
            op = {}
            op["date"] = row.date_dt.strftime("%d-%m-%Y")
            op["order_number"] = row.order_number
            op["Client"] = row.client
            op["Task"] = row.task
            op["Process"] = row.process
            op["state"] = row.state
            op["county"] = row.county
            op["mode"] = row.mode
            op["parcels"] = row.parcels
            op["exception"] = row.exception
            op["start_Time"] = str(row.startTime)
            op["end_Time"] = str(row.endTime)
            op["total_Time"] = str(row.totalTime)
            op["status"] = row.status
            op["last_updated_time"] = str(row.updated_time)
            op["comments"] = row.comments
            op["id"] = row.id
            output.append(op)
        
        final_output = json.dumps(output, indent = 4)   

        return final_output
    
   

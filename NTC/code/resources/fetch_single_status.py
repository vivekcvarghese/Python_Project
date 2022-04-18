import json

from models.report_table import EmployeeRprtModel
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class FetchSingleStatus(Resource):

    @jwt_required()
    def post(self):

        jdata = request.get_json()
        eid = jdata['id']
     
        res = EmployeeRprtModel.singleStatus(eid)
        output = []
        if res:
            op = {}
            op["date"] = res.date_dt.strftime("%Y-%m-%d")
            op["orderNumber"] = res.order_number
            op["Client"] = res.client
            op["Task"] = res.task
            op["Process"] = res.process
            op["state"] = res.state
            op["county"] = res.county
            op["mode"] = res.mode
            op["parcels"] = res.parcels
            op["exception"] = res.exception
            op["comments"] = res.comments
            if len(str(res.startTime)) == 8:
                op["startTime"] = str(res.startTime)
            else:
                temp = "0" + str(res.startTime)
                op["startTime"] = temp
            if len(str(res.endTime)) == 8:    
                op["endTime"] = str(res.endTime)
            else:
                temp = "0" + str(res.endTime)
                op["endTime"] = temp
            op["totalTime"] = res.totalTime
            op["status"] = res.status
            op["id"] = res.id
            
            output.append(op)

            output = json.dumps(output, indent = 4)   
    
        return output
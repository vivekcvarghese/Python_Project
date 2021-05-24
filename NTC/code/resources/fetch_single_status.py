import json

from models.fetch_emp_status import EmployeeRprtModel
from flask import request
from flask_restful import Resource


class FetchSingleStatus(Resource):


    def post(self):

        jdata = request.get_json()
        eid = jdata['id']
     
        res = EmployeeRprtModel.singleStatus(eid)
        
        output = []
        op = {}
        op["date"] = res.date_dt.strftime("%Y-%m-%d")
        op["orderNumber"] = res.order_number
        op["Client"] = res.client
        op["Task"] = res.task
        op["Process"] = res.process
        op["state"] = res.state
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
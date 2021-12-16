import json

from datetime import date, timedelta, datetime
from time import strptime
from db import db
from sqlalchemy import func
from models.report_table import EmployeeRprtModel
from models.employee import EmployeeModel
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class YearlyReport(Resource):
    @jwt_required()
    def post(self):

        jdata = request.get_json()
        year = jdata['date']
        sheet_name = jdata['sheetName']
        ml = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

        select_item = []

        if sheet_name == "Revenue":
            select_item.append(func.sum(EmployeeRprtModel.Revenue))
       
        elif sheet_name == "Productivity":
            select_item.append(((func.sum(EmployeeRprtModel.TargetTime))*100)/30)
    
        elif sheet_name == "Utilization":
            select_item.append((((func.sum(EmployeeRprtModel.totalTime))/480)*100)/30)
            
        elif sheet_name == "Orders":
            select_item.append(func.count(EmployeeRprtModel.order_number))


        res = EmployeeModel.getAllEmployees()

        final_array = []
        for i in res:
            final = {}

            result = db.session.query(*select_item, func.month(EmployeeRprtModel.date_dt))\
                .filter(func.year(EmployeeRprtModel.date_dt) == year,\
                EmployeeRprtModel.account_name == i.empcode, EmployeeRprtModel.status == 'Completed/Submitted').group_by(func.month(EmployeeRprtModel.date_dt)).all()
            
            final["empcode"] = i.empcode
            final["name"] = i.name
            if i.doj == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i.doj.strftime("%d-%m-%Y")
            final["search"] = i.search
            final["client"] = i.client
            final["task"] = i.TASK
            total = 0
            for j in result:
                final[ml[(j[1]-1)]] = float(round(j[0], 2))
                total += j[0]
            final["total"] = float(round(total, 2))
            final_array.append(final)


        output = {}
        output["data"] = final_array
        output["dates"] = ml
        output["sheet"] = sheet_name

        output = json.dumps(output, indent = 4)
        
        return output

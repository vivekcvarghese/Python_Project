import json

from datetime import date, timedelta, datetime
from time import strptime
from db import db
from sqlalchemy import func
from models.report_table import EmployeeRprtModel
from models.employee import EmployeeModel
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class RevenueRprt(Resource):
    @jwt_required()
    def post(self):

        jdata = request.get_json()
        dt = jdata['date']
        sheet_name = jdata['sheetName']
        dt = dt.split('-')
        month = dt[1]
        year = dt[0]
        select_item = []

        if sheet_name == "Revenue":
            select_item.append(func.sum(EmployeeRprtModel.Revenue))
       
        elif sheet_name == "Productivity":
            select_item.append(func.sum(EmployeeRprtModel.TargetTime)*100)
    
        elif sheet_name == "Utilization":
            select_item.append((func.sum(EmployeeRprtModel.totalTime)/480)*100)
            
        elif sheet_name == "Orders":
            select_item.append(func.count(EmployeeRprtModel.order_number))

        res = EmployeeModel.getAllEmployees()
        flag = None
        final_array = []
        for i in res:
            final = {}

            result = db.session.query(*select_item, EmployeeRprtModel.date_dt)\
                .filter(func.month(EmployeeRprtModel.date_dt) == month, func.year(EmployeeRprtModel.date_dt) == year,\
                EmployeeRprtModel.account_name == i.empcode).group_by(EmployeeRprtModel.date_dt).all()

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
                final[j[1].strftime("%Y-%m-%d")] = float(round(j[0], 2))
                total += j[0]
            final["total"] = float(round(total, 2))
            final_array.append(final)

        m = int(month)
        y = int(year)
        if m == 12:
            ndays = (date(y+1, 1, 1) - date(y, m, 1)).days
        else:
            ndays = (date(y, m+1, 1) - date(y, m, 1)).days
        d1 = date(y, m, 1)
        d2 = date(y, m, ndays)
        delta = d2 - d1
        dates = [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

        output = {}
        output["data"] = final_array
        output["dates"] = dates
        output["sheet"] = sheet_name

        output = json.dumps(output, indent = 4)
        return output

        
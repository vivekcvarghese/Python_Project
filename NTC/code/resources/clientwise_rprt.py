import json

from datetime import date, timedelta, datetime
from time import strptime
from db import db
from sqlalchemy import func
from models.report_table import EmployeeRprtModel
from flask import request
from flask_restful import Resource


class ClientRprt(Resource):

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
       
        elif sheet_name == "Volume":
            select_item.append(func.count(EmployeeRprtModel.order_number))

        
        result = db.session.query(func.distinct(EmployeeRprtModel.client)).filter(func.year(EmployeeRprtModel.date_dt) == year, func.month(EmployeeRprtModel.date_dt) == month).all()
        final_array = [] 
        for i in result:
            final = {}
            if i[0] != None and i[0] != 'NonProd':
                res = db.session.query(*select_item, EmployeeRprtModel.date_dt)\
                    .filter(func.year(EmployeeRprtModel.date_dt) == year, func.month(EmployeeRprtModel.date_dt) == month,\
                    EmployeeRprtModel.client == i[0], EmployeeRprtModel.status == 'Completed/Submitted').group_by(EmployeeRprtModel.date_dt).all()
            
                final['client'] = i[0]
                total = 0
                for j in res:
                    final[j[1].strftime("%Y-%m-%d")] = float(round(j[0], 2))
                    total += j[0]
                if total != 0:
                    final['total'] = float(round(total, 2))
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

        output = json.dumps(output, indent = 4)
        return output



class YearlyClientRprt(Resource):
    def post(self):

        jdata = request.get_json()
        startDate = jdata['startDate']
        endDate = jdata['endDate']

        result = db.session.query(func.distinct(EmployeeRprtModel.client))\
                .filter(EmployeeRprtModel.date_dt.between(startDate,endDate)).all()

        final_array = [] 
        for i in result:
            final = {}
            if i[0] != None and i[0] != 'NonProd':
                res = db.session.query(func.sum(EmployeeRprtModel.Revenue), func.count(EmployeeRprtModel.order_number))\
                    .filter(EmployeeRprtModel.date_dt.between(startDate,endDate),\
                    EmployeeRprtModel.client == i[0], EmployeeRprtModel.status == 'Completed/Submitted').one()

                final['client'] = i[0]
                final["revenue"] = float(round(res[0], 2))
                final["order_count"] = res[1]
                final_array.append(final)

        output = json.dumps(final_array, indent = 4)   

        return output
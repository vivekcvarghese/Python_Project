import json

from datetime import date, timedelta, datetime
from time import strptime
from db import db
from sqlalchemy import func
from models.fetch_emp_status import EmployeeRprtModel
from flask import request
from flask_restful import Resource


class ClientRprt(Resource):

    def post(self):

        jdata = request.get_json()
        dt = jdata['date']
        dt = dt.split('-')
        month = dt[1]
        year = dt[0]

        result = db.session.query(func.distinct(EmployeeRprtModel.client)).filter(func.year(EmployeeRprtModel.date_dt) == year, func.month(EmployeeRprtModel.date_dt) == month).all()
        final_array = [] 
        for i in result:
            final = {}
            if i[0] != None and i[0] != 'NonProd':
                res = db.session.query(func.sum(EmployeeRprtModel.Revenue), EmployeeRprtModel.date_dt)\
                    .filter(func.year(EmployeeRprtModel.date_dt) == year, func.month(EmployeeRprtModel.date_dt) == month,\
                    EmployeeRprtModel.client == i[0]).group_by(EmployeeRprtModel.date_dt).all()
            
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
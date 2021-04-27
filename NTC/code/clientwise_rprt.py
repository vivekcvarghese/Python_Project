import json
from datetime import date, timedelta, datetime
from time import strptime

from connection import connect_db
from flask import request
from flask_restful import Resource


class ClientRprt(Resource):

    def post(self):

        jdata = request.get_json()
        dt = jdata['date']
        dt = dt.split('-')
        month = dt[1]
        year = dt[0]

        cursor, database = connect_db()
        query = "SELECT DISTINCT(client) FROM emp_report WHERE month(date_dt) = '{}' AND year(date_dt) = '{}' ".format(month, year)
        cursor.execute(query)
        result = cursor.fetchall()
        final_array = [] 

        for i in result:
            final = {}
            if i[0] != None and i[0] != 'NonProd':
                query = "SELECT SUM(revenue), date_dt FROM emp_report WHERE month(date_dt) = '{}' AND year(date_dt) = '{}' AND client = '{}' GROUP BY date_dt".format(month, year, i[0])
                cursor.execute(query)
                res = cursor.fetchall()

                final['client'] = i[0]
                total = 0
                for j in res:
                    final[j[1].strftime("%Y-%m-%d")] = float(round(j[0], 2))
                    total += j[0]
                final['total'] = float(round(total, 2))
                final_array.append(final)

        cursor.close()
        database.close()

        m = int(month)
        y = int(year)
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
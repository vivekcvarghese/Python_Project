import json
from datetime import date, timedelta, datetime
from time import strptime

from connection import connect_db
from flask import request
from flask_restful import Resource


class RevenueRprt(Resource):

    def post(self):

        jdata = request.get_json()
        dt = jdata['date']
        sheet_name = jdata['sheetName']
        dt = dt.split('-')
        month = dt[1]
        year = dt[0]

        if sheet_name == "Revenue":
            x = "SUM(revenue)"
        elif sheet_name == "Productivity":
            x = "SUM(TargetTime)"
        elif sheet_name == "Utilization":
            x = "SUM(totalTime)"
        elif sheet_name == "Orders":
            x = "COUNT(order_number)"

        cursor, database = connect_db()
        query = "SELECT * FROM employee"
        cursor.execute(query)
        res = cursor.fetchall()

        flag = None
        final_array = []
        for i in res:
            final = {}
            query = "SELECT {}, date_dt FROM emp_report WHERE month(date_dt) = '{}' AND account_name = '{}' AND year(date_dt) = '{}' GROUP BY date_dt".format(x, month, i[1], year)
            cursor.execute(query)
            result = cursor.fetchall()

            final["emp_code"] = i[1]
            final["name"] = i[2]
            if i[3] == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i[3].strftime("%d-%m-%Y")
            final["search"] = i[4]
            final["client"] = i[5]
            final["task"] = i[6]
            total = 0
            for j in result:
                final[j[1].strftime("%Y-%m-%d")] = float(round(j[0], 2))
                total += j[0]
            final["total"] = float(round(total, 2))
            final_array.append(final)

        cursor.close()
        database.close()

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

        
import json
import datetime
import json

from connection import connect_db
from flask import request
from flask_restful import Resource


class EmployeeReport(Resource):


    def post(self):

        jdata = request.get_json()
        username = jdata['username']
        status = jdata['status']
        account_name = jdata['account_name']

        cursor, database = connect_db()
        query = """INSERT INTO emp_report (username, account_name, status) VALUES (%s, %s, %s)"""
        values = (username, account_name, status)
        cursor.execute(query, values)

        cursor.close()

        database.commit()
        database.close()

        return {"status": "submitted"}
    
    def get(self):

        cursor, database = connect_db()
        query = "SELECT * FROM emp_report WHERE DATE(created_date) = CURDATE()"
        cursor.execute(query)
        result = cursor.fetchall()

        output = []
        report = {}
        for row in result:
            report["username"] = row[1]
            report["account_name"] = row[2]
            report["status"] = row[3]
            report["time"] = row[4].strftime("%Y/%m/%d")

            output.append(report)
            report = {}

        print(output)

        cursor.close()
        database.close()

        output = json.dumps(output, indent = 4)   

        return output
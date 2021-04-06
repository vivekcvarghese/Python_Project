import json
import datetime


from connection import connect_db
from flask import request
from flask_restful import Resource
from fetch_emp_status import fetchStatus


class EmployeeReport(Resource):


    def post(self):

        jdata = request.get_json()
        username = jdata['username']
        inputs = jdata['inputs']
        account_name = jdata['account_name']
        
        cursor, database = connect_db()
        
        for i in inputs:

            query = """INSERT INTO emp_report (username, account_name, order_number, status, comments) VALUES (%s, %s, %s, %s, %s)"""
            values = (username, account_name, i['orderNumber'], i['status'], i['comments'])
            cursor.execute(query, values)

        cursor.close()
        database.commit()
        database.close()

        return {"status": "submitted"}
    
    def get(self):

        return fetchStatus(0)

     
        
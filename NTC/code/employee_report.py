import json
import datetime
import math


from connection import connect_db
from flask import request
from flask_restful import Resource
from fetch_emp_status import fetchStatus


class EmployeeReport(Resource):


    def post(self):

        jdata = request.get_json()
        data = jdata['inputs']

        cursor, database = connect_db()

        query = "SELECT band1, price FROM target_table WHERE  process = '{}'".format(data['Process']) 
        cursor.execute(query)
        res = cursor.fetchone()

        if res[0] != None:
            target_time = 1/res[0] 
            target_time = round(target_time,2)
            price = res[1]
        else:
            target_time = 0
            price = 0


       
        query = """INSERT INTO emp_report (username, account_name, date_dt, order_number, client, task, 
        process, state, startTime, endTime, totalTime, status, TargetTime, DayWiseBand, Revenue) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (data['username'], data['account_name'], data['date'], data['orderNumber'], data['Client'],
        data['Task'], data['Process'], data['state'], data['startTime'], data['endTime'], data['totalTime'],
        data['status'], target_time, 111, price)
        
        cursor.execute(query, values)

        cursor.close()
        database.commit()
        database.close()

        return {"status": "submitted"}
    
    def get(self):

        return fetchStatus(0)

     
        
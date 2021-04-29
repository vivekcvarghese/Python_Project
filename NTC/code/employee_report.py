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

        if res != None and data['status'] == 'Completed/Submitted' :
            target_time = 1/res[0] 
            # target_time = round(target_time,2)
            price = res[1]
        else:
            target_time = 0
            price = 0


        if data['id'] == "":

            query = """INSERT INTO emp_report (username, account_name, date_dt, order_number, client, task, 
            process, state, startTime, endTime, totalTime, status, TargetTime, DayWiseBand, Revenue) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (data['username'], data['account_name'], data['date'], data['orderNumber'], data['Client'],
            data['Task'], data['Process'], data['state'], data['startTime'], data['endTime'], data['totalTime'],
            data['status'], target_time, 0, price)
            
            cursor.execute(query, values)
        else:
            query = "UPDATE emp_report SET date_dt = %s, order_number = %s, client = %s, task = %s, process = %s, state = %s, startTime = %s, endTime = %s, totalTime = %s, status = %s, TargetTime = %s, DayWiseBand = %s, Revenue = %s WHERE id = '{}'".format(data['id'])
            values = (data['date'], data['orderNumber'], data['Client'], data['Task'], data['Process'], data['state'], data['startTime'], data['endTime'], data['totalTime'],
            data['status'], target_time, 0, price)
    
            cursor.execute(query, values)

        query = "SELECT SUM(TargetTime) FROM emp_report WHERE account_name = '{}' AND date_dt = '{}' AND status = 'Completed/Submitted'".format(data['account_name'], data['date'])
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result[0] != None:
            dwb = (result[0]/1)*100
            dwb = round(dwb,1)
        else:
            dwb = 0

        query = "UPDATE emp_report SET DayWiseBand = {} WHERE account_name = '{}' AND date_dt = '{}' AND status = 'Completed/Submitted'".format(dwb, data['account_name'], data['date'])
        cursor.execute(query)

        cursor.close()
        database.commit()
        database.close()

        return {"status": "submitted"}
    
    def get(self):

        return fetchStatus(0)

     
        
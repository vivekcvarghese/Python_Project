import json
import datetime


from connection import connect_db
from flask import request
from flask_restful import Resource


class ViewOwnStatus(Resource):


    def post(self):

        jdata = request.get_json()
        date = jdata['dateFilter']
        account_name = jdata['account_name']

        if(date == ''):
            foo = "DATE(created_date) = CURDATE()"
        else:
            foo = "DATE(created_date) = '{}'".format(date)
        
        cursor, database = connect_db()
        
        query = "SELECT * FROM emp_report WHERE account_name = '{}' AND {}".format(account_name, foo)
        cursor.execute(query)
        result = cursor.fetchall()

        print(result)
        output = []
        for row in result:
            op = {}
            op["date"] = row[3].strftime("%d-%m-%Y")
            op["order_number"] = row[4]
            op["Client"] = row[5]
            op["Task"] = row[6]
            op["Process"] = row[7]
            op["state"] = row[8]
            op["startTime"] = str(row[9])
            op["endTime"] = str(row[10])
            op["totalTime"] = row[11]
            op["status"] = row[12]
            op["username"] = row[1]
            output.append(op)
        
        cursor.close()
        database.commit()
        database.close()

        final_output = json.dumps(output, indent = 4)   

        print(final_output)

        return final_output
    
   

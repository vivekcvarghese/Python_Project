import json

from connection import connect_db
from flask import request
from flask_restful import Resource


class FetchSingleStatus(Resource):


    def post(self):

        jdata = request.get_json()
        eid = jdata['id']
     
        
        cursor, database = connect_db()
        query = "SELECT * FROM emp_report WHERE id = '{}'".format(eid)
        cursor.execute(query)
        res = cursor.fetchall()

        output = []
        for row in res:
            op = {}
            op["date"] = row[3].strftime("%Y-%m-%d")
            op["orderNumber"] = row[4]
            op["Client"] = row[5]
            op["Task"] = row[6]
            op["Process"] = row[7]
            op["state"] = row[8]
            if len(str(row[9])) == 8:
                op["startTime"] = str(row[9])
            else:
                temp = "0" + str(row[9])
                op["startTime"] = temp
            if len(str(row[10])) == 8:    
                op["endTime"] = str(row[10])
            else:
                temp = "0" + str(row[10])
                op["endTime"] = temp
            op["totalTime"] = row[11]
            op["status"] = row[12]
            op["id"] = row[0]
           
            output.append(op)
        
        cursor.close()
        database.close()

        output = json.dumps(output, indent = 4)   
    
        return output
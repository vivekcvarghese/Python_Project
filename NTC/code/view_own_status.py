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

        row = None
        output = []
        final = {}
        for row in result:
            op = {}
            op["order_number"] = row[3]
            op["status"] = row[4]
            op["comments"] = row[5]
            output.append(op)
        if row != None:
            final["user_status"] = output
            final["username"] = row[1]
            final["account_name"] = row[2]
            today = datetime.date.today()
            yesterday = today - datetime.timedelta(days = 1)
            date = row[6].strftime("%Y-%m-%d")
            if (date == str(today)):
                final["time"] = "{}, Today".format(row[6].strftime("%I:%M %p"))
            elif (date == str(yesterday)):
                final["time"] = "{}, Yesterday".format(row[6].strftime("%I:%M %p"))
            else:
                final["time"] = row[6].strftime("%I:%M %p,  %d-%m-%Y")



        cursor.close()
        database.commit()
        database.close()

        final_output = json.dumps(final, indent = 4)   

        return final_output
    
   

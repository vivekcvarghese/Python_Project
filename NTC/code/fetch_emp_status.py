import json
import datetime

from connection import connect_db

def fetchStatus(date):

        if(date == 0):
            foo = "date_dt = CURDATE()"
        else:
            foo = "date_dt = '{}'".format(date)

        cursor, database = connect_db()
        query = "SELECT * FROM employee"
        cursor.execute(query)
        res = cursor.fetchall()

        flag = None
        final_array = []
        for i in res:
            final = {}
            query = "SELECT COUNT(order_number), SUM(targetTime)*100, (SUM(totalTime)/480)*100, SUM(revenue) FROM emp_report WHERE {} AND account_name = '{}'".format(foo, i[1])
 
            cursor.execute(query)
            result = cursor.fetchone()
            
            final["emp_code"] = i[1]
            final["name"] = i[2]
            if i[3] == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i[3].strftime("%d-%m-%Y")
            final["search"] = i[4]
            final["client"] = i[5]
            final["task"] = i[6]
            
            if result[0] != 0:
                flag = 1
                final["order_count"] = result[0]
                final["productivity"] = float(round(result[1],1)) 
                final["utilization"] = float(round(result[2],2))
                final["revenue"] = float(round(result[3],2))
            else:
                final["order_count"] = 0
                final["productivity"] = 0
                final["utilization"] = 0
                final["revenue"] = 0
            
            final_array.append(final)


        cursor.close()
        database.close()
        if flag == None:
            final_array = []

        output = json.dumps(final_array, indent = 4)   

        return output





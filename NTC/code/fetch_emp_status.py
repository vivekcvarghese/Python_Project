import json
import datetime

from connection import connect_db

def fetchStatus(date):

        if(date == 0):
            foo = "DATE(created_date) = CURDATE()"
        else:
            foo = "DATE(created_date) = '{}'".format(date)

        cursor, database = connect_db()
        query = "SELECT DISTINCT(account_name), username, created_date FROM emp_report WHERE {}".format(foo)
        cursor.execute(query)
        res = cursor.fetchall()

        final_array = []
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)

        for i in res:
            final = {}
            ar = []
            query = "SELECT * FROM emp_report WHERE {} AND account_name = '{}' ORDER BY created_date DESC".format(foo, i[0])
            cursor.execute(query)
            result = cursor.fetchall()
            
            for j in result:
                st = {}
                st["order_number"] = j[3]
                st["status"] = j[4]
                st["comments"] = j[5]

                ar.append(st)
            
            final["user_status"] = ar
            final["username"] = i[1]
            final["account_name"] = i[0]
            date = i[2].strftime("%Y-%m-%d")
            if (date == str(today)):
                final["time"] = "{}, Today".format(i[2].strftime("%I:%M %p"))
            elif (date == str(yesterday)):
                final["time"] = "{}, Yesterday".format(i[2].strftime("%I:%M %p"))
            else:
                final["time"] = i[2].strftime("%I:%M %p,  %d-%m-%Y")

            final_array.append(final)


        cursor.close()
        database.close()

        output = json.dumps(final_array, indent = 4)   

        return output





import json
import datetime

from connection import connect_db

def fetchStatus(date):

        if(date == 0):
            foo = "DATE(created_date) = CURDATE()"
        else:
            foo = "DATE(created_date) = '{}'".format(date)

        cursor, database = connect_db()
        query = "SELECT * FROM emp_report WHERE {} ORDER BY created_date DESC".format(foo)
        cursor.execute(query)
        result = cursor.fetchall()

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)

        output = []
        report = {}
        for row in result:
            report["username"] = row[1]
            report["account_name"] = row[2]
            report["status"] = row[3]
            date = row[4].strftime("%Y-%m-%d")
            if (date == str(today)):
                report["time"] = "{}, Today".format(row[4].strftime("%I:%M %p"))
            elif (date == str(yesterday)):
                report["time"] = "{}, Yesterday".format(row[4].strftime("%I:%M %p"))
            else:
                report["time"] = row[4].strftime("%I:%M %p,  %d-%m-%Y")

            output.append(report)
            report = {}

        cursor.close()
        database.close()

        output = json.dumps(output, indent = 4)   

        return output

import json

from connection import connect_db

def fetchStatus(date):

        if(date == 0):
            foo = "DATE(created_date) = CURDATE()"
        else:
            foo = "DATE(created_date) = '{}'".format(date)

        cursor, database = connect_db()
        query = "SELECT * FROM emp_report WHERE {}".format(foo)
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

        cursor.close()
        database.close()

        output = json.dumps(output, indent = 4)   

        return output

import MySQLdb
from connection import connect_db

def RdData(filters = [], dates = "", time = ""):


        if dates == "" and time == "":
                goo = "created_date = (SELECT MAX(created_date) FROM data) AND DATE(created_date) = CURDATE()"
        elif dates != "" and time == "":
                goo = "created_date = (SELECT MAX(created_date) FROM data WHERE DATE(created_date) ='{}')".format(dates)

        if len(filters) != 0:
                sql_list = str(tuple([key for key in filters])).replace(',)', ')')
                foo = "AND SLAExpiration IN {}".format(sql_list)
        else:
                foo = ""
        cursor, database = connect_db()

        query1 = "SELECT DISTINCT(Task_Name) FROM data WHERE Task_Status = 'Available' AND {} {} ORDER BY Task_Name".format(goo, foo)
        cursor.execute(query1)
        result = cursor.fetchall()  

        tasks = []
        output = []
        dates = []
        for row in result:
                tasks.append(row[0])

        
        query2 = "SELECT DISTINCT(SLAExpiration) FROM data WHERE Task_Status = 'Available' AND {}".format(goo)
        print(query2)
        cursor.execute(query2)
        result = cursor.fetchall()    
        for row in result:
                dt1 = row[0].strftime("%Y/%m/%d")
                dates.append(dt1)

        for i in tasks:
                query = "SELECT State, COUNT(State) FROM data  WHERE Task_Name = '{}' AND Task_Status = 'Available' AND {} {} GROUP BY State ORDER BY State".format(i, goo, foo)
                
                cursor.execute(query)
                result = cursor.fetchall()

                state = {}
                state["Task_Name"] = i
                total_count = 0
                for row in result:
                        total_count += row[1]
                        state[row[0]] = row[1]

                state['Grand_total'] = total_count
                output.append(state)

        dt = {}
        dt["SLAExpiration"]  = dates  
        output.append(dt)
        cursor.close()

        database.close()
        
        return output
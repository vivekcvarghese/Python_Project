import MySQLdb

def RdData(filters = 0):
    
    if filters != 0 and len(filters) != 0:

            sql_list = str(tuple([key for key in filters])).replace(',)', ')')
            foo = "AND SLAExpiration IN {}".format(sql_list)
            too = "WHERE SLAExpiration IN {}".format(sql_list)
    else:
            foo = ""
            too = ""
    database = MySQLdb.connect (host="localhost", user = "root", passwd = "root", db = "ntc")
    cursor = database.cursor()

    query1 = "SELECT DISTINCT(Task_Name) FROM data {} ORDER BY Task_Name".format(too)
    cursor.execute(query1)
    result = cursor.fetchall()  

    tasks = []
    output = []
    dates = []
    for row in result:
            tasks.append(row[0])
    
    for i in tasks:
        query = "SELECT State, COUNT(State), SLAExpiration FROM data  WHERE Task_Name = '{}' AND Task_Status = 'Available' {} GROUP BY State ORDER BY State".format(i,foo)
        cursor.execute(query)
        result = cursor.fetchall()

        state = {}
        state["Task_Name"] = i
        total_count = 0
        for row in result:
                total_count += row[1]
                state[row[0]] = row[1]
                dt1 = row[2].strftime("%Y/%m/%d")
                if dt1 in dates:
                        continue
                else:   
                        dates.append(dt1)
        state['Grand_total'] = total_count
        output.append(state)

    dt = {}
    dt["SLAExpiration"]  = dates  
    output.append(dt)
    cursor.close()

    database.close()

    return output
import MySQLdb

def RdData(filters = []):
    
    if len(filters) != 0:

            sql_list = str(tuple([key for key in filters])).replace(',)', ')')
            foo = "AND SLAExpiration IN {}".format(sql_list)
    else:
            foo = ""
    database = MySQLdb.connect (host="localhost", user = "root", passwd = "root", db = "ntc")
    cursor = database.cursor()

    query1 = "SELECT DISTINCT(Task_Name) FROM data WHERE Task_Status = 'Available' {} ORDER BY Task_Name".format(foo)
    cursor.execute(query1)
    result = cursor.fetchall()  

    tasks = []
    output = []
    dates = []
    for row in result:
            tasks.append(row[0])

    
    query2 = "SELECT DISTINCT(SLAExpiration) FROM data WHERE Task_Status = 'Available'"
    cursor.execute(query2)
    result = cursor.fetchall()    
    for row in result:
        dt1 = row[0].strftime("%Y/%m/%d")
    dates.append(dt1)

    for i in tasks:
        query = "SELECT State, COUNT(State) FROM data  WHERE Task_Name = '{}' AND Task_Status = 'Available' {} GROUP BY State ORDER BY State".format(i,foo)
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
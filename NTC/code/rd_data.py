import MySQLdb

def RdData():
    
    database = MySQLdb.connect (host="localhost", user = "root", passwd = "root", db = "ntc")
    cursor = database.cursor()

    query1 = "SELECT DISTINCT(Task_Name) FROM data ORDER BY Task_Name"
    cursor.execute(query1)
    result = cursor.fetchall()  

    tasks = []
    output = {}
    for row in result:
            tasks.append(row[0])
    
    for i in tasks:
        query = "SELECT A.State, COUNT(B.State) FROM data A INNER JOIN data B ON(A.id=B.id) WHERE A.Task_Name = '{}' AND A.Task_Status = 'Available' GROUP BY B.State ORDER BY B.State".format(i)
        cursor.execute(query)
        result = cursor.fetchall()

        state = {}
        for row in result:
                state[row[0]] = row[1]
        output[i] = state

    cursor.close()

    database.close()

    return output
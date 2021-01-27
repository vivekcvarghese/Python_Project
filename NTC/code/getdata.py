import MySQLdb
import pandas as pd
import xlrd
import datetime

from tablib import Dataset
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class GetData(Resource):

    def post(self):

        def FormatDate(SLAexp):

            lst = []
            for i in range(len(SLAexp)):
                b = SLAexp[i].split(' ')[0]
                x = b.split("/")
                x = list(map(int, x)) 
                d = datetime.datetime(x[2], x[0], x[1])
                d = d.strftime("%Y/%m/%d")
                lst.append(d)
            return lst

        def DataInsertion(raw_data):

            data = Dataset().load(raw_data)
            
            Order_Number = data["Order Number"]
            State = data["State"]
            Task_Name = data["Task Name"]
            Task_Status = data["Task Status"]
            SLAExpiration = data["SLAExpiration"]

            SLAExpiration = FormatDate(SLAExpiration)

            for i in range(len(Order_Number)):
            
                query = """INSERT INTO data (Order_Number, State, Task_Name, Task_Status, SLAExpiration) VALUES (%s, %s, %s, %s, %s)"""
                values = (Order_Number[i], State[i], Task_Name[i], Task_Status[i], SLAExpiration[i])
                cursor.execute(query, values)
            
            return

        rvsi = request.files['rvsi'].read()  # In form data, I used "rvsi" as key.
        sp2 = request.files['sp2'].read()  # In form data, I used "sp2" as key.
        
        database = MySQLdb.connect (host="localhost", user = "root", passwd = "root", db = "ntc")
        cursor = database.cursor()

        query = "TRUNCATE TABLE data"
        cursor.execute(query)

        DataInsertion(rvsi)
        DataInsertion(sp2)

        cursor.close()

        # Commit the transaction
        database.commit()

        # Close the database connection
        database.close()

        #return jsonify(data.export('json'))
        return {"message":"success"},201

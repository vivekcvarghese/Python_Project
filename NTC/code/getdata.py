import MySQLdb
import pandas as pd
import xlrd
import datetime
import json

from connection import connect_db
from rd_data import RdData
from tablib import Dataset
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class GetData(Resource):

    def get(self):

        opData = RdData()
        opData = json.dumps(opData, indent = 4)   

        return opData

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
                
                query = """INSERT INTO data (Order_Number, State, Task_Name, Task_Status, SLAExpiration, processed) VALUES (%s, %s, %s, %s, %s,false)"""
                values = (Order_Number[i], State[i], Task_Name[i], Task_Status[i], SLAExpiration[i])
                cursor.execute(query, values)
            
            return

        rvsi = request.files['rvsi'].read()  # In form data, I used "rvsi" as key.
        sp2 = request.files['sp2'].read()  # In form data, I used "sp2" as key.

        cursor, database = connect_db()

        query = "UPDATE data SET processed = true"
        cursor.execute(query)
        try:
            DataInsertion(rvsi)
            DataInsertion(sp2)
        except:
            return json.dumps({"error_in_file" : "Invalid file"})
        cursor.close()

        # Commit the transaction
        database.commit()

        # Close the database connection
        database.close()

        return {"response":"file added successfully."}
       

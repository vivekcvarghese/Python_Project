import MySQLdb
import pandas as pd
import xlrd
import json

import datetime
from models.rd_data import DataModel
from tablib import Dataset
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

class GetData(Resource):
    @jwt_required()
    def get(self):
      
        opData = DataModel.RdData()
        opData = json.dumps(opData, indent = 4)   
        return opData
    @jwt_required()
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

        def DataInsertion(raw_data, timestampStr):

            data = Dataset().load(raw_data)
            
            Order_Number = data["Order Number"]
            State = data["State"]
            Task_Name = data["Task Name"]
            Task_Status = data["Task Status"]
            SLAExpiration = data["SLAExpiration"]

            SLAExpiration = FormatDate(SLAExpiration)

            # for i in range(len(Order_Number)):

            #     d = DataModel(Order_Number[i], State[i], Task_Name[i], Task_Status[i], SLAExpiration[i], timestampStr)
            #     d.save_to_db()
            objects=[DataModel(Order_Number[i], State[i], Task_Name[i], Task_Status[i], SLAExpiration[i], timestampStr) for i in range(len(Order_Number))]
            DataModel.save_bulk(objects)
                   
            return

        rvsi = request.files['rvsi'].read()  # In form data, I used "rvsi" as key.
        sp2 = request.files['sp2'].read()  # In form data, I used "sp2" as key.


        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
        try:
            DataInsertion(rvsi, timestampStr)
            DataInsertion(sp2, timestampStr)

        except:
            return {"response" : "Only RVSI and SP2 files allowed!"}

        return {"response":"file added successfully."}
       

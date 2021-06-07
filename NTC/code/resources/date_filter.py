import json

from models.rd_data import DataModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class DateFilter(Resource):

    def post(self):

        jdata = request.get_json()
        slaDates = jdata['date']
        pivot_date = jdata['pivotdate']
        time = jdata['time']
        opData = DataModel.RdData(slaDates, pivot_date, time)
        opData = json.dumps(opData, indent = 4)   

        return opData

        

    
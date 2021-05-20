import json

from models.rd_data import DataModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class DateFilter(Resource):

    def post(self):

        jdata = request.get_json()
        dates = jdata['date']
        pivot_date = jdata['pivotdate']

        opData = DataModel.RdData(self, dates, pivot_date)
        opData = json.dumps(opData, indent = 4)   

        return opData

        

    
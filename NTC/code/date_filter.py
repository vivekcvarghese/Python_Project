import json

from rd_data import RdData
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class DateFilter(Resource):

    def post(self):

        jdata = request.get_json()
        dates = jdata['date']

        opData = RdData(dates)
        opData = json.dumps(opData, indent = 4)   

        return opData

        #print(dates)

    
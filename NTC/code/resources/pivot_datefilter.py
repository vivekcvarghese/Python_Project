import json

from models.rd_data import DataModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class PivotDateFilter(Resource):

    def post(self):

        jdata = request.get_json()
        dates = jdata['pivotDate']
        time = jdata['time']
        filters = []

        opData = DataModel.RdData(self, filters,dates,time)
        opData = json.dumps(opData, indent = 4)   

        return opData

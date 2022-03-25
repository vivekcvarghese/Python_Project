import json
from unittest import result

from models.target_table import TargetModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

class TargetFilter(Resource):
    @jwt_required()
    def get(self):

        res = TargetModel.GetTargetTable()

        result=[
           {
               "id":i.id,
               "client":i.Client,
               "task":i.Task,
               "process":i.Process,
               "time":i.Time,
               "band1":i.band1,
               "band2":i.band2,
               "band3":i.band3,
               "price":i.price
           } for i in res
        ]

        return result
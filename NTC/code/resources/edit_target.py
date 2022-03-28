from models.target_table import TargetModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from db import db

class SingleTarget(Resource):
    @jwt_required()
    def get(self,id):

        res = TargetModel.GetSingleTarget(id)
        return TargetModel.setOutputFormat(res)

    @jwt_required()
    def put(self,id):

        data = request.get_json()
        try:
            res=db.session.query(TargetModel).filter(TargetModel.id == id).first()

            res.Time = data["Time"]
            res.band1 = data["band1"]
            res.band2 = data["band2"]
            res.band3 = data["band3"]
            res.price = data["price"]
            res.save_to_db()
            return {"response":"Success"}

        except:
            return {"response":"Error"}



class TargetFilter(Resource):
    @jwt_required()
    def get(self,client):

        res = TargetModel.GetTargetTable(client)
        return TargetModel.setOutputFormat(res)
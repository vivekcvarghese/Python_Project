from turtle import title
from models.target_table import TargetModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.dropdown_table import DropdownModel
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


    # @jwt_required()
    def delete(self,id):

        res=db.session.query(TargetModel).filter(TargetModel.id == id).first()
        #fetch array from dropdown table
        title = res.Client+res.Task
        dp = db.session.query(DropdownModel).filter(DropdownModel.title == title).first()
        arr = (dp.value).split(",")
        filtered = filter(lambda i: i != res.Process, arr)
        filtered= list(filtered)

        if len(filtered) == 0:
            dp.remove()
            dp1 = db.session.query(DropdownModel).filter(DropdownModel.title == res.Client).first()
            arr1 = (dp1.value).split(",")
            filtered1 = filter(lambda i: i != res.Task, arr1)
            filtered1= list(filtered1)
            if len(filtered1) == 0:
                dp1.remove()
                dp2 = db.session.query(DropdownModel).filter(DropdownModel.title == "Client").first()
                arr2 = (dp2.value).split(",")
                filtered2 = filter(lambda i: i != res.Client, arr2)
                filtered2= list(filtered2)
                dp2.value = ",".join(filtered2)
                dp2.save()

            else:
                dp1.value = ",".join(filtered1)
                dp1.save()

        else:
            dp.value = ",".join(filtered)
            dp.save()

        
        res.delete()
        return 





class TargetFilter(Resource):
    @jwt_required()
    def get(self,client):

        res = TargetModel.GetTargetTable(client)
        return TargetModel.setOutputFormat(res)
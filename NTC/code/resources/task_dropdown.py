import json

from models.dropdown_table import DropdownModel
from models.role import RoleModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

class DropDown(Resource):

    
    def get(self):

        # title = DropdownModel.getTitles()
        result = DropdownModel.getAll()
        res={element.title:element.value.split(",") for element in result}
        role=RoleModel.getroles()
        res["role"]=role
        
        # res = RoleModel.getroles()
        # op = {} 
        
        # for j in title:
        #     op[j] = []

        # for row in result:
        #     for i in title:
        #         if getattr(row, i) != None:
        #             op[i].append(getattr(row, i))

        # op["role"] = res            
        
        return res
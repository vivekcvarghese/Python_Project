import json

from models.dropdown_table import DropdownModel
from models.role import RoleModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class DropDown(Resource):

    def get(self):

        title = DropdownModel.getTitles()
        result = DropdownModel.getAll()
        res = RoleModel.getroles()
        op = {} 
        
        for j in title:
            op[j] = []

        for row in result:
            for i in title:
                if getattr(row, i) != None:
                    op[i].append(getattr(row, i))

        op["role"] = res            
        return op
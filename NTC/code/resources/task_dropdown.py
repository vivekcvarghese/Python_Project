import json

from models.dropdown_table import DropdownModel
from flask import Flask, request, jsonify
from flask_restful import Resource, reqparse

class DropDown(Resource):

    def get(self):

        title = DropdownModel.getTitles()
        result = DropdownModel.getAll()
        op = {} 
        
        for j in title:
            op[j] = []

        for row in result:
            for i in title:
                if getattr(row, i) != None:
                    op[i].append(getattr(row, i))
                    
        return op
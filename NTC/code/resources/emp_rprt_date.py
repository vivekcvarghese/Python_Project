import json
import datetime

from flask import request
from flask_restful import Resource
from models.report_table import EmployeeRprtModel

class EmpRprtDate(Resource):

    def post(self):

        jdata = request.get_json()
        date = jdata['dateFilter']

        return EmployeeRprtModel.fetchStatus(date)


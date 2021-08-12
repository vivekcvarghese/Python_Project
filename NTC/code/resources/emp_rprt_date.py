import json
import datetime

from flask import request
from flask_restful import Resource
from models.report_table import EmployeeRprtModel

class EmpRprtDate(Resource):
# Daily and yearly report page for manager
    def post(self):

        jdata = request.get_json()
        date = jdata['dateFilter']

        startDate = jdata['startDate']
        endDate = jdata['endDate']

        

        return EmployeeRprtModel.fetchStatus(date, startDate, endDate)


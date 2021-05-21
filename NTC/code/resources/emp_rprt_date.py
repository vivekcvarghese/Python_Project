import json
import datetime

from connection import connect_db
from flask import request
from flask_restful import Resource
from models.fetch_emp_status import EmployeeRprtModel

class EmpRprtDate(Resource):

    def post(self):

        jdata = request.get_json()
        date = jdata['dateFilter']

        return EmployeeRprtModel.fetchStatus(date)


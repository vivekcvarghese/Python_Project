import json
import datetime

from connection import connect_db
from flask import request
from flask_restful import Resource
from fetch_emp_status import fetchStatus

class EmpRprtDate(Resource):

    def post(self):

        jdata = request.get_json()
        print(jdata)
        date = jdata['dateFilter']

        return fetchStatus(date)


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from user import User
from getdata import GetData
from date_filter import DateFilter
from employee_report import EmployeeReport
from emp_rprt_date import EmpRprtDate
from view_own_status import ViewOwnStatus
from flask_cors import CORS

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
CORS(app)

api.add_resource(User, '/login')
api.add_resource(GetData, '/getfile')
api.add_resource(DateFilter, '/filter')
api.add_resource(EmployeeReport, '/empreport')
api.add_resource(EmpRprtDate, '/empreport/date')
api.add_resource(ViewOwnStatus, '/mystatus')


if __name__ == '__main__':
    app.run(debug=True)  
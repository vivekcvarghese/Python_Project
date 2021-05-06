from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from user import User
from getdata import GetData
from date_filter import DateFilter
from employee_report import EmployeeReport
from emp_rprt_date import EmpRprtDate
from view_own_status import ViewOwnStatus
from revenue_rprt import RevenueRprt
from clientwise_rprt import ClientRprt
from task_dropdown import DropDown
from fetch_single_status import FetchSingleStatus
from pivot_datefilter import PivotDateFilter
from add_employee import AddEmployee, EditEmployee
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
api.add_resource(DropDown, '/dropdown')
api.add_resource(RevenueRprt, '/revenue')
api.add_resource(ClientRprt, '/clientrprt')
api.add_resource(FetchSingleStatus, '/singlestatus')
api.add_resource(PivotDateFilter, '/pivottables')
api.add_resource(AddEmployee, '/addemployee')
api.add_resource(EditEmployee, '/editemployee/<string:empid>')

if __name__ == '__main__':
    app.run(debug=True)  
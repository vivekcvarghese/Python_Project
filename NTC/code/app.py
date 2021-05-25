from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import User
from resources.getdata import GetData
from resources.date_filter import DateFilter
from resources.employee_report import EmployeeReport
from resources.emp_rprt_date import EmpRprtDate
from resources.view_own_status import ViewOwnStatus
from resources.monthly_rprt import RevenueRprt
from resources.clientwise_rprt import ClientRprt
from resources.task_dropdown import DropDown
from resources.fetch_single_status import FetchSingleStatus
from resources.pivot_datefilter import PivotDateFilter
from resources.add_employee import AddEmployee, EditEmployee
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost/ntc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

# app.config['PROPAGATE_EXCEPTIONS'] = True
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
    from db import db
    db.init_app(app)
    app.run(debug=True)  


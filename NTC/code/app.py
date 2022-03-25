import os
from flask import Flask
from flask_restful import Api
# from sqlalchemy import true
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from resources.user import User, ResetPassword
from resources.getdata import GetData
from resources.date_filter import DateFilter
from resources.employee_report import EmployeeReport,DeleteEmployeeReport
from resources.emp_rprt_date import EmpRprtDate
from resources.view_own_status import ViewOwnStatus
from resources.monthly_rprt import RevenueRprt
from resources.clientwise_rprt import ClientRprt, YearlyClientRprt
from resources.task_dropdown import DropDown
from resources.fetch_single_status import FetchSingleStatus
from resources.pivot_datefilter import PivotDateFilter
from resources.add_employee import AddEmployee, EditEmployee
from resources.yearly_report import YearlyReport
from resources.add_role import AddRole, EditRole
from resources.edit_target import TargetFilter
from flask_cors import CORS

from dotenv import load_dotenv

load_dotenv()
pswd = os.getenv('MYSQL')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://root:root@docker_db_1/ntc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

# app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'ntcbpohyd**jwt'

api = Api(app)
CORS(app)

# test
# @app.before_first_request
# def create_tables():
#     db.create_all()

api.add_resource(User, '/api/login')
api.add_resource(GetData, '/api/getfile')
api.add_resource(DateFilter, '/api/filter')
api.add_resource(EmployeeReport, '/api/empreport')
api.add_resource(EmpRprtDate, '/api/empreport/date')
api.add_resource(ViewOwnStatus, '/api/mystatus')
api.add_resource(DropDown, '/api/dropdown')
api.add_resource(RevenueRprt, '/api/revenue')
api.add_resource(ClientRprt, '/api/clientrprt')
api.add_resource(YearlyClientRprt, '/api/yearlyclientrprt')
api.add_resource(FetchSingleStatus, '/api/singlestatus')
api.add_resource(PivotDateFilter, '/api/pivottables')
api.add_resource(AddEmployee, '/api/addemployee')
api.add_resource(EditEmployee, '/api/editemployee/<string:empid>')
api.add_resource(YearlyReport, '/api/yearlyemprprt')
api.add_resource(DeleteEmployeeReport, '/api/delemprprt')
api.add_resource(EditRole, '/api/editrole/<string:id>')
api.add_resource(AddRole, '/api/addrole')
api.add_resource(ResetPassword, '/api/resetpassword')
api.add_resource(TargetFilter, '/api/target')

from db import db

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True,host='0.0.0.0')
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from user import User
from getdata import GetData
from date_filter import DateFilter
from employee_report import EmployeeReport
from flask_cors import CORS

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
CORS(app)

api.add_resource(User, '/login')
api.add_resource(GetData, '/getfile')
api.add_resource(DateFilter, '/filter')
api.add_resource(EmployeeReport, '/empreport')

if __name__ == '__main__':
    app.run(debug=True)  
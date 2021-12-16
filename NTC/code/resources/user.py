import json

from flask import request
from sqlalchemy.sql.functions import func
from db import db
from flask_restful import Resource
from models.login import LoginModel
from models.employee import EmployeeModel
from models.role import RoleModel
from ldap3 import *
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

class User(Resource):

    def post(self):
        
        jdata = request.get_json()
        AccountName = jdata['username']
        pswd = jdata['password']
        # username = "NTCBPOHYD\\"+AccountName

        
        res = LoginModel.getcredentials(AccountName,pswd)
        if res != None:
            #check if the user is present in our application and fetch his/her role
            res1 = db.session.query(EmployeeModel.role).filter(EmployeeModel.empcode == AccountName, EmployeeModel.deleted == 0, EmployeeModel.updated_on == (db.session.query(func.max(EmployeeModel.updated_on)).filter(EmployeeModel.empcode == AccountName))).first()
            if(res1 == None or res1[0] == ""):
                return{"login":"Contact Manager"}
            des = RoleModel.getresources(res1[0])
            access_token = create_access_token(identity = AccountName)
            return {"login":"success", 
                    "name":res.name,
                    "account_name":res.username, 
                    "description": des,
                    "token": access_token,
                    "cn":"cn"}
        return {"login":"invalid credentials"}
class ResetPassword(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        res = LoginModel.getcredentials(data['username'], data['currentPassword'])
        if res != None:
            LoginModel.changePassword(data['username'], data['newPassword'])
            return {"response":"Success"}
        return {"response":"Incorrect Password"}
        # try:
        #     # AccountName = username.split("\\")[1]
            
        #     server = Server('ntcbpohyd.com')
        #     conn = Connection(server, user=username, password=pswd, auto_bind=True)
        #     conn.search('dc=ntcbpohyd,dc=com','(&(objectclass=person)(sAMAccountName ='+AccountName+'))', attributes=['displayName', 'description','distinguishedName'])
        
        # except:

        #     return {"login":"invalid credentials"}
        
        # Name = str(conn.entries[0].displayName)
        # description = str(conn.entries[0].description)
        # if (description == '[]'):
        #     description = ""

        # data = conn.entries[0].entry_dn
        # cn = data.split(',')[1].split('=')[1]

        # #check if the user is present in our application and fetch his/her role
        # res1 = db.session.query(EmployeeModel.role).filter(EmployeeModel.empcode == AccountName, EmployeeModel.deleted == 0).first()
        # if(res1 == None):
        #     return{"login":"Contact Manager"}
        # des = RoleModel.getresources(res1[0])
        # return {"login":"success", 
        #             "name":Name,
        #             "account_name":AccountName, 
        #             "description": des,
        #             "cn":cn}
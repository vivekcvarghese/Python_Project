import json
from sqlalchemy import func
from db import db
from models.role import RoleModel
from models.employee import EmployeeModel
from flask import request
from datetime import datetime
from flask_restful import Resource

class EditRole(Resource):

    def put(self,id):
        jdata = request.get_json()
        data = jdata['inputs'] 
        res = db.session.query(RoleModel).filter(RoleModel.id == id).first()

        res.resources =  ",".join(data['resources'])
        res.updated_by = data['username']
        res.updated_on = datetime.now()

        res.save_to_db()
        return {"response":"Success"}

class AddRole(Resource):

    def post(self):
        jdata = request.get_json()
        data = jdata['inputs'] 
        result = db.session.query(RoleModel.role).filter(RoleModel.role == data['role'], RoleModel.deleted == 0).all()
        if result:
            return {"response":"Employee role already exist !"}
        emp = RoleModel(data['role'],  ",".join(data['resources']), datetime.now(), data['username'], datetime.now(), data['username'], 0)
        emp.save_to_db()
        return {"response":"Success"}


    def get(self):
        res = RoleModel.getrolelist()
        return res

#delete role
    def put(self):
        jdata = request.get_json()
        data = jdata['inputs']


        st = EmployeeModel.__dict__['__table__'].alias("u")
        res1 = db.session.query(st.c.role).filter(st.c.deleted == 0, st.c.role == data['role'], st.c.updated_on == (db.session.query(func.max(EmployeeModel.updated_on))\
        .filter(EmployeeModel.empcode==st.c.empcode))).first()

        # res = db.session.query(EmployeeModel.role).filter(EmployeeModel.role == data['role'], EmployeeModel.deleted == 0).first()
        if(res1):
            return {"response":"Employee with this role exists"}

        res = db.session.query(RoleModel).filter(RoleModel.id == data['id']).first()
        res.updated_by = data['username']
        res.updated_on = datetime.now()
        res.deleted = 1

        res.save_to_db()
        return {"response":"Success"}

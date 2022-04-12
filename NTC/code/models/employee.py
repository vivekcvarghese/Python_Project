from db import db
from sqlalchemy import func
from sqlalchemy.sql import alias,select

import json
import datetime


class EmployeeModel(db.Model):
    __tablename__="employee_details"
    id=db.Column(db.Integer,primary_key=True)
    empcode =db.Column(db.String(100))
    name=db.Column(db.String(100))
    doj=db.Column(db.Date)
    search=db.Column(db.String(100))
    client=db.Column(db.String(100))
    TASK=db.Column(db.String(100))
    process=db.Column(db.String(100))
    state=db.Column(db.String(100))
    county=db.Column(db.String(100))
    shift=db.Column(db.String(100))
    production_status=db.Column(db.String(100))
    training_duration=db.Column(db.String(100))
    PORD=db.Column(db.Date)
    AORD=db.Column(db.Date)
    delay_reason=db.Column(db.String(100))
    delay_duration=db.Column(db.String(100))
    role=db.Column(db.String(100))
    created_on=db.Column(db.DateTime)
    created_by=db.Column(db.String(100))
    updated_on=db.Column(db.DateTime)
    updated_by=db.Column(db.String(100))
    deleted=db.Column(db.Boolean, default=False)

    def __init__(self,empcode,name,doj,search,client,TASK,process,state,county,shift,production_status,training_duration,PORD,AORD,delay_reason,delay_duration,role,created_on,created_by,updated_on,updated_by,deleted):
        self.empcode = empcode
        self.name = name
        self.doj = doj
        self.search = search
        self.client = client
        self.TASK = TASK
        self.process = process
        self.state = state
        self.county = county
        self.shift = shift
        self.production_status = production_status
        self.training_duration = training_duration
        self.PORD = PORD
        self.AORD = AORD
        self.delay_reason = delay_reason
        self.delay_duration = delay_duration
        self.role = role
        self.created_on = created_on
        self.created_by = created_by
        self.updated_on = updated_on
        self.updated_by = updated_by
        self.deleted = deleted

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getAllEmployees(cls):
        st = EmployeeModel.__dict__['__table__'].alias("u")
        return db.session.query(st).filter(st.c.deleted == 0, st.c.updated_on == (db.session.query(func.max(EmployeeModel.updated_on))\
        .filter(EmployeeModel.empcode==st.c.empcode))).all() 

    @classmethod
    def getSingleEmployee(cls, empid):
        st = EmployeeModel.__dict__['__table__'].alias("u")
        return db.session.query(st).filter(st.c.empcode == empid, st.c.updated_on == (db.session.query(func.max(EmployeeModel.updated_on))\
        .filter(EmployeeModel.empcode==st.c.empcode))).all()

    @classmethod
    def setOutputFormat(cls, data,temp):
        output = []
        for i in data:
            final = {}
            final["empcode"] = i.empcode
            final["name"] = i.name
            if i.doj == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i.doj.strftime("%Y-%m-%d")
            final["shift"] = i.shift    
            final["search"] = i.search
            final["client"] = i.client
            
            # if temp == 2:
            final["task"] = i.TASK

            # else:
            #     try:
            #         final["task"] = i.TASK.split(",")
            #     except:
            #         pass

            final["process"] = i.process
            final["state"] = i.state
            final["county"] = i.county
            final["production_status"] = i.production_status
            final["training_duration"] = i.training_duration
            if i.PORD == None:
                final["planned_out_of_review_date"] = "NA"
            else:
                final["planned_out_of_review_date"] = i.PORD.strftime("%Y-%m-%d")

            if i.AORD == None:
                final["actual_out_of_review_date"] = "NA"
            else:
                final["actual_out_of_review_date"] = i.AORD.strftime("%Y-%m-%d")
                
            final["delay_review_duration"] = i.delay_duration
            final["delay_reason"] = i.delay_reason
            final["role"] = i.role
            final["id"] = i.id

            output.append(final)
            # print(output)
    
        output = json.dumps(output, indent = 4)   
        return output

    
       
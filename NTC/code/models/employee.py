from db import db
from sqlalchemy import func

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
    shift=db.Column(db.String(100))
    production_status=db.Column(db.String(100))
    training_duration=db.Column(db.String(100))
    PORD=db.Column(db.Date)
    AORD=db.Column(db.Date)
    delay_reason=db.Column(db.String(100))
    delay_duration=db.Column(db.String(100))
    created_on=db.Column(db.DateTime)
    created_by=db.Column(db.String(100))
    updated_on=db.Column(db.DateTime)
    updated_by=db.Column(db.String(100))
    deleted=db.Column(db.Boolean, default=False)

    def __init__(self,empcode,name,doj,search,client,TASK,shift,production_status,training_duration,PORD,AORD,delay_reason,delay_duration,created_on,created_by,updated_on,updated_by,deleted):
        self.empcode = empcode
        self.name = name
        self.doj = doj
        self.search = search
        self.client = client
        self.TASK = TASK
        self.shift = shift
        self.production_status = production_status
        self.training_duration = training_duration
        self.PORD = PORD
        self.AORD = AORD
        self.delay_reason = delay_reason
        self.delay_duration = delay_duration
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
        return db.session.query(EmployeeModel,func.max(EmployeeModel.updated_on)).filter(EmployeeModel.deleted == 0).group_by(EmployeeModel.empcode).all() 

    @classmethod
    def getSingleEmployee(cls, empid):
        return db.session.query(EmployeeModel,func.max(EmployeeModel.updated_on)).filter(EmployeeModel.id == empid).all()

    @classmethod
    def setOutputFormat(cls, data,temp):
        print(data)
        output = []
        for i in data:
            final = {}
            final["empcode"] = i[0].empcode
            final["name"] = i[0].name
            if i[0].doj == None:
                final["doj"] = "NA"
            else:
                final["doj"] = i[0].doj.strftime("%Y-%m-%d")
            final["search"] = i[0].search
            final["client"] = i[0].client
            
            if temp == 2:
                final["task"] = i[0].TASK
            else:
                final["task"] = i[0].TASK.split(",")
                
            final["shift"] = i[0].shift
            final["productionStatus"] = i[0].production_status
            final["trainingDuration"] = i[0].training_duration
            if i[0].PORD == None:
                final["plannedOutOfReviewDate"] = "NA"
            else:
                final["plannedOutOfReviewDate"] = i[0].PORD.strftime("%Y-%m-%d")

            if i[0].AORD == None:
                final["actualOutOfReviewDate"] = "NA"
            else:
                final["actualOutOfReviewDate"] = i[0].AORD.strftime("%Y-%m-%d")

            final["delayReason"] = i[0].delay_reason
            final["delayReviewDuration"] = i[0].delay_duration
            final["id"] = i[0].id

            output.append(final)
            # print(output)
    
        output = json.dumps(output, indent = 4)   
        return output

    
       